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

# /* Intern modules */
from app import WebApp
from config import Config
from functions import prepare_directories
from logger import Logger


# Paths
zip_path = "data/archive.zip"
extract_dir = "extracted_data"

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# Download the ZIP file if it doesn't exist
if not os.path.exists(zip_path):
    st.warning("Downloading the ZIP file...")
    file_url = "https://perso.telecom-paristech.fr/nallegre-24/projet_bgdia700/recipe.zip"
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        st.success("ZIP file downloaded successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to download the ZIP file: {e}")
        st.stop()

# Extract the ZIP file if the directory doesn't exist
if not os.path.exists(extract_dir):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        st.success("ZIP file extracted successfully!")
    except zipfile.BadZipFile:
        st.error("The ZIP file is corrupted.")
        st.stop()

# Debug: List extracted files
extracted_files = os.listdir(extract_dir)
st.write(f"Extracted files: {extracted_files}")

# Check if required files exist
required_files = ["RAW_interactions.csv", "RAW_recipes.csv"]
missing_files = [f for f in required_files if f not in extracted_files]

if missing_files:
    st.error(f"The following required files are missing: {missing_files}")
    st.stop()

# Load data
interactions_path = os.path.join(extract_dir, "RAW_interactions.csv")
recipes_path = os.path.join(extract_dir, "RAW_recipes.csv")

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
