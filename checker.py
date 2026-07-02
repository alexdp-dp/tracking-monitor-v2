import re
import requests


USER_AGENT = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}

def check_site(site):

    result = {
        "name": site["name"],
        "url": site["url"],

        "online": False,
        "ssl": False,

        "gtm": {
            "status": "ERROR",
            "id": "-"
        },

        "ga4": {
            "status": "ERROR",
            "id": "-"
        },

        "meta": {
            "status": "ERROR"
        },

        "status": "ERROR"
    }

    try:

        response = requests.get(
            site["url"],
            timeout=15,
            headers=USER_AGENT,
            allow_redirects=True
        )
        print(response.headers.get("Server"))
        print(site["name"])
        print(response.status_code)
        print(response.url)

        html = response.text

        result["online"] = response.ok
        result["ssl"] = response.url.startswith("https://")

        #################################################
        # GTM
        #################################################

        gtm = re.search(r"GTM-[A-Z0-9]+", html)

        if gtm:

            result["gtm"]["status"] = "OK"
            result["gtm"]["id"] = gtm.group(0)

        #################################################
        # GA4
        #################################################

        ga4 = re.search(r"G-[A-Z0-9]+", html)

        if ga4:

            result["ga4"]["status"] = "OK"
            result["ga4"]["id"] = ga4.group(0)

        elif result["gtm"]["status"] == "OK":

            result["ga4"]["status"] = "WARNING"
            result["ga4"]["id"] = "Via GTM"

        #################################################
        # META
        #################################################

        meta_patterns = [
            "connect.facebook.net",
            "fbq(",
            "facebook.com/tr"
        ]

        if any(pattern in html for pattern in meta_patterns):

            result["meta"]["status"] = "OK"

        elif result["gtm"]["status"] == "OK":

            result["meta"]["status"] = "WARNING"

        #################################################
        # STATUS
        #################################################

        errors = []

        if not result["online"]:
            errors.append(True)

        if not result["ssl"]:
            errors.append(True)

        if result["gtm"]["status"] == "ERROR":
            errors.append(True)

        if result["ga4"]["status"] == "ERROR":
            errors.append(True)

        if result["meta"]["status"] == "ERROR":
            errors.append(True)

        result["status"] = "ERROR" if errors else "OK"

    except Exception:

        result["status"] = "ERROR"

    return result
