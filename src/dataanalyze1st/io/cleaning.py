import pandas as pd
import numpy as np
import re
import json
from fuzzywuzzy import fuzz
from langdetect import detect
from typing import Tuple

# 1. Common null values
SEMANTIC_NULLS = [
    "no data", "n/a", "null", "none", "--", "-", "missing", "vide",
    "pas de données", "indisponible", "indispo", ""
]

def normalize_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Replace common semantic null values with np.nan (case-insensitive)."""
    return df.applymap(
        lambda x: np.nan if isinstance(x, str) and x.strip().lower() in SEMANTIC_NULLS else x
    )

# 2. Fuzzy role detection
def infer_column_role(col_name: str) -> str:
    """Fuzzy match common engineering terms."""
    name = col_name.lower()

    if fuzz.partial_ratio(name, "date") > 80 or "time" in name:
        return "timestamp"
    if fuzz.partial_ratio(name, "température") > 80 or "temp" in name:
        return "temperature"
    if "débit" in name or "flow" in name:
        return "flow"
    if "pression" in name or "pressure" in name:
        return "pressure"
    return "unknown"

# 3. Language detection
def detect_language_for_column(col_name: str) -> str:
    try:
        return detect(col_name)
    except:
        return "unknown"

# 4. Numeric conversion
def auto_convert_numeric(df: pd.DataFrame) -> pd.DataFrame:
    return df.apply(lambda col: pd.to_numeric(col, errors='ignore'))

# 5. Semantic cleaner + context detector
def smart_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_nulls(df)
    df = auto_convert_numeric(df)

    # Show missing count per column
    print("🧹 Missing values per column before cleaning:")
    print(df.isnull().sum())

    # Don't drop all rows — keep ones where at least X% is filled
    threshold = int(0.7 * df.shape[1])  # Keep rows with ≥70% non-NA values
    df_cleaned = df.dropna(thresh=threshold)

    print(f"\n🧾 Rows before cleaning: {len(df)}")
    print(f"✅ Rows after cleaning: {len(df_cleaned)}")

    if df_cleaned.empty:
        raise ValueError("❌ All rows removed. Relax cleaning threshold or inspect input file.")

    return df_cleaned

# 6. Generate metadata map
def generate_column_metadata(df: pd.DataFrame) -> dict:
    metadata = {}
    for col in df.columns:
        metadata[col] = {
            "role": infer_column_role(col),
            "language": detect_language_for_column(col),
            "dtype": str(df[col].dtype),
        }
    return metadata

# 7. Save metadata to disk
def save_metadata(metadata: dict, output_path: str = "data/08_reporting/column_metadata.json"):
    with open(output_path, "w") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

def coerce_column_types(df: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
    total_cells = df.shape[0] * df.shape[1]
    numeric_cells = 0

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        numeric_cells += df[col].notna().sum()
        df[col] = df[col].fillna(0)  # Replace all non-numeric values with 0

    percentage_clean = round((numeric_cells / total_cells) * 100, 2)
    return df, percentage_clean