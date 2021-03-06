from numpy.linalg import linalg
from utils import process_query

class Query:

    def __init__(self, frequency_index, tf_idf_index, corpus):
        self.frequency_index = frequency_index
        self.tf_idf_index = tf_idf_index
        self.corpus = corpus
        self.corpus_size = len(corpus)

    def retrieve_limited_set(self, query_vector, index):
        limited_set = set()
        for term in query_vector:
            document_list = index.get(term, {})
            for doc in document_list.keys():
                limited_set.add(doc)
        return limited_set

    def create_document_vectors(self, query_vector, doc_list, index):
        doc_vectors = {}
        for doc_id in doc_list:
            doc_vectors[doc_id]=[]
        i = 0
        for term in query_vector:
            term_list = index.get(term,{})
            for doc_id in doc_list:
                doc_vectors[doc_id].insert(i, term_list.get(doc_id,0))
            i = i + 1;
        return doc_vectors

    def compute_cos_similarity(self, doc_vector, query_vector):
        return linalg.dot(doc_vector, query_vector)/(linalg.norm(doc_vector)*linalg.norm(query_vector))

    def rank_vectors(self, doc_vectors, query_vector):
        ranked_docs = []
        for id in doc_vectors:
            ranked_docs.append({"id":id, "score": self.compute_cos_similarity(doc_vectors[id], query_vector)})
        return sorted(ranked_docs, key=lambda doc: doc["score"], reverse=True)

    def execute_query(self, query):
        query_vector, query_freq_vector = process_query(query, self.frequency_index, self.corpus_size)
        limited_set = self.retrieve_limited_set(query_vector, self.tf_idf_index)
        doc_freq_vectors = self.create_document_vectors(query_vector, limited_set, self.tf_idf_index)
        results = self.rank_vectors(doc_freq_vectors, query_freq_vector)
        return results


