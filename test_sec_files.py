from collectors.sec_utils import get_10k_files_by_year

files = get_10k_files_by_year(
    ticker="F",
    base_dir="data/raw/sec"
)

for year, path in files:
    print(year, path)