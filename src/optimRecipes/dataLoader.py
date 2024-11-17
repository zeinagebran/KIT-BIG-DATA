"""Load and save data.

Load data from file or from URL (Google Drive) and save data in file.

"""
__authors__ = 'Nicolas Allègre'
__date__ = '29/10/2024'
__version__ = '0.1'

###############################################################################
# IMPORTS :

# /* Standard includes. */
import csv
import datetime
import io
import os
import sys
import zipfile
from dataclasses import dataclass

# /* Extern modules */
import numpy as np
import pandas as pd
import requests

# /* Intern modules */

###############################################################################
# CONSTANTES :
DATA_FILES = ['RAW_interactions.csv', 'RAW_recipes.csv']
CHARSET = 'UTF-8'
optimRecipes_DATATYPE = {
    'RAW_interactions.csv': {
        'user_id': 'int64',
        'recipe_id': 'int',
        'date': 'date',
        'rating': 'int',
        'review': 'str'
    },
    'RAW_recipes.csv': {
        'name': 'str',
        'id': 'int',
        'minutes': 'int',
        'contributor_id': 'int64',
        'submitted': 'date',
        'tags': 'list=str',
        'nutrition': 'list=float=7',
        'n_steps': 'int',
        'steps': 'list=str',
        'description': 'str',
        'ingredients': 'list=str',
        'n_ingredients': 'int',
    },
}


###############################################################################
# CLASS :
@dataclass
class dataLoader:
    """Manage data from extern."""
    data: any = None

    @staticmethod
    def loadcsv_tolist(file_path: str, dict: bool = False, delimiter: str = ',',
                       encoding: str = CHARSET) -> list[str | dict[str, str]]:
        """Load csv file into a list (static method).

        :param str file_path: path to data file
        :param bool dict: [default=False] load row in dict type (see csv.DictReader)
        :param str delimiter: [default=','] delimiter of CSV
        :return list[str | dict[str, str]]: data in list of row
        """
        data: list[str] = []

        with open(file_path, 'r', encoding=encoding) as file:
            if dict is False:
                spamreader = csv.reader(file, delimiter=delimiter)
            else:
                spamreader = csv.DictReader(file, delimiter=delimiter)
            for row in spamreader:
                data.append(row)

        return data

    @staticmethod
    def projectcsv_load_tolist(
            file_path: str, numpy_type: bool = False) -> tuple[list[any], list[str]]:
        """Load project csv file with typing.

        :param str file_path: path to data file
        :param bool numpy_type: [default=False] For loading data in nympy type.
        :return (headers=list(str), data): Return a tuple
            data : second element is a list of row parsed/typed
            headers : first element is the headers of CSVfile
        """
        data: list[any] = []
        headers: list[str] = []
        filename: str = os.path.basename(file_path)
        tmp = dataLooader.loadcsv_tolist(file_path)
        if tmp != []:
            headers = tmp[0]

        if filename not in optimRecipes_DATATYPE.keys() or tmp == []:
            print("File not is not the project known.", file=sys.stderr)
            return tmp, headers

        for i, row in enumerate(tmp[1:]):
            new_row = []
            for j, col in enumerate(row):
                cvt_type = optimRecipes_DATATYPE[filename].get(headers[j])
                new_row.append(dataLooader.convert(col, cvt_type))

            data.append(new_row)

        return data, headers

    @staticmethod
    def loadcsv_todataframe(file_path: str, delimiter: str = ',',
                       encoding: str = CHARSET) -> any:
        """Load csv file into a list (static method).

        :param str file_path: path to data file
        :param str delimiter: [default=','] delimiter of CSV
        :return pandas.Dataframe: data in list of row
        """
        data = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)
        for header in ['date', 'submitted']:
            if data.get(header) is None:
                continue

            data[header] = pd.to_datetime(data[header], errors='coerce', infer_datetime_format=True)
        
        return data
        

    @staticmethod
    def convert(col: str, cvt_type: str | None) -> any:
        """Convert a string in a specific type.

        :param str col: cellule of a data frame
        :param str cvt_type: type to convert (if None then no conversion)
        :return: the col data converted in type of cvt_type
        """
        if cvt_type is None or 'str' == cvt_type:
            return col
        if 'int' in cvt_type:
            return int(col)
        if 'float' == cvt_type:
            return float(col)
        if 'date' in cvt_type:
            return datetime.date.fromisoformat(col)
        if 'list=' in cvt_type:
            h = cvt_type.split('=')
            return [dataLooader.convert(x, h[1]) for x in col[1:-1].split(',')]

        return col
    
    @staticmethod
    def dll_google_zip(url: str, folder: str='extracted_data') -> str:
        """Download zip file and extract only needed data.
        
        :param str url: URL where zipfile are
        :param str folder: path where to extract CSV file
        :return str: path where CSV file are extracted
        """
        r = requests.get('https://drive.usercontent.google.com/download?id=1a2JonFLnOCvtML2ZQWFCtpniWwmmCUuo&export=download&confirm=t')
        if r.status_code != 200:
            print(f"Error to download file : {r.status_code}")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(folder, ['recipe/RAW_interactions.csv', 'recipe/RAW_recipes.csv'])
        
        del z
        del r  # to quickly remove from memory the zip file
        return os.path.join(folder, 'recipe')
        


if __name__ == 'main':
    # import src.optimRecipes.dataLoader as d
    # importlib.reload(d)
    file_path = '../../data/recipe/interactions_validation.csv'
    a = dataLooader.loadcsv_tolist(file_path)
    print(type(a))
    file_path = '../../data/recipe/RAW_recipes.csv'
    filename = os.path.basename(file_path)
    a = dataLooader.projectcsv_load_tolist(file_path)
    
    # path = dll_google_zip('https://drive.usercontent.google.com/download?id=1a2JonFLnOCvtML2ZQWFCtpniWwmmCUuo&export=download&confirm=t')
    path = 'extracted_data/recipe'
    recipes_df = dataLoader.loadcsv_todataframe(os.path.join(path, DATA_FILES[1]))
    interactions_df = dataLoader.loadcsv_todataframe(os.path.join(path, DATA_FILES[0]))
