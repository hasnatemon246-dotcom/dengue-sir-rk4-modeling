import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# File paths
csv_file = "data/dengue_summary2.xlsx"
output_image = "images/dengue_data_visualization.png"

print("Generating Dengue Data Visualization...\n" + "="*50)

try:
    # 1. Load CSV Data
    df = pd.read_excel(csv_file)

    # 2. Convert 'Date' column to datetime objects
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # 3. Convert numerical columns to float/int, safely handling missing 'N/A' values
    numeric_cols = ['Weekly Case', 'Weekly Death',
                    'Cumulative Case', 'Cumulative Death']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with invalid dates and sort chronologically
    df = df.dropna(subset=['Date']).sort_values('Date')

    # 4. Set overall Plot style and layout (2x2 Grid)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Dengue Epidemiological Trend Analysis',
                 fontsize=16, fontweight='bold', y=0.98)

    # Subplot 1: Weekly Cases
    axes[0, 0].plot(df['Date'], df['Weekly Case'], color='blue',
                    marker='o', linewidth=1, label='Weekly Cases')
    axes[0, 0].set_title('Weekly Cases', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Number of Cases')
    axes[0, 0].grid(True, linestyle='--', alpha=0.5)

    # Subplot 2: Weekly Deaths
    axes[0, 1].plot(df['Date'], df['Weekly Death'], color='red',
                    marker='o', linewidth=1, label='Weekly Deaths')
    axes[0, 1].set_title('Weekly Deaths', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Number of Deaths')
    axes[0, 1].grid(True, linestyle='--', alpha=0.5)

    # Subplot 3: Cumulative Cases
    axes[1, 0].plot(df['Date'], df['Cumulative Case'], color='orange',
                    marker='o', linewidth=1, label='Cumulative Cases')
    axes[1, 0].set_title('Cumulative Cases (Yearly Total)',
                         fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Total Cases')
    axes[1, 0].grid(True, linestyle='--', alpha=0.5)

    # Subplot 4: Cumulative Deaths
    axes[1, 1].plot(df['Date'], df['Cumulative Death'], color='purple',
                    marker='o', linewidth=1, label='Cumulative Deaths')
    axes[1, 1].set_title('Cumulative Deaths (Yearly Total)',
                         fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('Total Deaths')
    axes[1, 1].grid(True, linestyle='--', alpha=0.5)

    # Format Date Axis readability for all 4 subplots
    for ax in axes.flat:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

    # Adjust layout padding
    plt.tight_layout()

    # Save high-resolution PNG image
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"Success! Plot created and saved as '{output_image}'.")

    # Display the visual plot window
    plt.show()

except Exception as e:
    print(f"Error while plotting data: {e}")
