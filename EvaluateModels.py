from os import listdir
from pickle import load
from nltk.corpus import conll2002 as conll
import time


def evaluate_model(model, testdata=conll.chunked_sents("ned.testa")):
    """ Evaluate a given model on test data and print the results """

    # Inform the user when the evaluation has started
    start_time = time.time()
    print("Evaluating on", len(testdata), "samples. Start time: ", start_time)

    # Evaluate the model and print the score
    score = model.evaluate(testdata)
    print(score)

    # Inform the user of the elapsed and time times
    end_time = time.time()
    elapsed = end_time - start_time
    print("End time:", time.asctime(time.localtime(elapsed)), "(Elapsed:", round(elapsed, 2), ")")

    print(score.missed())

def evaluate_pickle(path):
    """ Helper function to unpickle a model to evaluate, given a path to the pickled model """
    with open(path, "rb") as file:
        model = load(file)
        evaluate_model(model)


def evaluate_all_pickles(path="./pickles"):
    """" Helper function to evaluate all pickled models in a folder, given the path to that folder"""
    for file in listdir(path):
        if file.endswith(".pickle"):
            evaluate_pickle(path + "/" + file)


def evaluated_models(models):
    """Convenience function to evaluated multiple models"""

    for model in models:
        print()
        print("-------------------START EVALUATION----------------------")
        evaluate_model(model)
