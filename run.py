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
    {
        'filename': 'msci_em.csv',
        'label': 'MSCI Emerging Markets',
        'color': 'green'
    },
    # You can add or remove files here
    # {
    #     'filename': 'inflation.csv',
    #     'label': 'Inflation',
    #     'color': 'red'
    # }
]

# Plotting configuration
FIGURE_SIZE = (15, 8)
LINE_WIDTH = 2
NORMALIZE_START = 100  # Starting value for normalization

# Set the style for better visualization
plt.style.use('classic')

# Create a figure with the configured size
plt.figure(figsize=FIGURE_SIZE)

# Read and plot each dataset
for file_config in FILES_TO_PLOT:
    try:
        # Read the data
        df = pd.read_csv(file_config['filename'])
        
        # Convert dates to datetime for better x-axis formatting
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%Y')
        
        # Normalize the values
        df['Value_Normalized'] = df['Value'] / df['Value'].iloc[0] * NORMALIZE_START
        
        # Plot the data
        plt.plot(df['Date'], 
                df['Value_Normalized'], 
                label=file_config['label'], 
                linewidth=LINE_WIDTH,
                color=file_config.get('color'))
        
        print(f"\nData for {file_config['label']}:")
        print(f"Start date: {df['Date'].iloc[0].strftime('%m/%Y')}")
        print(f"End date: {df['Date'].iloc[-1].strftime('%m/%Y')}")
        print(f"Final normalized value: {df['Value_Normalized'].iloc[-1]:.2f}")
        
    except Exception as e:
        print(f"Error processing {file_config['filename']}: {str(e)}")

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