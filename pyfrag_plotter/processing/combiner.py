""" Module that combines the data from inputfile and outputfile into a PyFragResultsObject object """
from pyfrag_plotter.pyfrag_object import PyFragResultsObject
import pandas as pd
from typing import Dict, Any


def create_pyfrag_object(results_data: pd.DataFrame, inputfile_data: Dict[str, Any]) -> PyFragResultsObject:
    raise NotImplementedError
