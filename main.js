document.addEventListener('DOMContentLoaded', function () {
    // Initialize the ECharts instance for the globe
    var globeChart = echarts.init(document.getElementById('globeContainer'));
  
    // Default city information (Austin, USA)
    let defaultCity = {
      country: "United States of America",
      city: "Austin",
      aqi: 75,
      co: 1.2,
      ozone: 60,
      no2: 40,
      pm25: 35
    };
  
    // This variable will store the last clicked (selected) data point
    let selectedData = null;
  
    // Helper function to update the info window (always shows all fields)
    function updateInfoWindow(data) {
      const infoWindow = document.getElementById('infoWindow');
      if (data) {
        infoWindow.querySelector('.info-country').innerHTML = `<strong>${data.country}</strong>`;
        infoWindow.querySelector('.info-city').textContent = data.city;
        infoWindow.querySelector('.value-aqi').textContent = data.aqi;
        infoWindow.querySelector('.value-co').textContent = data.co;
        infoWindow.querySelector('.value-ozone').textContent = data.ozone;
        infoWindow.querySelector('.value-no2').textContent = data.no2;
        infoWindow.querySelector('.value-pm25').textContent = data.pm25;
      }
    }
  
    // Helper function to update the info window for a selected pollutant.
    // This will update the "primary" pollutant display (here we use .value-aqi as the placeholder).
    function updateInfoWindowForPollutant(data, pollutant) {
      const infoWindow = document.getElementById('infoWindow');
      // Country and city remain the same.
      infoWindow.querySelector('.info-country').innerHTML = `<strong>${data.country}</strong>`;
      infoWindow.querySelector('.info-city').textContent = data.city;
      // Update the primary display based on the pollutant.
      if (pollutant === "AQI") {
        infoWindow.querySelector('.value-aqi').textContent = data.aqi;
      } else if (pollutant === "NO2") {
        infoWindow.querySelector('.value-aqi').textContent = data.no2;
      } else if (pollutant === "O3") {
        infoWindow.querySelector('.value-aqi').textContent = data.ozone;
      } else if (pollutant === "CO2") {
        infoWindow.querySelector('.value-aqi').textContent = data.co;
      }
      // (The other fields remain unchanged for now.)
    }
  
    // Initially update the info window to show the default city
    updateInfoWindow(defaultCity);
  
    // Variable to record the last time a hover event occurred
    let lastHoverTimestamp = Date.now();
  
    // Fetch CSV data
    fetch('data/processed_data/final_data.csv')
      .then(response => response.text())
      .then(csvText => {
        const lines = csvText.split('\n');
        // Header Information
        const header = lines[0].split(',');
        let pollutionData = [];
  
        // Parse fields from CSV
        for (let i = 1; i < lines.length; i++) {
          const row = lines[i].split(',');
          // Basic validation: skip if not enough columns
          if (row.length < 14) continue;
  
          // Extract relevant columns
          // CSV columns: Country, City, AQI Value, AQI Category, CO AQI Value, CO AQI Category,
          // Ozone AQI Value, Ozone AQI Category, NO2 AQI Value, NO2 AQI Category,
          // PM2.5 AQI Value, PM2.5 AQI Category, lat, lng
          const country = row[0];
          const city = row[1];
          const aqiValue = parseFloat(row[2]);
          const coAqiValue = parseFloat(row[4]);
          const ozoneAqiValue = parseFloat(row[6]);
          const no2AqiValue = parseFloat(row[8]);
          const pm25AqiValue = parseFloat(row[10]);
          const lat = parseFloat(row[12]);
          const lng = parseFloat(row[13]);
  
          if (isNaN(lat) || isNaN(lng)) continue;
  
          // Assign pollution level for coloring (based on overall AQI)
          let level = 1;
          if (aqiValue > 50 && aqiValue <= 100) level = 2;
          else if (aqiValue > 100 && aqiValue <= 150) level = 3;
          else if (aqiValue > 150) level = 4;
  
          // Build the node with extra data fields for later use
          pollutionData.push({
            country: country,
            city: city,
            aqi: aqiValue,
            co: coAqiValue,
            ozone: ozoneAqiValue,
            no2: no2AqiValue,
            pm25: pm25AqiValue,
            value: [lng, lat, 0],
            level: level
          });
        }
  
        const option = {
          backgroundColor: '#444',  // Matches the page background
          globe: {
            // Base texture for the Earth (colored image)
            baseTexture: 'picture/earth_bright.jpg',
            // Optional height texture (left empty)
            heightTexture: '',
            // Background image for starfield; high-res panoramic images are recommended
            environment: 'picture/starfield.jpg',
            shading: 'color',  // Use uniform color shading to remove day-night effects
            viewControl: {
              autoRotate: false,          // Disable auto-rotation
              enableRotate: false,        // Disable manual rotation
              targetCoord: [-95, 38]       // Center the view on the USA (approximate center)
            }
          },
          series: [
            {
              name: 'Pollution Points',
              type: 'scatter3D',
              coordinateSystem: 'globe',
              symbolSize: 10, // Increased size for a larger hit area
              selectedMode: 'single', // Enable click selection for dots
              emphasis: {
                itemStyle: {
                  shadowBlur: 12,
                  shadowColor: '#000',
                  opacity: 1
                },
                symbolSize: 14
              },
              select: {
                itemStyle: {
                  shadowBlur: 8,
                  shadowColor: '#000',
                  opacity: 1
                },
                symbolSize: 12
              },
              itemStyle: {
                // Base color determined by overall AQI level by default
                color: function (param) {
                  var lvl = param.data.level;
                  if (lvl === 1) return 'green';
                  else if (lvl === 2) return 'yellow';
                  else if (lvl === 3) return 'orange';
                  else return 'red';
                },
                opacity: 0.9
              },
              data: pollutionData
            }
          ]
        };
  
        globeChart.setOption(option);
  
        // Hover/click behavior state tracking
        let currentHovered = null;
  
        // Click event: if a dot is clicked, update the info window and store its data
        globeChart.on('click', function (params) {
          if (params.componentType === 'series' && params.seriesType === 'scatter3D') {
            selectedData = params.data;
            updateInfoWindow(selectedData);
          }
        });
  
        // Built-in mouseover event: update info window and record the hover timestamp
        globeChart.on('mouseover', function (params) {
          if (params.componentType === 'series' && params.seriesType === 'scatter3D') {
            currentHovered = params.dataIndex;
            updateInfoWindow(params.data);
            lastHoverTimestamp = Date.now();
            document.body.style.cursor = 'pointer';
          }
        });
  
        // Timer-based check: if no hover activity for 8 seconds, revert the info window
        const hoverTimeout = 8000; // 8 seconds
        setInterval(function () {
          if (Date.now() - lastHoverTimestamp > hoverTimeout) {
            currentHovered = null;
            updateInfoWindow(selectedData || defaultCity);
            document.body.style.cursor = 'default';
          }
        }, 1000);
  
      });
  
    // Event listener for the pollutant selector: update the visualization and info window
    document.getElementById("pollutantSelect").addEventListener("change", function(e) {
      let pollutant = e.target.value; // e.g., "NO2", "O3", "CO2"
      // For convenience, if no selection is made, default to AQI
      if (!pollutant) {
        pollutant = "AQI";
      }
      // Update the info window based on the currently displayed data (selectedData or default)
      let dataToShow = selectedData || defaultCity;
      updateInfoWindowForPollutant(dataToShow, pollutant);
  
      // Update the color mapping of the scatter3D series based on the selected pollutant.
      let newColorFunction;
      if (pollutant === "AQI") {
        newColorFunction = function(param) {
          var lvl = param.data.level;
          if (lvl === 1) return 'green';
          else if (lvl === 2) return 'yellow';
          else if (lvl === 3) return 'orange';
          else return 'red';
        };
      } else if (pollutant === "NO2") {
        newColorFunction = function(param) {
          var value = param.data.no2;
          if (value < 40) return 'green';
          else if (value < 80) return 'yellow';
          else if (value < 120) return 'orange';
          else return 'red';
        };
      } else if (pollutant === "O3") {
        newColorFunction = function(param) {
          var value = param.data.ozone;
          if (value < 60) return 'green';
          else if (value < 100) return 'yellow';
          else if (value < 140) return 'orange';
          else return 'red';
        };
      } else if (pollutant === "CO2") {
        newColorFunction = function(param) {
          var value = param.data.co;
          if (value < 1) return 'green';
          else if (value < 2) return 'yellow';
          else if (value < 3) return 'orange';
          else return 'red';
        };
      } else if (pollutant === "PM2.5") {
        newColorFunction = function(param) {
          var value = param.data.co;
          if (value < 1) return 'green';
          else if (value < 2) return 'yellow';
          else if (value < 3) return 'orange';
          else return 'red';
        };
      }
  
      // Update the option for the scatter3D series with the new color function.
      let currentOption = globeChart.getOption();
      currentOption.series[0].itemStyle.color = newColorFunction;
      globeChart.setOption(currentOption);
    });
});
