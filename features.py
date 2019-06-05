import re


def feature1_simple(sentence, i, history):
    """Simplest chunker features: Just the POS tag of the word"""
    word, pos = sentence[i]
    return {"pos": pos}


def feature2_prevpos(sentence, i, history):
    """POS tag of previous word"""
    posdict = feature1_simple(sentence, i, history)
    if i > 0:
        word, pos = sentence[i - 1]
        posdict["prev-pos"] = pos
    else:
        posdict["prev-pos"] = None
    return posdict


def feature3_nextpos(sentence, i, history):
    """POS tag of next word"""
    posdict = feature2_prevpos(sentence, i, history)
    if i < len(sentence) - 1:
        word, pos = sentence[i + 1]
        posdict["next-pos"] = pos
    else:
        posdict["next-pos"] = None
    return posdict


def feature4_cap(sentence, i, history):
    """Looks if the current word begins with a capital letter"""
    posdict = feature3_nextpos(sentence, i, history)
    if sentence[i][0][0].isupper():
        posdict["cap"] = True
    else:
        posdict["cap"] = False
    return posdict


def feature5_nextcap(sentence, i, history):
    """Looks if the next word begins with a capital letter"""
    posdict = feature4_cap(sentence, i, history)

    if i < len(sentence) - 1:
        word, pos = sentence[i+1]
        if word[0].isupper():
            posdict["next-cap"] = True
        else:
            posdict["next-cap"] = False
    else:
        posdict["next-cap"] = False
    return posdict


#def feature6_word(sentence, i, history):
#    """Makes the word itself a feature"""
#    posdict = feature5_nextcap(sentence, i, history)
#    posdict["word"] = sentence[i][0]
#    return posdict
