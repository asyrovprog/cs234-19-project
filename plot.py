import numpy as np
import argparse
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns


sns.set(style="whitegrid")

parser = argparse.ArgumentParser()
parser.add_argument("--timestamp", required=True, type=str)


def read_mistake_file(model, result_timestamp):
    df = pd.read_csv(f"results/{result_timestamp}/training_mistake_{model}.csv", header=None)
    df = df.transpose().expanding().mean()
    df = df.transpose().stack().to_frame().reset_index()
    df.columns = ["iter", "patient", "err"]
    df["algo"] = model
    return df


def plot_err(filename, data, x_col, y_col, group_col, plot_title, ci=None, closeup=False):
    figure(num=None, figsize=(8, 6), dpi=100, facecolor='w', edgecolor='k')
    ax = sns.lineplot(x=x_col, y=y_col, hue=group_col, data=data, ci=ci, markers=True)
    plt.xlabel("Patient Count")
    plt.ylabel("Fraction of Incorrect Decisions")
    x_start = 0
    x_end = 6500 if closeup else 5000
    y_start = 0.33 if closeup else 0.2
    y_end = 0.4 if closeup else 0.8
    plt.axis([x_start, x_end, y_start, y_end])
    plt.legend(loc="upper right", title="")
    plt.title(plot_title)
    plt.savefig(filename)
    plt.close()


def plot_model_errs(filename, result_timestamp, models, ci=None, closeup=False):
    """
    Plot "Fraction of Incorrect Decisions"

    :param filename: output PNG image file name
    :param result_timestamp: timestamp string as the result sub-folder name
    :param models: list of model names (as used in result file name)
    :param ci: whether to show error band; "sd" for stderr band, None suppresses err band
    :param closeup: plot a closeup version (useful when several models are plotted together)
    :return:
    """
    plot_data = pd.DataFrame()
    for m in models:
        df = read_mistake_file(m, result_timestamp)
        plot_data = plot_data.append(df)
    plot_err(filename, data=plot_data, x_col="patient", y_col="err", group_col="algo",
             plot_title="Algorithm Comparison - Fraction of Incorrect Decisions", ci=ci, closeup=closeup)


def read_regret_file(model, result_timestamp):
    df = pd.read_csv(f"results/{result_timestamp}/training_regret_{model}.csv", header=None)
    df = df.mean().cumsum().to_frame().reset_index()
    df.columns = ["patient", "regret"]
    df["algo"] = model
    return df


def plot_cumulative_regret(filename, data, x_col, y_col, group_col, plot_title, closeup=False):
    figure(num=None, figsize=(9, 6), dpi=100, facecolor='w', edgecolor='k')
    ax = sns.lineplot(x=x_col, y=y_col, data=data, hue=group_col, ci=None, markers=True)
    plt.xlabel("Patient Count")
    plt.ylabel("Cumulative Expected Regret")
    x_start = 2000 if closeup else 0
    x_end = 5000
    y_start = 600 if closeup else 0
    y_end = 1700
    plt.axis([x_start, x_end, y_start, y_end])
    plt.legend(loc="lower right", title="")
    plt.title(plot_title)
    plt.savefig(filename)
    plt.close()


def plot_model_regrets(filename, result_timestamp, models, closeup=False):
    plot_data = pd.DataFrame()
    for m in models:
        df = read_regret_file(m, result_timestamp)
        plot_data = plot_data.append(df)
    plot_cumulative_regret(filename, data=plot_data, x_col="patient", y_col="regret", group_col="algo",
                           plot_title="Algorithm Comparison - Cumulative Expected Regret", closeup=closeup)


if __name__ == '__main__':
    args = parser.parse_args()

    # Plot 1: "Fraction of Incorrect Decisions"
    models = ["FixedDose", "ClinicalDose", "LinUCBDisjoint", "LinUCBDisjointBasic",
              "DTree-Beta", "DTree-Basic-Beta", "DTree-UCB", "DTree-Basic-UCB", "Lasso"]
    imgfile = "err_all_models.png"
    plot_model_errs(f"results/{args.timestamp}/{imgfile}", args.timestamp, models, ci=None, closeup=False)

    # Plot 2: "Cumulative Expected Regret"
    imgfile = "regret_all_models.png"
    plot_model_regrets(f"results/{args.timestamp}/{imgfile}", args.timestamp, models, closeup=False)

