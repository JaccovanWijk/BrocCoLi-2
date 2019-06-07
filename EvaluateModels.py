import os
from pickle import load
from nltk.corpus import conll2002 as conll
import sys
import time


def evaluate_model(model, testdata=conll.chunked_sents("ned.testa")):
    """ Evaluate a given model on test data and print the results """

    print("-------------------START EVALUATING----------------------")

    # Inform the user when the evaluation has started
    start_time = time.time()
    print("Evaluating on", len(testdata), "samples. Start time: ", time.asctime(time.localtime(start_time)))

    # Evaluate the model and print the score
    score = model.evaluate(testdata)
    print(score)

    # Inform the user of the elapsed and time times
    end_time = time.time()
    elapsed = end_time - start_time
    print("End time:", time.asctime(time.localtime(elapsed)), "(Elapsed:", round(elapsed, 2), ")")

    #print(score.missed())


def evaluate_pickle(path):
    """ Unpickle a model to evaluate, given a path to the pickled model

    Keyword arguments:
    path -- The absolute or relative path to the pickled model. (Required)
    """

    with open(path, "rb") as file:
        model = load(file)
        evaluate_model(model)


def evaluate_all_pickles(path="./pickles"):
    """" Evaluate all pickled models in a folder, given the path to that folder.
    This function is called when using the module as the main module.

    Keyword arguments:
    path -- The absolute or relative to the folder containing the pickled models. (Default: "./pickles")
    Use the flag -p or -path when running this module as the main module to specify a path
    """

    # Check if the specified path exists at all
    if os.path.exists(path):

        # Collect all pickle files
        files = [x for x in os.listdir(path=path) if x.endswith(".pickle")]

        # If there are no pickle files in the specified folder, raise an error
        if len(files) == 0:
            raise ValueError("No pickled files found in the specified folder. Please try another path.")
        else:
            # Unpickle all pickled files
            print("Found", len(files), "pickled models.")
            for file in files:
                if file.endswith(".pickle"):
                    evaluate_pickle(path + "/" + file)

    # If not, raise an error
    else:
        raise ValueError("The path " + path + " does not exist.")


def evaluated_models(models):
    """Convenience function to evaluate multiple models"""

    print()
    print("-------------------START EVALUATION----------------------")
    for model in models:
        evaluate_model(model)
        print("-------------------------------------------------------")


if __name__ == "__main__":

    # If the user did not specify any command line arguments
    if len(sys.argv) <= 1:
        raise ValueError("Argument -path and a correct path are required")

    # If the user wants to specify a path
    elif sys.argv[1] == "-p" or sys.argv[1] == "-path":

        # Try to get the path from the command line
        try:
            path = sys.argv[2]
        except IndexError:
            raise IndexError("Please specify a path after using the", sys.argv[1], "flag")

        # Evaluate all pickles next
        evaluate_all_pickles(path=path)

    # If the user wants help
    elif sys.argv[1] == "-h" or sys.argv[1] == "-help":
        help(evaluate_all_pickles)
