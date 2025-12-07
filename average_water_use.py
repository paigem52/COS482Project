import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Load all CSVs matching the naming pattern
files = sorted(glob.glob('national_average_*.csv'))

years = []
wc_values = []

for f in files:
    # Extract year from file name
    year = int(os.path.basename(f).split('_')[2].split('.')[0])
    
    # Read the CSV
    df = pd.read_csv(f)
    
    # Compute the average WC for this year
    wc = df['WC (m3/MWh)'].mean()
    
    years.append(year)
    wc_values.append(wc)

# Create summary dataframe
summary = pd.DataFrame({
    'Year': years,
    'WC_m3_per_MWh': wc_values
}).sort_values('Year')


# --- BAR CHART ---
plt.figure(figsize=(10,5))
plt.bar(summary['Year'], summary['WC_m3_per_MWh'], color='orange')
plt.xlabel('Year')
plt.ylabel('Average Water Consumption (m3/MWh)')
plt.title('National Average Water Consumption by Year')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('water_usage_bar.png', dpi=300)
plt.show()


# --- LINE CHART ---
plt.figure(figsize=(10,5))
plt.plot(summary['Year'], summary['WC_m3_per_MWh'], marker='o', color='orange')
plt.xlabel('Year')
plt.ylabel('Average Water Consumption (m3/MWh)')
plt.title('National Average Water Consumption Trend')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('water_usage_line.png', dpi=300)
plt.show()

