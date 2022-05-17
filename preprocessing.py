import cv2
from hand_crafted_features import hand_crafted_features
import numpy as np
import glob
import sys
import os
from console_tools import *

IMAGES_DIR = 'website/static/data/images/training'


def get_images_paths(image_directory, file_extensions: [str]):
    """
    Function to receive every path to a file with ending "file_extension" in directory "image_directory".
    Parameters
    ----------
    image_directory : string
        Image directory. For example: 'static/images/database/'
    Returns
    -------
    - image_paths : list
        List of image paths (strings).
    Tasks
    -------
        - Iterate over every file_extension
            - Create a string pattern 
            - Use glob to retrieve all possible file paths (https://docs.python.org/3.7/library/glob.html )
            - Add the paths to a list  (extend)
        - Return result
        :param file_extensions:
        :param image_directory:
    """
    if file_extensions is None:
        file_extensions = ['png']
    allowed_ext = ['png', 'jpg']

    if not all([(ext.lower() in allowed_ext) for ext in file_extensions]):
        valid = ', '.join(allowed_ext)
        print(f'Invalid extension in list {file_extensions}. Valid extensions are: {valid}')
        return []

    images_paths = os.listdir(image_directory)

    images_full_path = []

    for image_path in images_paths:
        if image_path.split('.')[-1] in file_extensions:
            images_full_path.append(f'{image_directory}/{image_path}')

    return images_full_path


def create_feature_list(image_paths: [str]):
    """
    Function to create features for every image in "image_paths".
    Parameters
    ----------
    image_paths : list
        Image paths. List of image paths (strings).
    Returns
    -------
    - result : list of lists.
        List of 'feature_list' for every image. Each image is summarized as list of several features.
    Tasks
    -------
        - Iterate over all image paths
        - Read in the image
        - Extract features with class "feature_extractor"
        - Add features to a list "result"
    """
    result = []

    extractor = hand_crafted_features()

    for idx, path in enumerate(image_paths):
        print_progress_bar(iteration=idx,
                           total=len(image_paths) - 1,
                           header='Creating feature list:',
                           footer='Feature list created!')

        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        features = extractor.extract(img)
        result.append(features)

    return result


def write_to_file(feature_list, image_paths, output_path):
    """
    Function to write features into a CSV file.
    Parameters
    ----------
    feature_list : list
        List with extracted features. Should come from 'create_feature_list':
    image_paths : list
        Image paths. List of image paths (strings). Should come from 'get_images_paths':
    output_path : string
        Path to the directory where the index file will be created.
    Tasks
    -------
        - Open file ("output_name")
        - Iterate over all features (image wise)
        - Create a string with all features concerning one image seperated by ","
        - Write the image paths and features in one line in the file [format: image_path,feature_1,feature_2, ..., feature_n]
        - Close file eventually

        - Information about files http://www.tutorialspoint.com/python/file_write.htm 
    """
    file_path = output_path + os.sep + "features.csv"

    with open(file_path, "w") as file:
        for idx, features in enumerate(feature_list):
            print_progress_bar(iteration=idx,
                               total=len(feature_list) - 1,
                               header='Writing to file:',
                               footer='Write complete!')

            if not idx == 0:
                file.write('\n')

            output = image_paths[idx]

            for feature in features:
                output += ';' + str(feature)

            file.write(output)


def preprocessing_main(image_directory, output_path, file_extensions=("png", "jpg")):
    """
    Function which calls 'get_images_paths', 'create_feature_list' and 'write_to_file'
    """

    image_paths = get_images_paths(image_directory, file_extensions)

    feature_list = create_feature_list(image_paths)

    write_to_file(feature_list, image_paths, output_path)


if __name__ == '__main__':
    print(IMAGES_DIR)
    preprocessing_main(image_directory=IMAGES_DIR, output_path="website/static/data")
