import matplotlib.pyplot as plt
from matplotlib.pyplot import figure



def _generic_figure(figsize, dpi=800):
    figure(figsize=figsize, dpi=dpi)

def temporal_figure():
    _generic_figure((12,4))

def correlation_figure():
    _generic_figure((10,6))

def fig(figure_type=None):
    if figure_type=='temporal':
        temporal_figure()
    if figure_type=='correlation':
        correlation_figure()

def _generic_plot(x,y, plot_type=None):
    if plot_type=='bar':
        plt.bar(x, y)
    if plot_type=='plot':
        plt.plot(x, y, color='red')

def per_time_plot(df, col, save_img_path):
    fig(figure_type='temporal')
    _generic_plot(df.index, df[col], plot_type='bar')
    moving_average = df.rolling(7).mean()
    _generic_plot(df.index, moving_average[col], plot_type='plot')
    plt.title(f'{col} per time')
    plt.savefig(f'{save_img_path}/{col} per time.png', dpi=800)

def per_post_plot(df, col, save_img_path):
    fig(figure_type='temporal')
    _generic_plot(df['post_number'], df[col], plot_type='bar')
    moving_average = df.rolling(7).mean()
    _generic_plot(df['post_number'], moving_average[col], plot_type='plot')
    plt.title(f'{col} per post')
    plt.savefig(f'{save_img_path}/{col} per post.png', dpi=800)

def corr_plot(df, col, save_img_path):
    corr = df.corr()[col].drop(col).dropna().sort_values(ascending=False)
    fig(figure_type='correlation')
    _generic_plot(corr.index, corr, plot_type='bar')
    moving_average = corr.rolling(7).mean()
    _generic_plot(corr.index, moving_average, plot_type='plot')
    plt.title(f'{col} correlation')
    plt.xticks(rotation=90)
    plt.savefig(f'{save_img_path}/{col} correlation.png', dpi=800)

def per_hour_plot(df, col, save_img_path):
    hourly_df = df.groupby(df.index.hour).mean()
    fig(figure_type='correlation')
    _generic_plot(hourly_df.index, hourly_df[col], plot_type='bar')
    plt.title(f'{col} for each hour')
    plt.savefig(f'{save_img_path}/{col} for each hour.png', dpi=800)

def per_week_plot(df, col, save_img_path):
    weekly_df = df.groupby(df.index.day_of_week).mean()
    fig(figure_type='correlation')
    _generic_plot(weekly_df.index, weekly_df[col], plot_type='bar')
    plt.title(f'{col} for each day of the week')
    plt.savefig(f'{save_img_path}/{col} for each day of the week.png', dpi=800)

def plot_chain(df, col, save_img_path=None):
    # Plot per time
    per_time_plot(df, col, save_img_path)
    # Plot per post
    per_post_plot(df, col, save_img_path)
    # Correlation plot
    corr_plot(df, col, save_img_path)
    # Hourly plot
    per_hour_plot(df, col, save_img_path)
    # Plot
    per_week_plot(df, col, save_img_path)
