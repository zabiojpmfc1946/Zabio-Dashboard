---
name: zabio-weekly-analyst
description: Comprehensive financial analyst for Zabio. Use this skill once a week when the user provides new transaction data (CSV) to update KPIs, client velocity, concentration risk, and cohort retention. The skill automates data cleaning, processing, and dashboard generation, and handles deployment to the shared Vercel environment.
---

# Zabio Weekly Analyst

This skill automates the end-to-end data pipeline for the Zabio Strategic Dashboard. Follow these steps every time new raw data is received.

## Weekly Workflow

### 1. Data Ingestion
Accept the raw CSV file from the user. Save it to the project root for processing.

### 2. Run Automation
Execute the master orchestrator to clean entity names, calculate metrics, and regenerate the visuals:
```bash
python3 zabio-analyst/scripts/orchestrator.py <path_to_csv>
```

### 3. Quality Audit
Verify the output in the terminal and check `dashboard.html`. Ensure:
- Total volumes match business expectations.
- Client names are standardized (no "#N/A" or raw addresses).
- Heatmap shows current month activity.

### 4. Deploy & Sync
Push the updated dashboard and metrics to the team repository to trigger the Vercel update:
```bash
git add dashboard.html .tmp/metrics.json
git commit -m "Weekly data update: $(date +'%Y-%m-%d')"
git push origin main
```
**Repository**: [https://github.com/zabiojpmfc1946/Zabio-Dashboard](https://github.com/zabiojpmfc1946/Zabio-Dashboard)

## Bundled Resources

### Scripts (`scripts/`)
- `orchestrator.py`: Entry point for the weekly update.
- `correct_csv.py`: Cleans and standardizes company names using the wallet mapping.
- `process_data.py`: Computes financial KPIs, cohort retention, and market share.
- `generate_dashboard.py`: Renders the interactive HTML dashboard with zoom and tooltips.

### References (`references/`)
- `wallet_mapping.md`: Source of truth for entity addresses (if extracted from `correct_csv.py`).

## Technical Support
If the dashboard fails to render, ensure the CSV headers match:
`Transaction Hash,UnixTimestamp,DateTime (UTC),From,Empresa,To,TokenValue,USDValueDayOfTx,ContractAddress,TokenSymbol`
