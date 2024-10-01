import requests
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim

# 공중화장실 API에서 데이터를 가져오는 함수
def fetch_toilet_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # 응답 상태 코드 확인
        data = response.json()
        
        # 데이터 구조 확인
        if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
            return pd.DataFrame(data['response']['body']['items'])
        else:
            st.error("API 응답에서 공중화장실 데이터를 찾을 수 없습니다.")
            return pd.DataFrame()  # 빈 DataFrame 반환
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 오류: {e}")
        return pd.DataFrame()  # 빈 DataFrame 반환

# 내 위치를 얻는 함수 (예시로 서울의 좌표)
def get_my_location():
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode("Seoul")
    return location.latitude, location.longitude

# 공중화장실 데이터를 지도에 표시하는 함수
def map_toilets(toilets, my_location):
    # 지도 생성
    map_ = folium.Map(location=my_location, zoom_start=13)

    # 마커 추가
    for _, toilet in toilets.iterrows():
        folium.Marker(
            location=[toilet['latitude'], toilet['longitude']],
            popup=toilet.get('name', '이름 없음'),  # 이름이 없을 경우 대체 텍스트
        ).add_to(map_)

    # Streamlit에 지도 표시
    folium_static(map_)

# Streamlit 웹 애플리케이션 구성
def main():
    st.title("내 근처 공중화장실 찾기")

    # API URL 설정
    api_url = "https://zylalabs.com/api/2086/available+public+bathrooms+api/1869/get+public+bathrooms?lat=42&lng=-74.005974&page=1&per_page=10&offset=Optional"

    # 내 위치 가져오기
    my_location = get_my_location()

    # 공중화장실 데이터 가져오기
    toilets = fetch_toilet_data(api_url)

    if not toilets.empty:  # 데이터가 있을 때만 지도에 표시
        map_toilets(toilets, my_location)

if __name__ == "__main__":
    main()
