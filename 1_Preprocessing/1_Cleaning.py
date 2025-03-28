import pandas as pd
import matplotlib.pyplot as plt
import os

def clean_and_filter_products(input_csv):
    """
    Pipeline function to filter products based on opportunity list
    
    Args:
        input_csv (str): CSV filename to process (e.g. '2024.csv', '2020.csv')
        
    Returns:
        pd.DataFrame: Filtered dataframe containing only valid products
    """
    # Read the input data
    df = pd.read_csv(f'../Data/Raw_data/{input_csv}')
    df_opp = pd.read_csv('../Data/Raw_data/opp_List.csv')
    # Count records with whitespace before cleaning
    spaces_in_opp = (df_opp['Name'].str.len() != df_opp['Name'].str.strip().str.len()).sum()
    spaces_in_df = (df['Product'].str.len() != df['Product'].str.strip().str.len()).sum()
    
    # Remove leading and trailing whitespace
    df_opp['Name'] = df_opp['Name'].str.strip()
    df['Product'] = df['Product'].str.strip()
    
    # Print whitespace cleaning stats
    if spaces_in_opp > 0:
        print(f"Removed whitespace from {spaces_in_opp} records in opportunity list")
    if spaces_in_df > 0:    
        print(f"Removed whitespace from {spaces_in_df} records in main dataset")

    # Get valid products and filter
    valid_products = df_opp['Name'].tolist()
    df_filtered = df[df['Product'].isin(valid_products)]

    # Calculate filtering stats
    total_rows = df.shape[0]
    remaining_rows = df_filtered.shape[0]
    removed_percentage = ((total_rows - remaining_rows) / total_rows) * 100

    # Create visualization
    labels = ['Before Filtering', 'After Filtering']
    values = [df.shape[0], df_filtered.shape[0]]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values)
    plt.title(f'Number of Rows Before and After Filtering ({input_csv[:-4]}) \n'
            f'({removed_percentage:.1f}% of rows removed)')
    plt.ylabel('Number of Rows')

    for i, v in enumerate(values):
        plt.text(i, v, str(v), ha='center', va='bottom')
        
    print("Original df shape:", df.shape)
    print("Filtered df shape:", df_filtered.shape)
    plt.show()

    return df_filtered

df_2020=clean_and_filter_products(input_csv='2020.csv')
df_2021=clean_and_filter_products(input_csv='2021.csv')
df_2022=clean_and_filter_products(input_csv='2022.csv')
df_2023=clean_and_filter_products(input_csv='2023.csv')
df_2024=clean_and_filter_products(input_csv='2024.csv')

def clean_and_standardize_columns(df):
    # List of columns to keep
    columns_to_keep = ['AccountNumber', 'DealNumber', 'Total', 'Amount Off', 
                      'Net Accrued', 'Age in Days', 'Setup', 'Product']
    
    # Select only specified columns
    df_selected = df[columns_to_keep]
    
    # Print shape before and after column selection
    print(f"\nColumns before selection: {df.shape[1]}")
    print(f"Columns after selection: {df_selected.shape[1]}")
    
    # Check for null values before filling
    null_counts = df_selected.isnull().sum()
    if null_counts.any():
        print("\nNull values found in columns:")
        print(null_counts[null_counts > 0])
        
        # Fill numeric columns with mean
        numeric_cols = df_selected.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            if df_selected[col].isnull().any():
                mean_val = df_selected[col].mean()
                null_count = df_selected[col].isnull().sum()
                df_selected[col].fillna(mean_val, inplace=True)
                print(f"\nFilled {null_count} null values in {col} with mean: {mean_val:.2f}")
                
        # Fill non-numeric columns with mode
        non_numeric_cols = df_selected.select_dtypes(exclude=['int64', 'float64']).columns
        for col in non_numeric_cols:
            if df_selected[col].isnull().any():
                mode_val = df_selected[col].mode()[0]
                null_count = df_selected[col].isnull().sum()
                df_selected[col].fillna(mode_val, inplace=True)
                print(f"\nFilled {null_count} null values in {col} with mode: {mode_val}")
                
        # Verify no null values remain
        remaining_nulls = df_selected.isnull().sum()
        if remaining_nulls.any():
            print("\nWarning: Some null values could not be filled:")
            print(remaining_nulls[remaining_nulls > 0])
        else:
            print("\nAll null values have been successfully filled")
    else:
        print("\nNo null values found in the selected columns")
    
    # Convert Setup column by removing '$' and converting to float
    df_selected['Setup'] = df_selected['Setup'].str.replace('$', '').astype(float)
    
    # Convert other numeric columns to float (except Product which stays as string)
    numeric_cols = ['AccountNumber', 'DealNumber', 'Total', 'Amount Off', 
                   'Net Accrued', 'Age in Days', 'Setup']
    
    for col in numeric_cols:
        # Replace '-' with 0 before converting to float
        df_selected[col] = df_selected[col].replace('-', '0').astype(float)
        
    # Print dtypes after conversion
    print("\nColumn datatypes after conversion:")
    print(df_selected.dtypes)
    return df_selected

# Apply column selection to each dataframe
df_2020 = clean_and_standardize_columns(df_2020)
df_2021 = clean_and_standardize_columns(df_2021) 
df_2022 = clean_and_standardize_columns(df_2022)
df_2023 = clean_and_standardize_columns(df_2023)
df_2024 = clean_and_standardize_columns(df_2024)

def aggregate_account_deal_summary(df):
    # First get account level summary showing deals
    account_summary = df.groupby(['AccountNumber', 'DealNumber']).agg({
        'Total': 'sum',
        'Amount Off': 'sum', 
        'Net Accrued': 'sum',
        'Age in Days': 'first',
        'Setup': 'first',
        'Product': 'first'
    }).reset_index()
    
    # Sort by AccountNumber and DealNumber
    account_summary = account_summary.sort_values(['AccountNumber', 'DealNumber'])
    
    # Add deal count per account
    deal_counts = account_summary.groupby('AccountNumber')['DealNumber'].nunique()
    account_summary['Deals_Per_Account'] = account_summary['AccountNumber'].map(deal_counts)
    
    # Rename columns for clarity while keeping all information
    account_summary = account_summary.rename(columns={
        'Total': 'Total_Amount',
        'Amount Off': 'Total_Discount',
        'Net Accrued': 'Net_Total_Amount'
    })
    
    return account_summary

# Process each year's data
detailed_2020 = aggregate_account_deal_summary(df_2020)
detailed_2021 = aggregate_account_deal_summary(df_2021)
detailed_2022 = aggregate_account_deal_summary(df_2022)
detailed_2023 = aggregate_account_deal_summary(df_2023)
detailed_2024 = aggregate_account_deal_summary(df_2024)

def export_processed_data(detailed_dfs, years):
    # Create processed directory if it doesn't exist
    processed_dir = '../Data/processed'
    os.makedirs(processed_dir, exist_ok=True)
    
    # Save each year's detailed summary
    for df, year in zip(detailed_dfs, years):
        output_path = f'{processed_dir}/processed_{year}.csv'
        df.to_csv(output_path, index=False)
        print(f"Saved processed_{year}.csv to {processed_dir}/")

# Save all detailed summaries
detailed_dfs = [detailed_2020, detailed_2021, detailed_2022, detailed_2023, detailed_2024]
years = ['2020', '2021', '2022', '2023', '2024']
export_processed_data(detailed_dfs, years)





# Print various statistics and insights about the data
for year, df in [('2020', detailed_2020), ('2021', detailed_2021), 
                 ('2022', detailed_2022), ('2023', detailed_2023), 
                 ('2024', detailed_2024)]:
    # Accounts with multiple deals
    multi_deals = df[df['Deals_Per_Account'] > 1]['AccountNumber'].nunique()
    print(f"\n{year} Statistics:")
    print(f"- {multi_deals} accounts have multiple deals")
    
    # Average deal value (convert to numeric first)
    df['Total_Amount'] = pd.to_numeric(df['Total_Amount'], errors='coerce')
    avg_deal = df['Total_Amount'].mean()
    print(f"- Average deal amount: ${avg_deal:,.2f}")
        
    # Product distribution
    product_dist = df['Product'].value_counts()
    print(f"- Most common products:")
    for prod, count in product_dist.head(3).items():
        print(f"  * {prod}: {count} deals")











