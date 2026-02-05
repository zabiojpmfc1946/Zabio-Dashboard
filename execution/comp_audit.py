import csv
from collections import defaultdict

INPUT_FILE = "export-address-token-0x90eF96BCFB3e798C6565CBBA6a587F14b58003D3 (3)(Sheet1).csv"
EXCLUDE = {'Empresa', 'Zabio', '#N/A', ''}

def audit():
    comp_tokens = defaultdict(set)
    with open(INPUT_FILE, mode='r', encoding='latin-1') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 10: continue
            name = row[4].strip()
            if name in EXCLUDE: continue
            symbol = row[9].strip()
            comp_tokens[name].add(symbol)
            
    print(f"Total Companies Found: {len(comp_tokens)}")
    for name, tokens in sorted(comp_tokens.items()):
        print(f"{name}: {tokens}")

if __name__ == "__main__":
    audit()
