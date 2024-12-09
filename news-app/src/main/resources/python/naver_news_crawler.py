import pymongo
import requests
import datetime
from bs4 import BeautifulSoup

# MongoDB 연결 설정
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["news_db"]
mycol = mydb["news"]

# 네이버 뉴스 섹션 크롤링 함수
def naver_news_section(sid):
    url = f"https://news.naver.com/main/main.naver?sid1={sid}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    # 뉴스 타이틀, 언론사, 링크 추출
    headline_list = soup.find_all("strong", class_="sa_text_strong")
    headline_press = soup.find_all("div", class_="sa_text_press")
    headline_link = soup.find_all("a", class_="sa_text_title")

    # 리스트 초기화
    title_lst = []
    press_lst = []
    link_lst = []
    date_lst = []
    section_lst = []

    # 데이터가 비어 있으면 반환
    if not headline_list or not headline_press:
        print("No data found.")
        return []

    # 데이터 리스트 생성
    nowDate = datetime.datetime.now().strftime("%Y%m%d")

    for title, press, link in zip(headline_list, headline_press, headline_link):
        title_lst.append(title.get_text(strip=True))
        press_lst.append(press.get_text(strip=True))
        link_lst.append(link['href'])
        date_lst.append(nowDate)  # 현재 날짜를 저장
        section_lst.append(sid)   # 섹션 ID를 저장

    # 데이터 딕셔너리 생성
    resultList = [
        {
            "title": title,
            "link": link,
            "press": press,
            "date": date,
            "section": section
        }
        for title, press, link, date, section
        in zip(title_lst, press_lst, link_lst, date_lst, section_lst)
    ]

    # MongoDB에 삽입 (중복 체크)
    for news in resultList:
        if not mycol.find_one({"link": news["link"]}):
            mycol.insert_one(news)

    print(f"{len(resultList)}개의 뉴스를 저장했습니다.")

# 크롤링 실행 (예: 경제 섹션)
naver_news_section(101)  # 101은 경제 섹션
print("크롤링 완료", flush=True)
