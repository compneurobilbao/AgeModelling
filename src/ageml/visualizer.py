"""Implement the data visualizer.

Used in the AgeML project to enable the plotting of modelling results.

Classes:
--------
Visualizer - manages the visualization of data and results.
"""

import matplotlib.pyplot as plt
import math
import numpy as np
import os

from sklearn.linear_model import LinearRegression

from .utils import insert_newlines, create_directory

class Visualizer:

    """Manages the visualization of data and results.

    This class uses matplotlib to plot results.

    Parameters
    -----------
    out_dir: path to output directory where to save results

    Public methods:
    ---------------

    age_distribution(self, Y): Plot age distribution.

    features_vs_age(self, X, Y, features_name): Plots correlation between features and age.

    true_vs_pred_age(self, y_true, y_pred): Plot true age vs predicted age.

    age_bias_correction(self, y_true, y_pred, y_corrected): Plot before and after age bias correction procedure.
    """

    def __init__(self, out_dir):
        """Initialise variables."""
        self.set_directory(out_dir)

    def set_directory(self, path):
        """Set directory to store results."""
        self.dir = path

    def age_distribution(self, Ys, labels=None, name=''):
        """ Plot age distribution.

        Parameters
        ----------
        Ys: 2D-Array with list of ages; shape=(m, n)."""

        # Plot age distribution
        for Y in Ys:
            plt.hist(Y, bins=20, alpha=1/len(Ys))
        if labels is not None:
            plt.legend(labels)
        plt.xlabel('Age (years)')
        plt.ylabel('Count')

        # Make diectory for saving the file
        path_for_fig = os.path.join(self.dir, 'figures')
        create_directory(path_for_fig)
        plt.savefig(os.path.join(path_for_fig, 'age_distribution_%s.svg' % name))
        plt.close()

    def features_vs_age(self, X, Y, corr, order, feature_names):
        """Plot correlation between features and age.

        Parameters
        ----------
        X: 2D-Array with features; shape=(n, m)
        Y: 1D-Array with age; shape=n
        corr: 1D-Array with correlation coefficients; shape=m
        order: 1D-Array with order of features; shape=m
        feature_names: list of names of features, shape=m"""

        # Show results
        nplots = len(feature_names)
        plt.figure(figsize=(14, 3 * math.ceil(nplots / 4)))
        for i, o in enumerate(order):
            plt.subplot(math.ceil(nplots / 4), 4, i + 1)
            plt.scatter(Y, X[:, o], s=15)
            plt.ylabel(insert_newlines(feature_names[o], 4))
            plt.xlabel('age (years)')
            plt.title("Corr:%.2f" % corr[o])
        plt.tight_layout()
        path_for_fig = os.path.join(self.dir, 'figures')
        create_directory(path_for_fig)
        plt.savefig(os.path.join(path_for_fig, 'features_vs_age.svg'))
        plt.close()

    def true_vs_pred_age(self, y_true, y_pred):
        """Plot true age vs predicted age.

        Parameters
        ----------
        y_true: 1D-Array with true age; shape=n
        y_pred: 1D-Array with predicted age; shape=n."""

        # Find min and max age range to fit in graph
        age_range = np.arange(np.min([y_true, y_pred]), np.max([y_true, y_pred]))

        # Plot true vs predicted age
        plt.scatter(y_true, y_pred)
        plt.plot(age_range, age_range, color='k', linestyle='dashed')
        plt.xlabel('True Age')
        plt.ylabel('Predicted Age')
        path_to_fig = os.path.join(self.dir, 'figures')
        create_directory(path_to_fig)
        plt.savefig(os.path.join(path_to_fig, 'true_vs_pred_age.svg'))
        plt.close()

    def age_bias_correction(self, y_true, y_pred, y_corrected):
        """Plot before and after age bias correction procedure.

        Parameters
        ----------
        y_true: 1D-Array with true age; shape=n
        y_pred: 1D-Array with predicted age before age bias correction; shape=n.
        y_corrected: 1D-Array with predicted age after age bias correction; shape=n"""

        # Find min and max age range to fit in graph
        age_range = np.arange(np.min([y_true, y_pred, y_corrected]),
                              np.max([y_true, y_pred, y_corrected]))

        # Before age-bias correction
        LR_age_bias = LinearRegression(fit_intercept=True)
        LR_age_bias.fit(y_true.reshape(-1, 1), y_pred)
        plt.subplot(1, 2, 1)
        plt.plot(age_range, age_range, color='k', linestyle='dashed')
        plt.plot(age_range, LR_age_bias.predict(age_range.reshape(-1, 1)), color='r')
        plt.scatter(y_true, y_pred)
        plt.title('Before age-bias correction')
        plt.ylabel('Predicted Age')
        plt.xlabel('True Age')

        # After age-bias correction
        LR_age_bias.fit(y_true.reshape(-1, 1), y_corrected)
        plt.subplot(1, 2, 2)
        plt.plot(age_range, age_range, color='k', linestyle='dashed')
        plt.plot(age_range, LR_age_bias.predict(age_range.reshape(-1, 1)), color='r')
        plt.scatter(y_true, y_corrected)
        plt.title('After age-bias correction')
        plt.ylabel('Predicted Age')
        plt.xlabel('True Age')
        plt.tight_layout()
        path_to_fig = os.path.join(self.dir, 'figures')
        create_directory(path_to_fig)
        plt.savefig(os.path.join(path_to_fig, 'age_bias_correction.svg'))
        plt.close()
