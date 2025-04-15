import pandas as pd
from dataanalyze1st.io.header_parser import header_detection_node
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

SEMANTIC_NULLS = [
    "No Data", "N/A", "n/a", "null", "None", "--", "-", "missing",
    "pas de données", "indisponible", "vide", ""
]
def load_and_describe_data(df: pd.DataFrame) -> pd.DataFrame:
    """Returns basic info about the dataset."""
    print("🔍 First 5 rows:")
    print(df.head())

    print("\n📊 Description:")
    print(df.describe(include='all'))

    print("\n❓ Missing values:")
    print(df.isnull().sum())

    return df

from dataanalyze1st.io.cleaning import smart_clean_dataframe, generate_column_metadata, save_metadata

def clean_and_scale_data(df: pd.DataFrame) -> pd.DataFrame:
    """Semantic + smart cleaning, scale numerics, and save metadata."""
    df_cleaned = smart_clean_dataframe(df)
    numeric_cols = df_cleaned.select_dtypes(include="number").columns

    if df_cleaned.empty:
        raise ValueError("❌ All rows were dropped. Check preprocessing.")

    # Save metadata for visualization
    metadata = generate_column_metadata(df_cleaned)
    save_metadata(metadata)

    df_cleaned[numeric_cols] = StandardScaler().fit_transform(df_cleaned[numeric_cols])
    return df_cleaned



def compute_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Compute correlation matrix from numeric features."""
    return df.select_dtypes(include='number').corr()

def perform_pca(df: pd.DataFrame, n_components: int = 2) -> pd.DataFrame:
    """Perform PCA and return principal components."""
    numeric_df = df.select_dtypes(include='number')
    pca = PCA(n_components=n_components)
    pcs = pca.fit_transform(numeric_df)
    pca_df = pd.DataFrame(pcs, columns=[f"PC{i+1}" for i in range(n_components)])
    print("🧬 PCA Explained Variance Ratio:", pca.explained_variance_ratio_)
    return pca_df
