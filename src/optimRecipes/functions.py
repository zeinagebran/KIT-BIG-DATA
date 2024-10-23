import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import streamlit as st
from wordcloud import WordCloud

# DataExtractor class to handle data extraction and loading


class DataExtractor:
    def __init__(self, zip_file_path):
        self.zip_file_path = zip_file_path
        self.interactions_df = None
        self.recipes_df = None

    @st.cache_data
    # Use _self to avoid Streamlit's hashing error
    def extract_and_load_data(_self):
        try:
            print(f"Loading data from: {_self.zip_file_path}")
            with zipfile.ZipFile(_self.zip_file_path, 'r') as zip_ref:
                zip_ref.extractall("extracted_data")

            _self.interactions_df = pd.read_csv(
                "extracted_data/RAW_interactions.csv")
            _self.recipes_df = pd.read_csv("extracted_data/RAW_recipes.csv")

            # Convert 'date' column in interactions to datetime
            _self.interactions_df['date'] = pd.to_datetime(
                _self.interactions_df['date'], errors='coerce', infer_datetime_format=True
            )
            print(f"Number of unparsed dates: {
                  _self.interactions_df['date'].isna().sum()}")
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
    def __init__(self, interactions_df):
        self.interactions_df = interactions_df

    def plot_mean_interactions(self):
        self.interactions_df['date'] = pd.to_datetime(
            self.interactions_df['date'], errors='coerce')
        self.interactions_df['day_of_week'] = self.interactions_df['date'].dt.day_name(
        )

        # Calculate interactions per day of the week
        interactions_per_day = self.interactions_df.groupby(
            'day_of_week').size()

        # Reorder the days of the week for better readability
        interactions_per_day = interactions_per_day.reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday', 'Sunday']
        )

        fig, ax = plt.subplots(figsize=(8, 6))
        interactions_per_day.plot(
            kind='bar', ax=ax, color='skyblue', edgecolor='black')
        ax.set_title(
            'Average User Interactions by Day of the Week', fontsize=16)
        ax.set_xlabel('Day of the Week', fontsize=14)
        ax.set_ylabel('Average Number of Interactions', fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        ax.grid(True, linestyle='--', linewidth=0.7)
        return fig


# SeasonalityAnalysis class for seasonal interaction analysis
class SeasonalityAnalysis:
    def __init__(self, interactions_df):
        self.interactions_df = interactions_df

    def plot_seasonality(self):
        self.interactions_df['date'] = pd.to_datetime(
            self.interactions_df['date'], errors='coerce')
        self.interactions_df['year'] = self.interactions_df['date'].dt.year
        self.interactions_df['month'] = self.interactions_df['date'].dt.month_name(
        )
        self.interactions_df['season'] = self.interactions_df['date'].dt.month % 12 // 3 + 1
        self.interactions_df['season'] = self.interactions_df['season'].map(
            {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
        )

        interactions_per_month = self.interactions_df.groupby('month').size()
        ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
        interactions_per_month = interactions_per_month.reindex(ordered_months)

        interactions_per_season = self.interactions_df.groupby('season').size()
        ordered_seasons = ['Winter', 'Spring', 'Summer', 'Fall']
        interactions_per_season = interactions_per_season.reindex(
            ordered_seasons)

        fig, axes = plt.subplots(2, 1, figsize=(10, 10))
        sns.barplot(x=interactions_per_month.index,
                    y=interactions_per_month.values, ax=axes[0], palette='Blues')
        axes[0].set_title('Average User Interactions by Month', fontsize=16)
        axes[0].set_xlabel('Month', fontsize=14)
        axes[0].set_ylabel('Average Number of Interactions', fontsize=14)
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True, linestyle='--', linewidth=0.7)

        sns.barplot(x=interactions_per_season.index,
                    y=interactions_per_season.values, ax=axes[1], palette='coolwarm')
        axes[1].set_title('Average User Interactions by Season', fontsize=16)
        axes[1].set_xlabel('Season', fontsize=14)
        axes[1].set_ylabel('Average Number of Interactions', fontsize=14)
        axes[1].tick_params(axis='x', rotation=0)
        axes[1].grid(True, linestyle='--', linewidth=0.7)

        plt.tight_layout()
        return fig


# TopRecipesAnalysis class to analyze and visualize the most popular recipes
class TopRecipesAnalysis:
    def __init__(self, recipes_df, interactions_df):
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df

    def display_popular_recipes_and_visualizations(self):
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
        self._plot_top_recipes(grouped_df)
        self._display_selected_recipe_details(merged_df, grouped_df)
        self._plot_wordcloud(grouped_df, merged_df)

    def _format_to_datetime(self, df, column_name):
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
        return df

    def _rename_column(self, df, old_name, new_name):
        df.rename(columns={old_name: new_name}, inplace=True)
        return df

    def _merge_with(self, df, other_df, on_attribute):
        return pd.merge(df, other_df, on=on_attribute)

    def _format_to_numeric(self, df, column_name):
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
        return df

    def _filter_positive_ratings(self, df, rating_column, threshold=4):
        return df[df[rating_column] >= threshold]

    def _get_top_n_recipes_by_ratings(self, df, recipe_id_column, rating_column, n=15):
        top_recipes = df.groupby(recipe_id_column).size(
        ).reset_index(name='positive_ratings')
        top_recipes_sorted = top_recipes.sort_values(
            by='positive_ratings', ascending=False).head(n)
        return df[df[recipe_id_column].isin(top_recipes_sorted[recipe_id_column])]

    def _group_by_attribute_count(self, df, on_attributes):
        return df.groupby(on_attributes).size().reset_index(name='count')

    def _plot_top_recipes(self, grouped_df):
        st.title("Top 50 Most Popular Recipes Based on Ratings and Comments")
        sns.set(style="whitegrid")

        # Create a unique color palette for each recipe_id
        unique_recipes = grouped_df['recipe_id'].unique()
        palette = sns.color_palette("husl", len(unique_recipes))

        # Create barplot with associated colors for each recipe
        fig, ax = plt.subplots(figsize=(20, 15))
        sns.barplot(x='recipe_id', y='count', hue='rating',
                    data=grouped_df, palette=palette, dodge=True, ax=ax)

        # Add labels above bars
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='baseline', fontsize=12, color='black', xytext=(0, 5),
                        textcoords='offset points')

        ax.set_title('Number of Ratings per Recipe', fontsize=18)
        ax.set_xlabel('Recipe ID', fontsize=14)
        ax.set_ylabel('Number of Ratings', fontsize=14)
        ax.legend(title='Rating', loc='upper right')
        st.pyplot(fig)

    def _display_selected_recipe_details(self, merged_df, grouped_df):
        recipe_id = st.selectbox(
            "View recipe details:", grouped_df['recipe_id'].unique())
        selected_recipe = merged_df[merged_df['recipe_id'] == recipe_id]
        st.write(selected_recipe.head(10))

        # Format 'date' and extract 'year' for rating evolution
        selected_recipe = self._format_to_datetime(selected_recipe, 'date')
        selected_recipe['year'] = selected_recipe['date'].dt.year

        # Group data by 'year' and 'rating'
        grouped_by_date = selected_recipe.groupby(
            ['year', 'rating']).size().reset_index(name='count')
        unique_years = sorted(grouped_by_date['year'].unique())

        # Plot the rating evolution over time
        fig, ax = plt.subplots(figsize=(20, 15))
        sns.lineplot(x='year', y='count', hue='rating',
                     data=grouped_by_date, palette='coolwarm', ax=ax)

        ax.set_title(f"Evolution of Ratings for Recipe {
                     recipe_id} by Year and Rating Class", fontsize=18)
        ax.set_xlabel('Year', fontsize=14)
        ax.set_ylabel('Number of Ratings', fontsize=14)
        ax.set_xticks(unique_years)
        ax.set_xticklabels(unique_years, rotation=45)
        st.pyplot(fig)

        detailed_df = self._group_by_attribute_count(
            selected_recipe, ['recipe_id', 'date', 'rating'])
        st.write(detailed_df.head())

    def _plot_wordcloud(self, grouped_df, merged_df):
        unique_recipes = merged_df.drop_duplicates(subset=['recipe_id'])
        tags_text = ' '.join(unique_recipes[unique_recipes['recipe_id'].isin(
            grouped_df['recipe_id'])]['ingredients'].explode().dropna().unique())

        # Generate word cloud
        wordcloud = WordCloud(
            width=800, height=400, background_color='white', colormap='plasma').generate(tags_text)
        fig_wordcloud, ax_wordcloud = plt.subplots(figsize=(20, 15))
        ax_wordcloud.imshow(wordcloud, interpolation='bilinear')
        ax_wordcloud.axis('off')
        ax_wordcloud.set_title(
            'Word Cloud of Tags for Popular Recipes', fontsize=16)
        st.pyplot(fig_wordcloud)
