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


def analyze_yearly_trends():
    """
    Analyze and visualize yearly trends including totals, averages, and customer counts
    Uses colorful histograms and detailed statistics
    """
    print("\n=== YEARLY TREND ANALYSIS ===")
    print("=" * 50)
    
    # Set up color scheme
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
    
    # Compare total amounts across years
    print("\nComparing total amounts across years:")
    print("-" * 50)

    yearly_totals = {}
    for year, color in zip(['2020', '2021', '2022', '2023', '2024'], colors):
        stats_file = f'../Data/Average/account_stats_{year}.csv'
        if os.path.exists(stats_file):
            df = pd.read_csv(stats_file)
            total = df['Total_Amount'].sum()
            yearly_totals[year] = total
            print(f"{year} Total Amount: ${total:,.2f}")

    # Visualize yearly totals with enhanced styling
    plt.figure(figsize=(12, 7))
    years = list(yearly_totals.keys())
    totals = list(yearly_totals.values())

    bars = plt.bar(years, totals, color=colors)
    plt.title('Total Revenue by Year', fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Total Revenue ($)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    # Add value labels with enhanced formatting
    for bar, v in zip(bars, totals):
        plt.text(bar.get_x() + bar.get_width()/2, v,
                f'${v:,.0f}', 
                ha='center', va='bottom',
                fontsize=10, fontweight='bold')

    # Calculate and display year-over-year changes
    print("\nYear-over-Year Revenue Changes:")
    print("-" * 50)
    for i in range(1, len(years)):
        prev_year = years[i-1]
        curr_year = years[i]
        change = ((yearly_totals[curr_year] - yearly_totals[prev_year]) / yearly_totals[prev_year]) * 100
        print(f"{prev_year} → {curr_year}: {change:+.1f}% {'📈' if change > 0 else '📉'}")

    plt.show()

    # Calculate and visualize yearly averages
    print("\nYearly Average Deal Amounts:")
    print("-" * 50)

    yearly_averages = {}
    for year, color in zip(['2020', '2021', '2022', '2023', '2024'], colors):
        stats_file = f'../Data/Average/account_stats_{year}.csv'
        if os.path.exists(stats_file):
            df = pd.read_csv(stats_file)
            avg = df['Total_Amount'].mean()
            yearly_averages[year] = avg
            print(f"{year} Average Deal: ${avg:,.2f}")

    # Enhanced visualization of yearly averages
    plt.figure(figsize=(12, 7))
    years = list(yearly_averages.keys())
    averages = list(yearly_averages.values())

    bars = plt.bar(years, averages, color=colors)
    plt.title('Average Deal Amount by Year', fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Average Deal Amount ($)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    for bar, v in zip(bars, averages):
        plt.text(bar.get_x() + bar.get_width()/2, v,
                f'${v:,.0f}',
                ha='center', va='bottom',
                fontsize=10, fontweight='bold')

    plt.show()

    # Calculate and visualize monthly averages
    print("\nMonthly Average Deal Amounts:")
    print("-" * 50)

    monthly_averages = {year: avg/12 for year, avg in yearly_averages.items()}
    for year, monthly_avg in monthly_averages.items():
        print(f"{year} Monthly Average: ${monthly_avg:,.2f}")

    # Enhanced visualization of monthly averages
    plt.figure(figsize=(12, 7))
    bars = plt.bar(years, list(monthly_averages.values()), color=colors)
    plt.title('Average Monthly Deal Amount', fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Monthly Average ($)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    for bar, v in zip(bars, monthly_averages.values()):
        plt.text(bar.get_x() + bar.get_width()/2, v,
                f'${v:,.0f}',
                ha='center', va='bottom',
                fontsize=10, fontweight='bold')

    plt.show()

    # Calculate and visualize customer counts
    print("\nYearly Customer Analysis:")
    print("-" * 50)

    customers_per_year = {}
    for year, color in zip(['2020', '2021', '2022', '2023', '2024'], colors):
        stats_file = f'../Data/Average/account_stats_{year}.csv'
        if os.path.exists(stats_file):
            df = pd.read_csv(stats_file)
            unique_customers = df['AccountNumber'].nunique()
            customers_per_year[year] = unique_customers
            print(f"{year} Active Customers: {unique_customers:,}")

    # Enhanced visualization of customer counts
    plt.figure(figsize=(12, 7))
    years = list(customers_per_year.keys())
    customer_counts = list(customers_per_year.values())

    bars = plt.bar(years, customer_counts, color=colors)
    plt.title('Active Customers by Year', fontsize=14, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    for bar, v in zip(bars, customer_counts):
        plt.text(bar.get_x() + bar.get_width()/2, v,
                f'{v:,}',
                ha='center', va='bottom',
                fontsize=10, fontweight='bold')

    plt.show()

# Run the analysis
analyze_yearly_trends()
