import pytest
import matplotlib.pyplot as plt
import pandas as pd
from optimRecipes.functions import WeeklyAnalysis


@pytest.fixture
def sample_interactions():
    data = {
        'date': ['2024-01-01', '2024-02-15', '2024-03-15', '2024-07-01', '2024-10-15'],
        'user_id': [1, 2, 3, 4, 5]
    }
    return pd.DataFrame(data)


def test_weekly_analysis_initialization(sample_interactions):
    weekly_analysis = WeeklyAnalysis(sample_interactions)
    assert 'year' in weekly_analysis.interactions_df.columns, "Year column should be added."
    assert 'day_of_week' in weekly_analysis.interactions_df.columns, "Day of the week column should be added."


def test_weekly_plot_mean_interactions(sample_interactions):
    weekly_analysis = WeeklyAnalysis(sample_interactions)
    fig = weekly_analysis.plot_mean_interactions()
    assert isinstance(
        fig, plt.Figure), "plot_mean_interactions should return a matplotlib Figure."
    plt.close(fig)


def test_weekly_plot_interactions_for_year(sample_interactions):
    weekly_analysis = WeeklyAnalysis(sample_interactions)
    fig = weekly_analysis.plot_interactions_for_year(2024)
    assert isinstance(
        fig, plt.Figure), "plot_interactions_for_year should return a matplotlib Figure."
    plt.close(fig)
