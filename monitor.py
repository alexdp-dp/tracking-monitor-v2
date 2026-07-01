import json

from checker import check_site
from dashboard_generator import generate_dashboard
from emailer import send_email
from status_manager import load_status, save_status


with open("sites.json", "r", encoding="utf-8") as file:
    sites = json.load(file)


previous_status = load_status()

current_status = {}

results = []


for site in sites:

    result = check_site(site)

    results.append(result)

    current_status[result["name"]] = result["status"]

    old_status = previous_status.get(result["name"])

    if old_status is None:
        continue

    if old_status != result["status"]:

        if result["status"] == "ERROR":

            problems = []

            if not result["online"]:
                problems.append("• Website Offline")

            if not result["ssl"]:
                problems.append("• SSL invalid")

            if result["gtm"]["status"] == "ERROR":
                problems.append("• Google Tag Manager missing")

            if result["ga4"]["status"] == "ERROR":
                problems.append("• Google Analytics 4 missing")

            if result["meta"]["status"] == "ERROR":
                problems.append("• Meta Pixel missing")

            body = f"""
Tracking Monitor

Website:
{result["name"]}

Problems detected:

{chr(10).join(problems)}

URL:
{result["url"]}
"""

            send_email(
                f"🚨 ALERT - {result['name']}",
                body
            )

        else:

            send_email(
                f"✅ RECOVERED - {result['name']}",
                f"""
Tracking Monitor

Website:
{result["name"]}

Tracking has recovered.

URL:
{result["url"]}
"""
            )


generate_dashboard(results)

save_status(current_status)

print("Tracking Monitor finished successfully.")