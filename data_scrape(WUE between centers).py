import time
import pandas as pd
from io import StringIO

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

START_URL = "https://www.devera.ai/resources/the-environmental-impact-of-ai-energy-carbon-and-water-in-the-age-of-chatgpt"

def make_driver(headless=False):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,2000")
    opts.add_argument("--user-agent=Mozilla/5.0")
    return webdriver.Chrome(options=opts)


def extract_tables_from_page(driver):
    """
    Use Selenium to grab the HTML and let pandas read all <table> elements.
    Returns a list of DataFrames.
    """
    html = driver.page_source
    tables = pd.read_html(StringIO(html))  # avoid FutureWarning
    print(f"[INFO] Found {len(tables)} HTML tables on the Devera page.")
    return tables


def pick_digital_actions_table(tables):
    """
    Find the 'Electricity and CO2 footprint of common digital actions (10 units)'
    table. We look for 'Activity', 'Energy', and 'CO2' either in the *columns*
    or in the *first row* (since sometimes the header row is parsed as data).
    """
    for i, t in enumerate(tables):
        # Column names
        cols_lower = [str(c).lower() for c in t.columns]

        # First row values (if exists)
        if len(t) > 0:
            first_row_lower = [str(x).lower() for x in t.iloc[0].tolist()]
        else:
            first_row_lower = []

        combined = cols_lower + first_row_lower

        has_activity = any("activity" in s for s in combined)
        has_energy   = any("energy" in s for s in combined)
        has_co2      = any("co2" in s for s in combined)

        if has_activity and has_energy and has_co2:
            print(f"[INFO] Using table {i} as digital-actions table.")

            # If 'activity' etc. are in the first row but NOT in the column names,
            # promote the first row to be the header.
            if not any("activity" in s for s in cols_lower) and len(t) > 0:
                t = t.copy()
                t.columns = t.iloc[0]
                t = t.iloc[1:].reset_index(drop=True)

            return t

    print("[WARN] No obvious digital-actions table found; returning None.")
    return None


def main():
    driver = make_driver(headless=False)
    driver.get(START_URL)
    time.sleep(3)   # small delay so everything loads

    try:
        tables = extract_tables_from_page(driver)

        # Based on earlier inspection of the page:
        # tables[1] -> "Running the model: energy and carbon per user request"
        # tables[4] -> "Sustainability snapshot of major AI/cloud providers (2025)"
        energy_df   = tables[1]
        provider_df = tables[4]
        digital_df  = pick_digital_actions_table(tables)

        # ----- Energy per model table -----
        energy_df.columns = [str(c).strip() for c in energy_df.columns]
        energy_out = "devera_energy_per_request.csv"
        energy_df.to_csv(energy_out, index=False)
        print(f"[DONE] Saved energy per request table -> {energy_out}")
        print(energy_df.head())

        # ----- Provider WUE table -----
        provider_df.columns = [str(c).strip() for c in provider_df.columns]
        provider_out = "devera_provider_wue.csv"
        provider_df.to_csv(provider_out, index=False)
        print(f"[DONE] Saved provider WUE table -> {provider_out}")
        print(provider_df.head())

        # ----- Digital actions table (ChatGPT x10, Google Search x10, etc.) -----
        if digital_df is not None:
            digital_df.columns = [str(c).strip() for c in digital_df.columns]
            digital_out = "devera_digital_actions.csv"
            digital_df.to_csv(digital_out, index=False)
            print(f"[DONE] Saved digital actions table -> {digital_out}")
            print(digital_df.head())

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
