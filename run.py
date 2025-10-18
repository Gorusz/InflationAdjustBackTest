import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration section
FILES_TO_PLOT = [
    {
        'filename': 'gold.csv',
        'label': 'Gold',
        'color': 'gold'
    },
    {
        'filename': 'msci_world.csv',
        'label': 'MSCI World',
        'color': 'blue'
    },
    #{
    #    'filename': 'msci_em.csv',
    #    'label': 'MSCI Emerging Markets',
    #    'color': 'green'
    #},
    # You can add or remove files here
    # {
    #     'filename': 'inflation.csv',
    #     'label': 'Inflation',
    #     'color': 'red'
    # }
]

# Read and process inflation data
def get_inflation_data():
    inflation_df = pd.read_csv('inflation.csv')
    # Create a date series from the inflation data (using December values)
    dates = pd.to_datetime([f"{row['Year']}/12" for _, row in inflation_df.iterrows()], format='%Y/%m')
    values = inflation_df['Dec'].values
    return pd.DataFrame({'Date': dates, 'Value': values})

# Plotting configuration
FIGURE_SIZE = (15, 8)
LINE_WIDTH = 2
NORMALIZE_START = 100  # Starting value for normalization

# Set the style for better visualization
plt.style.use('classic')

# Create a figure with the configured size
plt.figure(figsize=FIGURE_SIZE)

# Load inflation data
inflation_df = get_inflation_data()
target_cpi = inflation_df[inflation_df['Date'] == '2024-12'].iloc[0]['Value']

# Read all datasets first to find the latest start date
datasets = {}
latest_start_date = None

for file_config in FILES_TO_PLOT:
    try:
        # Read the data
        df = pd.read_csv(file_config['filename'])
        
        # Convert dates to datetime for better x-axis formatting
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%Y')
        
        # Merge with inflation data to get CPI values
        df_with_cpi = pd.merge_asof(df, inflation_df, on='Date', direction='nearest', 
                                   suffixes=('', '_cpi'))
        
        # Adjust for inflation (to Dec 2024 dollars)
        df_with_cpi['Value_Adjusted'] = df_with_cpi['Value'] * (target_cpi / df_with_cpi['Value_cpi'])
        
        # Store the dataset
        datasets[file_config['label']] = {
            'df': df_with_cpi,
            'config': file_config
        }
        
        # Update latest start date
        start_date = df_with_cpi['Date'].min()
        if latest_start_date is None or start_date > latest_start_date:
            latest_start_date = start_date
            
    except Exception as e:
        print(f"Error processing {file_config['filename']}: {str(e)}")

# Plot each dataset starting from the latest start date
for label, dataset in datasets.items():
    try:
        df = dataset['df']
        config = dataset['config']
        
        # Filter data to start from the latest start date
        df_aligned = df[df['Date'] >= latest_start_date].copy()
        
        # Normalize the inflation-adjusted values to 100 at the start of the aligned period
        first_value = df_aligned['Value_Adjusted'].iloc[0]
        df_aligned['Value_Normalized'] = df_aligned['Value_Adjusted'] / first_value * NORMALIZE_START
        
        # Plot the data
        plt.plot(df_aligned['Date'], 
                df_aligned['Value_Normalized'], 
                label=config['label'], 
                linewidth=LINE_WIDTH,
                color=config.get('color'))
        
        print(f"\nData for {label}:")
        print(f"Aligned start date: {latest_start_date.strftime('%m/%Y')}")
        print(f"End date: {df_aligned['Date'].iloc[-1].strftime('%m/%Y')}")
        print(f"Final normalized value: {df_aligned['Value_Normalized'].iloc[-1]:.2f}")
        
    except Exception as e:
        print(f"Error plotting {label}: {str(e)}")

# Customize the plot
plt.title(f'Inflation-Adjusted Asset Performance (Dec 2024 Dollars)\nAligned from {latest_start_date.strftime("%m/%Y")} (Starting Value = 100)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Normalized Value (Log Scale)', fontsize=12)
plt.yscale('log')  # Set logarithmic scale for y-axis
plt.legend(fontsize=10, loc='upper left')
plt.grid(True, alpha=0.3, which='both')  # Add grid lines for both major and minor ticks

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the plot
plt.savefig('asset_comparison_normalized.png')

# Show the plot
plt.show()