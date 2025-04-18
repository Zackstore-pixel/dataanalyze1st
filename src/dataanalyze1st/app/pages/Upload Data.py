import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="📤 Upload Excel", layout="centered")

st.title("📤 Importer un fichier Excel")

uploaded_file = st.file_uploader("Déposez ici votre fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Save uploaded file to data/01_raw/
    filename = f"uploaded_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    save_path = os.path.join("data/01_raw", filename)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Fichier enregistré sous `{filename}` dans data/01_raw`")

    # Preview first sheet
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)
        st.subheader("🔍 Aperçu du premier onglet :")
        st.dataframe(df.head(20))
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
