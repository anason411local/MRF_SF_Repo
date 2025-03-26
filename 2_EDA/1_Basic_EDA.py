import pandas as pd

# Read the detailed 2020 data
df_2020 = pd.read_csv('../Data/processed/detailed_2020.csv')


df_2020.head()

df_2020.isnull().sum()

df_2020.info()


