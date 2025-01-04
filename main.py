import streamlit as st
import pandas as pd

# 지역 매핑 데이터 로드
@st.cache
def load_mapping_data():
    # 예제 데이터셋
    data = {
        "중학교명": ["선린중학교", "도곡중학교", "숭실중학교", "목일중학교"],
        "지역정보": ["서울특별시 용산구", "서울특별시 강남구", "서울특별시 동작구", "서울특별시 양천구"],
    }
    return pd.DataFrame(data)

# 지역 정보 추출 함수
def map_district(school_name, mapping_df):
    match = mapping_df[mapping_df["중학교명"] == school_name]
    if not match.empty:
        return match.iloc[0]["지역정보"]
    return "정보 없음"

# Streamlit 앱
st.title("중학교 지역별 분석")

# 사용자 파일 업로드
uploaded_file = st.file_uploader("학생 데이터 파일을 업로드하세요 (Excel 형식)", type=["xlsx"])

if uploaded_file:
    # Load Excel file
    user_data = pd.ExcelFile(uploaded_file)
    sheet_name = user_data.sheet_names[0]
    df = user_data.parse(sheet_name)

    # Rename columns
    df.columns = ['연번', '임시반', '임시번호', '중학교', '성명', '성별', '합격학과']
    df = df[~df['연번'].isin(['연번', None])]
    df['중학교'] = df['중학교'].astype(str)

    # 지역 매핑 데이터 로드
    mapping_df = load_mapping_data()

    # 지역 정보 추가
    df['지역'] = df['중학교'].apply(lambda x: map_district(x, mapping_df))

    # 지역별 통계
    district_stats = df['지역'].value_counts()

    # 결과 출력
    st.subheader("업로드된 데이터와 지역 정보")
    st.dataframe(df)

    st.subheader("지역별 통계")
    st.write(district_stats)

    st.subheader("지역별 통계 시각화")
    st.bar_chart(district_stats)

else:
    st.write("파일을 업로드하면 지역 정보와 통계가 표시됩니다.")
