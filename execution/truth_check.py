import csv
from collections import Counter
from datetime import datetime

INPUT_FILE = "export-address-token-0x90eF96BCFB3e798C6565CBBA6a587F14b58003D3 (3)(Sheet1).csv"

def analyze():
    symbols = Counter()
    companies = Counter()
    dates = []
    total_rows = 0
    
    with open(INPUT_FILE, mode='r', encoding='latin-1') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 10: continue
            total_rows += 1
            companies[row[4].strip()] += 1
            symbols[row[9].strip()] += 1
            dates.append(row[2])

    print(f"Total rows: {total_rows}")
    print("\nTop 20 Symbols:")
    for s, c in symbols.most_common(20):
        print(f"  {s}: {c}")
        
    print("\nTop 20 Companies (Column 4):")
    for s, c in companies.most_common(20):
        print(f"  '{s}': {c}")

    sorted_dates = sorted(dates)
    print(f"\nDate Range (lexicographical): {sorted_dates[0]} to {sorted_dates[-1]}")
    
if __name__ == "__main__":
    analyze()
