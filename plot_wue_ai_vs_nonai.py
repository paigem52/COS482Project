import re
import pandas as pd
import matplotlib.pyplot as plt

# Choose which grid/WUE you want to assume (liters per kWh).
# - 1.0   ~ Google-style WUE
# - 0.94  ~ ChatGPT per-request WUE you computed earlier
WUE_L_PER_KWH = 1.0


def load_digital_actions(csv_path="devera_digital_actions.csv"):
    """
    Load the 'Electricity and CO2 footprint of common digital actions (10 units)'
    table from Devera and return a cleaned DataFrame with numeric energy (Wh).
    """
    # Read with no header, then promote first row to header
    df_raw = pd.read_csv(csv_path, header=None)
    df_raw.columns = df_raw.iloc[0]
    df = df_raw.iloc[1:].reset_index(drop=True)

    # Standardize column names
    df.columns = ["Activity", "Energy (Wh)", "CO2 (g) [global avg]"]

    # Extract numeric Wh from strings like "3 Wh", "12.8 Wh"
    df["Energy_Wh_10units"] = (
        df["Energy (Wh)"]
        .astype(str)
        .str.extract(r"([\d\.]+)")
        .astype(float)
    )

    return df


def compute_water_per_unit(df):
    """
    Take the cleaned digital actions DataFrame and compute:
    - Energy per single unit (Wh)
    - Water per unit (L and mL) using the chosen WUE.
    """
    # Table is per 10 units → divide by 10 to get per 1 unit
    df["Energy_Wh_per_unit"] = df["Energy_Wh_10units"] / 10.0

    # Convert Wh → kWh
    df["Energy_kWh_per_unit"] = df["Energy_Wh_per_unit"] / 1000.0

    # Water = Energy * WUE
    df["Water_L_per_unit"] = df["Energy_kWh_per_unit"] * WUE_L_PER_KWH
    df["Water_mL_per_unit"] = df["Water_L_per_unit"] * 1000.0

    return df


def plot_water_bar_chart(df):
    """
    Plot water per unit (mL) for a subset of activities as a bar chart.
    """
    # Pick the activities you care about
    keep = [
        "ChatGPT x10 queries",
        "Google Search x10 queries",
        # uncomment if you want these too:
        #"TikTok x10 min",
        "Netflix x10 min",
    ]
    df_plot = df[df["Activity"].isin(keep)].copy()

    # Make nicer labels
    label_map = {
        "ChatGPT x10 queries": "ChatGPT (per query)",
        "Google Search x10 queries": "Google Search (per query)",
        "TikTok x10 min": "TikTok (per minute)",
        "Netflix x10 min": "Netflix (per minute)",
    }
    df_plot["Label"] = df_plot["Activity"].map(label_map)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(df_plot["Label"], df_plot["Water_mL_per_unit"])

    plt.ylabel("Water per action (mL)")
    plt.title("Water Use of AI vs Non-AI Digital Actions")
    plt.xticks(rotation=15, ha="right")

    # Add value labels on top of each bar (rounded to 3 decimals)
    for bar in bars:
        h = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            h,
            f"{h:.3f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()
    plt.savefig("WUE_AI_vs_nonAI_bar_chart.png", dpi=600)
    plt.show()


def main():
    df = load_digital_actions("devera_digital_actions.csv")
    df = compute_water_per_unit(df)

    print("[INFO] Digital actions with water per unit (mL):")
    print(df[["Activity", "Energy_Wh_per_unit", "Water_mL_per_unit"]])

    plot_water_bar_chart(df)


if __name__ == "__main__":
    main()
