from multiprocessing import Pool
from source.dictAdapter import DictAdapter


class DLevenshteinDistance:
    def __init__(self, dictAdapter: DictAdapter):
        self.dictAdapter = dictAdapter
        self.pool_len = 1  # os.cpu_count()
        self.pool = Pool(self.pool_len)

    @staticmethod
    def priority_error(s1, s2):
        len_s1, len_s2 = len(s1), len(s2)
        if len_s1 > len_s2:
            s2 += '_' * (len_s1 - len_s2)
        else:
            s1 += '_' * (len_s2 - len_s1)
        error = 0.0
        for index in range(len(s1)):
            if s1[index] != s2[index]:
                error += 1.0 / (2 + index)
        return error

    @classmethod
    def __get_distance(cls, word_1: str, word_2: str) -> float:
        distance = {}
        len_word_1 = len(word_1)
        len_word_2 = len(word_2)
        for i in range(-1, len_word_1 + 1):
            distance[(i, -1)] = i + 1
        for j in range(-1, len_word_2 + 1):
            distance[(-1, j)] = j + 1

        for i in range(len_word_1):
            for j in range(len_word_2):
                cost = 0 if word_1[i] == word_2[j] else 1
                distance[(i, j)] = min(distance[(i - 1, j)] + 1,           # удаления
                                       distance[(i, j - 1)] + 1,           # вставки
                                       distance[(i - 1, j - 1)] + cost, )  # подмены
                if i and j and word_1[i] == word_2[j - 1] and word_1[i - 1] == word_2[j]:
                    distance[(i, j)] = min(distance[(i, j)], distance[i - 2, j - 2] + cost)  # перестановки

        return distance[len_word_1 - 1, len_word_2 - 1] + cls.priority_error(word_1, word_2)

    @classmethod
    def get_distances(cls, base_word: str, found_words: set) -> list:
        result = []
        if len(found_words) == 0:
            return result
        for word in found_words:
            result.append((cls.__get_distance(base_word, word), word))
        return result

    def find(self, base_word: str) -> set:
        found_words = list(self.dictAdapter.find(base_word))
        args = []
        results = set()
        if len(found_words) > 0:
            if len(found_words) < self.pool_len:
                args = [('', []) for _ in range(self.pool_len)]
                args[0] = (base_word, found_words)
            else:
                step = int(len(found_words) / self.pool_len) + 1
                for index in range(0, len(found_words), step):
                    args.append((base_word, found_words[index:index + step]))
            pool_answer = self.pool.starmap(DLevenshteinDistance.get_distances, args)
            for words in pool_answer:
                results = results.union(words)
            return results
        return results
