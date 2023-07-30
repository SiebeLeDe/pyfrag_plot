import pandas as pd
import pytest
from pyfrag_plotter.processing_funcs import _trim_data_float, _trim_data_int, _trim_data_str, remove_dispersion_term
from pyfrag_plotter.errors import PyFragResultsProcessingError


@pytest.fixture
def test_df():
    return pd.DataFrame({
        "EnergyTotal": [
            0.40939,
            9.56754,
            15.22111,
            17.08688,
            19.07092,
            21.03672,
            22.79637,
            24.08829,
            23.96248,
            13.28778,
            0.34548,
            -6.09441,
            -22.56811,
            -33.61639,
            -36.88992,
            -37.21977]
        }
    )


def test_trim_data_float(test_df):
    result = _trim_data_float(test_df, 10.0, "EnergyTotal")
    assert len(result) == 2
    assert result["EnergyTotal"].max() <= 10.0


def test_trim_data_int(test_df):
    result = _trim_data_int(test_df, 3, "EnergyTotal")
    assert len(result) == 3


def test_trim_data_str_min(test_df):
    result = _trim_data_str(test_df, "min", "EnergyTotal")
    assert len(result) == 16


def test_trim_data_str_max(test_df):
    result = _trim_data_str(test_df, "max", "EnergyTotal")
    assert len(result) == 8
    assert result["EnergyTotal"].iloc[-1] == result["EnergyTotal"].max()


def test_trim_data_str_false(test_df):
    with pytest.raises(PyFragResultsProcessingError):
        _trim_data_str(test_df, "invalid", "EnergyTotal")


def test_remove_dispersion_term_with_dispersion():
    # Test the function with a dataframe that has a non-zero dispersion term
    df = pd.DataFrame({
        "Energy": [-10.0, -20.0, -30.0],
        "Disp": [0.1, 0.2, 0.3]
    })
    expected_df = df.copy()
    assert remove_dispersion_term(df).equals(expected_df)


def test_remove_dispersion_term_without_dispersion():
    # Test the function with a dataframe that has a zero dispersion term
    df = pd.DataFrame({
        "Energy": [-10.0, -20.0, -30.0],
        "Disp": [0.0, 0.0, 0.0]
    })
    expected_df = df.drop(columns=["Disp"])
    assert remove_dispersion_term(df).equals(expected_df)


def test_remove_dispersion_term_with_empty_dataframe():
    # Test the function with an empty dataframe
    df = pd.DataFrame()
    expected_df = pd.DataFrame()
    assert remove_dispersion_term(df).equals(expected_df)


def test_remove_dispersion_term_with_single_row_dataframe():
    # Test the function with a dataframe that has a single row
    df = pd.DataFrame({
        "Energy": [-10.0],
        "Disp": [0.0]
    })
    expected_df = df.drop(columns=["Disp"])
    assert remove_dispersion_term(df).equals(expected_df)
