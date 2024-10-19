import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import streamlit as st

# Function to extract and load data from a zip file


@st.cache_data
def extract_and_load_data(zip_file_path):
    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall("extracted_data")
    # Load the interactions dataset
    interactions_df = pd.read_csv("extracted_data/RAW_interactions.csv")
    return interactions_df

# Function to generate the plot for mean interactions by day of the week


def plot_mean_interactions(interactions_df):
    interactions_df['date'] = pd.to_datetime(
        interactions_df['date'], errors='coerce')
    interactions_df['year'] = interactions_df['date'].dt.year
    interactions_df['day_of_week'] = interactions_df['date'].dt.day_name()
    interactions_per_day_yearly = interactions_df.groupby(
        ['year', 'day_of_week']).size().unstack(fill_value=0)
    mean_interactions_per_day = interactions_per_day_yearly.mean()
    mean_interactions_per_day = mean_interactions_per_day.reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    fig, ax = plt.subplots(figsize=(8, 6))
    mean_interactions_per_day.plot(
        kind='bar', ax=ax, color='skyblue', edgecolor='black')
    ax.set_title('Average User Interactions by Day of the Week', fontsize=16)
    ax.set_xlabel('Day of the Week', fontsize=14)
    ax.set_ylabel('Average Number of Interactions', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    ax.grid(True, which='both', linestyle='--', linewidth=0.7)
    return fig

# Function to generate the plot for seasonality analysis


def plot_seasonality(interactions_df):
    interactions_df['date'] = pd.to_datetime(
        interactions_df['date'], errors='coerce')
    interactions_df['year'] = interactions_df['date'].dt.year
    interactions_df['month'] = interactions_df['date'].dt.month_name()
    interactions_df['season'] = interactions_df['date'].dt.month % 12 // 3 + 1
    interactions_df['season'] = interactions_df['season'].map(
        {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'})

    interactions_per_month_yearly = interactions_df.groupby(
        ['year', 'month']).size().unstack(fill_value=0)
    mean_interactions_per_month = interactions_per_month_yearly.mean()
    ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
    mean_interactions_per_month = mean_interactions_per_month.reindex(
        ordered_months, fill_value=0)

    interactions_per_season_yearly = interactions_df.groupby(
        ['year', 'season']).size().unstack(fill_value=0)
    mean_interactions_per_season = interactions_per_season_yearly.mean()
    ordered_seasons = ['Winter', 'Spring', 'Summer', 'Fall']
    mean_interactions_per_season = mean_interactions_per_season.reindex(
        ordered_seasons, fill_value=0)

    fig, axes = plt.subplots(2, 1, figsize=(10, 10))
    sns.barplot(x=mean_interactions_per_month.index,
                y=mean_interactions_per_month.values, ax=axes[0], palette='Blues')
    axes[0].set_title('Average User Interactions by Month', fontsize=16)
    axes[0].set_xlabel('Month', fontsize=14)
    axes[0].set_ylabel('Average Number of Interactions', fontsize=14)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True, which='both', linestyle='--', linewidth=0.7)

    sns.barplot(x=mean_interactions_per_season.index,
                y=mean_interactions_per_season.values, ax=axes[1], palette='coolwarm')
    axes[1].set_title('Average User Interactions by Season', fontsize=16)
    axes[1].set_xlabel('Season', fontsize=14)
    axes[1].set_ylabel('Average Number of Interactions', fontsize=14)
    axes[1].tick_params(axis='x', rotation=0)
    axes[1].grid(True, which='both', linestyle='--', linewidth=0.7)

    plt.tight_layout()
    return fig
