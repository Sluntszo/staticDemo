# -*- coding: utf-8 -*-
# @Author  : Wenzhuo Ma
# @Time    : 2025/1/26 23:28
# @Function: Analyze Cleaned Data and Save Statistics Separately

import os
import pandas as pd

def main():
    # Define file paths
    cleaned_data_path = '../data/processed_data/cleaned_data.csv'
    overall_stats_path = '../data/processed_data/overall_statistics.csv'
    country_stats_path = '../data/processed_data/country_statistics.csv'

    # Ensure output directory exists
    output_dir = os.path.dirname(overall_stats_path)
    os.makedirs(output_dir, exist_ok=True)

    # Check if cleaned data exists
    if not os.path.exists(cleaned_data_path):
        print(f"Cleaned data file not found: {cleaned_data_path}")
        return

    # Load cleaned data
    print("Loading cleaned data...")
    data_cleaned = pd.read_csv(cleaned_data_path, low_memory=False)

    # Step 1: Overall Statistics
    print("Calculating overall statistics...")
    overall_stats = data_cleaned.describe(include='all')
    print("Overall Statistics:\n", overall_stats)

    # Save overall statistics
    print(f"Saving overall statistics to: {overall_stats_path}")
    overall_stats.to_csv(overall_stats_path)
    print("Overall statistics saved.")

    # Step 2: Country-wise AQI Summary
    print("Calculating country-wise AQI statistics...")
    numeric_columns = ['AQI Value', 'CO AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'PM2.5 AQI Value']
    country_stats = data_cleaned.groupby('Country')[numeric_columns].agg(['mean', 'max', 'min', 'std', 'count'])
    print("Country-wise AQI Summary:\n", country_stats)

    # Save country-wise statistics
    print(f"Saving country-wise statistics to: {country_stats_path}")
    country_stats.to_csv(country_stats_path)
    print("Country-wise statistics saved.")

if __name__ == "__main__":
    main()
