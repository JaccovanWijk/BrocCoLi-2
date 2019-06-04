from os import listdir
from pickle import load

def evaluate_model(model, testdata, raw=False):
    """ Calculate the average score OR give all raw scores of a model """
    if raw:
        return model.evaluate(testdata)
    else:
        cs = model.evaluate(testdata)
        scores = [
            cs.accuracy(),
            cs.f_measure(),
            cs.precision(),
            cs.recall()
        ]
        return sum(scores)/float(len(scores))

def evaluate_pickle(path):
    """ Helper function to unpickles a model to evaluate """
    with open(path, "rb") as file:
        model = load(file)
        evaluate_model(model)

def evaluate_all_pickles(path):
    """" Helper function to evaluate all pickled models in a folder """
    for file in listdir(path):
        if file.endswith(".pickle"):
            evaluate_pickle(path + "/" + file)
