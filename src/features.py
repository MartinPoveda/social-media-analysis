"""
Module for adding features to the data
"""

# Import libraries for data_analysis
import numpy as np
import pandas as pd



def set_post_numero(df):
    """Add a column in the DataFrame to set a numero number for each post.
    The first post (sorted by date) will reveive the numero 1.

    Parameters
    ----------
    
    df : `pandas DataFrame`
        Data of the posts
    
    """
    df['post_number'] = np.arange(df.shape[0]) + 1



def count_post_length(df):
    """Count the number of characters for each post.

    Parameters
    ----------
    
    df : `pandas DataFrame`
        Data of the posts

    """
    df['post_length'] = df['Content'].str.len()



def time_since_last_post(df):
    """Count the time between the actual and the last post.

    Parameters
    ----------
    
    df : `pandas DataFrame`
        Data of the posts

    """
    df['time_last_post'] = df.index.to_series().diff()
