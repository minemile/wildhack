from tries import Trie


class AutoCompleterBaseline:
    def __init__(self, query_database, max_n=10):
        self.query_database = query_database  # its already sorted by query population
        self.max_n = max_n

    def predict_suffix(self, prefix_word):
        return self.query_database[
            self.query_database["query"].str.startswith(prefix_word)
        ][: self.max_n]

    def predict(self, sentence):
        words = sentence.split()
        if len(words) == 1:
            return self.predict_suffix(words[0])
        else:
            return self.predict_full_text(words)

    def predict_contains_mask(self, word):
        mask = self.query_database["query"].str.contains(word)
        print(f"Found for word: {word} {mask.sum()} instances")
        return mask

    def predict_full_text(self, words):
        mask = None
        for word in words:
            if mask is None:
                mask = self.predict_contains_mask(word)
            else:
                mask = mask & self.predict_contains_mask(word)
        return self.query_database[mask][: self.max_n]


class AutoCompleteBySuffix:
    def __init__(self, max_n=10):
        self.trie = Trie()
        self.max_n = max_n

    def make_trie(self, query_database):
        print(f"Making database for queries... It length: {len(query_database)}")
        for indx, row in query_database.iterrows():
            words = row["query"]
            popularity = row["query_popularity"]
            self.trie.insert(words, popularity)

    def query(self, query):
        return self.trie.query(query)


class AutoCompleteByInvertedIndex(AutoCompleteBySuffix):
    def __init__(self, inverted_index, trie, first_prefix=None, max_candidates=20):
        self.max_candidates = max_candidates
        self.inverted_index = inverted_index
        self.first_prefix = first_prefix
        self.trie = trie

    def query(self, query, max_n=None):
        splitted_query = query.split()
        query_candidates_all = []
        for word in splitted_query:
            candidates = self.get_candidates(word)

            candidates_queries = self.get_queries_from_inverted_index(candidates)
            query_candidates_all.append(candidates_queries)
        result = self.intersect_candidates(query_candidates_all)
        result = self.prepare_output(result, query, max_n)
        return result
    
    def get_candidates(self, word):
        candidates = self.trie.query(word)
        candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
        candidates = candidates[: self.max_candidates]
        return candidates

    def prepare_output(self, result, original_query, max_n=None):
        sorted_result = sorted(result, key=lambda x: x.popularity, reverse=True)
        if self.first_prefix is not None:
            return self.make_result_with_first_prefix(
                original_query, sorted_result, max_n
            )
        if max_n is not None:
            sorted_result = sorted_result[:max_n]
        return sorted_result

    def make_result_with_first_prefix(self, original_query, result, max_n):
        prefix_list = []
        for query_results in result:
            if len(prefix_list) >= self.first_prefix:
                break
            if query_results.words.startswith(original_query):
                prefix_list.append(query_results)

        sorted_result_sublist = []
        for query_results in result:
            if len(sorted_result_sublist) >= max_n - self.first_prefix:
                break
            if query_results not in prefix_list:
                sorted_result_sublist.append(query_results)
        sorted_result = prefix_list + sorted_result_sublist
        return sorted_result

    def intersect_candidates(self, candidates):
        return set.intersection(*candidates)

    def get_queries_from_inverted_index(self, word_candidates):
        queries = set()
        for candidate, counter, popularity in word_candidates:
            candidate_queries = self.inverted_index[candidate]
            queries = queries.union(candidate_queries)
        return queries
