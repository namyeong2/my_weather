import streamlit as st
import requests

# 1. 웹앱의 제목과 설명 부착
st.title("☀️ 지금 몇 도야?")
# 사용자가 화면에서 고른 글자(예: "서울")가 selected_city 변수에 저장됩니다.
selected_city = st.selectbox("확인하고 싶은 지역을 선택하세요.", list(locations.keys()))

# 고른 지역에 맞는 숫자를 도서관에서 꺼내옵니다.
nx = locations[selected_city]["nx"]
ny = locations[selected_city]["ny"]

# f-string을 사용하여 "서울 기온 확인하기"처럼 동적으로 변하게 합니다.
if st.button(f"{selected_city} 기온 확인하기"):
    # 이후의 API 호출 로직은 기존과 동일합니다.

st.write("공공데이터포털의 기상청 API를 활용한 웹앱입니다.")

# 2. 사용자로부터 인증키 입력받기 (보안을 위해 직접 입력)
auth_key = "f0cc4e1eb2f7f6c3613c93bcecf0e5e554ef9bd38070521b661234849bfd1791" 

# 이제 버튼을 누르지 않아도 바로 실행되게 하려면 'if st.button' 문을 제거하면 됩니다.
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
params = {
    'serviceKey' : auth_key,
    # ... 나머지 설정은 동일
}

# 3. '날씨 확인' 버튼 만들기
if st.button("현재 기온 확인하기"):
    if auth_key:
        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        
        # 선생님이 성공하셨던 그 설정값들입니다! [cite: 1670, 1692-1701]
        params = {
            'serviceKey' : auth_key,
            'pageNo' : '1',
            'numOfRows' : '10',
            'dataType' : 'JSON',
            'base_date' : '20260119', # 실행하는 날짜에 맞춰 수정 가능
            'base_time' : '1400',
            locations = {
    "대전(본부)": {"nx": 67, "ny": 134},
    "서울": {"nx": 60, "ny": 127},
    "부산": {"nx": 98, "ny": 76},
    "제주": {"nx": 52, "ny": 38}
}

        try:
            response = requests.get(url, params=params)
            data_dict = response.json()
            
            # 데이터 추출 로직 
            items = data_dict['response']['body']['items']['item']
            
            for item in items:
                if item['category'] == 'TMP': # 기온 데이터만 골라내기 
                    f_date = item['fcstDate']
                    f_time = item['fcstTime']
                    f_temp = item['fcstValue']
                    
                    # 화면에 예쁘게 출력하기
                    st.success(f"📅 날짜: {f_date} | ⏰ 시각: {f_time}")
                    st.metric(label="현재 기온", value=f"{f_temp} °C")
                    
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("인증키를 먼저 입력해 주세요!")