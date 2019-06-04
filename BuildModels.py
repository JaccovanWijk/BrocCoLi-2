from pickle import dump, load, Pickler
import os

def pickle_model(NER, folder="pickles", best=False):

    # Check if there is no picklefolder and make one
    last = "0"
    if not os.path.exists("./" + folder):
        os.makedirs("./" + folder)
    else:
        # If ther is a picklefolder, make sure old pickle are not overwritten
        old_pickles = sorted(os.listdir(path="./" + folder), reverse=True)
        if len(old_pickles) != 0:
            last = str(int(old_pickles[0].split(".")[0]) + 1)

    with open("./" + folder + "/" + last + ".pickle", "wb") as pickle:
        dump(NER, pickle)

    if best:
        with open("./best.pickle", "wb") as pickle:
            dump(NER, pickle)
