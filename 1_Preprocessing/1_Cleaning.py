import pandas as pd
import matplotlib.pyplot as plt
import os
# Read the 2020 data from Raw_data folder

df = pd.read_csv('../Data/Raw_data/2024.csv')
# Read the Oop_List data

df_opp = pd.read_csv('../Data/Raw_data/opp_List.csv')


# Filter df to only include products that are in df_opp's NAME column
# First, get the list of valid product names from df_opp
valid_products = df_opp['Name'].tolist()

# Filter df to only include rows where Product is in valid_products
df_filtered = df[df['Product'].isin(valid_products)]

# Show the results
print("Original df shape:", df.shape)
print("Filtered df shape:", df_filtered.shape)

# Create histogram to compare number of rows before and after filtering

# Calculate percentage of rows removed
total_rows = df.shape[0]
remaining_rows = df_filtered.shape[0]
removed_percentage = ((total_rows - remaining_rows) / total_rows) * 100

# Data for the histogram
labels = ['Before Filtering', 'After Filtering']
values = [df.shape[0], df_filtered.shape[0]]

# Create bar plot
plt.figure(figsize=(8, 6))
plt.bar(labels, values)

# Customize the plot
plt.title('Number of Rows Before and After Filtering\n'
          f'({removed_percentage:.1f}% of rows removed)')
plt.ylabel('Number of Rows')

# Add value labels on top of each bar
for i, v in enumerate(values):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.show()


# Update df with filtered version
df = df_filtered





