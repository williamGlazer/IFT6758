from typing import Tuple
import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
#from matplotlib.ticker import LinearLocator
import seaborn as sns

GOAL_COORDINATES = [(-89, 0), (89, 0)]

class NHLSimpleVisualization:
    """
    Class to create simple visualizations from a single pandas
    dataframe created with NHLCleaner. One instance corresponds
    to one dataframe, in turn corresponding to one season.
    
    Examples
    --------
    df = NHLCleaner.format_season("data/20162017.json")
    sv = NHLSimpleVisualization(df)
    sv.shot_types(path="figures/q5-1.png", title="Shots taken and goals scored by type (2016-2017)")
    sv.shot_type_and_distance(path="figures/q5-3.png", title="Proportion of successful shots by type and distance (2016-2017)")
    for (s, e) in [("2018", "2019"), ("2019", "2020"), ("2020", "2021")]:
        df = NHLCleaner.format_season(f"data/{s}{e}.json")
        sv = NHLSimpleVisualization(df)
        sv.shot_distance(path=f"figures/q5-2-{s}{e}.png", title=f"Proportion of successful shots by distance ({s}-{e})")
    """
    
    df  = None
    dpi = None
    
    fig_counter = 0
    
    def __init__(self, df: pd.DataFrame, seaborn: bool = True, dpi : int = 300) -> None:
        """
        Parameters
        ----------
        df : pd.DataFrame
            A pandas dataframe created by NHLCleaner.
        seaborn : bool
            Whether to use Seaborn
        dpi : int
            Resolution for saved figures
        """
        self.df = df
        if seaborn:
            sns.set()
    
    def _get_fig_counter() -> int:
        # get and increment a static counter for use with plt.figure()
        i = __class__.fig_counter
        __class__.fig_counter += 1
        return i
    
    def shot_types(self, path: str = None, label1: str = "Shots", label2: str = "Goals",
                   color1: str = "b", color2: str = "g",
                   xlabel: str = "Shots taken or goals scores",
                   ylabel: str = "Shot type",
                   title: str = "Shots taken and goals scored by type",
                   rotation: int = 45) -> None:
        """
        Creates the visualization of question 5.1 and saves it to a file.
        
        Parameters
        ----------
        path : str
            The path and file name where to save the visualization
            (if not provided, will use matplotlib.pyplot.show())
        label1 : str
            Legend label for shots
        label2 : str
            Legend label for goals
        color1 : str
            Bar colour for shots
        color2 : str
            Bar colour for goals
        xlabel : str
            Label for x axis
        ylabel : str
            Label for y axis
        title : str
            Title for figure
        rotation : int
            Rotation to apply to tick values of x axis
        """
        gb = self.df[["shot type", "goal"]].groupby(["shot type"]).agg(goals=("goal", "sum"), shots=("goal", "count"))
        plt.figure(__class__._get_fig_counter())
        plt.bar(gb.index, gb["shots"], label=label1, color=color1)
        plt.bar(gb.index, gb["goals"], label=label2, color=color2)
        plt.xticks(rotation = rotation)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        if path is None:
            plt.show()
        else:
            plt.savefig(path, dpi = self.dpi, bbox_inches = "tight")
        plt.clf()

    @staticmethod
    def _get_distance(src: Tuple[float, float]) -> float:
        # cheap trick: because we don't know in which net we are shooting,
        # we will just try both and pick the minimum
        if np.isnan(src[0]) or np.isnan(src[1]):
            return None
        else:
            candidates = np.array([distance.euclidean(src, tgt) for tgt in GOAL_COORDINATES])
            return candidates.min()
            

    def shot_distance(self, path: str = None, bins = 10,
                      bin_labels = None,
                      right: bool = True, draw: bool = True,
                      color: str = "b",
                      xlabel: str = "Distance",
                      ylabel: str = "Proportion of successful shots",
                      title: str = "Proportion of successful shots by distance",
                      rotation: int = 90) -> None:
        """
        Creates a visualization of question 5.2 and saves it to a file.
        
        Parameters
        ----------
        path : str
            The path and file name where to save the visualization
        bins : (see pandas.cut documentation)
            Passed on to pandas.cut as its "bins" argument
        bin_labels : (see pandas.cut documentation)
            Passed on to pandas.cut as its "labels" argument
        right : bool
            Wether to use right-open or right-closed intervals for the bins
        draw : bool
            Whether to draw the plot
        color : str
            Bar colour
        xlabel : str
            Label for x axis
        ylabel : str
            Label for y axis
        title : str
            Title for figure
        rotation : int
            Rotation to apply to tick values of x axis
        """
        self.df["distance"] = self.df.apply(lambda x: __class__._get_distance((x["x_coords"], x["y_coords"])), axis=1)
        # cast category as str makes it easier to use it in the plot
        self.df["distance cut"] = pd.cut(self.df["distance"], bins=bins, labels=bin_labels, right=right).astype("str")
        gb = self.df[["distance cut", "goal"]].groupby(["distance cut"]).agg(goals=("goal", "sum"), shots=("goal", "count")).drop("nan", errors="ignore")
        if draw:
            plt.figure(__class__._get_fig_counter())
            plt.bar(gb.index, gb["goals"]/gb["shots"], color=color)
            plt.xticks(rotation = rotation)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            if path is None:
                plt.show()
            else:
                plt.savefig(path, dpi = self.dpi, bbox_inches = "tight")
            plt.clf()
        

    def shot_type_and_distance(self, path: str = None, bins: int = 10, right: bool = True,
                      cmap: ListedColormap = cm.viridis,
                      xlabel: str = "Distance",
                      ylabel: str = "Type",
                      zlabel: str = "Proportion of successful shots",
                      title: str = "Proportion of successful shots by type and distance") -> None:
        """
        Creates the visualization of question 5.3 and saves it to a file.
        
        Parameters
        ----------
        path : str
            The path and file name where to save the visualization
        bins : int
            How many bins to split the distance in
        right : bool
            Wether to use right-open or right-closed intervals for the bins
        cmap : matplotlib.colors.ListedColormap
            Surface colour map
        xlabel : str
            Label for x axis
        ylabel : str
            Label for y axis
        zlabel : str
            Label for z axis
        title : str
            Title for figure
        """
        # compute distance stuff if shot_distance() was not called before
        if "distance" not in self.df.columns:
            self.shot_distance(bins = bins, right = right, draw = False)

        new_df = self.df[["shot type", "goal", "distance cut"]].pivot_table(index="shot type", columns="distance cut", values="goal", aggfunc="mean").drop("nan", axis=1).ffill()

        # the matplotlib stuff here is taken mostly from
        # https://matplotlib.org/stable/gallery/mplot3d/surface3d.html
        plt.figure(__class__._get_fig_counter())
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        # plot_surface will not accept strings: https://stackoverflow.com/q/41960448/2025742
        X = np.arange(len(new_df.columns))
        Y = np.arange(len(new_df.index))

        X, Y = np.meshgrid(X, Y)
        Z = new_df.to_numpy()
        surf = ax.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=True)
        ax.set_zlim(0, 1)
        #ax.zaxis.set_major_locator(LinearLocator(10))
        #ax.zaxis.set_major_formatter('{x:.02f}')
        fig.colorbar(surf)
        ax.set_xticklabels(new_df.columns)
        ax.set_yticklabels(new_df.index)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        plt.title(title)
        if path is None:
            plt.show()
        else:
            plt.savefig(path, dpi = self.dpi, bbox_inches = "tight")
        plt.clf()
        plt.cla()
