import glob
import time
import os
from source.dictAdapter import DictAdapterBuilder

def levenshtein_distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def priority_error(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    if len_s1 > len_s2:
        s2 += '_' * (len_s1 - len_s2)
    else:
        s1 += '_' * (len_s2 - len_s1)
    error = 0.0
    for index in range(len(s1)):
        if s1[index] != s2[index]:
            error += 1.0/(2 + index)
    return error

def damerau_levenshtein_distance(s1, s2):
    d = {}
    len_s1 = len(s1)
    len_s2 = len(s2)
    for i in range(-1, len_s1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len_s2 + 1):
        d[(-1, j)] = j + 1

    for i in range(len_s1):
        for j in range(len_s2):
            cost = 0 if s1[i] == s2[j] else 1
            d[(i, j)] = min(d[(i - 1, j)] + 1,  # deletion
                            d[(i, j - 1)] + 1,  # insertion
                            d[(i - 1, j - 1)] + cost,)  # substitution
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition

    return d[len_s1 - 1, len_s2 - 1] + priority_error(s1, s2)

if __name__ == '__main__':
    # da = DictAdapterBuilder() \
    #     .set_texts_dir('text corpora', encoding='utf-8') \
    #     .set_ngram_len(3) \
    #     .fit() \
    #     .save('dict.json') \
    #     .build()
    da = DictAdapterBuilder() \
        .open('dict.json') \
        .build()

    while True:
        base_word = input('base word: ')
        os.system('cls')

        print('base word: {}\n'.format(base_word))
        print('words: {}'.format(len(da.parse_words())))

        start_time = time.time()
        res_2 = [[damerau_levenshtein_distance(word, base_word), word] for word in da.find(base_word)]
        end_time = time.time()
        print('time: {}'.format(end_time - start_time))
        print(sorted(res_2)[:3])
