from pickle import dump
from datetime import datetime as dt
import os
import sys
import features
from nltk.corpus import conll2002 as conll
from custom_chunker import ConsecutiveNPChunker
from InputParser import parse_input
from inspect import getmembers, isfunction


def pickle_model(model, folder="pickles"):
    """"Pickle a given model and put in a specified folder name"""

    last = "0"

    # If the specified folder does not exist, create it
    if not os.path.exists("./" + folder):
        os.makedirs("./" + folder)

    # If there is a pickle-folder, make sure old pickle are not overwritten
    else:
        # Get all pickles already the folder and sort them. That way, we know which name to pick next
        old_pickles = [x for x in sorted(os.listdir(path="./" + folder), reverse=True) if x.endswith(".pickle")]
        if len(old_pickles) != 0:
            last = str(int(old_pickles[0].split(".")[0]) + 1)

    # Pickle the model and give it a proper name
    with open("./" + folder + "/" + last + ".pickle", "wb") as pickle:
        dump(model, pickle)


def train_model(feature, train_data=conll.chunked_sents("ned.train"), alg="IIS", folder="pickles"):
    """"Train a NER-tagger model and pickle it afterwards. Returns the trained model.

    Keyword arguments:

    alg -- The name of the algorithm to use.
    Must be one of ["IIS", "GIS", "NaiveBayes"] (Default = IIS).
    The flag to set this can be -a , -alg or -algorithm in the command line

    folder -- Which folder to save the pickled model(s) in (Default = "pickles")
    """

    print()
    print("--------------------START TRAINING-----------------------")

    # Read all info of feature from the tuple
    feature_name = feature[0]
    feature_function = feature[1]

    # Train the model and inform the user on start time
    print("Training on", len(train_data), "samples, using",
          feature_name, " on algorithm", alg)
    start_time = dt.now()
    print("Training start time:", start_time.strftime('%d-%m-%Y %H:%M:%S.%f')[:-3])
    model = ConsecutiveNPChunker(feature_function,
                                 train_data, algorithm=alg)

    # Inform the user on the elapsed and end times
    end_time = dt.now()
    elapsed = end_time - start_time
    print("Training end time:", end_time.strftime('%d-%m-%Y %H:%M:%S.%f')[:-3], "(Elapsed:", str(elapsed)[:-3] + ")")

    pickle_model(model=model, folder=folder)

    return model


if __name__ == "__main__":

    if sys.argv[1] == "-h" or sys.argv[1] == "-help":
        help(train_model)

    elif len(sys.argv) > 1:
        args = parse_input()

        all_features = getmembers(features, isfunction)  # Get all feature functions from module features

        # Sort them by name so the oldest feature comes first
        all_features_sorted = sorted(all_features, key=lambda y: y[0], reverse=True)

        print(all_features_sorted)
        most_recent_feature = all_features_sorted[0]

        train_model(alg=args['alg'], feature=all_features)
