import codecs
from collections import Counter
import csv
import utils
import sys


class Preprocessor:
    def __init__(self, path):
        self.corpus_path = path

    def parse_corpus(self, raw=False):
        corpus = {}
        i=1
        with open(self.corpus_path) as f:
            reader=csv.reader(f)
            for msg in reader:
                if raw:
                    corpus[int(i)] = str(msg[0])
                else:
                    corpus[int(i)] = utils.process_txt(str(msg[0]))
                i=i+1
        return corpus;

    def create_tokens(self, processed_corpus):
        corpus_tokens = set()
        for doc in processed_corpus:
            # for w in utils.process_txt(doc["msg"], True):
            for w in processed_corpus[doc]:
                corpus_tokens.add(w)
        return corpus_tokens

    def create_corpus_counter(self, processed_corpus):
        corpus_counter = {}
        for doc in processed_corpus:
            corpus_counter[doc]= Counter(processed_corpus[doc]);
        return corpus_counter
