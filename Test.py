import zipfile
import os
import pandas as pd


zip_file_path = "C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\archive.zip"
# extract

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall("extracted_data")

recipes_df = pd.read_csv("extracted_data/PP_recipes.csv")
interactions_df = pd.read_csv("extracted_data/interactions_test.csv")

print(recipes_df.head())
print(interactions_df.head())
