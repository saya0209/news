import pymongo
import requests
import xmltodict
from datetime import datetime

# MongoDB 연결
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["news_db"]
mycol = mydb["news"]

# 기상청 API 설정
API_KEY = "AN7DdHa0JaQSBkGxjr3up2CIJyY0DoqZRcE3jH0dO6swb4yPilpEG5oXN79R+HopMrYNlQyb9mQ+zNFgw2FRgQ=="  # 기상청 API 인증 키를 입력하세요.
BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

# 서울의 좌표 (nx, ny)
nx, ny = 60, 127

# 현재 날짜와 기준 시간(0200, 0500, 0800, ...) 설정
now = datetime.now()
base_date = now.strftime("%Y%m%d")  # 오늘 날짜 (예: 20241205)
base_time = "0500"  # 기준 시간은 자정 이후 가장 가까운 3시간 단위로 설정 (예: 0200, 0500)

# 뉴스 기사에 날씨 정보 추가 함수
def add_weather_info():
    for news in mycol.find({"weather": {"$exists": False}}):
        params = {
            "serviceKey": API_KEY,
            "pageNo": "1",
            "numOfRows": "10",
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": nx,
            "ny": ny
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.encoding = 'utf-8'
            response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킴

            weather_data = response.json()

            if "response" in weather_data and "body" in weather_data["response"]:
                items = weather_data["response"]["body"]["items"]["item"]

                # SKY(하늘 상태), TMP(온도), REH(습도) 추출
                sky = next((item["fcstValue"] for item in items if item["category"] == "SKY"), "알 수 없음")
                tmp = next((item["fcstValue"] for item in items if item["category"] == "TMP"), "알 수 없음")

                # 날씨 정보 결합
                weather_info = f"하늘 상태: {sky}, 온도: {tmp}°C"

                # MongoDB에 날씨 정보 업데이트
                mycol.update_one({"_id": news["_id"]}, {"$set": {"weather": weather_info}})
            else:
                print("응답에서 날씨 데이터를 찾을 수 없습니다.")
        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류 발생: {e}")

add_weather_info()
