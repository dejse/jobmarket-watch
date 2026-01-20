#!/usr/bin/env python3
"""
Simple script to deduplicate data.csv
Removes duplicate rows while preserving the header.
"""

import pandas as pd

def deduplicate_csv(input_file, output_file=None):
    """
    Remove duplicate rows from a CSV file.
    
    Args:
        input_file: Path to the input CSV file
        output_file: Path to save deduplicated data (defaults to overwriting input)
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Count original rows
    original_count = len(df)
    
    # Remove duplicates
    df_deduped = df.drop_duplicates()
    
    # Count deduplicated rows
    deduped_count = len(df_deduped)
    duplicates_removed = original_count - deduped_count
    
    # Save to output file (or overwrite input if not specified)
    if output_file is None:
        output_file = input_file
    
    df_deduped.to_csv(output_file, index=False)
    
    # Print summary
    print(f"Original rows: {original_count}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Final rows: {deduped_count}")
    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    # Deduplicate data.csv
    deduplicate_csv("data/data.csv")
    
    # To save to a different file instead, use:
    # deduplicate_csv("data/data.csv", "data/data_clean.csv")
