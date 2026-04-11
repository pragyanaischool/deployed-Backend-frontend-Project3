import streamlit as st
from utils import upload_csv

st.title(" Upload Student Data")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    st.info("File ready")

    if st.button("Upload & Store"):
        with st.spinner("Uploading..."):
            res = upload_csv(file.getvalue())

            if res.status_code == 200:
                st.success("Uploaded successfully ✅")
                st.json(res.json())
            else:
                st.error(res.text)
