import re


def feature01_pos(sentence, i, history):
    """Pos tag of current, previous and next word"""
    word, pos = sentence[i]

    # current pos
    features = {"pos": pos}

    # prev pos
    if i > 0:
        word, pos = sentence[i - 1]
        features["prev-pos"] = pos
    else:
        features["prev-pos"] = None

    # next pos
    if i < len(sentence) - 1:
        word, pos = sentence[i + 1]
        features["next-pos"] = pos
    else:
        features["next-pos"] = None

    return features

def feature02_cap(sentence, i, history):
    """Looks if the current word begins with a capital letter"""
    features = feature01_pos(sentence, i, history)
    if sentence[i][0][0].isupper():
        features["cap"] = True
    else:
        features["cap"] = False
    return features


def feature03_nextcap(sentence, i, history):
    """Looks if the next word begins with a capital letter"""
    features = feature02_cap(sentence, i, history)

    if i < len(sentence) - 1:
        word, pos = sentence[i+1]
        if word[0].isupper():
            features["next-cap"] = True
        else:
           features["next-cap"] = False
    else:
        features["next-cap"] = False
    return features


def feature04_word(sentence, i, history):
    """Makes the word itself a feature"""
    features = feature03_nextcap(sentence, i, history)
    features["word"] = sentence[i][0]
    return features


def feature05_numcaps(sentence, i, history):
    """How many capital letters the word has"""
    word, pos = sentence[i]
    all_caps = [x for x in word if x.isupper()]
    features = feature04_word(sentence, i, history)
    features['num-caps'] = len(all_caps)
    return features


def feature06_prev_iob(sentence, i, history):
    """If the previous word was already part of a NE"""
    features = feature05_numcaps(sentence, i, history)
    if i > 0 and len(history) > 1:
        features['prev-IOB'] = history[i - 1]
    else:
        features['prev-IOB'] = 'O'

    return features

def feature07_next_verb(sentence, i, history):
    """If the next word is a verb"""
    features = feature06_prev_iob(sentence, i, history)
    if i < len(sentence) - 1:
        word, pos = sentence[i + 1]
        features["next-verb"] = (pos == "V")
    else:
        features["next-verb"] = False
    return features

def feature08_length(sentence, i, history):
    """Length of word"""
    features = feature07_next_verb(sentence, i, history)
    features["length"] = len(sentence[i])
    return features

def feature09_cap_in_sentence(sentence, i, history):
    """Amount of caps in sentence"""
    features = feature08_length(sentence, i, history)
    features["caps"] = len(sentence)
    return features
