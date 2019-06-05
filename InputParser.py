import sys


def parse_input():
    """Reads the commandline input arguments return a dictionary with the values.
    Please note that this method ignores any invalid flags.
    This module cannot be run as a main module.
    """

    args = {
        'alg': "IIS",
        'tss': 0,
        'taf': False
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
                raise ValueError(alg + " is not a valid algorithm.")

            # If the user is lazy and doesn't want to type NaiveBayes fully
            elif args['alg'].lower() == "nb":
                alg = "NaiveBayes"

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
            args['taf'] = True

    return args
