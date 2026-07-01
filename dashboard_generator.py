from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def generate_dashboard(results):

    now = datetime.now(ZoneInfo("Europe/Bucharest"))

    last_check = now.strftime("%d.%m.%Y %H:%M:%S")
    next_check = (now + timedelta(minutes=5)).strftime("%d.%m.%Y %H:%M:%S")

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Tracking Monitor</title>

<style>

body{{
    font-family:Arial,Helvetica,sans-serif;
    background:#f3f3f3;
    margin:40px;
}}

h1{{
    margin-bottom:5px;
}}

.info{{
    color:#666;
    line-height:1.7;
    margin-bottom:20px;
}}

table{{
    width:100%;
    border-collapse:collapse;
    margin-top:25px;
    background:white;
    box-shadow:0 0 15px rgba(0,0,0,.08);
}}

th{{
    background:#222;
    color:white;
    padding:14px;
}}

td{{
    padding:14px;
    text-align:center;
    border-bottom:1px solid #eee;
}}

tr:hover{{
    background:#fafafa;
}}

.ok{{
    color:#16a34a;
    font-weight:bold;
}}

.warning{{
    color:#d97706;
    font-weight:bold;
}}

.error{{
    color:#dc2626;
    font-weight:bold;
}}

</style>

</head>

<body>

<h1>Tracking Monitor</h1>

<div class="info">
<b>Last check:</b> {last_check}<br>
<b>Next scheduled check:</b> {next_check}
</div>

<table>

<thead>

<tr>

<th>Website</th>
<th>Online</th>
<th>SSL</th>
<th>GTM</th>
<th>GTM ID</th>
<th>GA4</th>
<th>GA4 ID</th>
<th>Meta</th>
<th>Status</th>

</tr>

</thead>

<tbody>
"""

    for site in results:

        online = "🟢" if site["online"] else "🔴"

        ssl = "🟢" if site["ssl"] else "🔴"

        gtm = "🟢" if site["gtm"]["status"] == "OK" else "🔴"

        if site["ga4"]["status"] == "OK":
            ga4 = "🟢"
        elif site["ga4"]["status"] == "WARNING":
            ga4 = "🟡"
        else:
            ga4 = "🔴"

        if site["meta"]["status"] == "OK":
            meta = "🟢"
        elif site["meta"]["status"] == "WARNING":
            meta = "🟡"
        else:
            meta = "🔴"

        if site["status"] == "OK":
            status = '<span class="ok">🟢 OK</span>'
        else:
            status = '<span class="error">🔴 ERROR</span>'

        html += f"""

<tr>

<td>{site['name']}</td>

<td>{online}</td>

<td>{ssl}</td>

<td>{gtm}</td>

<td>{site['gtm']['id']}</td>

<td>{ga4}</td>

<td>{site['ga4']['id']}</td>

<td>{meta}</td>

<td>{status}</td>

</tr>

"""

    html += """

</tbody>

</table>

</body>

</html>

"""

    with open("dashboard.html", "w", encoding="utf-8") as file:

        file.write(html)