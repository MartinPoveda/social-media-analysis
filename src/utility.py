"""
Module gathering utility functions such as upload functions, aggregation functions, etc.
"""

# Import standard libraries
import os 
# Import libraries for data_analysis
import numpy as np
import pandas as pd

# Default values
DATA_PATH = f'{os.getcwd()}/data'



def read_file(file_name, date_col=None, data_path=DATA_PATH):
    """Read csv file containing a Timestamp column and return the appropriate DataFrame with the time in index.
    Note the data returned is sorted by date.

    Parameters
    ----------
    
    file_name : `str`
        Name of the file to upload (with .csv at the end)

    data_path : 'str default: DATA_PATH'
        Path of the data folder. By default it is set under the project directory

    Returns
    ----------
    pandas DataFrame
        Data uploaded with the time in index (posts are sorted by date).
    """
    df = pd.read_csv(f'{data_path}/{file_name}', index_col=date_col, parse_dates=True, date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M'))
    df.sort_index(inplace=True)
    return df



def pearson_correlation_col(df, col):
    """Compute the Pearson's correlation to the given column.

    Parameters
    ----------

    df : 'pandas DataFrame'
        Data of the posts
    
    col : 'str'
        Name of the column to look at

    Returns
    ----------
    pandas Series
        Pearson's correlation to the given column.
    """
    return df.corr(numeric_only=True)[col].drop(col).dropna().sort_values(ascending=False)



def by_hour(df, aggregation_method=lambda x: x.mean(numeric_only=True)):
    """Group the data by hours, aggregating with the method provided.

    Parameters
    ----------

    df : 'pandas DataFrame'
        Data of the posts

    aggregation_method : 'func default: lambda x: x.mean()'
        Function of aggregation. Average by default

    Returns
    ----------
    pandas DataFrame
        DataFrame per hour.
    """
    return aggregation_method(df.groupby(df.index.hour))



def by_day_name(df, aggregation_method=lambda x: x.mean(numeric_only=True)):
    """Group the data by day name, aggregating with the method provided.

    Parameters
    ----------

    df : 'pandas DataFrame'
        Data of the posts

    aggregation_method : 'func default: lambda x: x.mean()'
        Function of aggregation. Average by default

    Returns
    ----------
    pandas DataFrame
        DataFrame per day of the week.
    """
    return aggregation_method(df.groupby(df.index.day_name()))



def dict_to_df(df_dict, col):
    """Equivalent to df.xs but for a dataframe dictionnary.

    Parameters
    ----------

    df_dict : `dict`
        Data of different files
    
    col : 'str'
        Name of the column to look at

    Returns
    ----------
    pandas DataFrame
        Dataframe with the column desired for each dataset
    """
    dfs = []
    for key, df in df_dict.items():
        # Create a dataframe with the column desired (renamed by the name of the dataset)
        dfs.append(pd.DataFrame(np.array([df[col]]).transpose(), index=df.index, columns=[key]))
    result = pd.concat(dfs)
    result.sort_index(inplace=True)
    return result
