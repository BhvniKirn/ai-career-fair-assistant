import streamlit as st
import pandas as pd

st.set_page_config(page_title="Company Browser", page_icon="🏢", layout="wide")
st.title("🏢 Company & Role Browser")

@st.cache_data
def load_companies():
    return pd.read_csv("data/companies.csv")

df = load_companies()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    company = st.selectbox("Company", ["(All)"] + sorted(df["company"].unique().tolist()))
with col2:
    degree = st.selectbox("Degree Level", ["(All)"] + sorted(df["degree_level"].unique().tolist()))
with col3:
    location = st.selectbox("Location", ["(All)"] + sorted(df["location"].unique().tolist()))
with col4:
    sponsorship = st.selectbox("Sponsorship", ["(All)"] + sorted(df["sponsorship"].unique().tolist()))
with col5:
    search = st.text_input("Search text", "")

mask = [True] * len(df)
if company != "(All)":
    mask &= (df["company"] == company)
if degree != "(All)":
    mask &= (df["degree_level"] == degree)
if location != "(All)":
    mask &= (df["location"] == location)
if sponsorship != "(All)":
    mask &= (df["sponsorship"] == sponsorship)
if search.strip():
    s = search.lower()
    mask &= df.apply(lambda r: s in " ".join(map(str, r.values)).lower(), axis=1)

st.subheader("Results")
st.dataframe(df[mask].reset_index(drop=True), use_container_width=True)
