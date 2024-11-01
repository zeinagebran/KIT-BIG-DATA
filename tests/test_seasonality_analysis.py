import pytest
import matplotlib.pyplot as plt
import pandas as pd
from optimRecipes.functions import SeasonalityAnalysis


@pytest.fixture
def sample_interactions():
    data = {
        'date': ['2024-01-01', '2024-02-15', '2024-03-15', '2024-07-01', '2024-10-15'],
        'user_id': [1, 2, 3, 4, 5]
    }
    return pd.DataFrame(data)


def test_seasonality_initialization(sample_interactions):
    seasonality_analysis = SeasonalityAnalysis(sample_interactions)
    assert 'season' in seasonality_analysis.interactions_df.columns, "Season column should be added based on months."


def test_seasonality_plot(sample_interactions):
    seasonality_analysis = SeasonalityAnalysis(sample_interactions)
    fig = seasonality_analysis.plot_seasonality()
    assert isinstance(
        fig, plt.Figure), "plot_seasonality should return a matplotlib Figure."
    plt.close(fig)
