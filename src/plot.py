"""
Module gathering the different plots
"""

# Import librairies for Timedelta
import numpy as np
import pandas as pd
# Import libraries for plotting graphs
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
# Import internal libraries
from src import utility
from src import variable



def _generic_figure(figure_type=None):
    """Create a figure for standard use cases.
    The different type of figures are:
     - temporal
     - correlation

    Parameters
    ----------

    figure_type : 'str default: None'
        Type of the figure

    """
    if 'temporal' in figure_type:
        figure(figsize=(12,4), dpi=800)
    if figure_type=='correlation':
        figure(figsize=(10,6), dpi=800)



def _generic_plot(x,y, label=None, plot_type=None):
    """Create a plot for standard use cases.
    The different type of plots are:
     - bar plot
     - line plot
     - point plot

    Parameters
    ----------

    plot_type : 'str default: None'
        Type of the plot

    label : 'str default: None'
        Label of the plot

    """
    if plot_type=='bar':
        plt.bar(x, y, label=label)
    if plot_type=='plot':
        plt.plot(x, y)
    if plot_type=='point':
        plt.plot(x, y,'.', label=label)
    if plot_type=='box':
        sns.boxplot(data=y)



def _generic_graph(x,y, title_name, graph_type=None, save_img_path=None, moving_average=None, xticks_rotation=0, label=None):
    """Create a graph for standard use cases.
    The different type of graphs are:
     - temporal
     - temporal_diff
     - correlation

    Parameters
    ----------

    x : 'pandas Series'
        x axis values of the plot
    
    y : 'pandas Series'
        y axis values of the plot

    graph_type : 'str default: None'
        Type of the plot

    save_img_path : 'str default: None'
        Path to save the image

    moving_average : 'int default: None'
        Number of x ticks to compute the moving average.
        If x is a DatetimeIndex, thus it will be in days.

    xticks_rotation : 'float default: 0'
        Degree (in °) of the rotation of x ticks

    label : 'str default: None'
        Label of the plot

    """
    if graph_type=='temporal_diff':
        _generic_plot(x, y, plot_type='point', label=label)
    elif graph_type=='box':
        _generic_plot(x, y, plot_type='box', label=label)
    else:
        _generic_plot(x, y, plot_type='bar', label=label)
    # Add a title and rotate x ticks if necessary
    plt.title(title_name)
    plt.xticks(rotation=xticks_rotation)
    if graph_type=='temporal':
        # Add a line plot to see the trend over time (represented by the moving average)
        moving_average_y = y.rolling(moving_average).mean()
        _generic_plot(x, moving_average_y.reindex(y.index), plot_type='plot')
    else:
        pass
    plt.legend()
    # Save the graph
    plt.savefig(f'{save_img_path}/{title_name}.png', dpi=800)



def per_time_plot(df_dict, col, save_img_path=None, moving_average=7):
    """Create a graph to look at a feature (col) over time.

    Parameters
    ----------

    df_dict : `dict`
        Data of different files
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    moving_average : 'int default: 7'
        Number of x ticks to compute the moving average in days.
        By default, set to 7 days.

    """
    # Create the figure and a first plot
    _generic_figure(figure_type='temporal')
    for key, df in df_dict.items():
        _generic_graph(df.index, df[col], f'{col} per time', graph_type='temporal', save_img_path=save_img_path, moving_average=moving_average, label=key)



def per_publication_plot(df_dict, col, save_img_path=None, moving_average=7):
    """Create a graph to look at a feature (col) over the posts.

    Parameters
    ----------

    df_dict : `dict`
        Data of different files
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    moving_average : 'int default: 7'
        Number of x ticks to compute the moving average.
        By default, set to 7 posts.

    """
    # Create the figure and a first plot
    _generic_figure(figure_type='temporal')
    for key, df in df_dict.items():
        _generic_graph(df['publication_number'], df[col], f'{col} per publication', graph_type='temporal', save_img_path=save_img_path, moving_average=moving_average, label=key)



def per_time_since_last_plot(df_dict, col, save_img_path=None):
    """Create a graph to look at a feature (col) over the time between the actual post and the last one.

    Parameters
    ----------

    df_dict : `dict`
        Data of different files
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    moving_average : 'int default: 7'
        Number of x ticks to compute the moving average.
        By default, set to 7 posts.

    """
    # Create the figure and a first plot
    _generic_figure(figure_type='temporal_diff')
    # Note: [1:] is to avoid the first post which have not last post
    for key, df in df_dict.items():
        # Tranform timedelta serie into number of days (serie of float)
        x = df[1:]['time_last_publication'].dt.total_seconds() / variable.seconds_in_day
        _generic_graph(x, df[1:][col], f'{col} per time since last publication',
                       graph_type='temporal_diff', save_img_path=save_img_path, label=key)



def corr_plot(df_dict, col, save_img_path=None):
    """Create a graph to look at a feature (col) correlation with other columns.

    Parameters
    ----------

    df_dict : `dict`
        Data of different files
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    """
    # Create the figure and a first plot
    _generic_figure(figure_type='correlation')
    for key, df in df_dict.items():
        corr = utility.pearson_correlation_col(df, col)
        _generic_graph(corr.index, corr, f'{col} correlation', graph_type='correlation', save_img_path=save_img_path, xticks_rotation=90, label=key)



def per_hour_plot(df_dict, col, save_img_path=None):
    """Create a graph to look at a feature (col) for each hour.

    Parameters
    ----------

    df_dict : `dict`
        Data of different files
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    """
    # Create the figure and a first plot
    _generic_figure(figure_type='correlation')
    for key, df in df_dict.items():
        hourly_df = utility.by_hour(df)
        _generic_graph(hourly_df.index, hourly_df[col], f'{col} correlation', graph_type='correlation', save_img_path=save_img_path, label=key)



def per_week_plot(df_dict, col, save_img_path=None):
    """Create a graph to look at a feature (col) for each day of the week.

    Parameters
    ----------

    df_dict : `dict`
        Data of different files
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    """
    # Create the figure and a first plot
    _generic_figure(figure_type='correlation')
    for key, df in df_dict.items():
        weekly_df = utility.by_day_name(df)
        _generic_graph(weekly_df.index, weekly_df[col], f'{col} correlation', graph_type='correlation', save_img_path=save_img_path, label=key)



def mean_plot(df_dict, col, save_img_path=None):
    """Create a graph to look at a feature (col) distribution for each dataset.

    Parameters
    ----------

    df_dict : `dict`
        Data of different files
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    """
    df = utility.dict_to_df(df_dict, col)
    # Create the figure and a first plot
    _generic_figure(figure_type='correlation')
    _generic_graph(df.columns, df, f'{col} distribution', graph_type='box', xticks_rotation=90, save_img_path=save_img_path)



def plot_chain(df_dict, col, save_img_path=None, moving_average={'time':7,'post':7}):
    """Create a standard chain of graphs to look at when looking at a feature in the post data.

    Parameters
    ----------

    df_dict : `dict`
        Data of different files
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    moving_average : 'dict default: {'time':7,'post':7}'
        moving_average for the temporal plots.
        By default, 7 days for plot over the time and 7 posts for plot over the posts

    """
    # Plot per time
    per_time_plot(df_dict, col, save_img_path=save_img_path, moving_average=moving_average['time'])
    # Plot per post
    per_publication_plot(df_dict, col, save_img_path=save_img_path, moving_average=moving_average['post'])
    # Plot per time since last plot
    per_time_since_last_plot(df_dict, col, save_img_path=save_img_path)
    # Correlation plot
    corr_plot(df_dict, col, save_img_path=save_img_path)
    # Hourly plot
    per_hour_plot(df_dict, col, save_img_path=save_img_path)
    # Weekly Plot
    per_week_plot(df_dict, col, save_img_path=save_img_path)
