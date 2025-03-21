# streamlit_app.py

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/api/v1/call-quality"

st.title("Call Quality Metrics Analysis 📊")

# Fetch call quality metrics from FastAPI
st.sidebar.header("Data Fetching")
if st.sidebar.button("Fetch Call Quality Data"):
    with st.spinner("Fetching data..."):
        response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame.from_dict(data, orient="index").reset_index().rename(columns={"index": "call_id"})


        st.subheader("Silence Percentage per Call")
        fig, ax = plt.subplots()
        ax.bar(df["call_id"], df["silence_percentage"], color="blue")
        ax.set_ylabel("Silence Percentage (%)")
        ax.set_xticklabels(df["call_id"], rotation=45)
        st.pyplot(fig)

        st.subheader("Overtalk Percentage per Call")
        fig, ax = plt.subplots()
        ax.bar(df["call_id"], df["overtalk_percentage"], color="red")
        ax.set_ylabel("Overtalk Percentage (%)")
        ax.set_xticklabels(df["call_id"], rotation=45)
        ax.set_ylim(0, max(df["overtalk_percentage"]) + 10)
        st.pyplot(fig)

    else:
        st.error("Failed to fetch data. Please check the API.")
