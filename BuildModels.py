from pickle import dump
from nltk.corpus import conll2002 as conll
import features
from inspect import getmembers, isfunction
from datetime import datetime as dt
import os
import sys
from custom_chunker import ConsecutiveNPChunker
from InputParser import parse_input


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


def train_model(feature, train_data, alg="IIS", tss=0, taf=False, folder="pickles"):
    """"Train a NER-tagger model and pickle them afterwards. Returns all models in a list

    Keyword arguments:
    alg -- The algorithm to use during training (Default = "IIS")
    train_data -- The data set to train the model with (Default = The ned.train data set from the nltk conll2002 corpus)
    tss -- The train sample size to use (Default = 0, which means the whole data set)
    taf -- Whether to train every feature (Default = False)
    folder -- Which folder to save the pickled model(s) in (Default = "pickles")
    """

    print()
    print("--------------------START TRAINING-----------------------")

    # Save all models in a list, if the user wants to evaluate without needing to unpickle
    models = []

    # Read all info of feature from the tuple
    feature_name = feature[0]
    feature_function = feature[1]

    # Train the model and inform the user on start time
    print("Training on", len(train_data), "samples, using",
          feature_name, " on algorithm", alg)
    start_time = dt.now()
    print("Training start time:", start_time.strftime('%d-%m-%Y %H:%M:%S.%f'))
    model = ConsecutiveNPChunker(feature_function,
                                 train_data, algorithm=alg)
    models.append(model)

    # Inform the user on the elapsed and end times
    end_time = dt.now()
    elapsed = end_time - start_time
    print("Training end time:", end_time.strftime('%d-%m-%Y %H:%M:%S.%f'), "(Elapsed:", elapsed, ")")

    pickle_model(model=model, folder=folder)

    return model


if __name__ == "__main__":

    if sys.argv[1] == "-h" or sys.argv[1] == "-help":
        help(train_model)

    elif len(sys.argv) > 1:
        args = parse_input()
        train_model(alg=args['alg'], tss=args['tss'], taf=args['taf'])
