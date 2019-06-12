import sys
import features
from inspect import getmembers, isfunction


def parse_input():
    """Reads the commandline input arguments return a dictionary with the values.
    Please note that this method ignores any invalid flags.
    If you want to know which flags are available in which module, please consult their help by using -h or -help.
    This module cannot be run as a main module.
    """

    all_features = getmembers(features, isfunction)  # Get all feature functions from module features
    # Sort them by name so the oldest feature comes first
    all_features = sorted(all_features, key=lambda y: y[0], reverse=True)
    sorted_features = sorted(all_features, key=lambda y: y[0])

    args = {
        'alg': "IIS",
        'tss': 0,
        'feature': [all_features[0]]
    }

    # Loop trough all arguments and save them accordingly. Skip the first, because that's the module name.
    for i in range(1, len(sys.argv)):
        flag = sys.argv[i]

        # If the user wants to specify an algorithm
        if flag == "-a" or flag == "-alg" or flag == "-algorithm":

            # Throw an exception if the user does not specify an algorithm after passing the flag
            try:
                args['alg'] = sys.argv[i + 1]
            except IndexError:
                raise IndexError("Please specify an algorithm after using the " + flag + " flag.")

            # Throw an exception if the user does not specify an admissible algorithm
            if args['alg'].lower() not in ["iis", "gis", "nb", "naivebayes"]:
                raise ValueError(args['alg'] + " is not a valid algorithm.")

            # If the user is lazy and doesn't want to type NaiveBayes fully
            elif args['alg'].lower() == "nb":
                args['alg'] = "NaiveBayes"

        # If the user wants to specify the train sample size
        elif flag == "-tss" or flag == "-train_sample_size":

            # Throw an exception if the user doesn't specify a valid training size after passing the flag
            try:
                args['tss'] = sys.argv[i + 1]
            except IndexError:
                raise IndexError("Please specify a training size after passing the " + flag + " flag.")

            try:
                args['tss'] = int(args['tss'])
            except ValueError:
                raise ValueError(args['tss'], "is not an integer. Only integers can be used as a training size.")

            # Notify the user of an negative training size
            if args['tss'] < 0:
                print("You tried to specify a negative training size.",
                      "That doesn't make the training any faster, you know.",
                      "We will use the full train sample set instead.")
                args['tss'] = 0

        # If the user wants to test all features after on another
        elif flag == "-taf" or flag == "-test_all_features":
            args['feature'] = all_features

        elif flag == "-f" or flag == "-feature":
            value = 1

            # Raise an exception if the user does not specify anything after passing the flag
            try:
                value = str(sys.argv[i + 1])
            except IndexError:
                raise IndexError("Please specify a value after passing the", flag, " flag")

            # Try to convert to integer, never mind if it doesn't work
            try:
                value = int(value)
            except ValueError:
                pass

            # Raise an error if the user does not specify a string or integer
            if not isinstance(value, int) and not isinstance(value, str):
                raise TypeError("The value specified after the", flag, "flag is not of type int or str")

            # If the user specified a string
            elif isinstance(value, str):
                if value not in [x[0] for x in all_features]:
                    raise ValueError("The feature", value, "cannot be used, as it's not an existing feature")
                else:
                    args['feature'] = [x for x in all_features if x[0] == value]

            # If the user specified an integer
            elif isinstance(value, int):
                if value < 1:
                    raise IndexError("You must specify an 1-based index that corresponds to a feature")
                else:
                    try:
                        args['feature'] = [sorted_features[value - 1]]
                    except IndexError:
                        raise IndexError(value, "is not a valid index for a feature.")

    return args


if __name__ == '__main__':
    help(parse_input)
