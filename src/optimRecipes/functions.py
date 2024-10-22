import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import streamlit as st
from wordcloud import WordCloud


# Function to extract and load data from a zip file


@st.cache_data
def extract_and_load_data():
    # Extract the zip file
    #with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    #    zip_ref.extractall("extracted_data")
    # Load the interactions dataset
    #interactions_df = pd.read_csv("extracted_data/RAW_interactions.csv")
    interactions_df = pd.read_csv('/Users/habibatasamake/Desktop/MS_IA/BGDIA700 - Kit Big Data/Projet/archive/RAW_interactions.csv')
    recipes = pd.read_csv('/Users/habibatasamake/Desktop/MS_IA/BGDIA700 - Kit Big Data/Projet/archive/RAW_recipes.csv')
    return interactions_df, recipes

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



# Importez vos fonctions statiques ici
def format_to_datetime(df, column_name, date_format='%Y-%m-%d'):
    df[column_name] = pd.to_datetime(df[column_name], format=date_format)
    return df

def format_to_numeric(df, column_name):
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    return df

def rename_column(df, old_name, new_name):
    df.rename(columns={old_name: new_name}, inplace=True)
    return df

def merge_with(df, other_df, on_attribute):
    merged_df = pd.merge(df, other_df, on=on_attribute)
    return merged_df

def group_by_attribute_count(df, on_attributes):
    return df.groupby(on_attributes).size().reset_index(name='count')

def filter_positive_ratings(df, rating_column, threshold=4):
    return df[df[rating_column] >= threshold]

def get_top_n_recipes_by_ratings(df, recipe_id_column, rating_column, n=15):
    top_recipes = df.groupby(recipe_id_column).size().reset_index(name='positive_ratings')
    top_recipes_sorted = top_recipes.sort_values(by='positive_ratings', ascending=False).head(n)
    top_recipes_details = df[df[recipe_id_column].isin(top_recipes_sorted[recipe_id_column])]
    return top_recipes_details

# Fonction principale pour afficher les visualisations dans Streamlit
def display_popular_recipes_and_visualizations(recipe, interaction):
    # Formater la colonne 'submitted' en datetime
    recipe = format_to_datetime(recipe, 'submitted')

    # Renommer la colonne 'id' en 'recipe_id'
    recipe = rename_column(recipe, 'id', 'recipe_id')

    # Fusionner avec le DataFrame interaction
    merged_df = merge_with(recipe, interaction, on_attribute='recipe_id')

    # Convertir la colonne 'rating' en numérique
    merged_df = format_to_numeric(merged_df, 'rating')

    # Filtrer les ratings positifs (>= 4)
    filtered_df = filter_positive_ratings(merged_df, 'rating')

    # Compter les ratings positifs par recette et obtenir les 15 premières
    top_recipes = get_top_n_recipes_by_ratings(filtered_df, 'recipe_id', 'rating', n=15)

    # Grouper par 'recipe_id', 'name', et 'rating'
    grouped_df = group_by_attribute_count(top_recipes, ['recipe_id', 'name', 'rating'])
    
    st.title("Top 50 Most Popular Recipes Based on Ratings and Comments")

    # Configuration du style pour un aspect plus professionnel
    sns.set(style="whitegrid")

    # Créer une palette de couleurs unique pour chaque 'recipe_id'
    unique_recipes = grouped_df['recipe_id'].unique()
    palette = sns.color_palette("husl", len(unique_recipes))

    # Création du barplot avec les couleurs associées à chaque recette
    fig, ax = plt.subplots(figsize=(20, 15))
    sns.barplot(x='recipe_id', y='count', hue='rating', data=grouped_df, palette=palette, dodge=True, ax=ax)

    # Ajouter des labels au-dessus des barres
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='baseline', fontsize=12, color='black', xytext=(0, 5),
                    textcoords='offset points')

    ax.set_title('Number of Ratings per Recipe', fontsize=18)
    ax.set_xlabel('Recipe ID', fontsize=14)
    ax.set_ylabel('Number of Ratings', fontsize=14)
    ax.legend(title='Rating', loc='upper right')

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

    # Sélection d'une recette spécifique
    recipe_id = st.selectbox("View recipe details: ", grouped_df['recipe_id'].unique())
    selected_recipe = merged_df[merged_df['recipe_id'] == recipe_id]
    st.write(selected_recipe.head(10))
    
    # Formater la colonne 'date' et extraire l'année pour l'évolution des ratings
    selected_recipe = format_to_datetime(selected_recipe, 'date')
    selected_recipe['year'] = selected_recipe['date'].dt.year

    # Grouper les données par 'date' et 'rating'
    grouped_by_date = selected_recipe.groupby(['year', 'rating']).size().reset_index(name='count')

    # Extraire les années uniques pour l'axe des x
    unique_years = sorted(grouped_by_date['year'].unique())

    # Visualisation de l'évolution des ratings par date
    fig, ax = plt.subplots(figsize=(20, 15))
    sns.lineplot(x='year', y='count', hue='rating', data=grouped_by_date, palette='coolwarm', ax=ax)

    # Configuration des axes et du titre
    ax.set_title(f"Evolution of Ratings for Recipe {recipe_id} by Year and Rating Class", fontsize=18)
    ax.set_xlabel('Year', fontsize=14)
    ax.set_ylabel('Number of Ratings', fontsize=14)

    # Ajouter des ticks pour chaque année
    ax.set_xticks(unique_years)
    ax.set_xticklabels(unique_years, rotation=45)  # Rotation des labels pour éviter qu'ils se chevauchent

    # Afficher le graphique d'évolution dans Streamlit
    st.pyplot(fig)

    # Grouper les données par 'recipe_id', 'date', et 'rating' pour une vue détaillée
    detailed_df = group_by_attribute_count(selected_recipe, ['recipe_id', 'date', 'rating'])
    st.write(detailed_df.head())

    # Créer un texte à partir des tags (ou ingrédients) pour générer un nuage de mots
    unique_recipes = merged_df.drop_duplicates(subset=['recipe_id'])
    tags_text = ' '.join(unique_recipes[unique_recipes['recipe_id'].isin(grouped_df['recipe_id'])]['ingredients'].explode().dropna().unique())

    # Générer un nuage de mots
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='plasma').generate(tags_text)

    # Afficher le nuage de mots
    fig_wordcloud, ax_wordcloud = plt.subplots(figsize=(20, 15))
    ax_wordcloud.imshow(wordcloud, interpolation='bilinear')
    ax_wordcloud.axis('off')
    ax_wordcloud.set_title('Word Cloud of Tags for Popular Recipes', fontsize=16)

    # Afficher le graphique du nuage de mots
    st.pyplot(fig_wordcloud)
