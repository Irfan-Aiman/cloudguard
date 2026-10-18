import streamlit as st
import pandas as pd
import sys
import os

# Allow imports from the parent scanner directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scanner.s3_scanner import scan_s3_buckets
from scanner.activity_monitor import scan_cloudtrail_activity

st.set_page_config(page_title="CloudGuard Console", page_icon="🛡️", layout="wide")

# Sidebar
st.sidebar.title("🛡️ CloudGuard")
st.sidebar.caption("Connected to: us-east-2")  # Corrected to Ohio

if st.sidebar.button("Run Live Scan", type="primary"):
    st.rerun()

# Run actual scanners against AWS
with st.spinner("Querying AWS APIs..."):
    s3_results = scan_s3_buckets()
    cloudtrail_results = scan_cloudtrail_activity(hours_back=12)

# Convert live results into display format
live_findings = []

for item in s3_results:
    live_findings.append({
        "Service": item["service"],
        "Resource": item["resource"],
        "Severity": item["severity"],
        "Issue": item["issue"],
        "Status": "Open"
    })

for item in cloudtrail_results:
    live_findings.append({
        "Service": "CloudTrail / Network",
        "Resource": item["actor"],
        "Severity": item["severity"],
        "Issue": f"{item['event_name']} - {item['threat']}",
        "Status": "Open"
    })

st.title("Live Security Findings")

if live_findings:
    df = pd.DataFrame(live_findings)
    st.dataframe(df, use_container_width=True)
else:
    st.success("No security misconfigurations or suspicious activities found!")