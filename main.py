from custom_chunker import ConsecutiveNPChunker
from nltk.corpus import conll2002 as conll
import nltk
import features
import BuildModels as bm
import EvaluateModels as em
from inspect import getmembers, isfunction

def main():
    tiny_sample = 500
    # training = conll.chunked_sents("ned.train")  # Train with full dataset
    training = conll.chunked_sents("ned.train")[:tiny_sample] # SHORT DATASET: FOR DEMO/DEBUGGING ONLY!
    testing = conll.chunked_sents("ned.testa")

    best = 0

    all_features = getmembers(features, isfunction)
    all_features = sorted(all_features, key=lambda y: y[0])
    for feature in all_features:
        print("---------------------------------------------------------")
        print("Training on", len(training), "samples, using", feature[0])
        model = ConsecutiveNPChunker(feature[1],training)

        print("Evaluating on", len(testing),"samples...")
        score = em.evaluate_model(model, testing, raw=True)
        #print(em.evaluate_model(model, testing, raw=True))

        print(score)
        average = weighted_average(score)
        if average > best:
            bm.pickle_model(model, best=True)
            print("Current model is the best one yet!")
            best = average
        else:
            bm.pickle_model(model)

def print_score(score, previous):
    if isinstance(score, float) or isinstance(score, int) and isinstance(score, previous):
        if score > previous:
            print("Score:", round(score,3), "(+)")
        else:
            print(1)
    elif isinstance(score, nltk.chunk.util.ChunkScore):
        print("Accuracy:", round(score.accuracy(),3),
        "Precision:", round(score.precision(),3),
        "Recall:", round(score.recall(),3),
        "F-Measure", round(score.f_measure(),3))

def weighted_average(score, weights=[1,1,1,1]):
    """Caclulate score using weighted average"""
    average = weights[0] * score.accuracy()
    average += weights[1] * score.precision()
    average += weights[2] * score.recall()
    average += weights[3] * score.f_measure()
    return average/sum(weights)


if __name__=="__main__":
    main()
