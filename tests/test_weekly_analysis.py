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


def test_plot_mean_interactions_no_data():
    weekly_analysis = WeeklyAnalysis(pd.DataFrame(columns=['date', 'user_id']))
    fig = weekly_analysis.plot_mean_interactions()
    assert isinstance(
        fig, plt.Figure), "plot_mean_interactions should return a matplotlib Figure even with no data."
    plt.close(fig)


def test_plot_interactions_for_year_no_data():
    weekly_analysis = WeeklyAnalysis(pd.DataFrame(columns=['date', 'user_id']))
    fig = weekly_analysis.plot_interactions_for_year(2024)
    assert isinstance(
        fig, plt.Figure), "plot_interactions_for_year should return a matplotlib Figure even with no data."
    plt.close(fig)


def test_weekly_analysis_single_date(sample_interactions):
    # Test with a single date in interactions data
    sample_interactions_single_date = pd.DataFrame(
        {'date': ['2024-01-01'], 'user_id': [1]})
    weekly_analysis = WeeklyAnalysis(sample_interactions_single_date)
    fig = weekly_analysis.plot_mean_interactions()
    assert isinstance(
        fig, plt.Figure), "Expected a matplotlib Figure with a single date data"
    plt.close(fig)
