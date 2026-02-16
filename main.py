from collectors.data_collector import ESGDataCollector

COMPANIES = [
    {
        "name": "Unilever PLC",
        "ticker": "UL",
        "industry": "manufacturing"
    },
    {
        "name": "Johnson & Johnson",
        "ticker": "JNJ",
        "industry": "healthcare"
    },
    {
        "name": "JPMorgan Chase & Co.",
        "ticker": "JPM",
        "industry": "finance"
    },
    {
        "name": "Citigroup Inc.",
        "ticker": "C",
        "industry": "finance"
    },
    {
        "name": "Ford Motor Company",
        "ticker": "F",
        "industry": "manufacturing"
    }
]

if __name__ == "__main__":
    collector = ESGDataCollector()

    print("ESG Fraud Detection Project Initialized")

    # for company in COMPANIES:
    #     print(f"Downloading 10-K for {company['name']}")
    #     collector.download_10k(company["ticker"])











