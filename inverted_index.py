from collections import defaultdict


class Query:
    def __init__(self, indx, words, popularity, lemmas):
        self.indx = indx
        self.words = words
        self.popularity = popularity
        self.lemmas = lemmas
        self.lemma_of = None

    def __hash__(self) -> int:
        return self.indx

    def __repr__(self) -> str:
        template = f"Query indx: {self.indx}. Words: {self.words}. Score: {self.popularity}. Lemma: {self.lemmas}"
        if self.lemma_of is not None:
            template += f" Is lemma of: {self.lemma_of}"
        return template

    def set_lemma_of(self, lemma_of):
        self.lemma_of = lemma_of

    def reset_lemma_of(self):
        self.lemma_of = None

    def is_lemma_of(self):
        return self.lemma_of is not None


class InvertedIndex:
    def __init__(self, query_to_lemma_map):
        self.inverted_index = defaultdict(set)
        self.query_to_lemma_map = query_to_lemma_map

    def process_corpus(self, corpus):
        for indx, (words, popularity) in enumerate(corpus):
            lemmas = str(self.query_to_lemma_map[words])
            query = Query(indx, words, popularity, lemmas.split())
            splitted_words = words.split()
            for word in splitted_words:
                self.inverted_index[word].add(query)
        return self.inverted_index
