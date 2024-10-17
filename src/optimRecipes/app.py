import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Test import recipes_df

# trial
recipe_id = st.selectbox("Choisissez une recette:",
                         recipes_df['id'].unique())
selected_recipe = recipes_df[recipes_df['id'] == recipe_id]
st.write(selected_recipe)
