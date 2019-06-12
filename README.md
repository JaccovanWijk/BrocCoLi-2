# NER-Tagger

The following modules are present in this project:

- BuildModels.py
- custom_chunker.py
- EvaluateModels.py
- features.py
- InputParser.py
- main.py
- model_test.py
 
 Below you will find a description of every module and their functionality in alphabetical order.
 
### BuildModels.py
This module is used to pickle and train Ner-tagger models.
Given an algorithm, train data and a feature-set, it can train a model using the function `train_model`.
This function will also nicely print the start, end and elapsed times and display which feature-set is used.
After training, this module will use the function `pickle_model` to pickle the trained model for later use.
The specified folder will be created if it doesn't exist yet. If it does, it will pick the next name available.
The pickles will be named `0.pickle` , `1.pickle`, `2.pickle` etc. 
This module can be used on its own, but it is recommended to use `main.py` instead. 

### custom_chucker.py
This module is an edit of the original `custom_chucker.py` created by Alexis Dimitriadis to accept `NaiveBayes` as a valid algorithm.
It will create an pre-configured NER-tagger and chuncker. 

### EvaluateModels.py
This module is used to evaluated trained NER-taggers. Just like `BuildModels.py`, it will provide the user with information during 
execution about the times. This module can handle NER-tagger objects directly and pickled models. Present in this module is the `evaluate_all_pickles'
function which will evaluate all pickled models in a given folder. 

### features.py
This module contains all feature functions that can be used to enable the tagger to recognize NE's. This module is NOT meant to be used as
a standalone module, however it can be used to get all available functions. 

### InputParser.py
This module parses all the commandline arguments given. It will also raise errors when needed. This module can not be used as a main module. 
It only contains a single function `parse_input` that returns a dictionary with all the relevant arguments and their values.

### main.py
As the name suggests, this module is meant to be used as the main module. It trains, evaluates and pickles models based on the arguments
given in the commandline. If given no arguments, it will train a tagger on the complete conll2002 corpus using the IIS algorithm.
It used the `BuildModels.py` and `EvaluateModels.py` modules to accomplish this. 

### model_test.py
This module only opens the best.pickle file and prints its evaluation. 

### Evaluation-output.txt
This plain text file contains the results of evaluations that are done in `EvaluateModels.py`. It will also be created if it doesn't exist yet.
Lines will be appended to this text file every evaluation. It can easily be used to fill an Excel sheet to compare algorithms by splitting on semicolons.

