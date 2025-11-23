# @title main.py
import requests
import json
from datetime import datetime
import os

def get_fear_and_greed_index():
    # CNN 的隱藏 API 端點 (這是繪製歷史圖表的資料源，包含最新數據)
    url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

    # 必須加入 User-Agent 偽裝成瀏覽器，否則會被擋 (403 Forbidden)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 解析資料結構 (CNN 回傳的資料包含 'fear_and_greed' 物件)
        fng_data = data['fear_and_greed']

        score = fng_data['score']
        rating = fng_data['rating']
        timestamp = fng_data['timestamp']

        # 轉換時間格式
        dt_object = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

        return {
            "score": score,
            "rating": rating,
            "time": formatted_time
        }

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def send_notification(data):
    # 這裡示範印出結果，你可以改成發送到 Telegram/Discord/Line
    if data:
        message = f"CNN Fear & Greed Index: {int(data['score'])} ({data['rating']}) at {data['time']}"
        print(message)

        # [選項] 如果你想傳送到 Discord，取消下面註解並填入 Webhook URL
        # discord_url = os.environ.get('DISCORD_WEBHOOK_URL')
        # if discord_url:
        #     requests.post(discord_url, json={"content": message})

if __name__ == "__main__":
    data = get_fear_and_greed_index()
    send_notification(data)