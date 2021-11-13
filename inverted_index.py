from collections import defaultdict

class Query:
    def __init__(self, indx, words, popularity):
        self.indx = indx
        self.words = words
        self.popularity = popularity

    def __hash__(self) -> int:
        return self.indx

    def __repr__(self) -> str:
        return f"Query indx: {self.indx}. Words: {self.words}. Score: {self.popularity}"

class InvertedIndex:
    def __init__(self):
        self.inverted_index = defaultdict(set)

    def process_corpus(self, corpus):
        for indx, (words, popularity) in enumerate(corpus):
            query = Query(indx, words, popularity)
            splitted_words = words.split()
            for word in splitted_words:
                self.inverted_index[word].add(query)
        return self.inverted_index