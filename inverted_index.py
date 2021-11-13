from collections import defaultdict

class Query:
    def __init__(self, indx, words):
        self.indx = indx
        self.words = words

    def __hash__(self) -> int:
        return self.indx

    def __repr__(self) -> str:
        return f"Query indx: {self.indx}. Words: {self.words}"

class InvertedIndex:
    def __init__(self):
        self.inverted_index = defaultdict(set)

    def process_corpus(self, corpus):
        for indx, words in enumerate(corpus):
            query = Query(indx, words)
            splitted_words = words.split()
            for word in splitted_words:
                self.inverted_index[word].add(query)
        return self.inverted_index