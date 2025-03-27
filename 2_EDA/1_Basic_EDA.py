import pandas as pd
import matplotlib.pyplot as plt
# Read the detailed 2020 data
df_2020 = pd.read_csv('../Data/processed/processed_2020.csv')
df_2021 = pd.read_csv('../Data/processed/processed_2021.csv')
df_2022 = pd.read_csv('../Data/processed/processed_2022.csv')
df_2023 = pd.read_csv('../Data/processed/processed_2023.csv')
df_2024 = pd.read_csv('../Data/processed/processed_2024.csv')

# Read and analyze all files
def analyze_all_data(df, year):
    """
    Analyze deals data for a specific dataframe and year
    
    Args:
        df: Pandas DataFrame containing deals data
        year: Year of the data (used for file naming)
    
    Returns:
        tuple: (deals_distribution, account_statistics, overall_average)
    """
    # Get deals distribution
    deals_dist = df['Deals_Per_Account'].value_counts().sort_index()
    
    # Plot distribution
    plt.figure(figsize=(10, 6))
    deals_dist.plot(kind='bar')
    plt.title(f'Distribution of Deals Per Account - {year}')
    plt.xlabel('Number of Deals')
    plt.ylabel('Count of Accounts')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels
    for i, v in enumerate(deals_dist):
        plt.text(i, v, str(v), ha='center', va='bottom')
    plt.show()

    # Calculate account statistics
    account_stats_list = []
    print(f"\nDetailed analysis for {year}:")
    
    for num_deals in range(1, 10):
        deals = df[df['Deals_Per_Account'] == num_deals]
        if len(deals) > 0:
            avg_per_account = deals.groupby('AccountNumber')['Total_Amount'].agg(['count', 'mean'])
            account_stats_list.append(avg_per_account)
            
            print(f"\nAccounts with {num_deals} deal{'s' if num_deals > 1 else ''}:")
            print(f"Number of accounts: {len(deals)//num_deals}")
            print("\nExample averages:")
            print(avg_per_account.head())

    # Combine all statistics
    account_stats = pd.concat(account_stats_list)
    account_stats = account_stats.reset_index()
    account_stats = account_stats.rename(columns={
        'AccountNumber': 'AccountNumber',
        'count': 'Unique_Deal_Count',
        'mean': 'Total_Amount'
    })

    # Calculate overall average
    overall_avg = account_stats['Total_Amount'].mean()
    
    print("\nCombined statistics summary:")
    print(account_stats.head())
    print(f"\nTotal accounts analyzed: {len(account_stats)}")
    print(f"\nOverall average amount: ${overall_avg:,.2f}")
    
    # Create Average directory if it doesn't exist
    import os
    os.makedirs('../Data/Average', exist_ok=True)
    
    # Save account statistics with year in filename
    output_path = f'../Data/Average/account_stats_{year}.csv'
    account_stats.to_csv(output_path, index=False)
    print(f"\nAccount statistics saved to: {output_path}")
    
    return deals_dist, account_stats, overall_avg

analyze_all_data(df_2020, '2020')
analyze_all_data(df_2021, '2021')
analyze_all_data(df_2022, '2022')
analyze_all_data(df_2023, '2023')
analyze_all_data(df_2024, '2024')







