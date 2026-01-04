import requests
import time
import os

# ================= CONFIG =================
SHEIN_API_URL = "https://www.sheinindia.in/api/category/sverse-5939-37961?fields=SITE&currentPage=0&pageSize=40&format=json&query=%3Arelevance%3Agenderfilter%3AWomen%3Agenderfilter%3AMen&gridColumns=2&segmentIds=13%2C8%2C19&cohortIds=value%7Cwomen&customerType=Existing&facets=genderfilter%3AWomen%3Agenderfilter%3AMen&includeUnratedProducts=false&userClusterId=supervalue%7Cm1active%2Cactive%2Cmen%2Clowasp%2Cp_null%2CTT_TARGETING_DEC_TEMP%2CHT_TARGETING_DEC_TEMP&customertype=Existing&advfilter=true&platform=Desktop&showAdsOnNextPage=false&is_ads_enable_plp=true&displayRatings=true&segmentIds=&&store=shein"

TELEGRAM_BOT_TOKEN = "8215403214:AAHkcQAFrR3bRdF9ZVC0c_dmLykN8xvUuXo"
TELEGRAM_CHAT_ID = "8065343350"

CHECK_URL_ON_NOTIFY = "https://www.beeminer.top/btc/user/code?phone=9162925963"

DATA_FILE = "total_results.txt"
CHECK_INTERVAL = 2  # seconds
# =========================================


def get_total_results():
    try:
        res = requests.get(SHEIN_API_URL, timeout=10)
        data = res.json()
        return data["pagination"]["totalResults"]
    except Exception as e:
        print("Error fetching API:", e)
        return None


def read_old_value():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return f.read().strip()
    return None


def save_value(value):
    with open(DATA_FILE, "w") as f:
        f.write(str(value))


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

    # Call GET URL every time message is sent
    try:
        requests.get(CHECK_URL_ON_NOTIFY, timeout=5)
    except:
        pass


def main():
    print("🔄 Monitoring started...")

    while True:
        total_results = get_total_results()
        if total_results is None:
            time.sleep(CHECK_INTERVAL)
            continue

        old_value = read_old_value()

        # First time
        if old_value is None:
            save_value(total_results)
            msg = f"📢 SHEIN TOTAL RESULTS (FIRST TIME)\n\nTotal Results: {total_results}"
            send_telegram_message(msg)
            print("First value sent:", total_results)

        # Changed
        elif str(total_results) != old_value:
            diff = total_results - int(old_value)
            change_type = "⬆ Increased" if diff > 0 else "⬇ Decreased"

            msg = (
                f"🚨 SHEIN TOTAL RESULTS CHANGED\n\n"
                f"Old: {old_value}\n"
                f"New: {total_results}\n"
                f"Change: {change_type} ({diff})"
            )

            save_value(total_results)
            send_telegram_message(msg)
            print("Value changed:", old_value, "→", total_results)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
