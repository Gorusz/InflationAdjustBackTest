import pandas as pd

# Function to standardize date format
def standardize_date(date_str):
    try:
        # For dates like MM/DD/YYYY
        date = pd.to_datetime(date_str)
        return date.strftime('%m/%Y')
    except:
        try:
            # For dates like MM/YYYY
            return date_str
        except:
            print(f"Could not parse date: {date_str}")
            return date_str

# Process Gold data
print("Processing gold.csv...")
gold_df = pd.read_csv('gold.csv')
gold_df['Date'] = gold_df['Date'].apply(standardize_date)
gold_df.columns = ['Date', 'Value']
gold_df.to_csv('gold_standardized.csv', index=False)

# Process MSCI World data
print("Processing msci_world.csv...")
msci_world_df = pd.read_csv('msci_world.csv')
msci_world_df.columns = ['Date', 'Value']
msci_world_df.to_csv('msci_world_standardized.csv', index=False)

# Process MSCI EM data
print("Processing msci_em.csv...")
msci_em_df = pd.read_csv('msci_em.csv')
msci_em_df.columns = ['Date', 'Value']
msci_em_df.to_csv('msci_em_standardized.csv', index=False)

print("Standardization complete. New files created with '_standardized' suffix.")
print("\nFirst few rows of each standardized file:")
print("\nGold:")
print(gold_df.head())
print("\nMSCI World:")
print(msci_world_df.head())
print("\nMSCI EM:")
print(msci_em_df.head())