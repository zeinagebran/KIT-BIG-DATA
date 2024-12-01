Using KIT-BIG-DATA
==================

This document provides examples of how to use the KIT-BIG-DATA project.

Prerequisites
-------------

Make sure you have installed all necessary dependencies by following the instructions in `installation.rst`.

Usage Examples
--------------

**1. Importing Modules**

Here’s how to import the main project modules into your Python code:

.. code-block:: python

    from optimRecipes.functions import DataExtractor, WeeklyAnalysis, SeasonalityAnalysis
    from optimRecipes.analysis_top_15 import TopRecipesAnalysis

**2. Loading Data**

Use the `DataExtractor` class to load data from CSV files:

.. code-block:: python

    data_extractor = DataExtractor(zip_file_path="C:\\Users\\User\\Desktop\\MASTERE SPECIALISE IA\\KIT BIG DATA BGDIA700\\RESOURCES PROJET\\data.zip")
    interactions_df, recipes_df = data_extractor.extract_and_load_data()

**3. Weekly Interaction Analysis**

The `WeeklyAnalysis` class allows you to visualize the average number of interactions per day of the week:

.. code-block:: python

    weekly_analysis = WeeklyAnalysis(interactions_df=interactions_df)
    fig = weekly_analysis.plot_mean_interactions()
    fig.show()  # To display the graph

**4. Seasonal Interaction Analysis**

The `SeasonalityAnalysis` class allows you to view interactions by season and month:

.. code-block:: python

    seasonality_analysis = SeasonalityAnalysis(interactions_df=interactions_df)
    fig = seasonality_analysis.plot_seasonality()
    fig.show()  # To display the graph

**5. Analysis of the Most Popular Recipes**

Use the `TopRecipesAnalysis` class to display the most popular recipes based on user ratings:

.. code-block:: python

    top_recipes_analysis = TopRecipesAnalysis(recipes_df=recipes_df, interactions_df=interactions_df)
    top_recipes_analysis.display_popular_recipes_and_visualizations()

Options and Parameters
----------------------

- **`zip_file_path`**: Path to the ZIP file containing the CSV data.
- **`interactions_df`**: DataFrame of user interactions with recipes.
- **`recipes_df`**: DataFrame of available recipes.
- **`TopRecipesAnalysis.display_popular_recipes_and_visualizations`**: Displays a visual interface with Streamlit to interact with the recipe data.

Using with Streamlit
--------------------

First modify config file to specify ZIP file path.

To use the project with Streamlit, run the application with the following command in the terminal:

.. code-block:: bash

    set PYTHONPATH=src
    streamlit run src/optimRecipes/main.py

This will open a user interface in your browser to interact with the recipe data and generated visualizations.
