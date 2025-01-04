import streamlit as st
import pandas as pd

# Streamlit app title
st.title("학생 데이터 분석")

# File uploader
uploaded_file = st.file_uploader("학생 데이터 파일을 업로드하세요 (Excel 형식)", type=["xlsx"])

if uploaded_file:
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

    # Middle school stats
    middle_school_stats = df['중학교'].value_counts()

    # Gender stats
    gender_stats = df['성별'].value_counts()

    # Display data
    st.subheader("업로드된 데이터")
    st.dataframe(df)

    st.subheader("중학교 통계")
    st.write(middle_school_stats)

    st.subheader("성별 통계")
    st.write(gender_stats)

    # Visualizations
    st.subheader("시각화")

    # Middle school chart
    st.write("### 중학교별 학생 수 (상위 10개)")
    st.bar_chart(middle_school_stats.head(10))

    # Gender distribution chart
    st.write("### 성별 분포")
    gender_df = gender_stats.reset_index()
    gender_df.columns = ['성별', '학생 수']
    st.write(gender_df)
    st.bar_chart(data=gender_df, x='성별', y='학생 수')
else:
    st.write("파일을 업로드하면 데이터 분석 결과가 표시됩니다.")
