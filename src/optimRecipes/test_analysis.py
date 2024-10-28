import pytest
import pandas as pd
import matplotlib.pyplot as plt
from functions import WeeklyAnalysis  # Adjust the import as necessary


@pytest.fixture
def sample_data():
    """Create sample interaction data for testing with entries for all days."""
    data = {
        'date': [
            '2024-01-01',  # Monday
            '2024-01-02',  # Tuesday
            '2024-01-03',  # Wednesday
            '2024-01-04',  # Thursday
            '2024-01-05',  # Friday
            '2024-01-06',  # Saturday
            '2024-01-07',  # Sunday
            '2024-01-01',  # Monday (duplicate)
            '2024-01-02',  # Tuesday (duplicate)
            '2024-01-03'   # Wednesday (duplicate)
        ]
    }
    return pd.DataFrame(data)


def test_weekly_analysis(sample_data):
    """Test the WeeklyAnalysis class methods."""
    analysis = WeeklyAnalysis(sample_data)

    # Test plot_mean_interactions method
    fig = analysis.plot_mean_interactions()
    assert isinstance(fig, plt.Figure)  # Check if a figure is returned

    # Convert 'date' to datetime and extract 'day_of_week'
    sample_data['date'] = pd.to_datetime(sample_data['date'])
    sample_data['day_of_week'] = sample_data['date'].dt.day_name()

    # Calculate total counts for each day of the week
    counts = sample_data['day_of_week'].value_counts()

    # Calculate the mean interactions based on the total counts and the number of unique years
    expected_means = counts / sample_data['date'].dt.year.nunique()

    # Ensure expected means are ordered correctly
    expected_means = expected_means.reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], fill_value=0)

    # Get actual means from the analysis class
    actual_means = analysis.interactions_df.groupby(['year', 'day_of_week']).size(
    ).unstack(fill_value=0).mean().reindex(expected_means.index)

    # Print actual means for debugging
    print("Actual Means:\n", actual_means)

    # Remove the index name for comparison
    actual_means.index.name = None
    expected_means.name = None  # Remove name from expected means for comparison

    # Compare the series
    pd.testing.assert_series_equal(actual_means.fillna(
        0), expected_means.astype(float), check_exact=False, check_dtype=False)


if __name__ == "__main__":
    pytest.main()
