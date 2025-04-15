import streamlit as st

# App settings
st.set_page_config(page_title="Data Analysis App", layout="wide")

# Language selector (to be reused later)
lang = st.sidebar.selectbox("🌐 Choose Language / Choisir la langue", ["English", "Français"])

# Welcome message
if lang == "English":
    st.title("👋 Welcome to the Data Analysis App")
    st.write("Click on the pages (left sidebar) to explore correlation matrix, PCA results, and more.")
else:
    st.title("👋 Bienvenue dans l'application d'analyse de données")
    st.write("Cliquez sur les pages (barre latérale gauche) pour explorer la matrice de corrélation, les résultats PCA, etc.")
