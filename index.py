import requests
import os

def get_weather():
    # 使用 Open-Meteo 获取长沙天气 (经纬度：28.23, 112.94)
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
    
    # 简单的代码转文字逻辑
    weather_text = "晴朗" if code == 0 else "多云/阴天"
    if code >= 51: weather_text = "雨雪天气☔"

    bark_key = os.getenv('BARK_KEY')
    if not bark_key: return

    # 修改这里：取消 if code >= 51 的限制，改为每天推送
    title = f"今日天气报：{weather_text}"
    content = f"当前气温 {temp}℃。出门请留意！"
    
    # 发送请求
    requests.get(f"https://api.day.app/{bark_key}/{title}/{content}")
    print(f"推送成功：{title}")

if __name__ == "__main__":

    main()

