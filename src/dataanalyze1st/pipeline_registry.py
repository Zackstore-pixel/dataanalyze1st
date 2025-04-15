from kedro.pipeline import Pipeline
from dataanalyze1st.data_analysis.pipelines.pipeline import create_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    return {
        "__default__": create_pipeline()
    }
