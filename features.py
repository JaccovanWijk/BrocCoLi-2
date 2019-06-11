import re


def feature01_simple(sentence, i, history):
    """Simplest chunker features: Just the POS tag of the word"""
    word, pos = sentence[i]
    return {"pos": pos}


def feature02_prevpos(sentence, i, history):
    """POS tag of previous word"""
    features = feature01_simple(sentence, i, history)
    if i > 0:
        word, pos = sentence[i - 1]
        features["prev-pos"] = pos
    else:
        features["prev-pos"] = None
    return features


def feature03_nextpos(sentence, i, history):
    """POS tag of next word"""
    features = feature02_prevpos(sentence, i, history)
    if i < len(sentence) - 1:
        word, pos = sentence[i + 1]
        features["next-pos"] = pos
    else:
        features["next-pos"] = None
    return features


def feature04_cap(sentence, i, history):
    """Looks if the current word begins with a capital letter"""
    features = feature03_nextpos(sentence, i, history)
    if sentence[i][0][0].isupper():
        features["cap"] = True
    else:
        features["cap"] = False
    return features


def feature05_nextcap(sentence, i, history):
    """Looks if the next word begins with a capital letter"""
    features = feature04_cap(sentence, i, history)

    if i < len(sentence) - 1:
        word, pos = sentence[i+1]
        if word[0].isupper():
            features["next-cap"] = True
        else:
           features["next-cap"] = False
    else:
        features["next-cap"] = False
    return features


def feature06_word(sentence, i, history):
    """Makes the word itself a feature"""
    features = feature05_nextcap(sentence, i, history)
    features["word"] = sentence[i][0]
    return features


def feature07_numcaps(sentence, i, history):
    """How many capital letters the word has"""
    word, pos = sentence[i]
    all_caps = [x for x in word if x.isupper()]
    features = feature06_word(sentence, i, history)
    features['num-caps'] = len(all_caps)
    return features


def feature08_prev_iob(sentence, i, history):
    """If the previous word was already part of a NE"""
    features = feature07_numcaps(sentence, i, history)
    if i > 0 and len(history) > 1:
        features['prev-IOB'] = history[i - 1]
    else:
        features['prev-IOB'] = 'O'

    return features

def feature09_next_verb(sentence, i, history):
    """If the next word is a verb"""
    features = feature08_prev_iob(sentence, i, history)
    if i < len(sentence) - 1:
        word, pos = sentence[i + 1]
        features["next-verb"] = (pos == "V")
    else:
        features["next-verb"] = False
    return features
