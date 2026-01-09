import requests
import os
from datetime import datetime, timedelta, timezone

def get_weather():
    # 长沙经纬度 (28.23, 112.94)
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.23&longitude=112.94&current_weather=true"
    try:
        response = requests.get(url, timeout=10)
        return response.json()['current_weather']
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None

def main():
    weather = get_weather()
    if not weather: return

    code = weather['weathercode']
    temp = weather['temperature']
    
    # 1. 完善天气状态翻译
    weather_dict = {
        0: "晴朗 ☀️", 1: "大部晴朗 🌤️", 2: "多云 ⛅", 3: "阴天 ☁️",
        45: "雾 🌫️", 48: "雾 🌫️", 51: "毛毛雨 🌧️", 61: "小雨 ☔",
        71: "小雪 ❄️", 95: "雷阵雨 ⚡"
    }
    status = weather_dict.get(code, "天气更新中")

    # 2. 判断是否需要带伞 (雨雪天气预警)
    rain_alert = ""
    if code >= 51:
        rain_alert = "【带伞提醒☔】"

    # 3. 获取北京时间（让日志更清晰）
    beijing_time = timezone(timedelta(hours=8))
    now = datetime.now(beijing_time).strftime('%H:%M')

    # 4. 获取 Bark Key
    bark_key = os.getenv('BARK_KEY')
    if not bark_key:
        print("未检测到 BARK_KEY")
        return

    # 5. 构造推送内容 (每天都会发，下雨有特殊标记)
    title = f"{rain_alert}今日长沙天气"
    content = f"状态：{status}\n气温：{temp}℃\n更新于北京时间：{now}"
    
    # 发送请求
    requests.get(f"https://api.day.app/{bark_key}/{title}/{content}")
    print(f"[{now}] 推送成功！内容：{status} {temp}度")

if __name__ == "__main__":
    main()
