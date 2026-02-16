import os
from analytics.financial_alignment import financial_esg_alignment


def load_latest_10k(ticker):
    base_path = f"data/raw/sec/sec-edgar-filings/{ticker}/10-K"

    folders = sorted(os.listdir(base_path))
    latest_folder = folders[-1]

    file_path = os.path.join(
        base_path,
        latest_folder,
        "full-submission.txt"
    )

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


# Example: Ford
filing_text = load_latest_10k("F")

result = financial_esg_alignment(
    company_name="Ford Motor Company",
    industry="manufacturing",
    filing_text=filing_text
)

print("\nFinancial–ESG Alignment Result:\n")
print(result)