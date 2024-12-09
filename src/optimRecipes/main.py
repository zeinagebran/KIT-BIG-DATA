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

import os
import requests
import zipfile
import streamlit as st

# Path to the data file
zip_path = "data/archive.zip"
extract_dir = "data/extracted"

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

# URL of the hosted file
# Replace with your file's URL
file_url = "https://perso.telecom-paristech.fr/nallegre-24/projet_bgdia700/recipe.zip"

# Check if the ZIP file is missing
if not os.path.exists(zip_path):
    st.warning("The data archive is missing. Downloading it...")
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        st.success("File downloaded successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to download the file: {e}")
        st.stop()

# Extract the ZIP file
if not os.path.exists(extract_dir):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    st.success("Data extracted successfully!")

# Your application code can now use the extracted data


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
