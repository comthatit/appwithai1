import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Function to set Korean font
def set_korean_font():
    available_fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    korean_fonts = [font for font in available_fonts if 'Nanum' in font or 'Malgun' in font or 'Gulim' in font]

    if korean_fonts:
        font_prop = fm.FontProperties(fname=korean_fonts[0])
        plt.rcParams['font.family'] = font_prop.get_name()

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

    # Set Korean font
    set_korean_font()

    # Visualizations
    st.subheader("시각화")

    # Middle school chart
    st.write("### 중학교별 학생 수 (상위 10개)")
    top_middle_schools = middle_school_stats.head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_middle_schools.plot(kind='bar', ax=ax)
    ax.set_title("중학교별 학생 수 (상위 10개)", fontsize=14)
    ax.set_xlabel("중학교", fontsize=12)
    ax.set_ylabel("학생 수", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    # Gender distribution chart
    st.write("### 성별 분포")
    gender_stats_cleaned = gender_stats[gender_stats.index != 'nan']  # Exclude NaN values
    fig, ax = plt.subplots(figsize=(8, 8))
    gender_stats_cleaned.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
    ax.set_title("성별 분포", fontsize=14)
    ax.set_ylabel('')
    st.pyplot(fig)
else:
    st.write("파일을 업로드하면 데이터 분석 결과가 표시됩니다.")
