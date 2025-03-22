import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/api/v1/call-quality"

st.title("Call Quality Metrics Analysis")

def fetch_call_quality_data():
    """
    Fetch call quality metrics from the FastAPI backend.

    Returns:
    --------
    dict:
        A dictionary containing call quality metrics if successful, else None.
    """
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {str(e)}")
        return None

# Sidebar section for fetching data
st.sidebar.header("Data Fetching")
if st.sidebar.button("Fetch Call Quality Data"):
    with st.spinner("Fetching data..."):
        data = fetch_call_quality_data()

    if data:
        # Convert data to a Pandas DataFrame
        df = pd.DataFrame.from_dict(data["call_quality_metrics"], orient="index").reset_index()
        df.columns = ["call_id", "overtalk_percentage", "silence_percentage"]

        st.subheader("Silence Percentage per Call")
        fig, ax = plt.subplots()
        ax.bar(df["call_id"], df["silence_percentage"], color="blue")
        ax.set_ylabel("Silence Percentage (%)")
        ax.set_xticklabels(df["call_id"], rotation=45, ha="right")
        st.pyplot(fig)

        st.subheader("Overtalk Percentage per Call")
        fig, ax = plt.subplots()
        ax.bar(df["call_id"], df["overtalk_percentage"], color="red")
        ax.set_ylabel("Overtalk Percentage (%)")
        ax.set_xticklabels(df["call_id"], rotation=45, ha="right")
        ax.set_ylim(0, max(df["overtalk_percentage"]) + 10)
        st.pyplot(fig)
    else:
        st.error(" No data available. Please check the API.")

#streamlit run call_quality_dashboard.py
