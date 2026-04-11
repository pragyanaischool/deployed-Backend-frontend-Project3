import streamlit as st
from utils import get_ai_insights

st.title("🤖 AI Placement Insights")

st.write("Click below to analyze student data using AI")

if st.button("Generate Insights"):

    with st.spinner("Analyzing..."):

        res = get_ai_insights()

        if res.status_code == 200:

            insights = res.json().get("insights", "")

            st.success("Insights Generated ✅")

            st.markdown("### 📊 AI Analysis")
            st.write(insights)

        else:
            st.error("Failed to fetch AI insights")
