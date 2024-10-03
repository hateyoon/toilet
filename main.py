import requests
import pandas as pd
import xml.etree.ElementTree as ET
import streamlit as st  # Streamlit 모듈을 import

# 공공데이터 API에서 데이터를 가져오는 함수
def fetch_toilet_data(api_url, service_key):
    # 요청 URL 생성 (20개 데이터 요청)
    full_url = f"{api_url}?serviceKey={service_key}&numOfRows=20&pageNo=1"
    print(f"API 요청 URL: {full_url}")  # 요청 URL 출력
    response = requests.get(full_url)

    # 응답 상태 코드 확인
    if response.status_code == 200:
        try:
            # XML 응답 파싱
            root = ET.fromstring(response.content)
            toilets = []

            # XML의 각 row를 반복하여 데이터 수집
            for row in root.findall('.//row'):
                toilet_info = {
                    "장소": row.find('PBCTLT_PLC_NM').text,
                    "남자 화장실 수": row.find('MALE_WTRCLS_CNT').text,
                    "여자 화장실 수": row.find('FEMALE_WTRCLS_CNT').text,
                    "주소": row.find('REFINE_LOTNO_ADDR').text,
                    "위도": row.find('REFINE_WGS84_LAT').text,
                    "경도": row.find('REFINE_WGS84_LOGT').text,
                }
                toilets.append(toilet_info)

            return pd.DataFrame(toilets)
        except ET.ParseError:
            print("응답을 XML로 변환할 수 없습니다. 응답 내용:", response.text)  # 오류 시 응답 내용 출력
            return pd.DataFrame()
    else:
        print(f"Error: {response.status_code}, 응답 내용: {response.text}")  # 오류 시 응답 내용 출력
        return pd.DataFrame()

# 위치를 고정하고 데이터를 가져오는 함수
def get_fixed_location_and_data():
    # 고정된 위치 (서울의 좌표)
    my_location = (37.5665, 126.978)  # 서울의 위도와 경도
    api_url = "https://openapi.gg.go.kr/Publtolt"
    service_key = "d7c05f9db6034d66b9dedb464adbd9d6"
    
    # 공중화장실 데이터 가져오기
    toilets = fetch_toilet_data(api_url, service_key)
    
    return my_location, toilets

# Streamlit 애플리케이션 메인 로직
def main():
    st.title("공중 화장실 정보")
    my_location, toilets = get_fixed_location_and_data()

    if not toilets.empty:
        st.write(toilets)
    else:
        st.error("공중화장실 데이터가 없습니다.")  # 데이터가 없을 경우 에러 메시지

if __name__ == "__main__":
    main()
