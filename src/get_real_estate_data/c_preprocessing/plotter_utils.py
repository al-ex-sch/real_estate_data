import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker


def plot_distribution(dataframe, column):
    if column not in dataframe.columns:
        print(f"Column '{column}' not found in the dataframe.")
        return

    plt.figure(figsize=(10, 6))
    sns.histplot(dataframe[column], bins=30, kde=True, color='blue', edgecolor='black')
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    ax = plt.gca()
    formatter = FuncFormatter(lambda x, _: '{:.0f}'.format(x))
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    plt.show()


def plot_distribution_subplot(df, canton, metric, ax):
    """
    Plots the distribution of the specified metric for the given canton as a subplot.

    Args:
    df (pd.DataFrame): Dataframe containing the data.
    canton (str): The canton to filter the data by.
    metric (str): The metric to plot the distribution for.
    ax (matplotlib.axes.Axes): The axes object to plot the subplot on.
    """
    canton_data = df[df['canton'] == canton]
    sns.histplot(canton_data[metric], kde=True, ax=ax)
    ax.set_title(f'{canton}')
    ax.set_xlabel(metric)
    ax.set_ylabel('Frequency')
    ax.xaxis.set_major_formatter(ticker.EngFormatter())


def plot_all_cantons(df, cantons, metric):
    """
    Plots the distribution of the specified metric for all cantons in one plot made of subplots.

    Args:
    df (pd.DataFrame): Dataframe containing the data.
    cantons (list): List of cantons to plot.
    metric (str): The metric to plot the distribution for.
    """
    num_cantons = len(cantons)
    num_columns = 3
    num_rows = -(-num_cantons // num_columns)

    fig, axes = plt.subplots(num_rows, num_columns, figsize=(15, num_rows * 5), constrained_layout=True)

    for i, canton in enumerate(cantons):
        row, col = divmod(i, num_columns)
        plot_distribution_subplot(df, canton, metric, axes[row, col])

    for j in range(i + 1, num_rows * num_columns):
        row, col = divmod(j, num_columns)
        fig.delaxes(axes[row, col])

    plt.suptitle(f'Distribution of {metric} for all cantons', fontsize=16)
    plt.show()
