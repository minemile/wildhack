from tries import Trie

class AutoCompleterBaseline():
    def __init__(self, query_database, max_n=10):
        self.query_database = query_database # its already sorted by query population
        self.max_n = max_n

    def predict_suffix(self, prefix_word):
        return self.query_database[self.query_database['query'].str.startswith(prefix_word)][:self.max_n]

    def predict(self, sentence):
        words = sentence.split()
        if len(words) == 1:
            return self.predict_suffix(words[0])
        else:
            return self.predict_full_text(words)

    def predict_contains_mask(self, word):
        mask = self.query_database['query'].str.contains(word)
        print(f"Found for word: {word} {mask.sum()} instances")
        return mask

    def predict_full_text(self, words):
        mask = None
        for word in words:
            if mask is None:
                mask = self.predict_contains_mask(word)
            else:
                mask = mask & self.predict_contains_mask(word)
        return self.query_database[mask][:self.max_n]


class AutoCompleteBySuffix():
    def __init__(self, query_database, max_n=10):
        self.query_database = query_database
        self.trie = self.make_trie()
    
    def make_trie(self):
        trie = Trie()
        for indx, row in self.query_database.iterrows():
            words = row['query']
            popularity = row['query_popularity']
            trie.insert(words, popularity)


