import BuildModels as Bm
import EvaluateModels as Em
import sys
from InputParser import parse_input

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


if __name__ == "__main__":

    # If the user does not specify any arguments, they probably need some help.
    if len(sys.argv) <= 1:
        print("Oops! You did not specify any arguments. See the help below for more info.")
        help(main)

    # If the user asks for help, print the help statement
    elif "-h" in sys.argv or "-help" in sys.argv:
        help(main)

    else:
        args = parse_input()
        main(algorithm=args['alg'], train_sample_size=args['tss'], test_all_features=args['taf'])


