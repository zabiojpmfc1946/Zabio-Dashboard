import csv
import json
import os
import sys
import random
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
INPUT_FILE = "export-address-token-0x90eF96BCFB3e798C6565CBBA6a587F14b58003D3 (3)(Sheet1).csv"
OUTPUT_METRICS = ".tmp/metrics.json"
ZABIO_ADDRESS = "0x90ef96bcfb3e798c6565cbba6a587f14b58003d3".lower()
STABLECOIN_SYMBOLS = {'USDT', 'USDC', 'USDT0'}

LOCATION_DATA = {
    "Bogota": {"lat": 4.7110, "lon": -74.0721},
    "Medellin": {"lat": 6.2442, "lon": -75.5812}
}

# USER PROVIDED MAPPING
WALLET_TO_COMPANY = {
    "0x90ef96bcfb3e798c6565cbba6a587f14b58003d3": "Zabio",
    "0xd86a5afe3dcc8d76f8d61db8dcbb48b2a29eea27": "Keto Group",
    "0xd86a5619b4a49319d2b7957037cab8aff367ea27": "Keto Group",
    "0x13d4c51985a287c25754944576c50911fb407dad": "Carlos Daniel OTC",
    "0xf74c31a102045184fe7d3821b5a61a92e40f4b19": "Activos Digitales",
    "0x71133c094ae933a779652a1201b5be923818d51d": "MiTec",
    "0x3eb296527614f3c7be16d5f8684df164d23d90f6": "Cripto manantial",
    "0x1f35b83b6ea222abbd2b0f7ffe6dbec58797e1d0": "Soluciones de abastecimiento Integral",
    "0x2370a1530701333ce394303dfe78a6c7f6605c05": "Digital Cash",
    "0xf0f7d6e94598be070f24d2f23085f7dff1f82682": "Carlos Cassiani",
    "0xdef32069f1544a29098d241bea179df52f936a00": "Cripto Xpress",
    "0xd1f3bb79e36813be4f21576cdda5d50f26083629": "Robotica innovacion sas",
    "0x52c5982d5a919717093021fb2cb8a672f8ce54b3": "SOLUCIONES DIGITALES NFT SAS",
    "0xa2764222ecf035c17533791ecb4281aafe622144": "Vivian Johanna Piedrahita Correa",
    "0x65d79c2c0bdb7d47400a21b50902d47c8a67bed8": "GMBank Casa De Las Monedas",
    "0xd518414d370464d78557ee63d49db794ae91edc3": "Wesley Smith",
    "0xcb5c5d6e1e23e664cff8c321079ef1bfb5fe7c30": "Crypto Go SAS",
    "0xe6c3500fc00585ce70d4c84941d0cf3f865446b5": "Jascalla",
    "0x5de536645a0b9434401cdd1a591c4a7bbac4b3ce": "FYNORA SAS",
    "0xa1f680b0b21bbab38dc6a30e449a93a08536d056": "Nicolás Calle Marín",
    "0xadc307f7b889187b066cd41cfee7fa9bf06f2969": "Profitnanzas JH",
    "0x5e0df580a309fd887939cb746e53bfea1b8d558a": "Good Venture SAS",
    "0x405733b90642cc71fd8a4e0e2650ec5b1313fd78": "PS613 SAS",
    "0xca843bdc40cbe25656af91cfb17c080a59f26733": "Miguel Tobon",
    "0xd80e209f8add77d873c44b3521853c1181fe3c85": "Salomé Gaviria",
    "0xd760fdfc2513077b104a53ca7cbbf7fa382b6580": "Salomé Gaviria",
    "0xea1c3d1cdf4c0cfb987dba6f2e0996feb340904d": "SureFX",
    "0xcb5212ba34e9a51141c6842a8fc5654dabb68e7c": "CC Pay",
    "0xf13146c59922b34326bf1dfea77966866b045ed5": "Hugo Alejandro Castano",
    "0xe0f00cd1084189ce53472a423f1fa8ab166d76bb": "Yanet Giraldo",
    "0xfe70d9fb663ad57259c2c030ef064019c4a9c69c": "Santa Rosa Agroindustrial SAS",
    "0x272fc655c121237d8b67642eed5c4734a8c137c3": "Precooperativa Mercantil de Colombia",
    "0xaeb10598876351722e19657e89666e659bd009f1": "COLOCA GROUP",
    "0x95e267687da3f302ae3716d22b24610cab7960aa": "INVERSIONES R CASTRO S.A.S."
}

def clean_value(value):
    if not value or any(x in str(value) for x in ["N/A", "Empresa"]):
        return 0.0
    clean = str(value).replace('$', '').replace(',', '').replace('"', '').strip()
    try:
        return float(clean)
    except ValueError:
        return 0.0

def process_data(input_path):
    if not os.path.exists(".tmp"):
        os.makedirs(".tmp")

    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found.")
        return

    data_points = []
    with open(input_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try: next(reader)
        except StopIteration: return
        for row in reader:
            if len(row) < 10: continue
            try:
                dt = datetime.strptime(row[2].strip(), '%m/%d/%Y %H:%M')
                data_points.append((row, dt))
            except: continue

    if not data_points: return
    data_points.sort(key=lambda x: x[1])
    
    start_dt = data_points[0][1]
    end_dt = data_points[-1][1]
    
    total_volume = 0.0
    total_tx_count = 0
    comp_metrics = defaultdict(lambda: {"vol": 0.0, "tx": 0, "dep": 0.0, "with": 0.0, "first_seen": None, "tx_dates": []})
    daily_vol = defaultdict(float)
    daily_client_vol = defaultdict(lambda: defaultdict(float))

    # Delta Calculation Windows
    curr_window_start = end_dt - timedelta(days=30)
    prev_window_start = end_dt - timedelta(days=60)
    prev_window_end = curr_window_start

    # Metrics Buckets
    m_curr = {"vol": 0.0, "tx": 0}
    m_prev = {"vol": 0.0, "tx": 0}

    for row, dt in data_points:
        from_addr = row[3].lower()
        to_addr = row[5].lower()
        symbol = row[9].strip()
        val = clean_value(row[6])
        
        # Delta Metrics Accumulation
        if any(s in symbol for s in [s for s in STABLECOIN_SYMBOLS]):
            if curr_window_start < dt <= end_dt:
                m_curr["vol"] += val
                m_curr["tx"] += 1
            elif prev_window_start < dt <= prev_window_end:
                m_prev["vol"] += val
                m_prev["tx"] += 1

        client_addr = from_addr if to_addr == ZABIO_ADDRESS else to_addr
        name = WALLET_TO_COMPANY.get(client_addr)
        if not name or name == "Zabio": continue

        if comp_metrics[name]["first_seen"] is None:
            comp_metrics[name]["first_seen"] = dt
        
        comp_metrics[name]["tx_dates"].append(dt)
        comp_metrics[name]["tx"] += 1
        total_tx_count += 1
        
        if any(s in symbol for s in STABLECOIN_SYMBOLS):
            total_volume += val
            comp_metrics[name]["vol"] += val
            day_str = dt.strftime('%Y-%m-%d')
            daily_vol[day_str] += val
            daily_client_vol[name][day_str] += val
            if to_addr == ZABIO_ADDRESS: comp_metrics[name]["dep"] += val
            else: comp_metrics[name]["with"] += val

    # Calculate Deltas for Entities
    verified_now = 0
    verified_prev = 0
    active_now = 0
    active_prev = 0

    for name, m in comp_metrics.items():
        if m["first_seen"] <= end_dt: verified_now += 1
        if m["first_seen"] <= curr_window_start: verified_prev += 1
        
        if any(curr_window_start <= d <= end_dt for d in m["tx_dates"]): active_now += 1
        if any(prev_window_start <= d <= prev_window_end for d in m["tx_dates"]): active_prev += 1

    def calc_delta(curr, prev):
        if prev == 0: return 100.0 if curr > 0 else 0.0
        return ((curr - prev) / prev) * 100.0

    delta_verified = calc_delta(verified_now, verified_prev)
    delta_active = calc_delta(active_now, active_prev)
    delta_vol = calc_delta(m_curr["vol"], m_prev["vol"])
    
    avg_tx_curr = m_curr["vol"] / m_curr["tx"] if m_curr["tx"] > 0 else 0
    avg_tx_prev = m_prev["vol"] / m_prev["tx"] if m_prev["tx"] > 0 else 0
    delta_avg_tx = calc_delta(avg_tx_curr, avg_tx_prev)

    sorted_comps = sorted(comp_metrics.items(), key=lambda x: x[1]["vol"], reverse=True)
    top_clients = [c[0] for c in sorted_comps[:5]]
    
    top_3_vol = sum(c[1]["vol"] for c in sorted_comps[:3])
    others_vol = total_volume - top_3_vol
    share_data = [
        {"label": sorted_comps[0][0], "vol": round(sorted_comps[0][1]["vol"], 2)},
        {"label": sorted_comps[1][0], "vol": round(sorted_comps[1][1]["vol"], 2)},
        {"label": sorted_comps[2][0], "vol": round(sorted_comps[2][1]["vol"], 2)},
        {"label": "Others", "vol": round(others_vol, 2)}
    ]

    velocity_data = []
    for name, m in comp_metrics.items():
        if m["tx"] > 0:
            velocity_data.append({
                "name": name,
                "tx_count": m["tx"],
                "avg_val": round(m["vol"] / m["tx"], 2),
                "total_vol": round(m["vol"], 2)
            })

    all_days = sorted(daily_vol.keys())
    volume_time_series = []
    for d in all_days:
        point = {"date": d, "total": round(daily_vol[d], 2)}
        for client in top_clients:
            point[client] = round(daily_client_vol[client][d], 2)
        volume_time_series.append(point)

    months = []
    curr = start_dt.replace(day=1, hour=0, minute=0, second=0)
    while curr <= end_dt:
        months.append(curr.strftime('%Y-%m'))
        if curr.month == 12: curr = curr.replace(year=curr.year+1, month=1)
        else: curr = curr.replace(month=curr.month+1)

    cohorts = defaultdict(list)
    for name, m in comp_metrics.items():
        acq_month = m["first_seen"].strftime('%Y-%m')
        cohorts[acq_month].append(name)

    retention_matrix = []
    for acq_month in sorted(cohorts.keys()):
        row_data = {"cohort": acq_month, "size": len(cohorts[acq_month]), "activity": []}
        cohort_members = cohorts[acq_month]
        for check_month in months:
            if check_month < acq_month:
                row_data["activity"].append(None)
                continue
            active_in_month = 0
            for name in cohort_members:
                if any(dt.strftime('%Y-%m') == check_month for dt in comp_metrics[name]["tx_dates"]):
                    active_in_month += 1
            row_data["activity"].append(round((active_in_month / len(cohort_members)) * 100, 1))
        retention_matrix.append(row_data)

    churn_trend = []
    curr_date = start_dt
    while curr_date <= end_dt:
        active_count = 0
        total_so_far = 0
        limit = curr_date - timedelta(days=30)
        for name, m in comp_metrics.items():
            if m["first_seen"] <= curr_date:
                total_so_far += 1
                if any(limit <= tx_dt <= curr_date for tx_dt in m["tx_dates"]):
                    active_count += 1
        churn_trend.append({"date": curr_date.strftime('%Y-%m-%d'), "active": active_count, "inactive": total_so_far - active_count})
        curr_date += timedelta(days=4)

    activity_limit = end_dt - timedelta(days=30)
    
    results = {
        "summary": {
            "onboarded_companies": len(comp_metrics),
            "verified_delta": round(delta_verified, 1),
            "active_companies_30d": active_now,
            "active_delta": round(delta_active, 1),
            "total_stablecoin_volume": round(total_volume, 2),
            "volume_delta": round(delta_vol, 1),
            "total_transactions": total_tx_count,
            "global_avg_tx": round(total_volume / total_tx_count, 2) if total_tx_count > 0 else 0,
            "avg_tx_delta": round(delta_avg_tx, 1),
            "range_start": start_dt.strftime('%d/%m/%Y'),
            "range_end": end_dt.strftime('%d/%m/%Y')
        },
        "share_data": share_data,
        "velocity_data": velocity_data,
        "volume_series": volume_time_series,
        "top_clients": top_clients,
        "retention_matrix": {
            "months": months,
            "data": retention_matrix
        },
        "churn_trend": churn_trend,
        "companies": [{
            "company": n, "volume": round(m["vol"], 2), "transactions": m["tx"],
            "deposits": round(m["dep"], 2), "withdrawals": round(m["with"], 2),
            "is_active": any(activity_limit <= tx_dt <= end_dt for tx_dt in m["tx_dates"]),
            "location": LOCATION_DATA[random.choice(["Bogota", "Medellin"])]
        } for n, m in sorted_comps]
    }
    
    with open(OUTPUT_METRICS, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Metrics Processed.")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE
    process_data(path)
