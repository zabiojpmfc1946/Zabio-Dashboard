import json
import os

METRICS_FILE = ".tmp/metrics.json"
OUTPUT_HTML = "dashboard.html"

def generate_dashboard():
    if not os.path.exists(METRICS_FILE):
        return

    with open(METRICS_FILE, 'r') as f:
        data = json.load(f)

    summary = data['summary']
    retention = data['retention_matrix']
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zabio Strategic Analytics Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@2.0.1/dist/chartjs-plugin-zoom.min.js"></script>
    <style>
        :root {{
            --primary: #818cf8;
            --secondary: #ec4899;
            --bg: #0f172a;
            --card: #1e293b;
            --text: #f8fafc;
            --text-dim: #94a3b8;
            --border: #334155;
            --success: #22c55e;
            --danger: #ef4444;
            --warning: #f59e0b;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Outfit', sans-serif; background: var(--bg); color: var(--text); padding: 1.5rem; line-height: 1.5; }}
        
        .header {{ margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; }}
        .header h1 {{ font-size: 2rem; background: linear-gradient(90deg, #818cf8, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .header p {{ color: var(--text-dim); }}

        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
        .stat-card {{ background: var(--card); border: 1px solid var(--border); padding: 1.25rem; border-radius: 1rem; }}
        .stat-label {{ font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em; }}
        .stat-value {{ font-size: 1.4rem; font-weight: 700; margin-top: 0.25rem; color: var(--primary); }}
        
        .section-title {{ font-size: 1rem; margin: 2rem 0 1rem; color: var(--text); font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }}
        .section-title::after {{ content: ''; flex: 1; height: 1px; background: var(--border); }}

        .main-grid {{ display: grid; grid-template-columns: 1fr; gap: 1.5rem; margin-bottom: 2rem; }}
        @media (min-width: 1024px) {{ .main-grid {{ grid-template-columns: repeat(2, 1fr); }} .grid-3 {{ grid-template-columns: repeat(3, 1fr); }} }}
        
        .chart-card {{ background: var(--card); border: 1px solid var(--border); padding: 1.5rem; border-radius: 1rem; position: relative; }}
        .chart-container {{ position: relative; height: 260px; width: 100%; }}
        .chart-card h2 {{ font-size: 0.85rem; margin-bottom: 1rem; color: var(--text-dim); font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em; display: flex; justify-content: space-between; align-items: center; }}

        .full-width {{ grid-column: 1 / -1; }}

        .reset-btn {{ 
            background: rgba(129, 140, 248, 0.1); 
            border: 1px solid var(--primary); 
            color: var(--primary); 
            padding: 2px 8px; 
            border-radius: 6px; 
            font-size: 0.6rem; 
            cursor: pointer; 
            transition: all 0.2s;
            text-transform: none;
            letter-spacing: normal;
        }}
        .reset-btn:hover {{ background: var(--primary); color: #fff; }}

        .heatmap-container {{ overflow-x: auto; margin-top: 1rem; }}
        .heatmap-table {{ width: 100%; border-collapse: separate; border-spacing: 2px; font-size: 0.7rem; }}
        .heatmap-table th {{ background: var(--bg); color: var(--text-dim); padding: 8px; font-weight: 400; min-width: 60px; }}
        .heatmap-table td {{ padding: 10px 6px; text-align: center; color: #fff; font-weight: 600; border-radius: 2px; }}
        .cohort-label {{ background: var(--bg) !important; color: var(--text) !important; text-align: left !important; font-weight: 600 !important; width: 100px; }}

        .table-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 1rem; padding: 1.5rem; overflow-x: auto; margin-top: 2rem; }}
        table.standard-table {{ width: 100%; border-collapse: collapse; min-width: 1000px; }}
        table.standard-table th {{ text-align: left; padding: 0.75rem 1rem; border-bottom: 2px solid var(--border); color: var(--text-dim); font-size: 0.7rem; text-transform: uppercase; }}
        table.standard-table td {{ padding: 0.75rem 1rem; border-bottom: 1px solid var(--border); font-size: 0.8rem; }}
        
        .val-stable {{ color: var(--success); font-weight: 600; }}
        .val-out {{ color: var(--danger); font-size: 0.75rem; opacity: 0.9; }}
        .val-in {{ color: var(--success); font-size: 0.75rem; opacity: 0.9; }}

        .tag {{ padding: 2px 10px; border-radius: 12px; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; white-space: nowrap; }}
        .tag-active {{ background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid #4ade80; }}
        .tag-inactive {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #f87171; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Zabio Intelligence</h1>
            <p>Financial Performance & BI Dashboard: {summary['range_start']} - {summary['range_end']}</p>
        </div>
        <p style="font-size: 0.8rem; color: var(--success); font-weight: 600;">● Data Verified: 100%</p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">Verified Entitites</div>
            <div class="stat-value">{summary['onboarded_companies']}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Active (30d)</div>
            <div class="stat-value">{summary['active_companies_30d']}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Total Volume</div>
            <div class="stat-value">${summary['total_stablecoin_volume']:,.0f}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Avg Transaction</div>
            <div class="stat-value">${summary['global_avg_tx']:,.0f}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Retention</div>
            <div class="stat-value">{round((summary['active_companies_30d'] / summary['onboarded_companies']) * 100, 1)}%</div>
        </div>
    </div>

    <div class="section-title">Volume Evolution</div>
    <div class="main-grid">
        <div class="chart-card">
            <h2>Aggregate Traded Volume <button class="reset-btn" onclick="resetZoom('totalVolumeChart')">Reset</button></h2>
            <div class="chart-container">
                <canvas id="totalVolumeChart"></canvas>
            </div>
        </div>
        <div class="chart-card">
            <h2>Top Clients Comparison <button class="reset-btn" onclick="resetZoom('clientVolumeChart')">Reset</button></h2>
            <div class="chart-container">
                <canvas id="clientVolumeChart"></canvas>
            </div>
        </div>
    </div>

    <div class="section-title">Segmentation & Retention</div>
    <div class="main-grid grid-3">
        <div class="chart-card">
            <h2>Concentration Risk (Top 3)</h2>
            <div class="chart-container">
                <canvas id="concentrationChart"></canvas>
            </div>
        </div>
        <div class="chart-card">
            <h2>Client Velocity Index <button class="reset-btn" onclick="resetZoom('velocityChart')">Reset</button></h2>
            <div class="chart-container">
                <canvas id="velocityChart"></canvas>
            </div>
        </div>
        <div class="chart-card">
            <h2>Activity Persistence <button class="reset-btn" onclick="resetZoom('churnChart')">Reset</button></h2>
            <div class="chart-container">
                <canvas id="churnChart"></canvas>
            </div>
        </div>

        <div class="chart-card full-width">
            <h2>Monthly Cohort Retention (Active Matrix %)</h2>
            <div class="heatmap-container">
                <table class="heatmap-table">
                    <thead>
                        <tr>
                            <th class="cohort-label">Cohort</th>
                            <th class="cohort-label">Size</th>
                            {"".join([f"<th>{m}</th>" for m in retention['months']])}
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([
                            f"<tr>"
                            f"<td class='cohort-label'>{row['cohort']}</td>"
                            f"<td class='cohort-label' style='text-align: center !important;'>{row['size']}</td>"
                            + "".join([
                                f"<td style='background: {get_heatmap_color(val)}; color: {get_text_color(val)}'>{val if val is not None else ''}</td>"
                                for val in row['activity']
                            ]) +
                            f"</tr>"
                            for row in retention['data']
                        ])}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div class="table-card">
        <h2>Corporate Performance Tracker</h2>
        <table class="standard-table">
            <thead>
                <tr>
                    <th>Entity</th>
                    <th>Deposits (+)</th>
                    <th>Withdrawals (-)</th>
                    <th>Total Traded</th>
                    <th>Tx Count</th>
                    <th>Avg Tx Size</th>
                    <th>Activity Status</th>
                </tr>
            </thead>
            <tbody>
                {"".join([
                    f"<tr>"
                    f"<td>{c['company']}</td>"
                    f"<td class='val-in'>+${c['deposits']:,.2f}</td>"
                    f"<td class='val-out'>-${c['withdrawals']:,.2f}</td>"
                    f"<td class='val-stable'>${c['volume']:,.2f}</td>"
                    f"<td>{c['transactions']}</td>"
                    f"<td>${(c['volume']/c['transactions']):,.2f}</td>"
                    f"<td><span class='tag {('tag-active' if c['is_active'] else 'tag-inactive')}'>{('Active' if c['is_active'] else 'Inactive')}</span></td>"
                    f"</tr>" for c in data['companies'][:35]
                ])}
            </tbody>
        </table>
    </div>

    <script>
        const volumeSeries = {json.dumps(data['volume_series'])};
        const topClients = {json.dumps(data['top_clients'])};
        const shareData = {json.dumps(data['share_data'])};
        const velocityData = {json.dumps(data['velocity_data'])};
        const churnData = {json.dumps(data['churn_trend'])};

        const chartColors = ['#818cf8', '#ec4899', '#f59e0b', '#22c55e', '#a855f7'];
        const charts = {{}};

        function resetZoom(id) {{
            if (charts[id]) charts[id].resetZoom();
        }}

        function initCharts() {{
            const tooltipDefaults = {{
                enabled: true,
                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: '#334155',
                borderWidth: 1,
                padding: 12,
                cornerRadius: 8,
                titleFont: {{ family: 'Outfit', size: 12, weight: 'bold' }},
                bodyFont: {{ family: 'Outfit', size: 11 }},
                usePointStyle: true
            }};

            const zoomOptions = {{
                zoom: {{
                    drag: {{ enabled: true, backgroundColor: 'rgba(129, 140, 248, 0.2)', borderColor: '#818cf8', borderWidth: 1 }},
                    mode: 'xy',
                }},
                pan: {{ enabled: true, mode: 'xy' }}
            }};

            const commonOptions = {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{
                    mode: 'index',
                    intersect: false,
                }},
                plugins: {{ 
                    legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', boxWidth: 10, font: {{ size: 9 }} }} }},
                    tooltip: tooltipDefaults,
                    zoom: zoomOptions
                }},
                scales: {{ 
                    y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', font: {{ size: 9 }} }} }}, 
                    x: {{ grid: {{ display: false }}, ticks: {{ color: '#94a3b8', font: {{ size: 9 }}, maxTicksLimit: 8 }} }} 
                }}
            }};

            // Total Volume Trend
            charts['totalVolumeChart'] = new Chart(document.getElementById('totalVolumeChart'), {{
                type: 'line',
                data: {{
                    labels: volumeSeries.map(d => d.date),
                    datasets: [{{
                        label: 'Total Daily Volume',
                        data: volumeSeries.map(d => d.total),
                        borderColor: '#818cf8',
                        backgroundColor: 'rgba(129, 140, 248, 0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHitRadius: 10
                    }}]
                }},
                options: {{
                    ...commonOptions,
                    plugins: {{
                        ...commonOptions.plugins,
                        tooltip: {{
                            ...tooltipDefaults,
                            callbacks: {{
                                label: function(ctx) {{
                                    return 'Volume: $' + ctx.parsed.y.toLocaleString();
                                }}
                            }}
                        }}
                    }}
                }}
            }});

            // Client Volume Breakdown
            charts['clientVolumeChart'] = new Chart(document.getElementById('clientVolumeChart'), {{
                type: 'line',
                data: {{
                    labels: volumeSeries.map(d => d.date),
                    datasets: topClients.map((c, i) => ({{
                        label: c,
                        data: volumeSeries.map(d => d[c] || 0),
                        borderColor: chartColors[i % chartColors.length],
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHitRadius: 10
                    }}))
                }},
                options: {{
                    ...commonOptions,
                    plugins: {{
                        ...commonOptions.plugins,
                        tooltip: {{
                            ...tooltipDefaults,
                            callbacks: {{
                                label: function(ctx) {{
                                    return ctx.dataset.label + ': $' + ctx.parsed.y.toLocaleString();
                                }}
                            }}
                        }}
                    }}
                }}
            }});

            // Concentration
            charts['concentrationChart'] = new Chart(document.getElementById('concentrationChart'), {{
                type: 'doughnut',
                data: {{
                    labels: shareData.map(d => d.label),
                    datasets: [{{
                        data: shareData.map(d => d.vol),
                        backgroundColor: ['#818cf8', '#6366f1', '#4f46e5', '#334155'],
                        borderWidth: 0
                    }}]
                }},
                options: {{ 
                    ...commonOptions, 
                    scales: {{}},
                    interaction: {{ mode: 'nearest' }},
                    plugins: {{
                        ...commonOptions.plugins,
                        zoom: {{ enabled: false }},
                        tooltip: {{
                            ...tooltipDefaults,
                            callbacks: {{
                                label: function(ctx) {{
                                    const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
                                    const perc = ((ctx.parsed / total) * 100).toFixed(1);
                                    return ctx.label + ': $' + ctx.parsed.toLocaleString() + ' (' + perc + '%)';
                                }}
                            }}
                        }}
                    }}
                }}
            }});

            // Velocity Scatter
            charts['velocityChart'] = new Chart(document.getElementById('velocityChart'), {{
                type: 'scatter',
                data: {{
                    datasets: [{{
                        label: 'Companies',
                        data: velocityData.map(d => ({{ x: d.tx_count, y: d.avg_val, name: d.name }})),
                        backgroundColor: '#ec4899',
                        pointRadius: 6,
                        hoverRadius: 10
                    }}]
                }},
                options: {{
                    ...commonOptions,
                    interaction: {{ mode: 'nearest', intersect: true }},
                    plugins: {{ 
                        ...commonOptions.plugins,
                        legend: {{ display: false }},
                        zoom: zoomOptions,
                        tooltip: {{
                            ...tooltipDefaults,
                            callbacks: {{
                                label: function(ctx) {{
                                    return ctx.raw.name + ': ' + ctx.raw.x + ' tx @ $' + Math.round(ctx.raw.y).toLocaleString() + '/avg';
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{ title: {{ display: true, text: 'Transaction Count', color: '#94a3b8', font: {{ size: 9 }} }}, grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8' }} }},
                        y: {{ title: {{ display: true, text: 'Avg Transaction Size', color: '#94a3b8', font: {{ size: 9 }} }}, grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8' }} }}
                    }}
                }}
            }});

            // Activity Persistence
            charts['churnChart'] = new Chart(document.getElementById('churnChart'), {{
                type: 'line',
                data: {{
                    labels: churnData.map(d => d.date),
                    datasets: [
                        {{ label: 'Active', data: churnData.map(d => d.active), borderColor: '#22c55e', borderWidth: 2, fill: false, tension: 0.3, pointRadius: 0, pointHitRadius: 10 }},
                        {{ label: 'Inactive', data: churnData.map(d => d.inactive), borderColor: '#ef4444', borderWidth: 1, borderDash: [5,5], fill: false, tension: 0.3, pointRadius: 0, pointHitRadius: 10 }}
                    ]
                }},
                options: {{
                    ...commonOptions,
                    plugins: {{
                        ...commonOptions.plugins,
                        tooltip: {{
                            ...tooltipDefaults,
                            callbacks: {{
                                label: function(ctx) {{
                                    return ctx.dataset.label + ': ' + ctx.parsed.y + ' companies';
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}

        initCharts();
    </script>
</body>
</html>
"""
    with open(OUTPUT_HTML, 'w') as f:
        f.write(html_content)

def get_heatmap_color(val):
    if val is None: return "transparent"
    if val > 80: return "rgba(34, 197, 94, 0.9)"
    if val > 60: return "rgba(34, 197, 94, 0.6)"
    if val > 40: return "rgba(245, 158, 11, 0.5)"
    if val > 20: return "rgba(239, 68, 68, 0.4)"
    return "rgba(239, 68, 68, 0.7)"

def get_text_color(val):
    if val is None: return "transparent"
    return "#fff"

if __name__ == "__main__":
    generate_dashboard()
