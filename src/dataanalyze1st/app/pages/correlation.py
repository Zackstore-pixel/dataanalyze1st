import streamlit as st
import pandas as pd

st.title("🔗 Correlation Matrix Viewer")

try:
    df = pd.read_parquet("data/04_feature/correlation_matrix.parquet")
    st.write(df)
    st.dataframe(df.style.background_gradient(cmap='coolwarm', axis=None))
except Exception as e:
    st.warning(f"⚠️ Could not load correlation matrix: {e}")
