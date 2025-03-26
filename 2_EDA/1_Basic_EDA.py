import pandas as pd

# Read the detailed 2020 data
df_2020 = pd.read_csv('../Data/processed/processed_2020.csv')


df_2020.head()

df_2020.isnull().sum()

df_2020.info()

df_2020.describe()

df_2020.shape

df_2020.columns




# Analyze distribution of Deals_Per_Account
deals_dist = df_2020['Deals_Per_Account'].value_counts().sort_index()

# Create a bar plot to visualize the distribution
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
deals_dist.plot(kind='bar')
plt.title('Distribution of Deals Per Account')
plt.xlabel('Number of Deals')
plt.ylabel('Count of Accounts')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels on top of each bar
for i, v in enumerate(deals_dist):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.show()

# Show the numerical breakdown
print("\nNumerical breakdown of deals per account:")
print(deals_dist)
print("\nPercentage breakdown:")
print((deals_dist / len(df_2020) * 100).round(2), "%")


df_2020.head()



# Check for duplicate Deal Numbers
duplicate_deals = df_2020[df_2020.duplicated(subset=['DealNumber'], keep=False)]

print("\nNumber of duplicate Deal Numbers:", len(duplicate_deals))

if len(duplicate_deals) > 0:
    print("\nDuplicate Deal Numbers found:")
    print(duplicate_deals.sort_values('Deal_Number'))
else:
    print("\nNo duplicate Deal Numbers found.")


    # Calculate average Total_Amount per DealNumber
    deal_averages = df_2020.groupby('DealNumber')['Total_Amount'].mean()
    
    # Calculate total sum of all deal averages
    total_deal_averages = deal_averages.sum()
    
    # Get count of unique deal numbers
    unique_deals_count = df_2020['DealNumber'].nunique()
    
    # Calculate overall average per unique deal
    overall_deal_average = total_deal_averages / unique_deals_count
    
    print("\nAnalysis of Deal Amounts:")
    print(f"Total sum of deal averages: ${total_deal_averages:,.2f}")
    print(f"Number of unique deals: {unique_deals_count}")
    print(f"Overall average amount per unique deal: ${overall_deal_average:,.2f}")
    
    # Display first few deal averages for verification
    print("\nSample of average amounts per deal:")
    print(deal_averages.head())
