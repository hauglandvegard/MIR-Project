import glob
from console_tools import print_progress_bar
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Flatten
from keras.models import Model
from keras import backend as K
from keras.models import load_model
from keras import optimizers
from keras_preprocessing.image import load_img
import numpy as np
import cv2
import matplotlib.pyplot as plt
from pathlib import Path


def get_images_paths(image_directory, file_extensions=(".png", ".jpg")):
    '''
    Copied from preprocessing file
    '''
    # Initialize a empty list of image paths
    image_paths = []

    # For every file extension
    for file_extension in file_extensions:
        # Create a pattern string 
        image_pattern = image_directory + "*" + file_extension
        # Add all paths to images matching the pattern to the list
        image_paths.extend(glob.glob(image_pattern))

    # Return the list with all image paths
    return image_paths


def load_gray_normalized(image_path, shape=(28, 28)):
    # Reading image
    img = cv2.imread(image_path)

    # Resizing
    img = cv2.resize(img, shape)

    # Converting to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Normalizing image
    zeros = np.zeros(img.shape)
    img = img.astype('float64')
    img = cv2.normalize(img, zeros, 0, 1, cv2.NORM_MINMAX)

    return img


class auto_encoder():
    epochs = 200
    encoder_name = 'static/auto_encoder_model/encoder_{}_epochs.h5'.format(epochs)
    ae_name = 'static/auto_encoder_model/ae_{}_epochs.h5'.format(epochs)
    database = "website/static/data/images/training/"
    image_size = (256, 256)

    def __init__(self):

        if not Path(self.ae_name).exists() or not Path(self.ae_name).exists():
            # TODO: get all image paths
            image_paths = get_images_paths(self.database)

            # TODO: read in images and create numpy for keras
            images = np.empty((len(image_paths), 28, 28))

            for idx, path in enumerate(image_paths):
                print_progress_bar(iteration=idx,
                                   total=len(image_paths) - 1,
                                   header='Reading in images...',
                                   footer='All images read!')

                images[idx] = load_gray_normalized(path)

            print(images.shape)
            print(images[0])

            # TODO: train model (function call)

            # TODO: save model (function call)

            pass
        else:
            # TODO: load autoencoder and encoder from file
            pass

    def train_model(self):
        # TODO: Create
        # create input
        visible = Input(shape=(28, 28, 1))

        # apply layers
        conv1 = Conv2D(32, kernel_size=4, activation='relu')(visible)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

        # flatten
        flat = Flatten()(pool1)

        # apply hidden layer
        hidden1 = Dense(10, activation='relu')(flat)

        # Create output
        output = Dense(num_classes, activation="softmax")(hidden1)

        # create model
        model = Model(inputs=visible, outputs=output)

        # TODO: compile
        model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

        # TODO: Fit
        model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)
        score = model.evaluate(x_test, y_test, verbose=0)

        # TODO: set self.autoencoder

        # TODO: set self.encoder

        pass

    def save_models(self):
        self.encoder.save(self.encoder_name)
        self.autoencoder.save(self.ae_name)

    def extract(self, x):
        # TODO: use self.encoder to return features
        pass

    def visualize_example(self, input_image):
        # TODO: visualize input and output image of your autoencoder (self.autoencoder)
        # Display original
        ax = plt.subplot(2, 1, 1)
        plt.imshow(input_image)
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # Display reconstruction
        ax = plt.subplot(2, 1, 2)
        plt.imshow(input_image)
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        plt.show()
        pass


if __name__ == '__main__':
    input_name = "website/static/data/images/full/371876.png"
    input_image = np.array(
        cv2.resize(cv2.imread(input_name, cv2.IMREAD_GRAYSCALE), (256, 256), interpolation=cv2.INTER_AREA))

    ae = auto_encoder()
    ae.visualize_example(input_image)
