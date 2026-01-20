import streamlit as st
import requests
from datetime import datetime

# 1. 환경 설정 및 데이터 정의 (최상단에 위치)
locations = {
    "대전(본부)": {"nx": 67, "ny": 134},
    "서울": {"nx": 60, "ny": 127},
    "부산": {"nx": 98, "ny": 76},
    "제주": {"nx": 52, "ny": 38}
}

# 2. 웹앱의 제목과 설명
st.title("☀️ 실시간 동네 기온 예보")
st.info("공공데이터포털의 기상청 API를 활용한 웹앱입니다.")

# 3. 지역 선택 UI
selected_city = st.selectbox("확인하고 싶은 지역을 선택하세요.", list(locations.keys()))
nx = locations[selected_city]["nx"]
ny = locations[selected_city]["ny"]

# 4. 날씨 확인 로직
if st.button(f"{selected_city} 기온 확인하기"):
    # 인증키 설정
    auth_key = "f0cc4e1eb2f7f6c3613c93bcecf0e5e554ef9bd38070521b661234849bfd1791" 
    
    # 단기예보(getVilageFcst) 호출을 위한 설정값
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    
    # 오늘 날짜와 현재 시간에 맞게 자동 설정
    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    base_time = "0500" # 기상청 단기예보가 발표되는 안정적인 시간대 설정

    params = {
        'serviceKey' : auth_key,
        'pageNo' : '1',
        'numOfRows' : '100', # 넉넉하게 가져오기
        'dataType' : 'JSON',
        'base_date' : base_date,
        'base_time' : base_time,
        'nx' : nx, #
        'ny' : ny  #
    }

    try:
        response = requests.get(url, params=params)
        data_dict = response.json()
        
        # 데이터 추출 로직
        items = data_dict['response']['body']['items']['item']
        
        found = False
        for item in items:
            if item['category'] == 'TMP': # TMP: 1시간 기온
                f_date = item['fcstDate']
                f_time = item['fcstTime']
                f_temp = item['fcstValue']
                
                # 화면에 예쁘게 출력하기
                st.success(f"📍 {selected_city} 기상 예보 정보")
                st.write(f"📅 예보 날짜: {f_date} | ⏰ 예보 시각: {f_time}")
                st.