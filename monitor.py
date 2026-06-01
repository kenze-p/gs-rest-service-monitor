import requests
import time
import logging
from datetime import datetime

# Konfiguracija
SERVICE_URL = "http://13.217.213.8:777/greeting"
SLACK_BOT_TOKEN = "xoxb-11237836384599-11257003422564-jDQKQZ3swLQx0UlMpQm0wM1v"
SLACK_CHANNEL_ID = "C0B78UK9ATD"
CHECK_INTERVAL = 30  # sekundi

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)

def send_slack_message(message):
    try:
        requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
            json={"channel": SLACK_CHANNEL_ID, "text": message}
        )
    except Exception as e:
        logging.error(f"Failed to send Slack message: {e}")

def check_service():
    try:
        response = requests.get(SERVICE_URL, timeout=5)
        return response.status_code == 200
    except:
        return False

last_status = None

logging.info("🚀 Monitoring started!")

while True:
    is_up = check_service()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if last_status is None or is_up != last_status:
        if is_up:
            msg = f"✅ [{now}] Service is UP - {SERVICE_URL}"
        else:
            msg = f"❌ [{now}] Service is DOWN - {SERVICE_URL}"
        
        logging.info(msg)
        send_slack_message(msg)

    last_status = is_up
    time.sleep(CHECK_INTERVAL)
