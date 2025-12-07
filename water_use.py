import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("data.csv")

# Make sure Date is a datetime column
df["Date"] = pd.to_datetime(df["Date"])

# Create a time-series plot of water consumption intensity
plt.figure(figsize=(10, 5))
plt.plot(df["Date"], df["WC (m3/MWh)"])

plt.xlabel("Date and Time")
plt.ylabel("Water Consumption Intensity (m³/MWh)")
plt.title("AECI Water Consumption Intensity Over Time")

plt.tight_layout()
plt.savefig("aeci_wc_timeseries.png", dpi=300)
plt.show()
