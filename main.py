import random
import statistics
import time
import os
from source.dictAdapter import DictAdapterBuilder, DictAdapter
from source.d_levenshtein_distance import DLevenshteinDistance
from source.metrics import STD, MSE


def run(adapter):
    d_l_distance = DLevenshteinDistance(adapter)
    base_word = ""
    while True:
        base_word = input('Введите слово: ')
        os.system('cls')
        if base_word == 'q':
            break
        print('Ваше слово:  {}\n'.format(base_word))
        start_time = time.time()
        results = d_l_distance.find(base_word)
        end_time = time.time()
        print('Время выполнения: {}'.format(end_time - start_time))

        for index, res in enumerate(sorted(results)):
            print(f'{index + 1} | {res[0]:.3f}   {res[1]}')
            if index == 4:
                break


def run_testing(adapter, words: list, actual_visible):
    d_l_distance = DLevenshteinDistance(adapter)
    actual_answers = []
    for word in words:
        index = random.randint(0, len(word) - 1)
        word = word[:index] + '_' + word[index + 1:]
        actual_answers.append(sorted(d_l_distance.find(word))[:5])
    convert_actual_answers = []
    for answers in actual_answers:
        convert_answers = []
        for answer in answers:
            convert_answers.append(answer[1])
        convert_actual_answers.append(convert_answers)
    print(STD.get(convert_actual_answers, words))
    print(MSE.get(convert_actual_answers, words))


if __name__ == '__main__':
    os.system('cls')

    actual = [["qwerty"], ["привет", "здрасте", "f"], ["f", "f", "здрsсте", "f", "f", "f"]]
    targets =["qwerty", "приет", "здрsсте"]
    x = [1 if actual[index] == targets[index] else 0 for index in range(len(actual))]
    #print(STD.get(actual, targets))
    #print(MSE.get(actual, targets))

    dictAdapter = None
    while True:
        print("1 | загрузить словарь")
        print("2 | создать словарь")
        print("3 | запуск")
        print("4 | тестирование")
        print("5 | выйти")
        cin = input(">> ")
        if cin == "1":
            dictAdapter = DictAdapterBuilder() \
                .open('dict.json') \
                .build()
        elif cin == "2":
            dictAdapter = DictAdapterBuilder() \
                .load_texts('text corpora', encoding='utf-8') \
                .set_ngram_len(3) \
                .fit() \
                .save('dict.json') \
                .build()
        elif cin == "3":
            if isinstance(dictAdapter, DictAdapter):
                run(dictAdapter)
        elif cin == "4":
            words_data = DictAdapterBuilder() \
                .load_texts('text test', encoding='utf-8') \
                .build() \
                .words_data
            if isinstance(dictAdapter, DictAdapter):
                run_testing(dictAdapter, list(words_data), 5)
        elif cin == "5":
            break
