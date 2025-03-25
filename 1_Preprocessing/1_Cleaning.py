import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the  data from Raw_data folder and filter data  based on OPP  list
def filter_products_pipeline(input_csv):
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

df_2020=filter_products_pipeline(input_csv='2020.csv')
df_2021=filter_products_pipeline(input_csv='2021.csv')
df_2022=filter_products_pipeline(input_csv='2022.csv')
df_2023=filter_products_pipeline(input_csv='2023.csv')
df_2024=filter_products_pipeline(input_csv='2024.csv')









