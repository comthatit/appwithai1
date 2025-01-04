import streamlit as st
import pandas as pd

# Load address mapping data
@st.cache
def load_address_data():
    try:
        address_df = pd.read_excel("address.xls")
        address_df.columns = ["중학교명", "시", "구"]  # Ensure columns match expected names
        return address_df
    except Exception as e:
        st.error(f"주소 매핑 데이터 로드 중 오류가 발생했습니다: {e}")
        return None

# Function to map school names to region information
def map_region(school_name, address_df):
    match = address_df[address_df["중학교명"] == school_name]
    if not match.empty:
        return f"{match.iloc[0]['시']} {match.iloc[0]['구']}"
    return "정보 없음"

# Streamlit app title
st.title("학생 데이터 분석 및 지역 추가")

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

        # Load address data
        address_df = load_address_data()
        if address_df is not None:
            # Add region information
            df['지역'] = df['중학교'].apply(lambda x: map_region(x, address_df))

            # Display updated data
            st.subheader("업데이트된 데이터")
            st.dataframe(df)

            # Download updated file
            st.subheader("업데이트된 파일 다운로드")
            output_file = "updated_data.xlsx"
            df.to_excel(output_file, index=False)
            with open(output_file, "rb") as file:
                st.download_button(
                    label="업데이트된 파일 다운로드",
                    data=file,
                    file_name="updated_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            # Regional statistics
            st.subheader("지역별 통계 (구별)")
            district_stats = df['지역'].value_counts()
            st.write(district_stats)

            # Visualization
            st.subheader("지역별 통계 시각화")
            st.bar_chart(district_stats)

    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
else:
    st.write("파일을 업로드하면 지역 정보와 통계가 표시됩니다.")
