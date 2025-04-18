from kedro.pipeline import Pipeline, node, pipeline
from dataanalyze1st.io.header_parser import header_detection_node
from kedro.pipeline import Pipeline, node, pipeline
from dataanalyze1st.data_analysis.nodes_uploaded import header_detection_uploaded
from dataanalyze1st.data_analysis.nodes.nodes import (

    load_and_describe_data,
    clean_and_scale_data,
    compute_correlation_matrix,
    perform_pca
)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        # === Clean both raw Excel files ===
        node(
            func=header_detection_node,
            inputs="data_echelon",
            outputs="parsed_data_echelon",
            name="header_detection_echelon"
        ),
        node(
            func=header_detection_node,
            inputs="dataconsovapeur",
            outputs="parsed_data_conso",
            name="header_detection_conso"
        ),

        # === Perform analysis on one of the parsed files ===
        node(
            func=load_and_describe_data,
            inputs="parsed_data_echelon",
            outputs="described_data",
            name="describe_node"
        ),
        node(
            func=clean_and_scale_data,
            inputs="described_data",
            outputs="clean_scaled_data",
            name="clean_scale_node"
        ),
        node(
            func=compute_correlation_matrix,
            inputs="clean_scaled_data",
            outputs="correlation_matrix",
            name="correlation_node"
        ),
        node(
            func=perform_pca,
            inputs="clean_scaled_data",
            outputs="pca_result",
            name="pca_node"
        ),
    ])
from kedro.pipeline import Pipeline, node, pipeline
from dataanalyze1st.data_analysis.nodes_uploaded import header_detection_uploaded

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=header_detection_uploaded,
            inputs="uploaded_file",
            outputs="cleaned_uploaded_data",
            name="header_detection_uploaded"
        )
    ])
