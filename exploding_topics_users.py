import time
import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup  # pip install beautifulsoup4

START_URL = "https://explodingtopics.com/blog/chatgpt-users#chatgpt-user-growth"


def make_driver(headless=False):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,2000")
    opts.add_argument("--user-agent=Mozilla/5.0")
    return webdriver.Chrome(options=opts)


def extract_monthly_visits(html):
    """
    Parse the 'Here's how ChatGPT monthly visits progressed over time:'
    section and return a DataFrame with month and visits (in millions).
    """
    soup = BeautifulSoup(html, "html.parser")
    # Get all text as one big string with spaces
    text = soup.get_text(" ")

    marker = "Here's how ChatGPT monthly visits progressed over time:"
    start_idx = text.find(marker)
    if start_idx == -1:
        print("[WARN] Could not find monthly-visits section marker.")
        return None

    # Take chunk from marker onward
    chunk = text[start_idx:]

    # Optionally cut off at the end of the table section
    end_marker = "If you pay attention"
    end_idx = chunk.find(end_marker)
    if end_idx != -1:
        chunk = chunk[:end_idx]

    # Collapse whitespace
    chunk = " ".join(chunk.split())

    # Example we want to match:
    # "December 2022 264.7 million"
    # "February 2023 1.3 billion"
    pattern = r"([A-Za-z]+\s+\d{4})\s+([\d\.]+)\s+(million|billion)"
    matches = re.findall(pattern, chunk)

    if not matches:
        print("[WARN] No month/visits matches found in the monthly-visits chunk.")
        # Uncomment for debugging:
        # print(chunk)
        return None

    rows = []
    for month_str, num_str, unit in matches:
        try:
            value = float(num_str)
        except ValueError:
            continue

        # Normalize to "millions of visits"
        if unit.lower() == "billion":
            visits_millions = value * 1000.0
        else:
            visits_millions = value

        rows.append(
            {
                "month_label": month_str,       # e.g., "December 2022"
                "visits_millions": visits_millions,
                "visits_raw_value": value,
                "visits_unit": unit,            # "million" or "billion"
            }
        )

    if not rows:
        print("[WARN] Parsed zero valid rows.")
        return None

    df = pd.DataFrame(rows)

    # Optional: convert month_label → datetime
    

    return df


def main():
    driver = make_driver(headless=False)
    driver.get(START_URL)
    time.sleep(3)  # let the page load

    try:
        html = driver.page_source
        visits_df = extract_monthly_visits(html)

        if visits_df is not None:
            out_path = "explodingtopics_chatgpt_monthly_visits.csv"
            visits_df.to_csv(out_path, index=False)
            print(f"[DONE] Saved ChatGPT monthly visits table -> {out_path}")
            print(visits_df)
        else:
            print("[ERROR] Could not build monthly visits DataFrame.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
