import time
import os
from source.dictAdapter import DictAdapterBuilder
from source.d_levenshtein_distance import DLevenshteinDistance


def run(adapter):
    d_l_distance = DLevenshteinDistance(adapter)
    while True:
        base_word = input('Введите слово: ')
        os.system('cls')
        print('Ваше слово:  {}\n'.format(base_word))

        start_time = time.time()
        results = d_l_distance.find(base_word)
        end_time = time.time()
        print('Время выполнения: {}'.format(end_time - start_time))

        for index, res in enumerate(results):
            print(f'{index + 1} | {res[0]:.3f}   {res[1]}')
            if index == 4:
                break


if __name__ == '__main__':
    os.system('cls')
    while True:
        print("1 | загрузить словарь")
        print("2 | создать словарь")
        print("3 | выйти")
        cin = input(">> ")
        if cin == "1":
            dictAdapter = DictAdapterBuilder() \
                .open('dict.json') \
                .build()
            run(dictAdapter)
        elif cin == "2":
            dictAdapter = DictAdapterBuilder() \
                .set_texts_dir('text corpora', encoding='utf-8') \
                .set_ngram_len(3) \
                .fit() \
                .save('dict.json') \
                .build()
            run(dictAdapter)
        elif cin == "3":
            break
