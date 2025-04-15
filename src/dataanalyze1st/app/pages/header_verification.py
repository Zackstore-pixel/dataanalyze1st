import streamlit as st
import pandas as pd

st.title("🧠 Header Detection Confirmation")

try:
    df = pd.read_parquet("data/02_intermediate/parsed_data.parquet")
    st.subheader("✅ Headers Detected:")
    st.write(df.columns.tolist())

    st.subheader("📦 Sample Data:")
    st.dataframe(df.head())

    if st.button("✅ Yes, these headers are correct"):
        st.success("Awesome! You're ready to proceed to the next step.")
    if st.button("❌ No, re-run with another row"):
        st.warning("You can override header detection or choose manually (coming soon).")

except Exception as e:
    st.error(f"⚠️ Error loading parsed data: {e}")
