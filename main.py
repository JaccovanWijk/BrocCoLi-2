import nltk
import BuildModels as Bm
import EvaluateModels as Em
import sys


def main(algorithm="IIS", train_sample_size=0, test_all_features=False):
    """" The main method for using the NER-tagger.
    This method trains, pickles and evaluates the models, skipping the unpickling part for efficiency
    This method is faster and easier than using EvaluateModels and BuildModels, but has less options

    Keyword arguments:

    algorithm -- The name of the algorithm to use. Must be one of ["IIS", "GIS", "NaiveBayes"]. (Default = IIS)
    The flag to set this can be -a or -alg or -algorithm in the command line

    train_sample_size -- The number of training samples to use as an integer.
    Must be between 0 and the length of the conll ned.train. (Default = full ned.train)
    To set this, use flag -tss or -train_sample_size in the command line

    test_all_features -- Boolean, whether to test all features after each other on alphabetical order.
    This argument can be useful when implementing multiple new features in between testing to visualize improvement.
    If set to False, will force the NER-tagger to train on the most recent feature instead of all.
    To set this, ust flag -taf or -test_all_features in the command line.
    """

    # Train model(s) and pickle them.
    models = Bm.train_model(alg=algorithm, tss=train_sample_size, taf=test_all_features)

    # Evaluate the models
    Em.evaluated_models(models=models)


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

        # If the user wants to test all features after on another
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


