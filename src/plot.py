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

def per_time_plot(df, col, save_img_path):
    _generic_bar_plot(df.index, df[col], figure_type='temporal')
    plt.title(f'{col} per time')
    plt.savefig(f'{save_img_path}/{col} per time.png', dpi=800)

def per_post_plot(df, col, save_img_path):
    _generic_bar_plot(df['post_number'], df[col], figure_type='temporal')
    plt.title(f'{col} per post')
    plt.savefig(f'{save_img_path}/{col} per post.png', dpi=800)

def corr_plot(df, col, save_img_path):
    corr = df.corr()[col].drop(col).dropna().sort_values(ascending=False)
    _generic_bar_plot(corr.index, corr, figure_type='correlation')
    plt.title(f'{col} correlation')
    plt.xticks(rotation=90)
    plt.savefig(f'{save_img_path}/{col} correlation.png', dpi=800)

def per_hour_plot(df, col, save_img_path):
    hourly_df = df.groupby(df.index.hour).mean()
    _generic_bar_plot(hourly_df.index, hourly_df[col], figure_type='correlation')
    plt.title(f'{col} for each hour')
    plt.savefig(f'{save_img_path}/{col} for each hour.png', dpi=800)

def per_week_plot(df, col, save_img_path):
    weekly_df = df.groupby(df.index.day_of_week).mean()
    _generic_bar_plot(weekly_df.index, weekly_df[col], figure_type='correlation')
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
