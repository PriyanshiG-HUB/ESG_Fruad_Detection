import os

def get_10k_files_by_year(ticker, base_dir, years=[2022, 2023, 2024]):
    """
    Returns full-submission.txt paths for selected years
    """
    filings_dir = os.path.join(
        base_dir,
        "sec-edgar-filings",
        ticker,
        "10-K"
    )

    selected_files = []

    for folder in os.listdir(filings_dir):
        for year in years:
            if f"-{str(year)[-2:]}-" in folder:
                file_path = os.path.join(
                    filings_dir,
                    folder,
                    "full-submission.txt"
                )
                if os.path.exists(file_path):
                    selected_files.append((year, file_path))

    return selected_files