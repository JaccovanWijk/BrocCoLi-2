import re


def feature1_simple(sentence, i, history):
    """Simplest chunker features: Just the POS tag of the word"""
    word, pos = sentence[i]
    return {"pos": pos}


def feature2_prevpos(sentence, i, history):
    """POS tag of previous word"""
    features = feature1_simple(sentence, i, history)
    if i > 0:
        word, pos = sentence[i - 1]
        features["prev-pos"] = pos
    else:
        features["prev-pos"] = None
    return features


def feature3_nextpos(sentence, i, history):
    """POS tag of next word"""
    features = feature2_prevpos(sentence, i, history)
    if i < len(sentence) - 1:
        word, pos = sentence[i + 1]
        features["next-pos"] = pos
    else:
        features["next-pos"] = None
    return features


def feature4_cap(sentence, i, history):
    """Looks if the current word begins with a capital letter"""
    features = feature3_nextpos(sentence, i, history)
    if sentence[i][0][0].isupper():
        features["cap"] = True
    else:
        features["cap"] = False
    return features


def feature5_nextcap(sentence, i, history):
    """Looks if the next word begins with a capital letter"""
    features = feature4_cap(sentence, i, history)

    if i < len(sentence) - 1:
        word, pos = sentence[i+1]
        if word[0].isupper():
            features["next-cap"] = True
        else:
           features["next-cap"] = False
    else:
        features["next-cap"] = False
    return features


def feature6_word(sentence, i, history):
    """Makes the word itself a feature"""
    features = feature5_nextcap(sentence, i, history)
    features["word"] = sentence[i][0]
    return features


def feature7_numcaps(sentence, i, history):
    """How many capital letters the word has"""
    word, pos = sentence[i]
    all_caps = [x for x in word if x.isupper()]
    features = feature6_word(sentence, i, history)
    features['num-caps'] = len(all_caps)
    return features


def feature8_prev_iob(sentence, i, history):
    """If the previous word was already part of a NE"""
    features = feature7_numcaps(sentence, i, history)
    if i > 0 and len(history) > 1:
        features['prev-IOB'] = history[i - 1]
    else:
        features['prev-IOB'] = 'O'
        
    return features


def feature9_all_caps(sentence, i, history):
    """If the word is written in all caps"""
    word, pos = sentence[i]
    features = feature8_prev_iob(sentence, i, history)
    if word.isupper():
        features['all-caps'] = True
    else:
        features['all-caps'] = False
    return features


def feature10_prev_cap(sentence, i, history):
    """If the previous word starts with a capital letter"""
    features = feature9_all_caps(sentence, i, history)
    if not i == 0 and len(sentence) > 1:
        word, pos = sentence[i - 1]
        if word[0].isupper():
            features['prev-cap'] = True
        else:
            features['prev-cap'] = False
    else:
        features['prev-cap'] = False
    return features
