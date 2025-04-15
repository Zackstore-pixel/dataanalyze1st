import streamlit as st
import pandas as pd

st.title("🧬 PCA Result Viewer")

try:
    df = pd.read_parquet("data/04_feature/pca_result.parquet")
    st.write("Preview of PCA-transformed data:")
    st.dataframe(df)
except Exception as e:
    st.warning(f"⚠️ Could not load PCA result: {e}")
