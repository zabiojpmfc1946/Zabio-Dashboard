# Zabio Analytics Directive

This directive describes how to maintain and update the Zabio Business Intelligence Dashboard.

## Overview
The analytics system follows a 3-layer architecture:
- **Layer 3 (Execution)**: Python scripts that handle raw data and visualization.
- **Layer 2 (Orchestration)**: This directive, guiding the process.
- **Layer 1 (Skill)**: The `zabio-analyst` skill for agentic automation.

## Update Process

1. **Prepare Data**:
   - Export the latest transaction data from the blockchain explorer or CRM in CSV format.
   - Ensure the file is named `export-address-token-0x90... (Sheet1).csv` or update `INPUT_FILE` in `execution/process_data.py`.

2. **Process Metrics**:
   - Run the processing script to generate the intermediate metrics:
     ```bash
     python3 execution/process_data.py
     ```
   - This writes to `.tmp/metrics.json`.

3. **Generate Dashboard**:
   - Run the dashboard generation script:
     ```bash
     python3 execution/generate_dashboard.py
     ```
   - This produces `dashboard.html`.

4. **Verify**:
   - Open `dashboard.html` in a browser to review the KPIs.

## KPIs Measured
- **Total Clients**: Unique active addresses.
- **Active Clients**: Addresses with activity in the last 7 trailing days.
- **Total Volume (USD)**: Sum of all transactions in USD value.
- **Token Distribution**: Volume share by token (USDT, COPC, etc.).
- **Top Clients**: Table of the most significant entities by volume.
