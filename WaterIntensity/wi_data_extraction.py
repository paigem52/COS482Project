# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV file (skip first three header rows)
df = pd.read_csv(
    'WaterIntensity/global-water-consumption-in-the-energy-sector-by-fuel-and-power-generation-type-in-the-stated-policies-scenario-2021-and-2030.csv', 
    skiprows=3, index_col=0
)

# Clean column names (remove quotes and extra spaces)
df.columns = [col.strip().replace('"','') for col in df.columns]

# Clean index (remove whitespace)
df.index = df.index.astype(str).str.strip()

# Convert all data to numeric (in case of strings/commas)
df = df.apply(pd.to_numeric, errors='coerce')

# Prepare data for grouped bar chart
years = ['2021', '2030']  # index is string now
energy_types = df.columns
bar_width = 0.35
x = np.arange(len(energy_types))

# Create figure
plt.figure(figsize=(12,6))

# Bars for each year
plt.bar(x - bar_width/2, df.loc['2021'].values, width=bar_width, label='2021', color='#D4A017')
plt.bar(x + bar_width/2, df.loc['2030'].values, width=bar_width, label='2030', color="#12518B")

# Labels and formatting
plt.xticks(x, energy_types, rotation=45)
plt.xlabel('Energy Type')
plt.ylabel('Units: bcm')
plt.title('Energy Data Comparison: 2021 vs 2030')
plt.legend()
plt.tight_layout()

# Save and show
plt.savefig('WaterIntensity_BarChart.png')
plt.show()