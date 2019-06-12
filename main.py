import BuildModels as Bm
import EvaluateModels as Em
import sys
from nltk.corpus import conll2002 as conll
from InputParser import parse_input


def main(feature_set, algorithm="IIS", train_sample_size=0):
    """" The main method for using the NER-tagger.
    This method trains, pickles and evaluates the models, skipping the
    unpickling part for efficiency. This method is faster and easier than
    using EvaluateModels and BuildModels, but has less options.

    Use the flags -h or -help to get this help message.
    This flag will overrule any other flags.

    Keyword arguments:

    algorithm -- The name of the algorithm to use.
    Must be one of ["IIS", "GIS", "NaiveBayes"] (Default = IIS).
    The flag to set this can be -a or -alg or -algorithm in the command line

    train_sample_size -- The number of training samples to use as an integer.
    Must be between 0 and the length of the conll ned.train. (Default = full ned.train)
    To set this, use flag -tss or -train_sample_size in the command line

    test_all_features -- Boolean, whether to test all features after
    each other on alphabetical order.
    This argument can be useful when implementing multiple new features
    in between testing to visualize improvement.
    To set this, ust flag -taf or -test_all_features in the command line.
    This flag will overwrite feature_set if passed later in the command line.

    feature_set -- The list of features on which we are going to be training.
    Please note that every next feature calls all the previous features as well.
    For example, feature 3 also calls feature 2 and 1.
    Use the flag -feature or -f to only use a specific feature.
    This flag will overwrite test_all_features when passed later in the command line.
    """

    train_data = conll.chunked_sents("ned.train")

    # Resize the testing size if necessary
    if 0 < train_sample_size < len(train_data):
        train_data = conll.chunked_sents("ned.train")[:train_sample_size]

    for feature in feature_set:

        # Train model(s) and pickle them.
        model = Bm.train_model(feature=feature, train_data=train_data, alg=algorithm)

        # Evaluate the models
        Em.evaluate_model(model)


if __name__ == "__main__":

    # If the user asks for help, print the help statement
    if "-h" in sys.argv or "-help" in sys.argv:
        help(main)

    # Else, parse the input and run the algorithm
    else:
        args = parse_input()
        main(algorithm=args['alg'], train_sample_size=args['tss'], feature_set=args['feature'])
