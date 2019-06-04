from custom_chunker import ConsecutiveNPChunker
from nltk.corpus import conll2002 as conll
import nltk
import features
import BuildModels as Bm
import EvaluateModels as Em
import sys
from inspect import getmembers, isfunction


def main(algorithm="IIS", train_sample_size=0, test_all_features=False):
    """" The main method for using the NER-tagger.
    This method trains a model, tests it and pickles the result.
    This method also prints evaluation scores.

    Keyword arguments:

    algorithm -- The name of the algorithm to use. Must be one of ["IIS", "GIS", "NaiveBayes"]. (Default = IIS)
    The flag to set this can be -a or -alg or -algorithm in the command line

    train_sample_size -- The number of training samples to use as an integer.
    Must be between 0 and the length of the conll ned.train. (Default = full ned.train)
    To set this, use flag -tss or -train_sample_size in the command line

    test_all_features -- Boolean, whether to test all features after each other on alphabetical order.
    This argument can be usefull when implementing multiple new features in between testing to visualize improvement.
    If set to False, will force the NER-tagger to train on the most recent feature instead of all.
    To set this, ust flag -taf or -test_all_features in the command line.
    """

    # Set the training and testing samples
    training = conll.chunked_sents("ned.train")
    testing = conll.chunked_sents("ned.testa")

    # Resize the testing size if necessary
    if 0 < train_sample_size < len(training):
        training = conll.chunked_sents("ned.train")[:train_sample_size]

    best = 0

    all_features = getmembers(features, isfunction)  # Get all feature functions from module features
    all_features = sorted(all_features, key=lambda y: y[0])  # Sort them so the oldest feature comes first

    # If we only want to test the newest feature, create a list with only that feature method in it
    if not test_all_features:
        all_features = [all_features[len(all_features) - 1]]

    for feature in all_features:
        print("---------------------------------------------------------")
        print("Training on", len(training), "samples, using", feature[0], " on algorithm", algorithm)
        model = ConsecutiveNPChunker(feature[1], training, algorithm=algorithm)

        print("Evaluating on", len(testing),"samples...")
        score = Em.evaluate_model(model, testing, raw=True)
        #print(em.evaluate_model(model, testing, raw=True))

        print(score)
        average = weighted_average(score)  # Calculate the weighted average score

        # If we are doing better...
        if average > best:
            Bm.pickle_model(model, best=True)  # Pickle the model!
            print("Current model is the best one yet!")
            best = average  # Update our 'old' best with our current best

        # Otherwise, just pickle the model
        else:
            Bm.pickle_model(model)


def print_score(score, previous):

    # Check if our score is a float or an int, and our previous is as well
    if isinstance(score, float) or isinstance(score, int) and isinstance(score, previous):
        if score > previous:
            print("Score:", round(score, 3), "(+)")
        else:
            print(1)
    elif isinstance(score, nltk.chunk.util.ChunkScore):
        print(
            "Accuracy:", round(score.accuracy(), 3),
            "Precision:", round(score.precision(), 3),
            "Recall:", round(score.recall(), 3),
            "F-Measure", round(score.f_measure(), 3)
        )


def weighted_average(score, weights=(1, 1, 1, 1)):
    """Calculate score using weighted average.

    Keyword arguments:
    score -- The score of type nltk.chunck.util.ChunckScore on which to compute the average. (Required)
    weights -- The weights associated with each of the 4 performance metrics. (Optional, default = (1, 1, 1, 1))

    This method is not meant to be called directly. This is a helper function to the main() function.
    """
    average = weights[0] * score.accuracy()
    average += weights[1] * score.precision()
    average += weights[2] * score.recall()
    average += weights[3] * score.f_measure()
    return average/sum(weights)

def parse_input():
    """Reads the commandline input arguments and uses it's contents to call the main method.
    Please note that this method ignores any invalid flags.
    """

    alg = "IIS"
    tss = 0
    taf = False

    # Loop trough all arguments and save them accordingly. Skip the first, because that's the module name.
    for i in range(1, len(sys.argv)):
        flag = sys.argv[i]

        # If the user wants to specify an algorithm
        if flag == "-a" or flag == "-alg" or flag == "-algorithm":

            # Throw an exception if the user does not specify an algorithm after passing the flag
            try:
                alg = sys.argv[i + 1]
            except IndexError:
                raise IndexError("Please specify an algorithm after using the " + flag + " flag.")

            # Throw an exception if the user does not specify an admissible algorithm
            if alg.lower() not in ["iis", "gis", "nb", "naivebayes"]:
                raise ValueError(alg + " is not a valid algorithm.")

            # If the user is lazy and doesn't want to type NaiveBayes fully
            elif alg.lower() == "nb":
                alg = "NaiveBayes"

        # If the user wants to specify the train sample size
        elif flag == "-tss" or flag == "-train_sample_size":

            # Throw an exception if the user doesn't specify a valid training size after passing the flag
            try:
                tss = sys.argv[i + 1]
            except IndexError:
                raise IndexError("Please specify a training size after passing the " + flag + " flag.")

            try:
                tss = int(tss)
            except ValueError:
                raise ValueError(tss, "is not an integer. Only integers can be used as a training size.")

            # Notify the user of an negative training size
            if tss < 0:
                print("You tried to specify a negative training size.",
                      "That doesn't make the training any faster, you know.",
                      "We will use the full train sample set instead.")
                tss = 0

        elif flag == "-taf" or flag == "-test_all_features":
            taf = True

    main(algorithm=alg, train_sample_size=tss, test_all_features=taf)


if __name__ == "__main__":

    # If the user does not specify any arguments, they probably need some help.
    if len(sys.argv) <= 1:
        print("Oops! You did not specify any arguments. See the help below for more info.")
        help(main)

    # If the user asks for help, print the help statement
    elif "-h" in sys.argv or "-help" in sys.argv:
        help(main)

    else:
        parse_input()


