import streamlit as st
import pandas as pd
from utils import get_students

st.title("📊 Analytics Dashboard")

res = get_students()

if res.status_code == 200:

    df = pd.DataFrame(res.json())

    if not df.empty:

        st.subheader("📌 Key Metrics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Avg CGPA", round(df["be_cgpa"].mean(), 2))

        with col2:
            st.metric("Placement Rate", round(df["placed"].mean() * 100, 2))

        st.subheader("📈 CGPA Chart")
        st.bar_chart(df.set_index("name")["be_cgpa"])

        st.subheader("⚠️ At Risk Students (CGPA < 6)")
        st.dataframe(df[df["be_cgpa"] < 6])

    else:
        st.warning("No data available")

else:
    st.error("Failed to fetch data")
