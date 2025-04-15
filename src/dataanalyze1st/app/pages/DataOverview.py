import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📁 Cleaned Dataset Overview")

# Datasets to show
files = {
    "Echelon Data": {
        "path": "data/02_intermediate/parsed_data_echelon.parquet",
        "description": "🔍 Mesures vapeur ACP28% pour l’échangeur dans différents échelons."
    },
    "Consommation Vapeur": {
        "path": "data/02_intermediate/parsed_data_conso.parquet",
        "description": "📊 Données de consommation vapeur issues du circuit ACP."
    }
}

for name, meta in files.items():
    st.subheader(name)
    st.markdown(meta["description"])

    try:
        df = pd.read_parquet(meta["path"])
        numeric_cells = df.select_dtypes("number").astype(bool).sum().sum()
        total_cells = df.size
        clean_percent = round((numeric_cells / total_cells) * 100, 2)

        st.success(f"✅ Statistically clean: **{clean_percent}%**")

        with st.expander("🔎 Preview dataset"):
            st.dataframe(df.head(50))
    except Exception as e:
        st.error(f"⚠️ Could not load file: {e}")
