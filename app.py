from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    # 공공화장실 데이터 가져오기
    api_url = "https://openapi.gg.go.kr/Publtolt"
    service_key = "41675d0dcd4e425eb5638c6a93d0b35f"  # 여기에 공공데이터 API 키를 입력하세요
    toilets = []

    for page in range(1, 11):  # 10페이지까지 요청
        full_url = f"{api_url}?serviceKey={service_key}&numOfRows=100&pageNo={page}"
        response = requests.get(full_url)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for row in root.findall('.//row'):
                toilet_info = {
                    "name": row.find('PBCTLT_PLC_NM').text,
                    "latitude": row.find('REFINE_WGS84_LAT').text,
                    "longitude": row.find('REFINE_WGS84_LOGT').text,
                }
                toilets.append(toilet_info)
        else:
            print(f"Error: {response.status_code}")

    print(f"Total toilets retrieved: {len(toilets)}")  # 가져온 화장실 수 출력

    return render_template('index.html', toilets=toilets)  # HTML 파일에 데이터 전달

if __name__ == '__main__':
    app.run(debug=True)  # Flask 서버 실행
