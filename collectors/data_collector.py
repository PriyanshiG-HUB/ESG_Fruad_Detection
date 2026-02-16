# collectors/data_collector.py

import os
import requests
import pandas as pd
from sec_edgar_downloader import Downloader


class ESGDataCollector:
    def __init__(self):
        self.sec_dir = r"C:\ESG_Fraud_Detection\data\raw\sec"
        self.epa_dir = r"C:\ESG_Fraud_Detection\data\raw\epa"

        os.makedirs(self.sec_dir, exist_ok=True)
        os.makedirs(self.epa_dir, exist_ok=True)

        self.dl = Downloader(
            company_name="ESG Fraud Detection Project",
            email_address="student@college.edu",
            download_folder=self.sec_dir
        )

    # -------- SEC EDGAR --------
    def download_10k(self, ticker):
        path = os.path.join(self.sec_dir, "sec-edgar-filings", ticker, "10-K")

        # Prevent duplicate downloads
        if os.path.exists(path):
            print(f"10-K already exists for {ticker}, skipping download.")
            return

        # Download only 2022–2024 filings
        self.dl.get(
            "10-K",
            ticker,
            after="2022-01-01",
            before="2025-01-01"
        )

    # -------- EPA DATA --------
    def fetch_epa_emissions(self, company_name, facility_id):
        base_url = "https://data.epa.gov/efservice"
        url = f"{base_url}/PUB_FACTS_SECTOR_GHG/FACILITY_ID/{facility_id}/JSON"

        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()

            df = pd.DataFrame(response.json())

            company_folder = os.path.join(
                self.epa_dir, company_name.replace(" ", "_")
            )
            os.makedirs(company_folder, exist_ok=True)

            df.to_csv(
                f"{company_folder}/{facility_id}.csv",
                index=False
            )

            print(f"EPA data saved for {company_name}")

        except Exception as e:
            print(f"EPA fetch failed for {company_name}: {e}")
            print("→ Using EPA fallback value (handled later)")