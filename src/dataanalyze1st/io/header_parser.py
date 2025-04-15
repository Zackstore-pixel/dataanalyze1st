import pandas as pd
import numpy as np
from dateutil.parser import parse as date_parse
from dataanalyze1st.io.cleaning import coerce_column_types
from typing import List, Tuple

# Step 1: detect if value looks like a date
def is_date(string: str) -> bool:
    try:
        date_parse(str(string), fuzzy=False)
        return True
    except Exception:
        return False

# Step 2: detect which row is most likely to be the header
def detect_header_row(df: pd.DataFrame, max_rows_to_check=10) -> int:
    scores = []
    for i in range(min(len(df), max_rows_to_check)):
        row = df.iloc[i]
        non_empty = row.notna().sum()
        date_like = sum([is_date(val) for val in row])
        string_like = sum([isinstance(val, str) for val in row])
        score = non_empty + 0.5 * string_like + 2 * date_like
        scores.append((i, score))
    
    best_row = max(scores, key=lambda x: x[1])[0]
    return best_row

# Step 3: apply that row as the header
def parse_headers(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    # Assume first 2 rows are header: row 0 = group (e.g., Echelon J), row 1 = actual column name
    top_row = df.iloc[0].fillna("")       # Row 0
    second_row = df.iloc[1].fillna("")    # Row 1

    combined_headers = []
    seen = set()

    for i, (cat, label) in enumerate(zip(top_row, second_row)):
        name = f"{cat} - {label}".strip(" -") if cat else label
        if not name or str(name).lower() in ["nan", "no data", ""]:
            name = f"column_{i}"
        elif name in seen:
            name = f"{name}_{i}"
        seen.add(name)
        combined_headers.append(name)

    # Apply new headers
    df.columns = combined_headers
    df = df.drop(index=[0, 1])  # drop both header rows
    df = df.reset_index(drop=True)

    return df, combined_headers

# ✅ Step 4: create the node to plug into Kedro

def header_detection_node(df: pd.DataFrame) -> pd.DataFrame:
    df_parsed, _ = parse_headers(df)
    df_cleaned, clean_score = coerce_column_types(df_parsed)

    print(f"📊 ✅ Data is {clean_score}% statistically clean and ready for analysis.")

    return df_cleaned

