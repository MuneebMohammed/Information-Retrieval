from indexing import Indexer
from preprocessor import Preprocessor
from query import Query
import re
import csv

class System:
    def __init__(self, corpus_path, freq_index_path, tf_idf_index_path, create_index=False):
        self.preprocessor = Preprocessor(corpus_path);
        self.corpus = {}
        # if create_index, then run the create_indexes, otherwise, load them from their already existing file locations
        if create_index:
            print("Creating frequency and tf_idf_indexes.")
            self.corpus = self.preprocessor.parse_corpus()
            tokens = self.preprocessor.create_tokens(self.corpus)
            c_counter = self.preprocessor.create_corpus_counter(self.corpus)
            self.indexer = Indexer(c_counter, tokens)
            # Uncomment and run with create_index set to True if you would like to see the results using the
            # different, but faster optimized algorithm for indexing
            # self.frequency_index = self.indexer.create_frequency_index_optimized()
            self.frequency_index = self.indexer.create_frequency_index()
            self.indexer.index_to_file(self.frequency_index, freq_index_path)
            self.tf_idf_index = self.indexer.create_tf_idf_index(self.frequency_index, len(self.frequency_index))
            self.indexer.index_to_file(self.tf_idf_index, tf_idf_index_path)
        else:
            print("Loading frequency and tf_idf indexes.")
            self.corpus = self.preprocessor.parse_corpus(True)
            self.indexer = Indexer()
            self.frequency_index = self.indexer.load_index(freq_index_path)
            self.tf_idf_index = self.indexer.load_index(tf_idf_index_path)
        self.query = Query(self.frequency_index, self.tf_idf_index, self.corpus)


    def test_system(self, query):
        results = []
        query_results = self.query.execute_query(query)
        for i in range(len(query_results)):
            if i >= 100:
                break
            string_write = str(self.corpus[int(query_results[i].get("id"))])
            string_write = string_write.replace('\n',"").strip()
            results.append(string_write)
        return results

#system = System("data/tweets.csv", "index/frequency-index.txt", "index/tf-idf-index.txt", True)

