import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "explodingtopics_chatgpt_monthly_visits.csv"


def load_and_prepare(csv_path=CSV_PATH):
    """
    Load scraped ChatGPT monthly visits and ensure proper date sorting.
    """
    df = pd.read_csv(csv_path)

    # Ensure month_date exists and is datetime
    if "month_date" not in df.columns:
        df["month_date"] = pd.to_datetime(df["month_label"], format="%B %Y")

    df = df.sort_values("month_date").reset_index(drop=True)
    return df


def plot_monthly_visits_line(df):
    """
    Plot ChatGPT monthly visits as a line graph.
    """
    plt.figure(figsize=(12, 6))

    plt.plot(
        df["month_date"],
        df["visits_millions"],
        marker="o",
        linestyle="-",
        linewidth=2,
        color="#4a90e2",
    )

    # Add point labels
    for x, y in zip(df["month_date"], df["visits_millions"]):
        plt.text(
            x,
            y,
            f"{y:.0f}M",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.title("ChatGPT Monthly Visits Over Time")
    plt.ylabel("Monthly Visits (millions)")
    plt.xlabel("Date")
    plt.grid(True, alpha=0.3)

    # Format x-axis ticks nicely
    plt.xticks(df["month_date"], df["month_label"], rotation=60, ha="right")

    plt.tight_layout()

    output_file = "chatgpt_monthly_visits_line_chart.png"
    plt.savefig(output_file, dpi=600)
    print(f"[DONE] Saved line chart -> {output_file}")

    plt.show()


def main():
    df = load_and_prepare(CSV_PATH)
    print("[INFO] Loaded data:")
    print(df)
    plot_monthly_visits_line(df)


if __name__ == "__main__":
    main()
