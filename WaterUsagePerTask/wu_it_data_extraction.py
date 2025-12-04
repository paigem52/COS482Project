# ---------------------------
# Full script: Scrape + Add Hardcoded Use Cases + Single Inference Plot
# ---------------------------

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import time

# ---- Selenium setup ----
options = Options()
# options.headless = True  # optional
driver = webdriver.Chrome(options=options)

url = "https://talirezun.com/energy-and-water-footprint-of-gen-ai-dashboard/"
driver.get(url)
time.sleep(5)

html = driver.page_source
driver.quit()

# ---- Parse HTML ----
tables = pd.read_html(StringIO(html))
df_inference = tables[0]
df_inference.columns = ["Task", "Model", "Energy_Wh", "Water_mL"]
df_inference["Water_L"] = df_inference["Water_mL"] / 1000

# ---------------------------------------------
# HARD-CODED USE CASES (NON-TEXT)
# ---------------------------------------------
df_extra = pd.DataFrame({
    "Task": ["Code Generation", "Image Description", "Data Analysis"],
    "Model": ["GPT-4o", "GPT-4o", "GPT-4o"],
    "Water_mL": [15, 12, 18]
})
df_extra["Water_L"] = df_extra["Water_mL"] / 1000

df_extra_llama = pd.DataFrame({
    "Task": ["Code Generation", "Image Description", "Data Analysis"],
    "Model": ["LLaMA 3.1", "LLaMA 3.1", "LLaMA 3.1"],
    "Water_mL": [9, 8, 13]
})
df_extra_llama["Water_L"] = df_extra_llama["Water_mL"] / 1000

# ---------------------------------------------
# Fix LLaMA naming issues
# ---------------------------------------------
def clean_model_names(df):
    return df.assign(Model=df["Model"].str.strip().str.replace("Llama", "LLaMA", case=False))

df_inference = clean_model_names(df_inference)
df_extra = clean_model_names(df_extra)
df_extra_llama = clean_model_names(df_extra_llama)

# ---------------------------------------------
# Remove empty/all-NA columns (FutureWarning fix)
# ---------------------------------------------
df_inference = df_inference.dropna(axis=1, how='all')
df_extra = df_extra.dropna(axis=1, how='all')
df_extra_llama = df_extra_llama.dropna(axis=1, how='all')

# ---------------------------------------------
# Merge all inference tasks
# ---------------------------------------------
df_inference = pd.concat([df_inference, df_extra, df_extra_llama], ignore_index=True)

# ---------------------------------------------
# REMOVE ChatGPT ("Saying Please")
# ---------------------------------------------
df_inference = df_inference[df_inference["Model"] != "ChatGPT"]
df_inference = df_inference[~df_inference["Task"].str.contains("Please", na=False, case=False)]

# ---------------------------------------------
# Colors
# ---------------------------------------------
model_colors = {
    "GPT-4o": "#4C72B0",
    "LLaMA 3.1": "#55A868"
}

# ---------------------------------------------
# Single Inference Plot
# ---------------------------------------------
pivot_inf = df_inference.pivot(index="Task", columns="Model", values="Water_L")

fig, ax = plt.subplots(figsize=(10, 6))

bars = pivot_inf.plot(
    kind="bar",
    ax=ax,
    color=[model_colors.get(m, "#888") for m in pivot_inf.columns]
)

ax.set_title("Water Consumption by AI Use Case (Inference Only)")
ax.set_ylabel("Water (Liters)")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
ax.grid(axis="y", linestyle="--", alpha=0.5)

# Bar labels
for container in ax.containers:
    labels = [f"{v.get_height():.2f}" if v.get_height() > 0 else "" for v in container]
    ax.bar_label(container, labels=labels, padding=3)

plt.tight_layout()

# Save and show
plt.savefig('InferenceTasks_BarChart.png')
plt.show()

