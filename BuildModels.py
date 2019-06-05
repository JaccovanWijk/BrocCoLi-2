from pickle import dump, load, Pickler
from nltk.corpus import conll2002 as conll
import features
from inspect import getmembers, isfunction
import time
import os
from custom_chunker import ConsecutiveNPChunker


def pickle_model(model, folder="pickles"):
    """"Pickle a given model and put in a specified folder name"""

    last = "0"

    # If the specified folder does not exist, create it
    if not os.path.exists("./" + folder):
        os.makedirs("./" + folder)

    # If there is a pickle-folder, make sure old pickle are not overwritten
    else:
        old_pickles = sorted(os.listdir(path="./" + folder), reverse=True)
        if len(old_pickles) != 0:
            last = str(int(old_pickles[0].split(".")[0]) + 1)

    # Pickle the model and give it a proper name
    with open("./" + folder + "/" + last + ".pickle", "wb") as pickle:
        dump(model, pickle)


def train_model(alg="IIS", train_data=conll.chunked_sents("ned.train"), tss=0, taf=False, folder="pickles"):
    """"Train a NER-tagger model and pickle them afterwards. Returns all models in a list

    Keyword arguments:
    alg -- The algorithm to use during training (Default = "IIS")
    train_data -- The data set to train the model with (Default = The ned.train data set from the nltk conll2002 corpus)
    tss -- The train sample size to use (Default = 0, which means the whole data set)
    taf -- Whether to train every feature (Default = False)
    folder -- Which folder to save the pickled model(s) in
    """

    # Save all models in a list, if the user wants to evaluate without needing to unpickle
    models = []

    # Resize the testing size if necessary
    if 0 < tss < len(train_data):
        train_data = conll.chunked_sents("ned.train")[:tss]

    all_features = getmembers(features, isfunction)  # Get all feature functions from module features
    all_features = sorted(all_features, key=lambda y: y[0])  # Sort them so the oldest feature comes first

    # If we only want to test the newest feature, create a list with only that feature method in it
    if not taf:
        all_features = [all_features[len(all_features) - 1]]

    print()
    print("--------------------START TRAINING-----------------------")

    # Loop trough all features we want to check
    for feature in all_features:

        # Train the model and inform the user on start time
        print("Training on", len(train_data), "samples, using", feature[0], " on algorithm", alg)
        start_time = time.time()
        print("Training start time:", time.asctime(time.localtime(start_time)))
        model = ConsecutiveNPChunker(feature[1], train_data, algorithm=alg)
        models.append(model)

        # Inform the user on the elapsed and end times
        end_time = time.time()
        elapsed = end_time - start_time
        print("Training end time:", time.asctime(time.localtime(elapsed)), "(Elapsed:", round(elapsed, 2), ")")

        pickle_model(model=model, folder=folder)

    return models
