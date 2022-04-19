from hand_crafted_features import hand_crafted_features
# from ae import auto_encoder
from searcher import Searcher
import cv2
from pathlib import Path
import csv
import numpy as np

QUERY_IMAGE = 'images/3223.png'

class Query:

    def __init__(self, path_to_index):
        """
        Init function of the Query class. Sets 'path_to_index' to the class variable 'path_to_index'.
        Class variables 'query_image_name' and 'results' are set to None.
        Parameters
        ----------
        path_to_index : string
            Path to the index file.
        """
        self.__path_to_index = path_to_index
        self.__query_image_name = None
        self.__results = None
        self.__query_image = None
        self.__features = None

    def set_image_name(self, query_image_name):
        """
        Function to set the image name if it does not match the current one. Afterwards the image is loaded and features are retrieved.
        Parameters
        ----------
        query_image_name : string
            Image name of the query. For example: 'static/images/query/test.png'
        Tasks
        ---------
            - Check if 'query_image_name' is different to 'self.query_image_name'
            - If yes:
                - Set 'self.results' to None
                - Overwrite 'query_image_name'
                - Read in the image and save it under 'self.query_image'
                - Calculate features
        """
        if query_image_name == self.__query_image_name:
            return False

        self.__results = None
        self.__query_image_name = query_image_name
        self.__query_image = cv2.imread(self.__query_image_name, cv2.IMREAD_GRAYSCALE)
        self.calculate_features()

    def calculate_features(self):
        """
        Function to calculate features for the query image.
        Tasks
        ---------
            - Check if "self.query_image" is None -> exit()
            - Extract features with "FeatureExtractor" and set to "self.features"
        """
        extractor = hand_crafted_features()
        self.__features = extractor.extract(self.__query_image)

    def run(self, limit=10):
        """
        Function to start a query if results have not been computed before.
        Parameters
        ----------
        limit : int
            Amount of results that will be retrieved. Default: 10.
        Returns
        -------
        - results : list
            List with the 'limit' first elements of the 'results' list. 

        Tasks
        ---------
            - Check if 'self.results' is None
            - If yes:
                - Create a searcher and search with features
                - Set the results to 'self.results'
            - Return the 'limit' first elements of the 'results' list.
        """
        if self.__results is None:
            my_searcher = Searcher(self.__path_to_index)
            self.__results = my_searcher.search(self.__features)

        return self.__results[:limit]


if __name__ == "__main__":
    query = Query(path_to_index="static/features.csv")
    query.set_image_name(query_image_name=QUERY_IMAGE)
    query_result = query.run()
    print("Retrieved images: ", query_result)
