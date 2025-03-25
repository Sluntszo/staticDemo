import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from tqdm import tqdm
import time

def reverse_geocode(lat, lng, geolocator, geocode):
    try:
        location = geocode((lat, lng), exactly_one=True, language='en')
        if location:
            address = location.raw.get('address', {})
            country = address.get('country', '')
            city = address.get('city', '') or address.get('town', '') or address.get('village', '') or address.get('hamlet', '')
            # Some locations might have different administrative levels
            if not city:
                city = address.get('county', '')
            return country, city
        else:
            return '', ''
    except (GeocoderServiceError, GeocoderTimedOut) as e:
        print(f"Geocoding error for coordinates ({lat}, {lng}): {e}")
        return '', ''

def main():
    # Initialize geolocator with a user agent
    geolocator = Nominatim(user_agent="city_country_verification")
    
    # Use RateLimiter to respect Nominatim's usage policy (1 request per second)
    geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1, max_retries=3, error_wait_seconds=5.0)
    
    # Read the CSV file
    try:
        df = pd.read_csv('data.csv')
    except FileNotFoundError:
        print("The file 'data.csv' was not found.")
        return
    except pd.errors.EmptyDataError:
        print("The file 'data.csv' is empty.")
        return
    except pd.errors.ParserError:
        print("Error parsing 'data.csv'. Please ensure it's a valid CSV file.")
        return
    
    print("Data Read.")

    # Check if 'lat' and 'lng' columns exist
    if 'lat' not in df.columns or 'lng' not in df.columns:
        print("The CSV file must contain 'lat' and 'lng' columns.")
        return
    
    # Initialize new columns
    df['NEW_Country'] = ''
    df['NEW_City'] = ''
    
    # Iterate over the DataFrame with progress bar
    for idx, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows"):
        lat = row['lat']
        lng = row['lng']
        
        # Ensure lat and lng are valid numbers
        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            print(f"Invalid coordinates at row {idx}: lat={row['lat']}, lng={row['lng']}")
            df.at[idx, 'NEW_Country'] = ''
            df.at[idx, 'NEW_City'] = ''
            continue
        
        # Reverse geocode to get country and city
        country, city = reverse_geocode(lat, lng, geolocator, geocode)
        
        # Update the DataFrame
        df.at[idx, 'NEW_Country'] = country
        df.at[idx, 'NEW_City'] = city
        
        # Optional: Sleep to avoid hitting rate limits (handled by RateLimiter)
        # time.sleep(1)
    
    # Save the updated DataFrame to a new CSV file
    output_file = 'data_verified.csv'
    df.to_csv(output_file, index=False)
    print(f"Verification complete. Updated data saved to '{output_file}'.")

if __name__ == "__main__":
    main()
