import streamlit as st
from utils import add_student

st.title("➕ Add Student")

name = st.text_input("Name")
tenth = st.number_input("10th %", 0.0, 100.0)
twelfth = st.number_input("12th %", 0.0, 100.0)
cgpa = st.number_input("BE CGPA", 0.0, 10.0)

skills = st.text_input("Skills")
domain = st.text_input("Domain")

projects = st.number_input("Projects", 0)
hackathons = st.number_input("Hackathons", 0)
papers = st.number_input("Papers", 0)

placed = st.checkbox("Placed")
company = st.text_input("Company")
salary = st.number_input("Salary", 0.0)
company_type = st.selectbox(
    "Company Type",
    ["Product", "Service", "Support"]
)

if st.button("Add Student"):

    data = {
        "name": name,
        "tenth": tenth,
        "twelfth": twelfth,
        "be_cgpa": cgpa,
        "skills": skills,
        "domain": domain,
        "projects": projects,
        "hackathons": hackathons,
        "papers": papers,
        "placed": placed,
        "company": company,
        "salary": salary,
        "company_type": company_type
    }

    res = add_student(data)

    if res.status_code == 200:
        st.success("Student added ✅")
        st.json(res.json())
    else:
        st.error(res.text)
