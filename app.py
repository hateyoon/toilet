from flask import Flask, render_template, jsonify
import requests
import xml.etree.ElementTree as ET
import json

app = Flask(__name__)

# 화장실 API URL (예시 URL을 사용하세요)
API_URL = "https://openapi.gg.go.kr/Publtolt?KEY=d7c05f9db6034d66b9dedb464adbd9d6&pIndex=1&pSize=1000"

# XML 데이터를 JSON으로 변환하는 함수
def xml_to_dict(element):
    """주어진 XML Element를 재귀적으로 파싱해서 Python 딕셔너리로 변환"""
    result = {}
    # element의 자식 요소가 있는지 확인
    if len(element) > 0:
        for child in element:
            child_result = xml_to_dict(child)  # 자식 요소를 재귀적으로 파싱
            if child.tag in result:
                # 중복 태그일 경우, 리스트로 처리
                if isinstance(result[child.tag], list):
                    result[child.tag].append(child_result)
                else:
                    result[child.tag] = [result[child.tag], child_result]
            else:
                result[child.tag] = child_result
    else:
        # 자식 요소가 없으면 해당 요소의 텍스트 값을 저장
        result = element.text

    return result


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toilets')
def toilets():
    # API에서 화장실 데이터 가져오기
    response = requests.get(API_URL)
    print(response)
    xml_data = response.content

    # XML 데이터 파싱
    root = ET.fromstring(xml_data)
    # XML을 JSON으로 변환
    json_data = json.dumps(xml_to_dict(root), indent=4)

# 사용자에게 JSON 응답으로 전달 (여기서는 출력 예시)
    print(json_data)
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

    return jsonify(json.loads(json_data)["row"])

if __name__ == '__main__':
    app.run(debug=True)
