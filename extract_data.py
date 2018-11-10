import numpy as np
from os import listdir
from os.path import isdir, isfile, join
from constants import *
import cv2


# Iterate through images in dir, converting them to 45x45 pixel arrays
# dir is the path to the folder, n is the #/character the folder represents
def grab_imgs(dir, n):
    max_examples = 2000
    size = min(max_examples, len(listdir(dir)))
    total_array = np.zeros((size, 45, 45))
    labels_vector = np.zeros((size, 1))
    labels_vector.fill(n)
    for ind, f in enumerate(listdir(dir)):
        if ind >= max_examples:
            break
        img = cv2.imread(join(dir, f), flags=cv2.IMREAD_GRAYSCALE)
        total_array[ind,:,:] = img


    # split data into test, validation, and training sets, based on parameters in constants file
    split_location = int(size * TEST_SPLIT)
    return total_array[split_location:,:,:], labels_vector[split_location:], total_array[:split_location,:,:], labels_vector[:split_location]


# Iterate through dir indexing data relating to the desired labels
def from_dir(dir):
    training_data = np.empty((0, 45, 45), int)
    training_labels = np.empty((0,1), int)
    test_data = np.empty((0, 45, 45), int)
    test_labels = np.empty((0,1), int)
    labels = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
              "+": 10, "-": 11, "times": 12, "div": 13, "forward_slash": 13, "=": 14}

    # iterate through each sub-directory
    if isdir(dir):
        chars_dir = [f for f in listdir(dir) if not f.startswith('.')]# if isdir(join(dir, f))]
        for dirs in chars_dir:
            if dirs in labels:
                new_train_matrix, new_train_labels, new_test_matrix, new_test_labels = grab_imgs(join(dir, dirs), labels[dirs])
                training_data = np.append(training_data, new_train_matrix, axis=0)
                training_labels = np.append(training_labels, new_train_labels)
                test_data = np.append(test_data, new_test_matrix, axis=0)
                test_labels = np.append(test_labels, new_test_labels)
                print("{} completed with {} in training and {} in test".format(dirs, len(training_labels), len(test_labels)))


    return training_data, training_labels, test_data, test_labels


if __name__ == "__main__":
    training_data, training_labels, test_data, test_labels = from_dir(PATH_TO_IMAGES)
    np.save(PATH_TO_SAVED + "training_data", training_data)
    np.save(PATH_TO_SAVED + "training_labels", training_labels)
    np.save(PATH_TO_SAVED + "test_data", test_data)
    np.save(PATH_TO_SAVED + "test_labels", test_labels)
