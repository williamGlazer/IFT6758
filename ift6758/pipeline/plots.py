import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

from sklearn.calibration import CalibrationDisplay


def plot_roc(truth: list[int], probas: list[float], labels: list[str]):
    """
    Displays ROC curves for different models
    """

    for t, p, l in zip(truth, probas, labels):
        fpr, tpr, _ = roc_curve(t, p)
        auc = roc_auc_score(t, p)

        plt.plot(fpr, tpr, label=f"{l}, AUC={auc:.3f}")

    plt.grid()
    plt.xlim((0, 1))
    plt.ylim((0, 1))
    plt.legend()
    plt.xlabel("TPR")
    plt.ylabel("FPR")
    plt.title("ROC curve")
    plt.show()


def plot_goal_rate(truth: list[int], probas: list[float], labels: list[str]):
    """
    Displays Goal rate curves for different models
    """

    for t, p, l in zip(truth, probas, labels):
        df = pd.DataFrame({"probability": p, "goal": t})
        percentiles = pd.qcut(df["probability"], q=100, duplicates="drop")
        goal_rate = df.groupby(percentiles).goal.mean()

        plt.plot(list(range(len(percentiles.unique()))), goal_rate, label=l)

    plt.ylim((0, 1))
    plt.xlim((0, 100))
    plt.xlabel("Model predicted shot probability percentile")
    plt.ylabel("Goal rate")
    plt.grid()
    plt.legend()
    plt.title("Goal rate by Probability percentile")
    plt.show()


def plot_goal_cumsum(truth: list[int], probas: list[float], labels: list[str]):
    for t, p, l in zip(truth, probas, labels):
        df = pd.DataFrame({"probability": p, "goal": t})
        percentiles = pd.qcut(df["probability"], q=100, duplicates="drop")
        grouped_goals = df.groupby(percentiles).goal.sum()
        proportion_goals = grouped_goals.cumsum() / grouped_goals.sum()

        plt.plot(list(range(len(percentiles.unique()))), proportion_goals, label=l)

    plt.ylim((0, 1))
    plt.xlim((0, 100))
    plt.xlabel("Model predicted shot probability percentile")
    plt.ylabel("Proportion")
    plt.grid()
    plt.legend()
    plt.title("Proportion of goals by Probability percentile")
    plt.show()


def plot_calibration(truth: list[int], probas: list[float], labels: list[str]):
    ax = plt.gca()
    for t, p, l in zip(truth, probas, labels):
        CalibrationDisplay.from_predictions(t, p, ax=ax, n_bins=40, label=l)


def plot_all(truth: list[int], probas: list[float], labels: list[str]):
    plot_roc(truth, probas, labels)
    plot_goal_rate(truth, probas, labels)
    plot_goal_cumsum(truth, probas, labels)
    plot_calibration(truth, probas, labels)