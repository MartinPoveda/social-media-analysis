"""
Module for adding features to the data
"""

# Import libraries for data_analysis
import numpy as np
import pandas as pd



def set_publication_numero(df_dict):
    """Add a column in the DataFrame to set a numero number for each publication.
    The first publication (sorted by date) will reveive the numero 1.

    Parameters
    ----------
    
    df_dict : `dict`
        Data of different files
    
    """
    for df in df_dict.values():
        df['publication_number'] = np.arange(df.shape[0]) + 1



def count_content_length(df_dict):
    """Count the number of characters for each content.

    Parameters
    ----------
    
    df_dict : `dict`
        Data of different files

    """
    for key, df in df_dict.items():
        if key != 'reel':
            df['content_length'] = df['Content'].str.len()



def time_since_last_publication(df_dict):
    """Count the time between the actual and the last publication of that type.

    Parameters
    ----------
    
    df_dict : `dict`
        Data of different files

    """
    for df in df_dict.values():
        df['time_last_publication'] = df.index.to_series().diff()
