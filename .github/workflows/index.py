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
    
    # 获取你在 GitHub Secrets 中配置的 Bark Key (为了安全，不直接写在代码里)
    bark_key = os.getenv('BARK_KEY')
    
    if not bark_key:
        print("未检测到 BARK_KEY，请在 Settings -> Secrets 中配置")
        return

    # 逻辑：只要是雨天或雪天 (code >= 51) 就推送
    if code >= 51:
        title = "天气预警☔"
        content = f"要下雨了，气温{temp}度，出门记得带伞！"
        requests.get(f"https://api.day.app/{bark_key}/{title}/{content}")
        print("推送成功！")
    else:
        # 为了测试方便，晴天也可以发个简单的通知（测试完可以删掉这行）
        requests.get(f"https://api.day.app/{bark_key}/天气日报/今日天气晴好，气温{temp}度☀️")
        print("今天不会下雨喔！")

if __name__ == "__main__":
    main()
