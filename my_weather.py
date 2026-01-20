import streamlit as st
import requests
from datetime import datetime

# 1. 환경 설정 및 데이터 정의 (가장 먼저 나와야 합니다)
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
nx = locations[selected_city]["nx"] #
ny = locations[selected_city]["ny"] #

# 4. 날씨 확인 버튼 및 로직
if st.button(f"{selected_city} 기온 확인하기"):
    # 선생님이 입력하신 인증키를 사용합니다.
    auth_key = "f0cc4e1eb2f7f6c3613c93bcecf0e5e554ef9bd38070521b661234849bfd1791" 
    
    # 기상청 단기예보 API 주소
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    
    # 현재 날짜 및 발표 시간 설정
    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    base_time = "0500" # 안정적인 데이터를 위해 05시 발표분 사용

    params = {
        'serviceKey' : auth_key,
        'pageNo' : '1',
        'numOfRows' : '100',
        'dataType' : 'JSON',
        'base_date' : base_date,
        'base_time' : base_time,
        'nx' : nx,
        'ny' : ny
    }

    try:
        response = requests.get(url, params=params)
        data_dict = response.json()
        
        # 데이터 추출
        items = data_dict['response']['body']['items']['item']
        
        for item in items:
            # TMP 카테고리가 '1시간 기온'을 의미합니다.
            if item['category'] == 'TMP': 
                f_date = item['fcstDate']
                f_time = item['fcstTime']
                f_temp = item['fcstValue']
                
                # 화면 출력 (여기가 63번 줄 근처입니다. 문장을 끝까지 완성했습니다!)
                st.success(f"📍 {selected_city} 지역 예보 정보")
                st.write(f"📅 날짜: {f_date} | ⏰ 시각: {f_time}")
                st.metric(label="현재 예상 기온", value=f"{f_temp} °C")
                break # 하나의 데이터만 출력하고 멈춤
                
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")