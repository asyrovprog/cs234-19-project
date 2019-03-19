import numpy as np
import argparse
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.patches import Rectangle
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


def get_culumative_mean_error_df(result_timestamp, models):
    plot_data = pd.DataFrame()
    for m in models:
        df = read_mistake_file(m, result_timestamp)
        plot_data = plot_data.append(df)
    return plot_data


def plot_err(filename, data, x_col, y_col, group_col, plot_title, ci=None, closeup=False):
    figure(num=None, figsize=(8, 6), dpi=100, facecolor='w', edgecolor='k')
    ax = sns.lineplot(x=x_col, y=y_col, hue=group_col, data=data, ci=ci, markers=True)
    plt.xlabel("Patient Count")
    plt.ylabel("Fraction of Incorrect Decisions")
    x_start = 0
    x_end = 6500 if closeup else 5000
    y_start = 0.33 if closeup else 0.2
    y_end = 0.42 if closeup else 0.8
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
    plot_data = get_culumative_mean_error_df(result_timestamp, models)
    plot_err(filename, data=plot_data, x_col="patient", y_col="err", group_col="algo",
             plot_title="Algorithm Comparison - Fraction of Incorrect Decisions", ci=ci, closeup=closeup)


def read_regret_file(model, result_timestamp):
    df = pd.read_csv(f"results/{result_timestamp}/training_regret_{model}.csv", header=None)
    df = df.mean().cumsum().to_frame().reset_index()
    df.columns = ["patient", "regret"]
    df["algo"] = model
    return df


def get_cumulative_regret_df(result_timestamp, models):
    plot_data = pd.DataFrame()
    for m in models:
        df = read_regret_file(m, result_timestamp)
        plot_data = plot_data.append(df)
    return plot_data


def plot_cumulative_regret(filename, data, x_col, y_col, group_col, plot_title, closeup=False):
    figure(num=None, figsize=(9, 6), dpi=100, facecolor='w', edgecolor='k')
    ax = sns.lineplot(x=x_col, y=y_col, data=data, hue=group_col, ci=None, markers=True)
    plt.xlabel("Patient Count")
    plt.ylabel("Cumulative Expected Regret")
    x_start = 2000 if closeup else 0
    x_end = 5000
    y_start = 600 if closeup else 0
    y_end = None
    plt.axis([x_start, x_end, y_start, y_end])
    plt.legend(loc="lower right", title="")
    plt.title(plot_title)
    plt.savefig(filename)
    plt.close()


def plot_model_regrets(filename, result_timestamp, models, closeup=False):
    plot_data = get_cumulative_regret_df(result_timestamp, models)
    plot_cumulative_regret(filename, data=plot_data, x_col="patient", y_col="regret", group_col="algo",
                           plot_title="Algorithm Comparison - Cumulative Expected Regret", closeup=closeup)


def read_risk_file(model, result_timestamp):
    df = pd.read_csv(f"results/{result_timestamp}/training_risk_{model}.csv", header=None)
    df = df.sum(axis=0).values.reshape((3, 3))
    df = pd.DataFrame(data=df, columns=["Low", "Medium", "High"], index=["True_Low", "True_Medium", "True_High"])
    total = df.sum(axis=1)
    total = total * 100 / total.sum()
    df = df.transpose().apply(lambda x: round(x / x.sum(), 4)).transpose()
    df["Total"] = total
    return df


def plot_confusion_matrix(data, model, xticklabels, yticklabels, i, cbar_ax):
    ax = sns.heatmap(data, annot=True, vmin=0, vmax=1, cmap="Blues", cbar=i == 0,
                     yticklabels=yticklabels, xticklabels=xticklabels, cbar_ax=None if i else cbar_ax)
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, edgecolor='limegreen', lw=3))
    ax.add_patch(Rectangle((1, 1), 1, 1, fill=False, edgecolor='limegreen', lw=3))
    ax.add_patch(Rectangle((2, 2), 1, 1, fill=False, edgecolor='limegreen', lw=3))
    ax.add_patch(Rectangle((0, 2), 1, 1, fill=False, edgecolor='red', lw=3))
    ax.add_patch(Rectangle((2, 0), 1, 1, fill=False, edgecolor='red', lw=3))
    plt.xlabel(f"{model} Assigned Dosage")
    plt.ylabel("True Dosage")


def plot_model_risks(filename, result_timestamp, models):
    figure(num=None, figsize=(20, 10), dpi=100, facecolor='w', edgecolor='k')
    cbar_ax = plt.axes([.91, .3, .01, .4])
    for i in range(len(models)):
        df = read_risk_file(models[i], result_timestamp)
        yticklabels=[f"Low\n({df.iloc[0][3].astype(int)}%)", f"Medium\n({df.iloc[1][3].astype(int)}%)",
                     f"High\n({df.iloc[2][3].astype(int)}%)"]
        xticklabels=["Low", "Medium", "High"]
        plt.subplot(2, 4, i+1)
        plot_confusion_matrix(df.iloc[:,:3], models[i], xticklabels, yticklabels, i, cbar_ax)
    plt.subplots_adjust(wspace = 0.4, hspace = 0.4)
    plt.suptitle("Risk Analysis - Assigned Dosage Confusion Matrix")
    plt.savefig(filename)
    plt.close()


def export_stats(timestamp, models, err_stats_fname, regret_stats_fname):
    df1 = get_culumative_mean_error_df(timestamp, models)
    df1.to_csv(err_stats_fname, index=None, header=True)
    df2 = get_cumulative_regret_df(timestamp, models)
    df2.to_csv(regret_stats_fname, index=None, header=True)


if __name__ == '__main__':
    args = parser.parse_args()

    # Plot 1: "Fraction of Incorrect Decisions"
    models = ["FixedDose", "ClinicalDose", "LinUCBDisjoint", "LinUCBDisjointBasic",
              "DTree", "DTree-Alt", "Lasso"]
    imgfile = "err_all_models.png"
    plot_model_errs(f"results/{args.timestamp}/{imgfile}", args.timestamp, models, ci=None, closeup=False)

    # Plot 2: "Cumulative Expected Regret"
    imgfile = "regret_all_models.png"
    plot_model_regrets(f"results/{args.timestamp}/{imgfile}", args.timestamp, models, closeup=False)

    # Plot 3: "Risk Analysis - Assigned Dosage Confusion Matrix"
    imgfile = "risk_all_models.png"
    plot_model_risks(f"results/{args.timestamp}/{imgfile}", args.timestamp, models)

    # export plot data to csv
    export_stats(args.timestamp, models,
                 f"results/{args.timestamp}/stats_cumulative_mean_err.csv",
                 f"results/{args.timestamp}/stats_cumulative_regret.csv")
