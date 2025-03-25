# -*- coding: utf-8 -*-
# @Author  : Wenzhuo Ma
# @Time    : 2025/1/26 23:28
# @Function: Data Cleaning Script for Handling Missing Values and Removing Duplicates (Country + City)

import os
import pandas as pd

def main():
    # Define file paths
    input_file_path = '../data/raw_data/raw_data.csv'
    output_file_path = '../data/processed_data/cleaned_data.csv'

    # Ensure output directory exists
    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)

    # Check if input file exists
    if not os.path.exists(input_file_path):
        print(f"File not found: {input_file_path}")
        return

    # Load data
    print("Loading data...")
    data = pd.read_csv(input_file_path, low_memory=False)

    # Step 1: Handle Missing Values
    print("Handling missing values...")
    missing_values_summary = data.isnull().sum()
    print("Missing values summary:\n", missing_values_summary)
    data_cleaned = data.dropna()
    print(f"Rows after dropping missing values: {len(data_cleaned)}")

    # Step 2: Remove Duplicates Based on Country and City
    print("Checking for duplicates based on 'Country' and 'City'...")
    duplicates_count = data_cleaned.duplicated(subset=['Country', 'City']).sum()
    print(f"Number of duplicates found: {duplicates_count}")

    print("Removing duplicates...")
    # Keep only the first occurrence of each Country + City combination
    data_cleaned = data_cleaned.drop_duplicates(subset=['Country', 'City'], keep='first')
    print(f"Rows after removing duplicates: {len(data_cleaned)}")

    # Save the cleaned data
    print(f"Saving cleaned data to: {output_file_path}")
    data_cleaned.to_csv(output_file_path, index=False)
    print("Data cleaning complete.")

if __name__ == "__main__":
    main()
