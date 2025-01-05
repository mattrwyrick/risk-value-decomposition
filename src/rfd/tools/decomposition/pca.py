
import numpy as np
import pandas as pd

from sklearn.decomposition import PCA, FastICA
from sklearn.preprocessing import StandardScaler

from rfd.settings import SEED


def get_pca_components(df, n_components=1, seed=SEED, include_meta=True):
    """
    Get the principal components from the df
    :param df:
    :param n_components:
    :param seed:
    :param include_meta:
    :return:
    """
    if SEED:
        np.random.seed(seed)
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(df)

    if include_meta:
        loadings = pca.components_
        explained_variance = pca.explained_variance_ratio_
        return principal_components, loadings, explained_variance
    else:
        return principal_components


def get_ica_components(df, n_components=1, seed=SEED, include_meta=True):
    """
    Get the independent components from the df
    :param df:
    :param n_components:
    :param seed:
    :param include_meta:
    :return:
    """
    if SEED:
        np.random.seed(seed)
    pca = FastICA(n_components=n_components)
    principal_components = pca.fit_transform(df)

    if include_meta:
        loadings = pca.components_
        return principal_components, loadings, None
    else:
        return principal_components


def get_optimal_n_components(df, seed=SEED):
    """
    Detect the optimal number of components to use
    :param df:
    :param seed:
    :return:
    """
    if SEED:
        np.random.seed(seed)

    pca = PCA()
    scaler = StandardScaler()

    df_scaled = scaler.fit_transform(df)
    pca.fit(df_scaled)

    explained_variance = pca.explained_variance_ratio_
    second_derivative = np.diff(np.diff(explained_variance))
    elbow_point = np.argmax(second_derivative) + 2  # +2 because we took the second derivative

    return elbow_point



