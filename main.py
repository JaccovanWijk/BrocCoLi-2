from custom_chunker import ConsecutiveNPChunker
from features import simple_features_1

tiny_sample = 300
# training = conll.chunked_sents("ned.train")  # Train with full dataset
training = conll.chunked_sents("ned.train")[:tiny_sample] # SHORT DATASET: FOR DEMO/DEBUGGING ONLY!
testing = conll.chunked_sents("ned.testa")

simple_nl_NER = ConsecutiveNPChunker(simple_features_1, training)

print(simple_nl_NER.evaluate(testing))
