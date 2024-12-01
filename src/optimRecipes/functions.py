import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
import pandas as pd
import seaborn as sns
import zipfile
import streamlit as st
from nltk.corpus import stopwords
from wordcloud import WordCloud

from config import Config
#from optimRecipes.config import Config



# DataExtractor class to handle data extraction and loading


class DataExtractor:
    """
    A class to handle data extraction and loading for recipe and interaction datasets stored in a zip file.

    Attributes:
        zip_file_path (str): The file path to the zip file containing the datasets.
        interactions_df (pd.DataFrame or None): DataFrame to store interactions data after loading.
        recipes_df (pd.DataFrame or None): DataFrame to store recipes data after loading.
    """

    def __init__(self, zip_file_path):
        """
        Initializes the DataExtractor class with the path to the zip file.

        Args:
            zip_file_path (str): The file path to the zip file containing the datasets.
        """
        self.zip_file_path = zip_file_path
        self.interactions_df = None
        self.recipes_df = None

    @st.cache_data
    # Use _self to avoid Streamlit's hashing error
    def extract_and_load_data(_self):
        """
        Extracts and loads recipes and interactions datasets from a zip file.

        This method reads CSV files for interactions and recipes directly from the specified path
        and caches the results to optimize performance with Streamlit.

        Returns:
            tuple: A tuple containing two DataFrames:
                - interactions_df (pd.DataFrame): DataFrame containing interactions data.
                - recipes_df (pd.DataFrame): DataFrame containing recipes data.
        """
        # _self.interactions_df = pd.read_csv(
        #    'C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\RAW_interactions.csv')
        # _self.recipes_df = pd.read_csv(
        #    'C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\RAW_recipes.csv')

        try:
            print(f"Loading data from: {_self.zip_file_path}")
            with zipfile.ZipFile(_self.zip_file_path, 'r') as zip_ref:
                zip_ref.extractall("extracted_data")

            _self.interactions_df = pd.read_csv(
                "/Users/habibatasamake/Desktop/KIT-BIG-DATA/src/optimRecipes/extracted_data/archive/RAW_interactions.csv")
            _self.recipes_df = pd.read_csv("/Users/habibatasamake/Desktop/KIT-BIG-DATA/src/optimRecipes/extracted_data/archive/RAW_recipes.csv")

            # Convert 'date' column in interactions to datetime
            _self.interactions_df['date'] = pd.to_datetime(
                _self.interactions_df['date'], errors='coerce', infer_datetime_format=True
            )
            print(f"Number of unparsed dates: { _self.interactions_df['date'].isna().sum()}")
            print("Data loaded successfully!")
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

        return _self.interactions_df, _self.recipes_df


# Ensure that DataExtractor is used when calling the extract_and_load_data method
def get_data(zip_file_path):
    extractor = DataExtractor(zip_file_path)
    return extractor.extract_and_load_data()
# WeeklyAnalysis class for weekly interaction analysis


class WeeklyAnalysis:
    """
    A class to analyze and visualize the average number of user interactions by day of the week.

    Attributes:
        interactions_df (pd.DataFrame): DataFrame containing interactions data.
    """

    def __init__(self, interactions_df):
        # Store the dataframe and ensure the 'date' column is in datetime format
        self.interactions_df = interactions_df
        self.interactions_df['date'] = pd.to_datetime(
            self.interactions_df['date'], errors='coerce')
        # Extract year and day of the week for analysis
        self.interactions_df['year'] = self.interactions_df['date'].dt.year
        self.interactions_df['day_of_week'] = self.interactions_df['date'].dt.day_name()

    def plot_mean_interactions(self):
        # Calculate interactions per day of the week for each year
        interactions_per_day_yearly = self.interactions_df.groupby(
            ['year', 'day_of_week']).size().unstack(fill_value=0)

        # Calculate the mean interactions per day across all years
        mean_interactions_per_day = interactions_per_day_yearly.mean()

        # Reorder the days of the week for better readability
        ordered_days = ['Monday', 'Tuesday', 'Wednesday',
                        'Thursday', 'Friday', 'Saturday', 'Sunday']
        mean_interactions_per_day = mean_interactions_per_day.reindex(
            ordered_days, fill_value=0)

        # Define the color palette
        colors = ['#FF5733', '#33FF57', '#3357FF',
                  '#FF33A8', '#FFC300', '#33FFF9', '#8E44AD']

        # Plotting with the custom color palette
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x=mean_interactions_per_day.index,
                    y=mean_interactions_per_day.values,
                    ax=ax, palette=colors)

        # Add titles and labels with enhanced styling
        ax.set_title('Average User Interactions by Day of the Week', fontsize=16)
        ax.set_xlabel('Day of the Week', fontsize=14)
        ax.set_ylabel('Average Number of Interactions', fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        ax.grid(True, linestyle='--', linewidth=0.7)
        return fig

    def plot_interactions_for_year(self, year):
        # Filter the data for the selected year
        yearly_data = self.interactions_df[self.interactions_df['year'] == year]

        # Count interactions per day of the week
        interactions_per_day = yearly_data['day_of_week'].value_counts().reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], fill_value=0
        )

        # Define the color palette
        colors = ['#FF5733', '#33FF57', '#3357FF',
                  '#FF33A8', '#FFC300', '#33FFF9', '#8E44AD']

        # Plotting with the same color palette
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x=interactions_per_day.index,
                    y=interactions_per_day.values,
                    ax=ax, palette=colors)

        # Add titles and labels with enhanced styling
        ax.set_title(f'User Interactions by Day of the Week for {year}', fontsize=16)
        ax.set_xlabel('Day of the Week', fontsize=14)
        ax.set_ylabel('Number of Interactions', fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        ax.grid(True, linestyle='--', linewidth=0.7)
        return fig


class SeasonalityAnalysis:
    """
    A class to analyze and visualize seasonal trends in user interactions.

    Attributes:
        interactions_df (pd.DataFrame): DataFrame containing interactions data with a 'date' column.
    """

    def __init__(self, interactions_df):
        """
        Initializes the SeasonalityAnalysis class with a DataFrame of interactions data.

        Args:
            interactions_df (pd.DataFrame): DataFrame containing interactions data, including a 'date' column.
        """
        self.interactions_df = interactions_df
        self.interactions_df['date'] = pd.to_datetime(
            self.interactions_df['date'], errors='coerce')
        self.interactions_df['year'] = self.interactions_df['date'].dt.year
        self.interactions_df['month'] = self.interactions_df['date'].dt.month_name(
        )

        # Ensure month values are integers, then map to seasons
        self.interactions_df['season'] = self.interactions_df['date'].dt.month.map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        }).fillna('Unknown')

    def plot_seasonality(self):
        # Monthly interactions averaged across all years
        interactions_per_month = self.interactions_df.groupby('month').size()
        ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
        interactions_per_month = interactions_per_month.reindex(
            ordered_months, fill_value=0)
        average_interactions_per_month = interactions_per_month / \
            self.interactions_df['year'].nunique()

        # Seasonal interactions
        interactions_per_season = self.interactions_df.groupby('season').size()
        ordered_seasons = ['Winter', 'Spring', 'Summer', 'Fall']
        interactions_per_season = interactions_per_season.reindex(
            ordered_seasons, fill_value=0)
        average_interactions_per_season = interactions_per_season / \
            self.interactions_df['year'].nunique()

        # Define a unique color palette for each month
        month_colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A8', '#FFC300', '#33FFF9',
                        '#8E44AD', '#3498DB', '#2ECC71', '#E67E22', '#E74C3C', '#95A5A6']

        # Create subplots
        fig, axes = plt.subplots(2, 1, figsize=(10, 10))

        # Monthly Plot with unique colors for each month
        sns.barplot(x=average_interactions_per_month.index,
                    y=average_interactions_per_month.values,
                    ax=axes[0], palette=month_colors)
        axes[0].set_title('Average User Interactions by Month', fontsize=16)
        axes[0].set_xlabel('Month', fontsize=14)
        axes[0].set_ylabel('Average Number of Interactions', fontsize=14)
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True, linestyle='--', linewidth=0.7)

        # Seasonal Plot
        sns.barplot(x=average_interactions_per_season.index,
                    y=average_interactions_per_season.values,
                    ax=axes[1], palette='coolwarm')
        axes[1].set_title('Average User Interactions by Season', fontsize=16)
        axes[1].set_xlabel('Season', fontsize=14)
        axes[1].set_ylabel('Average Number of Interactions', fontsize=14)
        axes[1].tick_params(axis='x', rotation=0)
        axes[1].grid(True, linestyle='--', linewidth=0.7)

        plt.tight_layout()
        return fig

    def plot_seasonality_for_year(self, year):
        # Filter interactions for the selected year
        yearly_data = self.interactions_df[self.interactions_df['year'] == year]

        # Monthly interactions
        interactions_per_month = yearly_data['month'].value_counts().reindex(
            ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December'],
            fill_value=0
        )

        # Seasonal interactions
        interactions_per_season = yearly_data['season'].value_counts().reindex(
            ['Winter', 'Spring', 'Summer', 'Fall'], fill_value=0
        )

        # Define a unique color palette for each month
        month_colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A8', '#FFC300', '#33FFF9',
                        '#8E44AD', '#3498DB', '#2ECC71', '#E67E22', '#E74C3C', '#95A5A6']

        # Create subplots
        fig, axes = plt.subplots(2, 1, figsize=(10, 10))

        # Monthly Plot with unique colors for each month
        sns.barplot(x=interactions_per_month.index,
                    y=interactions_per_month.values, ax=axes[0], palette=month_colors)
        axes[0].set_title(f'User Interactions by Month for {year}', fontsize=16)
        axes[0].set_xlabel('Month', fontsize=14)
        axes[0].set_ylabel('Number of Interactions', fontsize=14)
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True, linestyle='--', linewidth=0.7)

        # Seasonal Plot
        sns.barplot(x=interactions_per_season.index,
                    y=interactions_per_season.values, ax=axes[1], palette='coolwarm')
        axes[1].set_title(f'User Interactions by Season for {year}', fontsize=16)
        axes[1].set_xlabel('Season', fontsize=14)
        axes[1].set_ylabel('Number of Interactions', fontsize=14)
        axes[1].tick_params(axis='x', rotation=0)
        axes[1].grid(True, linestyle='--', linewidth=0.7)

        plt.tight_layout()
        return fig
# TopRecipesAnalysis class to analyze and visualize the most popular recipes


class TopRecipesAnalysis:
    """
    A class to analyze and visualize the most popular recipes based on ratings and interactions data.

    Attributes:
        recipes_df (pd.DataFrame): DataFrame containing recipe data.
        interactions_df (pd.DataFrame): DataFrame containing interactions data.
    """

    def __init__(self, recipes_df, interactions_df):
        """
        Initializes the TopRecipesAnalysis class with recipes and interactions DataFrames.

        Args:
            recipes_df (pd.DataFrame): DataFrame containing recipe data.
            interactions_df (pd.DataFrame): DataFrame containing interactions data.
        """
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df

    def display_popular_recipes_and_visualizations(self):
        """
        Displays the most popular recipes based on various criteria and provides options to visualize them.
        Includes options to filter recipes by year range and display details for a selected recipe.
        """
        # Format 'submitted' column and rename 'id' to 'recipe_id'
        self.recipes_df = self._format_to_datetime(
            self.recipes_df, 'submitted')
        self.recipes_df = self._rename_column(
            self.recipes_df, 'id', 'recipe_id')

        # Merge recipes with interactions data
        merged_df = self._merge_with(
            self.recipes_df, self.interactions_df, 'recipe_id')

        # Convert ratings to numeric and filter positive ratings
        merged_df = self._format_to_numeric(merged_df, 'rating')
        filtered_df = self._filter_positive_ratings(merged_df, 'rating')

        # Get top recipes and their details
        top_recipes = self._get_top_n_recipes_by_ratings(
            filtered_df, 'recipe_id', 'rating', n=15)
        grouped_df = self._group_by_attribute_count(
            top_recipes, ['recipe_id', 'name', 'rating'])

        # Plot the results

        st.title("🍲 Top Recipes Analysis Dashboard")

        st.subheader(
            "Explore popular recipes, filter by year range, and view detailed stats!")
        if st.button("🔝 Display recipes with the most positive ratings over the years"):
            self._plot_top_recipes(grouped_df)

        if st.button("🗓️ Display recipes with positive ratings (2000-2010)"):
            self._plot_top_recipes_from_2000_to_2010(filtered_df)

        if st.button("🗓️ Display recipes with positive ratings (2010-2018)"):
            self._plot_top_recipes_from_2010_to_2018(filtered_df)

        # if st.button("Display selected recipes details"):
        self._display_selected_recipe_details(merged_df, grouped_df)

        # self._plot_top_recipes(grouped_df)
        # self._display_selected_recipe_details(merged_df, grouped_df)
        # self._plot_wordcloud(grouped_df, merged_df)

    def _format_to_datetime(self, df, column_name):
        """
        Converts a specified column in the DataFrame to datetime format.

        Args:
            df (pd.DataFrame): The DataFrame containing the column to be converted.
            column_name (str): The name of the column to convert.

        Returns:
            pd.DataFrame: The modified DataFrame with the column in datetime format.
        """
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
        return df

    def _rename_column(self, df, old_name, new_name):
        """
        Renames a column in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the column to rename.
            old_name (str): The current name of the column.
            new_name (str): The new name for the column.

        Returns:
            pd.DataFrame: The modified DataFrame with the renamed column.
        """
        df.rename(columns={old_name: new_name}, inplace=True)
        return df

    def _merge_with(self, df, other_df, on_attribute):
        """
        Merges two DataFrames on a specified attribute.

        Args:
            df (pd.DataFrame): The first DataFrame.
            other_df (pd.DataFrame): The second DataFrame to merge with.
            on_attribute (str): The column name on which to merge the DataFrames.

        Returns:
            pd.DataFrame: The merged DataFrame.
        """
        return pd.merge(df, other_df, on=on_attribute)

    def _format_to_numeric(self, df, column_name):
        """
        Converts a specified column in the DataFrame to a numeric format.

        Args:
            df (pd.DataFrame): The DataFrame containing the column to convert.
            column_name (str): The name of the column to convert.

        Returns:
            pd.DataFrame: The modified DataFrame with the column in numeric format.
        """
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
        return df

    def _filter_positive_ratings(self, df, rating_column, threshold=4):
        """
        Filters the DataFrame for rows with ratings greater than or equal to the threshold.

        Args:
            df (pd.DataFrame): The DataFrame to filter.
            rating_column (str): The name of the column containing ratings.
            threshold (int, optional): The rating threshold. Defaults to 4.

        Returns:
            pd.DataFrame: The filtered DataFrame with ratings above or equal to the threshold.
        """
        return df[df[rating_column] >= threshold]

    def _get_top_n_recipes_by_ratings(self, df, recipe_id_column, rating_column, n=15):
        """
        Retrieves the top N recipes based on the number of positive ratings.

        Args:
            df (pd.DataFrame): The DataFrame containing recipe ratings.
            recipe_id_column (str): The column name for recipe IDs.
            rating_column (str): The column name for ratings.
            n (int, optional): The number of top recipes to retrieve. Defaults to 15.

        Returns:
            pd.DataFrame: The DataFrame containing the top N recipes by rating count.
        """
        # Filter positive ratings (assuming positive ratings are > 0 or some threshold)
        positive_df = df[df[rating_column] > 0]

        # Count positive ratings for each recipe
        top_recipes = positive_df.groupby(
            recipe_id_column).size().reset_index(name='positive_ratings')

        # Sort recipes by the count of positive ratings in descending order and take the top N
        top_recipes_sorted = top_recipes.sort_values(
            by='positive_ratings', ascending=False).head(n)

        # Return the DataFrame with only the top N recipes
        return df[df[recipe_id_column].isin(top_recipes_sorted[recipe_id_column])]

    def _group_by_attribute_count(self, df, on_attributes):
        return df.groupby(on_attributes).size().reset_index(name='count')

    def display_recipes(self, df, df_time=None):
        """
        Displays a bar plot of recipe ratings using seaborn.

        Args:
            df (pd.DataFrame): The DataFrame containing recipes and rating counts.
        """
        # Create a unique color palette for each recipe_id
        unique_recipes = df['recipe_id'].unique()
        palette = sns.color_palette("husl", len(unique_recipes))

        # Create barplot with associated colors for each recipe
        fig, ax = plt.subplots(figsize=(20, 15))
        sns.barplot(x='recipe_id', y='count', hue='rating',
                    data=df, palette=palette, dodge=True, ax=ax)

        # Add labels above bars
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='baseline', fontsize=12, color='black', xytext=(0, 5),
                        textcoords='offset points')

        ax.set_title('🍽️ Number of Ratings per Recipe', fontsize=18)
        ax.set_xlabel('Recipe ID', fontsize=14)
        ax.set_ylabel('Number of Ratings', fontsize=14)
        ax.legend(title='Rating', loc='upper right')
        st.pyplot(fig)
        grouped_df = df.copy()
        
        if df_time is not None:
            grouped_df = grouped_df.merge(
                df_time[['recipe_id', 'minutes']],
                on='recipe_id',
                how='left'
            )
            grouped_df['minutes'] = pd.to_numeric(grouped_df['minutes'], errors='coerce')

            grouped_df = grouped_df.drop_duplicates(subset=['recipe_id'])
            #st.write((grouped_df))
            
            st.subheader("⏱️ Distribution of Preparation Times for Top Recipes")
            if 'minutes' in grouped_df.columns:
                prep_time = grouped_df['minutes']
                
                # Filtrer les temps aberrants (optionnel)
                prep_time = prep_time[prep_time.between(10, 250)]
                
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.histplot(prep_time, bins=20, kde=True, color='skyblue', ax=ax)
                mean_prep_time = prep_time.mean()
                ax.axvline(mean_prep_time, color='red', linestyle='--', label=f'Mean: {mean_prep_time:.2f} min')
                
                # Ajouter les détails visuels
                ax.set_title('⏱️ Distribution of Preparation Times for Top Recipes', fontsize=16)
                ax.set_xlabel('Preparation Time (minutes)', fontsize=14)
                ax.set_ylabel('Frequency', fontsize=14)
                plt.xticks(fontsize=12)
                plt.yticks(fontsize=12)
                ax.legend(fontsize=12)
                st.pyplot(fig)
            else:
                st.warning("The 'minutes' column is missing in the dataset. Cannot plot preparation time distribution.")
            

    def _plot_top_recipes(self, grouped_df):
        """
        Plots the top recipes based on ratings over the years.

        Args:
            grouped_df (pd.DataFrame): DataFrame with top recipes and ratings.
        """
        st.title("🌟 Top 15 Most Popular Recipes by Ratings and Comments")
        sns.set(style="whitegrid")
        self.display_recipes(grouped_df)

    def _plot_top_recipes_from_2000_to_2010(self, df):
        """
        Plots top recipes based on ratings between the years 2000 and 2010.

        Args:
            df (pd.DataFrame): The DataFrame containing recipe data.
        """
        st.title("📆 Top Recipes from 2000 to 2010 by Ratings")
        sns.set(style="whitegrid")
        # verif pour eviter les erreurs
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        filtered_df = df[(df['date'].dt.year >= 2000) &
                         (df['date'].dt.year <= 2010)]
        # Get top recipes and their details
        top_recipes = self._get_top_n_recipes_by_ratings(
            filtered_df, 'recipe_id', 'rating', n=15)
        grouped_df = self._group_by_attribute_count(
            top_recipes, ['recipe_id', 'name', 'rating'])
        self.display_recipes(grouped_df, df)
        # Affichage de la distribution des temps de préparation
        # Joindre grouped_df avec df pour récupérer les temps de préparation

    def _plot_top_recipes_from_2010_to_2018(self, df):
        """
        Plots top recipes based on ratings between the years 2010 and 2018.

        Args:
            df (pd.DataFrame): The DataFrame containing recipe data.
        """
        st.title("📆 Top Recipes from 2010 to 2018 by Ratings")
        sns.set(style="whitegrid")
        # verif pour eviter les erreurs
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        filtered_df = df[(df['date'].dt.year >= 2010) &
                         (df['date'].dt.year <= 2018)]
        # Get top recipes and their details
        top_recipes = self._get_top_n_recipes_by_ratings(
            filtered_df, 'recipe_id', 'rating', n=15)
        grouped_df = self._group_by_attribute_count(
            top_recipes, ['recipe_id', 'name', 'rating'])
        self.display_recipes(grouped_df, df)

    def _display_selected_recipe_details(self, merged_df, grouped_df):
        """
        Displays detailed information and visualizations for a selected recipe.

        Args:
            merged_df (pd.DataFrame): DataFrame containing merged recipe and interaction data.
            grouped_df (pd.DataFrame): DataFrame containing grouped recipe data.
        """
        recipe_id = st.selectbox("🔍 Select a recipe for details:",
                                 grouped_df['recipe_id'].unique(), key="recipe_select")
        selected_recipe = merged_df[merged_df['recipe_id'] == recipe_id]

        # Temps de préparation et nombre d'étapes
        st.write(
            f"### Deatils for the recipe : {selected_recipe['name'].iloc[0]}")
        
        st.write(
            f"**⏱️ Preparation Time:** {selected_recipe['minutes'].iloc[0]} minutes")
        st.write(f"**🔢 Number of Steps:** {selected_recipe['n_steps'].iloc[0]}")
        # Informations nutritionnelles
        nutrition_info = selected_recipe['nutrition'].iloc[0].strip("[]").split(",")
        st.write("### 🥗 Nutritional Information (per portion):")
        st.write(f" - **Calories:** {nutrition_info[0]}")
        st.write(f" - **Sugar:** {nutrition_info[1]} PVD")
        st.write(f" - **Sodium:** {nutrition_info[2]} PVD")
        st.write(f" - **Protein:** {nutrition_info[3]} PVD")
        st.write(f" - **Saturated Fat:** {nutrition_info[4]} PVD")
        st.write(f" - **Carbohydrates:** {nutrition_info[5]} PVD")

        # Tags et Ingrédients
        st.write("### 🏷️ Tags:")
        st.write(", ".join(selected_recipe['tags'].iloc[0].strip("[]").split(",")))
        st.write("### 🥄 Ingredients:")
        st.write(
            ", ".join(selected_recipe['ingredients'].iloc[0].strip("[]").split(",")))

        # Popularité et note moyenne
        total_ratings = selected_recipe['rating'].count()
        average_rating = selected_recipe['rating'].mean()
        st.write(f"**🌟 Total Ratings:** {total_ratings}")
        st.write(f"**⭐ Average Rating:** {average_rating:.1f}/5")

        # Format 'date' and extract 'year' for rating evolution
        selected_recipe = self._format_to_datetime(selected_recipe, 'date')
        selected_recipe['year'] = selected_recipe['date'].dt.year

        # Group data by 'year' and 'rating'
        grouped_by_date = selected_recipe.groupby(
            ['year', 'rating']).size().reset_index(name='count')
        unique_years = sorted(grouped_by_date['year'].unique())

        # Plot the rating evolution over time
        st.write("### 📈 Ratings Evolution Over Years")
        fig, ax = plt.subplots(figsize=(20, 15))
        sns.lineplot(x='year', y='count', hue='rating',
                     data=grouped_by_date, palette='coolwarm', ax=ax)

        ax.set_title(f"Evolution of Ratings for Recipe id {recipe_id} and name {selected_recipe['name'].iloc[0]} by Year and Rating Class", fontsize=18)
        ax.set_xlabel('Year', fontsize=14)
        ax.set_ylabel('Number of Ratings', fontsize=14)
        ax.set_xticks(unique_years)
        ax.set_xticklabels(unique_years, rotation=45)
        st.pyplot(fig)


class CommonWordsAnalysis:

    def __init__(self, recipes_df, interactions_df, cfg):
        self.cfg = cfg
        self.recipes = recipes_df
        self.interactions = interactions_df
        self.min_rating = cfg.min_rating
        self.min_num_ratings = cfg.min_num_ratings
        self.num_top_recipes = cfg.num_top_recipes

    # def compute_interactions_df(self, recipe, interactions):
    #    # recipe_histogram
    #    recipe["submitted"] = recipe["submitted"].apply(lambda x: int(x[0:4]))
    #    year_list = sorted(recipe["submitted"].unique())
    #    num_recipes_list = [len(recipe[recipe["submitted"] == year]) for year in year_list]
#
    #    # Interactions histogram
    #    interactions["date"] = interactions["date"].apply(lambda x: int(x[0:4]))
    #    num_interactions_list = [len(interactions[interactions["date"] == year]) for year in year_list]
#
    #    # Combining the histograms
    #    df = pd.DataFrame({"num_interactions": num_interactions_list,
    #                       "num_recipes": num_recipes_list},
    #                      index = year_list)
    #    return df

    def process_name(self, name: str):
        name_array = [word for word in name.split(' ') if word != '']
        return [word for word in name_array if word not in stopwords.words("english")]

    def compute_average_rating(self, recipe_id: int):
        ratings = self.interactions[self.interactions["recipe_id"]
                                    == recipe_id]["rating"].to_numpy()
        if len(ratings) == 0:
            return -1, 0
        else:
            return np.mean(ratings), len(ratings)

    def format_recipe(self, year: int):
        self.recipes["submitted"] = self.recipes["submitted"].apply(
            lambda x: int(x[0:4]))
        self.recipes = self.recipes[self.recipes["submitted"] == year]
        ratings = [self.compute_average_rating(
            recipe_id)[0] for recipe_id in self.recipes["id"].to_numpy()]
        number_of_ratings = [self.compute_average_rating(
            recipe_id)[1] for recipe_id in self.recipes["id"].to_numpy()]
        self.recipes["average_rating"] = ratings
        self.recipes["number_of_ratings"] = number_of_ratings
        self.recipes = self.recipes[self.recipes["average_rating"] != -1]

    def compute_top_keywords(self):
        top_recipe = self.recipes[(self.recipes["average_rating"] > self.min_rating) & (
            self.recipes["number_of_ratings"] > self.min_num_ratings)]
        top_recipe["name"] = top_recipe["name"].apply(self.process_name)
        top_keywords_list = list(
            itertools.chain.from_iterable(top_recipe["name"].to_numpy()))
        top_keywords_to_count_dict = {}
        for keyword in top_keywords_list:
            if keyword in top_keywords_to_count_dict.keys():
                top_keywords_to_count_dict[keyword] += 1
            else:
                top_keywords_to_count_dict[keyword] = 1
        sorted_top_keywords_to_count_dict = sorted(
            top_keywords_to_count_dict.items(), key=lambda x: x[1], reverse=True)
        N = sum(
            [t[1] for t in sorted_top_keywords_to_count_dict[:self.num_top_recipes]])
        text_array = [(t[0], t[1] / N)
                      for t in sorted_top_keywords_to_count_dict[:self.num_top_recipes]]
        cst = 1 / text_array[-1][1]
        text_array = [(t[0], math.ceil(cst * t[1])) if math.ceil(cst *
                                                                 t[1]) <= 10 else (t[0], 10) for t in text_array]
        text = " ".join([" ".join([t[0] for _ in range(t[1])])
                        for t in text_array])
        wc = WordCloud(max_font_size=50, max_words=20,
                       background_color="white", relative_scaling=1).generate(text)
        return wc


def prepare_directories(cfg: Config):
    cfg.logging_dir.mkdir(parents=True, exist_ok=True)
    cfg.run_cfg_dir.mkdir(parents=True, exist_ok=True)
