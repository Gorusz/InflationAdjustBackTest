import pandas as pd

# Read the inflation data
df = pd.read_csv('inflation.csv')

# Display the first 5 rows
print("\nFirst 5 rows of the inflation data:")
print(df.head())

# Display basic information about the dataset
print("\nDataset information:")
print(df.info())
