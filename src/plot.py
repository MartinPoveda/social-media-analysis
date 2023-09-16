import matplotlib.pyplot as plt
from matplotlib.pyplot import figure



def _generic_figure(figsize, dpi=800):
    figure(figsize=figsize, dpi=dpi)

def temporal_figure():
    _generic_figure((12,4))

def correlation_figure():
    _generic_figure((10,6))

def _generic_bar_plot(x,y, figure_type=None):
    if figure_type=='temporal':
        temporal_figure()
    if figure_type=='correlation':
        correlation_figure()
    plt.bar(x, y)

def plot_chain(df, col):
    # Plot
    _generic_bar_plot(df.index, df[col], figure_type='temporal')
    plt.title(f'{col} per time')
    # Plot
    _generic_bar_plot(df['post_number'], df[col], figure_type='temporal')
    plt.title(f'{col} per post')
    # Plot
    reach_corr = df.corr()[col].drop(col).dropna().sort_values(ascending=False)
    _generic_bar_plot(reach_corr.index, reach_corr, figure_type='correlation')
    plt.title(f'{col} correlation')
    plt.xticks(rotation=90)
    # Plot
    hourly_df = df.groupby(df.index.hour).mean()
    _generic_bar_plot(hourly_df.index, hourly_df[col], figure_type='correlation')
    plt.title(f'{col} for each hour')
    # Plot
    weekly_df = df.groupby(df.index.day_of_week).mean()
    _generic_bar_plot(weekly_df.index, weekly_df[col], figure_type='correlation')
    plt.title(f'{col} for each day of the week')
