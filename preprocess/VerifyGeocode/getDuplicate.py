import pandas as pd

def filter_duplicate_country_city(input_file: str, output_file: str):
    """
    Reads a CSV file, identifies rows with duplicate Country and City combinations,
    and writes these duplicate rows to a new CSV file.

    Parameters:
    - input_file (str): Path to the input CSV file (e.g., 'data.csv').
    - output_file (str): Path to the output CSV file to save duplicates (e.g., 'duplicates.csv').
    """

    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(input_file)
        print(f"Successfully read '{input_file}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{input_file}' is empty.")
        return
    except pd.errors.ParserError:
        print(f"Error: The file '{input_file}' could not be parsed. Please ensure it's a valid CSV.")
        return

    # Check if 'Country' and 'City' columns exist
    required_columns = ['Country', 'City']
    for col in required_columns:
        if col not in df.columns:
            print(f"Error: The required column '{col}' is missing from the CSV.")
            return

    # Optional: Display the total number of rows
    total_rows = df.shape[0]
    print(f"Total rows in the dataset: {total_rows}")

    # Identify duplicate combinations of 'Country' and 'City'
    # The 'keep=False' parameter marks all duplicates as True
    duplicates_mask = df.duplicated(subset=['Country', 'City'], keep=False)

    # Filter the DataFrame to keep only duplicate rows
    duplicates_df = df[duplicates_mask].copy()

    # Optional: Display the number of duplicate rows found
    duplicate_rows = duplicates_df.shape[0]
    print(f"Number of duplicate rows found: {duplicate_rows}")

    if duplicate_rows == 0:
        print("No duplicate Country-City combinations found.")
        return

    # Save the duplicate rows to a new CSV file
    try:
        duplicates_df.to_csv(output_file, index=False)
        print(f"Duplicate rows have been saved to '{output_file}'.")
    except Exception as e:
        print(f"Error: Could not write to '{output_file}'. Exception: {e}")

def main():
    # Define input and output file paths
    input_csv = 'data.csv'          # Replace with your input file path if different
    output_csv = 'duplicates.csv'   # Replace with your desired output file path

    # Call the function to filter duplicates
    filter_duplicate_country_city(input_csv, output_csv)

if __name__ == "__main__":
    main()
