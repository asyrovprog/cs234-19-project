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
    x_end = 5000
    y_start = 0.3 if closeup else 0.2
    y_end = 0.45 if closeup else 0.8
    plt.axis([x_start, x_end, y_start, y_end])
    plt.legend(loc="upper right", title="")
    plt.title(plot_title)
    plt.savefig(filename)
    plt.close()


def plot_model_errs(filename, result_timestamp, models, ci=None, closeup=False):
    plot_data = pd.DataFrame()
    for m in models:
        df = read_mistake_file(m, result_timestamp)
        plot_data = plot_data.append(df)
    plot_err(filename, data=plot_data, x_col="patient", y_col="err", group_col="algo",
             plot_title="Algorithm Comparison - Fraction of Incorrect Decisions", ci=ci, closeup=closeup)


if __name__ == '__main__':
    args = parser.parse_args()

    # Plot 1: All model errs
    models = ["FixedDose", "ClinicalDose", "LinUCBDisjoint", "LinUCBDisjointBasic",
              "TreeHeuristic", "TreeHeuristicBasic", "Lasso"]
    imgfile = "err_all_models.png"
    plot_model_errs(f"results/{args.timestamp}/{imgfile}", args.timestamp, models, ci=None, closeup=True)
