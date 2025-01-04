import streamlit as st
import pandas as pd

# Streamlit app title
st.title("📊 우리학교 입학생 통계 📚")

# File uploader
uploaded_file = st.file_uploader("학생 데이터 파일을 업로드하세요 (Excel 형식)", type=["xlsx"])

if uploaded_file:
    try:
        # Load user data
        user_data = pd.ExcelFile(uploaded_file)
        sheet_name = user_data.sheet_names[0]
        df = user_data.parse(sheet_name)

        # Rename columns
        df.columns = ['연번', '임시반', '임시번호', '중학교', '성명', '성별', '합격학과']
        df = df[~df['연번'].isin(['연번', None])]
        df['중학교'] = df['중학교'].astype(str)

        # Middle school statistics
        middle_school_stats = df['중학교'].value_counts()
        class_stats = df['임시반'].value_counts()
        department_stats = df['합격학과'].value_counts()

        # Display data
        st.subheader("업로드된 데이터")
        st.dataframe(df)

        # Display middle school statistics
        st.subheader("중학교별 학생 수 통계")
        st.write(middle_school_stats)

        # Display department statistics
        st.subheader("합격학과별 학생 수 통계")
        st.write(department_stats)

        # Visualization
        st.subheader("중학교별 학생 수 시각화 📈")
        st.bar_chart(middle_school_stats)


        st.subheader("합격학과별 학생 수 시각화 🎓")
        st.bar_chart(department_stats)

    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
else:
    st.write("파일을 업로드하면 다양한 입학생 통계가 표시됩니다.")
