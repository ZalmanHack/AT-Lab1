import glob
import os.path
import re
import json

from tqdm import tqdm


class DictAdapter:
    def __init__(self):
        self._ngram_len: int = 3
        self._dict_data: dict = {}
        self._text_data: str = ''

    @property
    def ngram_len(self):
        return self._ngram_len

    @property
    def dict_data(self):
        return self._dict_data

    @ngram_len.setter
    def ngram_len(self, value: int):
        if self._ngram_len == value:
            return
        self._ngram_len = value

    @dict_data.setter
    def dict_data(self, value: dict):
        if self._dict_data == value:
            return
        self._dict_data = value

    @ngram_len.deleter
    def ngram_len(self):
        del self._ngram_len

    @dict_data.deleter
    def dict_data(self):
        del self._dict_data

    def set_texts_dir(self, dir_path: str, encoding: str):
        self._text_data = ''
        for path in glob.glob(os.path.join(dir_path, '*.txt')):
            with open(path, 'r', encoding=encoding) as file:
                self._text_data += file.read()

    @staticmethod
    def __key_to_int(data):
        if isinstance(data, dict):
            return {int(k): v for k, v in data.items()}
        return data

    # получение уникального списка слов
    def __parse_words(self):
        return sorted(set(re.findall('[а-яёЁ]{2,}', self._text_data.lower())))

    # дополнение длины слова до розмера N-граммы
    def __normalize(self, word: str) -> str:
        word = word.lower()
        if len(word) >= self.ngram_len:
            return word
        else:
            return word + '_' * abs(self.ngram_len - len(word))

    def __get_ngrams(self, word):
        word = word.lower()
        word_normalize = self.__normalize(word)
        n_gram_count = len(word_normalize) - self.ngram_len + 1
        return [word_normalize[pos:pos + self.ngram_len] for pos in range(n_gram_count)]

    # разбитие слов на N-граммы
    def __add_ngrams(self, word: str):
        word = word.lower()
        for index, ngram in enumerate(self.__get_ngrams(word)):
            if index in self.dict_data:
                if ngram in self.dict_data[index]:
                    self.dict_data[index][ngram] = self.dict_data[index][ngram] + [word]
                else:
                    self.dict_data[index][ngram] = [word]
            else:
                self.dict_data[index] = {ngram: [word]}

    def fit(self) -> None:
        self.dict_data: dict = {}
        words = self.__parse_words()
        [self.__add_ngrams(word) for word in tqdm(words, desc=f"Создание словаря")]

    def save(self, file_name: str) -> None:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(json.dumps({"ngram_len": self.ngram_len,
                                   "dict_data": self.dict_data},
                                  indent=4, ensure_ascii=False))

    def open(self, file_name) -> None:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.loads('\n'.join([line for line in tqdm(file, desc="Чтение словаря")]))
            self.ngram_len = int(data["ngram_len"])
            self.dict_data = self.__key_to_int(data["dict_data"])
            pass

    def get(self) -> dict:
        return self.dict_data

    # возвращает список слов для каждой найденой N граммы
    def find(self, word: str) -> set:
        words = set()
        for index, ngram in enumerate(tqdm(self.__get_ngrams(word), desc=f"Поиск {self.ngram_len}-грамм", ncols=100)):
            if index in self.dict_data and ngram in self.dict_data[index]:
                words = words.union(self.dict_data[index][ngram])
        return words


class DictAdapterBuilder:
    def __init__(self):
        self.dictAdapter = DictAdapter()

    def set_texts_dir(self, dir_path: str, encoding: str):
        self.dictAdapter.set_texts_dir(dir_path, encoding)
        return self

    def set_ngram_len(self, value: int):
        self.dictAdapter.ngram_len = value
        return self

    def fit(self):
        self.dictAdapter.fit()
        return self

    def save(self, file_name: str):
        self.dictAdapter.save(file_name)
        return self

    def open(self, file_name):
        self.dictAdapter.open(file_name)
        return self

    def build(self):
        return self.dictAdapter
