def simple_features_1(sentence, i, history):
    """Simplest chunker features: Just the POS tag of the word"""
    word, pos = sentence[i]
    return { "pos": pos }
