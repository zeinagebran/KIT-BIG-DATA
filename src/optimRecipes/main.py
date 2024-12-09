"""optimRecipes/main.py file.

main entry for the optimRecipes app.

"""
###############################################################################
# IMPORTS :
# /* Standard includes. */
# /* Extern modules */
import nltk

import os
import requests
import zipfile
import streamlit as st
import pandas as pd

import glob

# /* Intern modules */
from app import WebApp
from config import Config
from functions import prepare_directories
from logger import Logger


zip_path = "data/archive.zip"
extract_dir = "extracted_data"

# Extract ZIP file
if not os.path.exists(extract_dir):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    st.success("ZIP file extracted successfully!")

# Debug: List extracted files
extracted_files = os.listdir(extract_dir)
st.write(f"Extracted files: {extracted_files}")

# Dynamically search for the required files
interactions_path = glob.glob(f"{extract_dir}/**/RAW_interactions.csv", recursive=True)
recipes_path = glob.glob(f"{extract_dir}/**/RAW_recipes.csv", recursive=True)

if not interactions_path or not recipes_path:
    st.error("Required files not found in the extracted data.")
    st.stop()

# Use the first match
interactions_path = interactions_path[0]
recipes_path = recipes_path[0]

st.success(f"Found RAW_interactions.csv at: {interactions_path}")
st.success(f"Found RAW_recipes.csv at: {recipes_path}")

# Load data
try:
    interactions_df = pd.read_csv(interactions_path)
    recipes_df = pd.read_csv(recipes_path)
    st.success("Data loaded successfully!")
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()


def main():
    """Entry point of the module."""
    nltk.download('stopwords')
    cfg = Config()
    prepare_directories(cfg=cfg)
    log_module = Logger(cfg=cfg)
    app = WebApp(log_module=log_module, cfg=cfg)
    app.run()


if __name__ == '__main__':
    main()
