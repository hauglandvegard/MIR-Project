# import the necessary packages
import csv
import math
import numpy as np
from numpy.core import sqrt, add
from pathlib import Path


def square_rooted(x):
    """
    Function to calculate the root of the sum of all squared elements of a vector (iterable).
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    Returns
    -------
    square rooted : float
        Root of the sum of all squared elements of 'x'.
    """
    pass


def euclidean_distance(x, y):
    """
    Function to calculate the euclidean distance for two lists 'x' and 'y'.
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.
    Returns
    -------
    euclidean distance : float
        The euclidean distance between vectors `x` and `y`.
    Help
    -------
    https://pythonprogramming.net/euclidean-distance-machine-learning-tutorial/
    """
    result = 0

    for i in range(len(x)):
        result += (x[i] - y[i]) ** 2

    return sqrt(result)


def manhattan_distance(x, y):
    """
    Function to calculate the manhattan distance for two lists 'x' and 'y'.
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.
    Returns
    -------
    manhattan distance : float
        The manhattan distance between vectors `x` and `y`.
    """
    pass


def minkowski_distance(x, y, p):
    """
    Function to calculate the minkowski distance for two lists 'x' and 'y'.
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.
    p : int
        P-value.
    Returns
    -------
    minkowski distance : float
        The minkowski distance between vectors `x` and `y`.
    """
    pass


def cosine_similarity(x, y):
    """
    Function to calculate the cosine similarity for two lists 'x' and 'y'.
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.
    Returns
    -------
    cosine similarity : float
        The cosine similarity between vectors `x` and `y`.
    Help
    -------
        - Compute numerator
        - Compute denominator with the help of "square_rooted"
        - Calculate similarity
        - Change range to [0,1] rather than [-1,1]
    """
    pass


def cosine_distance(x, y):
    """
    Function to calculate the cosine distance for two lists 'x' and 'y'.
    Parameters
    ----------
    x : (N,) array_like
        Input array.
    y : (N,) array_like
        Input array.
    Returns
    -------
    cosine distance : float
        The cosine distance between vectors `x` and `y`.
    Help
    -------
        - Convert 'cosine similarity' to distance.
    """
    pass


class Searcher:

    def __init__(self, path_to_index):
        """
        Init function of the Searcher class. Sets 'path_to_index' to the class variable 'path_to_index'.
        Parameters
        ----------
        x : string
            Path to the index file.
        """
        self.__path_to_index = path_to_index

        pass

    def search(self, query_features):
        """
        Function retrieve similar images based on the queryFeatures
        Parameters
        ----------
        query_features : list
            List of features.
        Returns
        -------
        results : list
            List with the retrieved results (tuple). Tuple: First element is name and the second the distance of the image.
        Task
        -------
            - If there is no index file -> Print error and return False [Hint: Path(*String*).exists()]
            - Open the index file
            - Read in CSV file [Hint: csv.reader()]
            - Iterate over every row of the CSV file
                - Collect the features and cast to float
                - Calculate distance between query_features and current features list
                - Save the result in a dictionary: key = image_path, Item = distance
            - Close file
            - Sort the results according their distance
            - Return limited results
        """
        if not self.__path_to_index:
            return False

        result = []

        with open(self.__path_to_index, "r") as file:
            content = file.read()

            for line in content.split('\n'):
                features = line.split(';')

                image_path = features[0]
                del features[0]

                feature_list = [float(x) for x in features]

                distance = euclidean_distance(feature_list, query_features)

                if distance == 0 and image_path == '':
                    print('hello')

                result.append((image_path, distance))

        result.sort(key=lambda x: x[1])
        return result
