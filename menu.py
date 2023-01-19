import menu as st
import oneai
import os
import sys
import webbrowser
import asyncio
import streamlit.components.v1 as components
from design import *
import requests
import json

from clustering_main import *

# def find_clusters(collection_name, api_key, search_text, uri):
#     url = f"{uri}/clustering/v1/collections/{collection_name}/clusters/find?multilingual=true&translate=true&similarity_threshold=0.5&text={search_text}"
#     headerrs = {"api-key": api_key}
#     response = requests.request("GET", url, headers=headers, data=payload)
#     return response.text()
# # search_text = st.text_input("Enter Search Text")
#     # if st.button("Find Clusters"):
#     #     clusters = find_clusters(collection_name, api_key, search_text, uri)
#     #     st.write(clusters)
#     #     st.stop()


def start_loader():
    envierment = st.selectbox("Select Enviroment", ("Prod", "Staging"))
    api_key = st.text_input("Enter API Key")
    if envierment == "Prod":
        uri = "https://api.oneai.com"
    if envierment == "Staging":
        uri = "https://staging.oneai.com"
    collection_name = st.text_input("Enter Collection Name")
    uploaded_file = st.file_uploader("Upload File", type=["csv"])
    skills = st.multiselect(
        "Select Skills",
        (
            "action-items",
            "anonymize",
            "detect-language",
            "service-email-insights",
            "emotions",
            "headline",
            "highlights",
            "html-extract-article",
            "keywords",
            "names",
            "numbers",
            "business-entities",
            "enhance",
            "sales-insights",
            "sentiments",
            "sentences",
            "dialogue-segmentation",
            "subheading",
            "summarize",
            "article-topics",
        ),
    )
    input_skill = st.selectbox("Select Input Skill", skills)
    st.markdown(skills)
    col1, col2 = st.columns(2)
    main_column = col1.number_input("Enter Main Column (A = 0,B=1...)", min_value=0)
    timestamp_column = col2.number_input(
        "Enter Timestamp Column (A = 0,B=1...)", min_value=0
    )
    col3, col4 = st.columns(2)
    row_range_min = col3.number_input("Enter First Row", min_value=0)
    row_range_max = col4.number_input("Enter Last Row", min_value=0)
    # if st.button("Start Clustering"):
    #     upload_csv_to_collection(
    #         source_file_path=uploaded_file.name,
    #         collection_name=collection_name,
    #         main_column=main_column,
    #         timestamp_column=timestamp_column,
    #         skills=skills,
    #         row_range_start=row_range_min,
    #         row_range_end=row_range_max,
    #         input_skill=input_skill,
    #     )
    #     st.stop()
