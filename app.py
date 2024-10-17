from flask import Flask, render_template, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# 화장실 API URL (예시 URL을 사용하세요)
API_URL = "https://openapi.gg.go.kr/Publtolt"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toilets')
def toilets():
    # API에서 화장실 데이터 가져오기
    response = requests.get(API_URL)
    xml_data = response.content

    # XML 데이터 파싱
    root = ET.fromstring(xml_data)
    toilets_list = []

    for toilet in root.findall('.//toilet'):  # XML 구조에 맞게 수정
        name = toilet.find('name').text
        latitude = toilet.find('latitude').text
        longitude = toilet.find('longitude').text
        toilets_list.append({
            'name': name,
            'latitude': float(latitude),
            'longitude': float(longitude)
        })

    return jsonify(toilets_list)

if __name__ == '__main__':
    app.run(debug=True)
