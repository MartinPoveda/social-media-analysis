"""
Module gathering the different plots
"""

# Import librairies for Timedelta
import pandas as pd
# Import libraries for plotting graphs
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
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



def _generic_plot(x,y, plot_type=None):
    """Create a plot for standard use cases.
    The different type of plots are:
     - bar plot
     - line plot
     - point plot

    Parameters
    ----------

    plot_type : 'str default: None'
        Type of the plot

    """
    if plot_type=='bar':
        plt.bar(x, y)
    if plot_type=='plot':
        plt.plot(x, y, color='red')
    if plot_type=='point':
        plt.plot(x,y,'.')



def _generic_graph(x,y, title_name, graph_type=None, save_img_path=None, moving_average=None, xticks_rotation=0):
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

    """
    # Create the figure and a first plot
    _generic_figure(figure_type=graph_type)
    if graph_type=='temporal_diff':
        _generic_plot(x, y, plot_type='point')
    else:
        _generic_plot(x, y, plot_type='bar')
    # Add a title and rotate x ticks if necessary
    plt.title(title_name)
    plt.xticks(rotation=xticks_rotation)
    if graph_type=='temporal':
        # Add a line plot to see the trend over time (represented by the moving average)
        moving_average_y = y.rolling(moving_average).mean()
        _generic_plot(x, moving_average_y.reindex(y.index), plot_type='plot')
    else:
        pass
    # Save the graph
    plt.savefig(f'{save_img_path}/{title_name}.png', dpi=800)



def per_time_plot(df, col, save_img_path=None, moving_average=7):
    """Create a graph to look at a feature (col) over time.

    Parameters
    ----------

    df : 'pandas DataFrame'
        Data of the posts
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    moving_average : 'int default: 7'
        Number of x ticks to compute the moving average in days.
        By default, set to 7 days.

    """
    _generic_graph(df.index, df[col], f'{col} per time', graph_type='temporal', save_img_path=save_img_path, moving_average=moving_average)



def per_post_plot(df, col, save_img_path=None, moving_average=7):
    """Create a graph to look at a feature (col) over the posts.

    Parameters
    ----------

    df : 'pandas DataFrame'
        Data of the posts
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    moving_average : 'int default: 7'
        Number of x ticks to compute the moving average.
        By default, set to 7 posts.

    """
    _generic_graph(df['post_number'], df[col], f'{col} per post', graph_type='temporal', save_img_path=save_img_path, moving_average=moving_average)



def per_time_since_last_plot(df, col, save_img_path=None):
    """Create a graph to look at a feature (col) over the time between the actual post and the last one.

    Parameters
    ----------

    df : 'pandas DataFrame'
        Data of the posts
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    moving_average : 'int default: 7'
        Number of x ticks to compute the moving average.
        By default, set to 7 posts.

    """
    # Note: [1:] is to avoid the first post which have not last post
    _generic_graph(df[1:]['time_last_post'], df[1:][col], f'{col} per time since last post', graph_type='temporal_diff', save_img_path=save_img_path)



def corr_plot(df, col, save_img_path=None):
    """Create a graph to look at a feature (col) correlation with other columns.

    Parameters
    ----------

    df : 'pandas DataFrame'
        Data of the posts
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    """
    corr = utility.pearson_correlation_col(df, col)
    _generic_graph(corr.index, corr, f'{col} correlation', graph_type='correlation', save_img_path=save_img_path, xticks_rotation=90)



def per_hour_plot(df, col, save_img_path=None):
    """Create a graph to look at a feature (col) for each hour.

    Parameters
    ----------

    df : 'pandas DataFrame'
        Data of the posts
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    """
    hourly_df = utility.by_hour(df)
    _generic_graph(hourly_df.index, hourly_df[col], f'{col} correlation', graph_type='correlation', save_img_path=save_img_path)



def per_week_plot(df, col, save_img_path=None):
    """Create a graph to look at a feature (col) for each day of the week.

    Parameters
    ----------

    df : 'pandas DataFrame'
        Data of the posts
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    """
    weekly_df = utility.by_day_name(df)
    _generic_graph(weekly_df.index, weekly_df[col], f'{col} correlation', graph_type='correlation', save_img_path=save_img_path)



def plot_chain(df, col, save_img_path=None, moving_average={'time':7,'post':7}):
    """Create a standard chain of graphs to look at when looking at a feature in the post data.

    Parameters
    ----------

    df : 'pandas DataFrame'
        Data of the posts
    
    col : 'str'
        Name of the column to look at


    save_img_path : 'str default: None'
        Path to save the image

    moving_average : 'dict default: {'time':7,'post':7}'
        moving_average for the temporal plots.
        By default, 7 days for plot over the time and 7 posts for plot over the posts

    """
    # Plot per time
    per_time_plot(df, col, save_img_path=save_img_path, moving_average=moving_average['time'])
    # Plot per post
    per_post_plot(df, col, save_img_path=save_img_path, moving_average=moving_average['post'])
    # Plot per time since last plot
    per_time_since_last_plot(df, col, save_img_path=save_img_path)
    # Correlation plot
    corr_plot(df, col, save_img_path=save_img_path)
    # Hourly plot
    per_hour_plot(df, col, save_img_path=save_img_path)
    # Weekly Plot
    per_week_plot(df, col, save_img_path=save_img_path)
