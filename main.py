import streamlit as st
import pandas as pd
import re  # Regular expressions for extracting location data

def extract_district(school_name):
    """Extract district information from school name using regex."""
    match = re.search(r'(서울시\\s[가-힣]+구)', school_name)
    if match:
        return match.group(1)
    return "기타"

# Streamlit app title
st.title("지역별 중학교 통계 분석")

# File uploader
uploaded_file = st.file_uploader("학생 데이터 파일을 업로드하세요 (Excel 형식)", type=["xlsx"])

if uploaded_file:
    try:
        # Load Excel file
        data = pd.ExcelFile(uploaded_file)
        sheet_name = data.sheet_names[0]
        df = data.parse(sheet_name)

        # Rename columns
        df.columns = ['연번', '임시반', '임시번호', '중학교', '성명', '성별', '합격학과']
        df = df[~df['연번'].isin(['연번', None])]
        df['연번'] = pd.to_numeric(df['연번'], errors='coerce')
        df['중학교'] = df['중학교'].astype(str)
        df['성별'] = df['성별'].astype(str)

        # Extract district information
        df['지역'] = df['중학교'].apply(extract_district)

        # District statistics
        district_stats = df['지역'].value_counts()

        # Display data
        st.subheader("업로드된 데이터")
        st.dataframe(df)

        st.subheader("지역별 통계")
        st.write(district_stats)

        # Visualization
        st.subheader("지역별 통계 시각화")
        st.bar_chart(district_stats)

    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
else:
    st.write("파일을 업로드하면 데이터 분석 결과가 표시됩니다.")
