import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the data if not already done
interactions_df = pd.read_csv("extracted_data/RAW_interactions.csv")

# Step 1: Data Overview
# Display the first 5 rows to get an overview of the data
print("Preview of the data:")
print(interactions_df.head())

# Display information about the columns and their data types
print("\nDataframe Info:")
print(interactions_df.info())

# Step 2: Data Cleaning
# Statistical summary of the dataset
print("\nStatistical Summary:")
print(interactions_df.describe(include='all'))

# Check for missing values in each column
print("\nMissing Values in each column:")
print(interactions_df.isnull().sum())

# Handle missing values in the 'date' column by dropping rows with missing dates
interactions_df.dropna(subset=['date'], inplace=True)
print("\nMissing values in 'date' column after dropping rows with missing dates:")
print(interactions_df['date'].isnull().sum())

# Check for duplicate rows
num_duplicates = interactions_df.duplicated().sum()
print(f"\nNumber of duplicate rows: {num_duplicates}")

# Drop duplicates if necessary
if num_duplicates > 0:
    interactions_df.drop_duplicates(inplace=True)
    print(f"Duplicates removed. Number of remaining rows: {len(interactions_df)}")

# Step 3: Data Type Conversion
# Convert 'date' column to datetime format
interactions_df['date'] = pd.to_datetime(
    interactions_df['date'], errors='coerce')

# Extract the month and year from the 'date'
interactions_df['month'] = interactions_df['date'].dt.month_name()
interactions_df['year'] = interactions_df['date'].dt.year

# Define seasons based on the months
interactions_df['season'] = interactions_df['date'].dt.month % 12 // 3 + 1
interactions_df['season'] = interactions_df['season'].map({
    1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'
})

# Step 4: Exploratory Analysis
# Count interactions per month
interactions_per_month = interactions_df['month'].value_counts()
# Reorganize months for chronological display
ordered_months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
interactions_per_month = interactions_per_month.reindex(
    ordered_months, fill_value=0)

print("\nNumber of interactions per month:")
print(interactions_per_month)

# Count interactions per season
interactions_per_season = interactions_df['season'].value_counts()
# Reorganize seasons for better display
ordered_seasons = ['Winter', 'Spring', 'Summer', 'Fall']
interactions_per_season = interactions_per_season.reindex(
    ordered_seasons, fill_value=0)

print("\nNumber of interactions per season:")
print(interactions_per_season)

# Step 5: Visualization
# Plot for interactions per month
plt.figure(figsize=(10, 6))
sns.barplot(x=interactions_per_month.index,
            y=interactions_per_month.values, palette='Blues')
plt.title('User Interactions by Month', fontsize=16)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Number of Interactions', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.tight_layout()
plt.show()

# Plot for interactions per season
plt.figure(figsize=(8, 5))
sns.barplot(x=interactions_per_season.index,
            y=interactions_per_season.values, palette='coolwarm')
plt.title('User Interactions by Season', fontsize=16)
plt.xlabel('Season', fontsize=14)
plt.ylabel('Number of Interactions', fontsize=14)
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.tight_layout()
plt.show()

# Step 6: Analysis of Mean Interactions per Month and Season
# Calculate interactions per month for each year and then the mean interactions per month
interactions_per_month_yearly = interactions_df.groupby(
    ['year', 'month']).size().unstack(fill_value=0)
mean_interactions_per_month = interactions_per_month_yearly.mean()
mean_interactions_per_month = mean_interactions_per_month.reindex(
    ordered_months)

print("\nMean interactions per month across all years:")
print(mean_interactions_per_month)

# Plotting the mean interactions per month
plt.figure(figsize=(10, 6))
sns.barplot(x=mean_interactions_per_month.index,
            y=mean_interactions_per_month.values, palette='Blues')
plt.title('Average User Interactions by Month', fontsize=16)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Average Number of Interactions', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.tight_layout()
plt.show()

# Calculate interactions per season for each year and then the mean interactions per season
interactions_per_season_yearly = interactions_df.groupby(
    ['year', 'season']).size().unstack(fill_value=0)
mean_interactions_per_season = interactions_per_season_yearly.mean()
mean_interactions_per_season = mean_interactions_per_season.reindex(
    ordered_seasons)

print("\nMean interactions per season across all years:")
print(mean_interactions_per_season)

# Plotting the mean interactions per season
plt.figure(figsize=(8, 5))
sns.barplot(x=mean_interactions_per_season.index,
            y=mean_interactions_per_season.values, palette='coolwarm')
plt.title('Average User Interactions by Season', fontsize=16)
plt.xlabel('Season', fontsize=14)
plt.ylabel('Average Number of Interactions', fontsize=14)
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.tight_layout()
plt.show()
# Step 7: Final Check for Duplicates
# Check for duplicate rows in the cleaned and processed data
num_duplicates_after = interactions_df.duplicated().sum()
print(f"\nNumber of duplicate rows after cleaning: {num_duplicates_after}")

# If duplicates are found, display a few examples
if num_duplicates_after > 0:
    print("Examples of duplicate rows after cleaning:")
    print(interactions_df[interactions_df.duplicated()].head())

# Optional: Check for duplicates considering only user_id, recipe_id, and date
# This ensures that each user interaction with a specific recipe on a particular date is unique
duplicate_interactions_after = interactions_df.duplicated(
    subset=['user_id', 'recipe_id', 'date'])
num_duplicate_interactions_after = duplicate_interactions_after.sum()

print(f"Number of duplicate interactions (by user_id, recipe_id, and date) after cleaning: {num_duplicate_interactions_after}")

if num_duplicate_interactions_after > 0:
    print("Examples of duplicate interactions after cleaning:")
    print(interactions_df[duplicate_interactions_after].head())
