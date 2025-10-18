import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Set the style for better visualization
plt.style.use('classic')

# Read all data files
inflation_df = pd.read_csv('inflation.csv')
gold_df = pd.read_csv('gold.csv')
msci_em_df = pd.read_csv('msci_em.csv')
msci_world_df = pd.read_csv('msci_world.csv')

# Convert dates to datetime for better x-axis formatting
gold_df['Date'] = pd.to_datetime(gold_df['Date'], format='%m/%d/%Y')
msci_world_df['Date'] = pd.to_datetime(msci_world_df['Date'], format='%m/%Y')
msci_em_df['Date'] = pd.to_datetime(msci_em_df['Date'], format='%m/%Y')

# Normalize the values (set starting point to 100)
gold_df['Value_Normalized'] = gold_df['Value'] / gold_df['Value'].iloc[0] * 100
msci_world_df['IWDA_Normalized'] = msci_world_df['IWDA'] / msci_world_df['IWDA'].iloc[0] * 100
msci_em_df['EM_Normalized'] = msci_em_df['MSCI Emerging Markets'] / msci_em_df['MSCI Emerging Markets'].iloc[0] * 100

# Create a figure with a larger size
plt.figure(figsize=(15, 8))

# Plot each dataset
plt.plot(msci_world_df['Date'], msci_world_df['IWDA_Normalized'], label='MSCI World', linewidth=2)
plt.plot(msci_em_df['Date'], msci_em_df['EM_Normalized'], label='MSCI Emerging Markets', linewidth=2)
plt.plot(gold_df['Date'], gold_df['Value_Normalized'], label='Gold', linewidth=2)

# Customize the plot
plt.title('Normalized Asset Performance Comparison (Starting Value = 100)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Normalized Value', fontsize=12)
plt.legend(fontsize=10, loc='upper left')
plt.grid(True, alpha=0.3)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot
plt.savefig('asset_comparison_normalized.png')

# Show the plot
plt.show()

# Display some basic statistics
print("\nComparison of returns:")
end_dates = {
    'MSCI World': msci_world_df['Date'].max(),
    'MSCI EM': msci_em_df['Date'].max(),
    'Gold': gold_df['Date'].max()
}

print(f"\nFinal normalized values (starting from 100):")
print(f"MSCI World (as of {end_dates['MSCI World'].strftime('%Y-%m')}): {msci_world_df['IWDA_Normalized'].iloc[-1]:.2f}")
print(f"MSCI EM (as of {end_dates['MSCI EM'].strftime('%Y-%m')}): {msci_em_df['EM_Normalized'].iloc[-1]:.2f}")
print(f"Gold (as of {end_dates['Gold'].strftime('%Y-%m')}): {gold_df['Value_Normalized'].iloc[-1]:.2f}")