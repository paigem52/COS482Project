import re
import pandas as pd
import matplotlib.pyplot as plt


def load_and_clean_provider_wue(csv_path="devera_provider_wue.csv"):
    """
    Load the provider WUE table from Devera and return:
        provider | wue_L_per_kWh
    as a clean DataFrame with numeric WUE.
    """
    # Read with no header so the first row stays as data
    df_raw = pd.read_csv(csv_path, header=None)

    # First row is the header row in the file
    df_raw.columns = df_raw.iloc[0]
    df = df_raw.iloc[1:].reset_index(drop=True)

    # Standardize column names
    df.columns = [
        "provider",
        "carbon_goal",
        "renewable",
        "pue",
        "water_goal",
        "wue_raw",
    ]

    # Extract numeric WUE from strings like "0.15 L/kWh", "~1 L/kWh", "ND (...)"
    def extract_wue(value):
        if isinstance(value, str):
            match = re.search(r"[\d.]+", value)
            if match:
                return float(match.group(0))
        return None  # for "ND" or missing

    df["wue_L_per_kWh"] = df["wue_raw"].apply(extract_wue)

    # Only keep provider and numeric WUE
    return df[["provider", "wue_L_per_kWh"]]


def add_chatgpt_wue(df):
    """
    Add a row for ChatGPT using Devera's numbers:
    ~0.32 mL water and 0.34 Wh per ChatGPT query.
    """
    water_L = 0.32 / 1000.0   # 0.32 mL → 0.00032 L
    energy_kWh = 0.34 / 1000.0  # 0.34 Wh → 0.00034 kWh
    wue_chatgpt = water_L / energy_kWh  # L per kWh (≈ 0.94)

    new_row = {
        "provider": "ChatGPT (per request)",
        "wue_L_per_kWh": wue_chatgpt,
    }

    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)


def plot_wue_bar_chart(df):
    """
    Plot a bar chart of WUE (L/kWh) by provider/system.
    """
    # Drop entries with no numeric WUE (e.g., Microsoft "ND")
    df_plot = df.dropna(subset=["wue_L_per_kWh"])

    plt.figure(figsize=(8, 5))
    bars = plt.bar(df_plot["provider"], df_plot["wue_L_per_kWh"])
    plt.ylabel("Water Usage Efficiency (L/kWh)")
    plt.title("Water Usage Efficiency Between Data Centers and ChatGPT")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2f}",     # format to 2 decimals
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.savefig("WUE Data Center Comparison Bar Chart.png", dpi = 600)
    plt.show()


def main():
    provider_wue = load_and_clean_provider_wue("devera_provider_wue.csv")
    provider_wue = add_chatgpt_wue(provider_wue)

    print("[INFO] Cleaned WUE data:")
    print(provider_wue)

    # Optional: save cleaned data
    provider_wue.to_csv("wue_between_centers_clean.csv", index=False)
    print("[DONE] Saved cleaned WUE data -> wue_between_centers_clean.csv")

    # Plot the bar chart
    plot_wue_bar_chart(provider_wue)


if __name__ == "__main__":
    main()
