import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
interactions_df = pd.read_csv("./extracted_data/RAW_interactions.csv")

# Step 1: Data Overview
# Display the first few rows to understand the structure of the data
print("Preview of the data:")
print(interactions_df.head())

# Display information about the dataset
print("\nDataframe Info:")
print(interactions_df.info())

# Get a statistical summary of the dataset
print("\nStatistical Summary:")
print(interactions_df.describe(include='all'))

# Step 2: Data Cleaning
# Check for missing values
print("\nMissing Values in each column:")
print(interactions_df.isnull().sum())

# Handle missing values in the 'date' column if they exist
# For demonstration, let's drop rows with missing 'date' values
interactions_df.dropna(subset=['date'], inplace=True)
print("\nMissing values in 'date' column after dropping rows with missing dates:")
print(interactions_df['date'].isnull().sum())

# Check for duplicate rows
print(f"\nNumber of duplicate rows: {interactions_df.duplicated().sum()}")
# Drop duplicates if necessary
interactions_df.drop_duplicates(inplace=True)

# Step 3: Data Type Conversion
# Convert 'date' column to datetime
interactions_df['date'] = pd.to_datetime(
    interactions_df['date'], errors='coerce')

# Extract additional features
interactions_df['day_of_week'] = interactions_df['date'].dt.day_name()
interactions_df['year'] = interactions_df['date'].dt.year

# Step 4: Exploratory Analysis
# Count interactions by day of the week
day_counts = interactions_df['day_of_week'].value_counts()
# Reorder the days for a better visualization
ordered_days = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = day_counts.reindex(ordered_days, fill_value=0)

print("\nNumber of interactions per day of the week:")
print(day_counts)

# Plotting the distribution of interactions per day
plt.figure(figsize=(8, 6))
sns.barplot(x=day_counts.index, y=day_counts.values, palette='Blues')
plt.title('Number of Interactions by Day of the Week', fontsize=16)
plt.xlabel('Day of the Week', fontsize=14)
plt.ylabel('Number of Interactions', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.tight_layout()
plt.show()

# Calculate the mean interactions per day across all years for normalization
interactions_per_day_yearly = interactions_df.groupby(
    ['year', 'day_of_week']).size().unstack(fill_value=0)
mean_interactions_per_day = interactions_per_day_yearly.mean()
mean_interactions_per_day = mean_interactions_per_day.reindex(ordered_days)

print("\nMean interactions per day of the week across all years:")
print(mean_interactions_per_day)

# Plotting the mean interactions per day
plt.figure(figsize=(8, 6))
mean_interactions_per_day.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Average User Interactions by Day of the Week', fontsize=16)
plt.xlabel('Day of the Week', fontsize=14)
plt.ylabel('Average Number of Interactions', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.tight_layout()
plt.show()
duplicate_rows = interactions_df.duplicated()
num_duplicates = duplicate_rows.sum()

print(f"Number of duplicate rows: {num_duplicates}")

# If there are duplicates, display a few examples
if num_duplicates > 0:
    print("Examples of duplicate rows:")
    print(interactions_df[duplicate_rows].head())

# Optional: Check for duplicates considering only user_id, recipe_id, and date
# This can be helpful if you want to ensure each user interaction with a specific recipe on a particular date is unique
duplicate_interactions = interactions_df.duplicated(
    subset=['user_id', 'recipe_id', 'date'])
num_duplicate_interactions = duplicate_interactions.sum()

print(f"Number of duplicate interactions (by user_id, recipe_id, and date): {num_duplicate_interactions}")

if num_duplicate_interactions > 0:
    print("Examples of duplicate interactions:")
    print(interactions_df[duplicate_interactions].head())
