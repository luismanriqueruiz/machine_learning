import streamlit as st
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz


def load_har(file):
    har_data = json.load(file)
    return har_data

def extract_entries(har_data):
    return har_data.get("log", {}).get("entries", [])

def process_entries(entries):
    data = []
    utc_zone = pytz.utc
    jst_zone = pytz.timezone("Asia/Tokyo")

    for entry in entries:
        request_url = entry["request"]["url"]
        method = entry["request"]["method"]
        status = entry["response"]["status"]
        started_date_time = entry["startedDateTime"]
        time_taken = entry["time"]

        # Convert to JST
        dt_utc = datetime.strptime(started_date_time, "%Y-%m-%dT%H:%M:%S.%fZ")  # Parse UTC time
        dt_utc = utc_zone.localize(dt_utc)  # Ensure it's treated as UTC
        dt_jst = dt_utc.astimezone(jst_zone)  # Convert to JST

        data.append({
            "Method": method,
            "URL": request_url,
            "Status": status,
            #"Start Time": started_date_time,
            "Start Time": dt_jst.strftime("%Y-%m-%d %H:%M:%S.%f"),  # Format as string
            "Time Taken (ms)": time_taken
        })
    return pd.DataFrame(data)

def plot_response_times(df):
    fig = px.histogram(df, x="Time Taken (ms)", nbins=10, title="Response Time Distribution")
    st.plotly_chart(fig)

def plot_status_codes(df):
    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status Code", "Count"]
    fig = px.bar(status_counts, x="Status Code", y="Count", title="Status Code Distribution")
    st.plotly_chart(fig)

def plot_time_series(df):
    fig = px.line(df, x="Start Time", y="Time Taken (ms)", title="Response Time Over Time")
    st.plotly_chart(fig)

def check_timestamp_errors(df):
    df["Start Time"] = pd.to_datetime(df["Start Time"], errors='coerce')
    df = df.sort_values("Start Time")
    df["Time Diff"] = df["Start Time"].diff().dt.total_seconds()
    errors = df[df["Time Diff"] < 0]
    return errors

def color_status(val):
    if 200 <= val < 300:
        color = 'green'
    elif 300 <= val < 400:
        color = 'blue'
    elif 400 <= val < 500:
        color = 'orange'
    else:
        color = 'red'
    return f'background-color: {color}'

st.title("HAR File Analyzer")

st.markdown("""
    <style>
        .block-container { max-width: 95% !important; }
    </style>
    """, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload HAR File", type=["har"])

if uploaded_file:
    with st.spinner("Processing HAR file..."):
        har_data = load_har(uploaded_file)
        entries = extract_entries(har_data)
        df = process_entries(entries)

        st.markdown("""
        ### HTTP Status Codes Explanation
        - **400 (Bad Request):** The server cannot process the request due to a client error (e.g., malformed request syntax, invalid request message framing).
        - **0 (No Response / Network Error):** This usually means the request never reached the server or was blocked (e.g., due to a network issue, CORS policy, or firewall).
        - **200 (OK):** The request was successful, and the server returned the requested data.
        - **404 (Not Found):** The requested resource was not found on the server.
        - **204 (No Content):** The request was successful, but the server has no content to return.
        """)
        
        st.subheader("Request Data")
        st.dataframe(df.style.applymap(color_status, subset=["Status"]))
        
        st.subheader("Response Time Analysis")
        plot_response_times(df)
        
        st.subheader("Status Code Distribution")
        plot_status_codes(df)
        
        st.subheader("Response Time Over Time")
        plot_time_series(df)
        
        st.subheader("Timestamp Errors")
        errors_df = check_timestamp_errors(df)
        st.dataframe(errors_df) if not errors_df.empty else st.write("No timestamp errors detected.")
        
        st.subheader("Request Details Table")
        selected_url = st.selectbox("Select a request URL", df["URL"].unique())
        request_details = next(entry["request"] for entry in entries if entry["request"]["url"] == selected_url)
        request_df = pd.DataFrame(request_details["headers"])
        st.write("Request Headers")
        st.dataframe(request_df)
        st.write("Other Request Details")
        st.json(request_details, expanded=False)