from __future__ import annotations

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
        self._words_data: set = set()

    @property
    def ngram_len(self) -> int:
        return self._ngram_len

    @property
    def dict_data(self) -> dict:
        return self._dict_data

    @property
    def text_data(self) -> str:
        return self._text_data

    @property
    def words_data(self) -> set:
        return self._words_data

    @ngram_len.setter
    def ngram_len(self, value: int) -> None:
        if self._ngram_len == value:
            return
        self._ngram_len = value

    @dict_data.setter
    def dict_data(self, value: dict) -> None:
        if self._dict_data == value:
            return
        self._dict_data = value

    @text_data.setter
    def text_data(self, value: str) -> None:
        if self._text_data == value:
            return
        self._text_data = value

    @words_data.setter
    def words_data(self, value: set) -> None:
        if self._words_data == value:
            return
        self._words_data = value

    @ngram_len.deleter
    def ngram_len(self) -> None:
        del self._ngram_len

    @dict_data.deleter
    def dict_data(self) -> None:
        del self._dict_data

    @text_data.deleter
    def text_data(self) -> None:
        del self._text_data

    @words_data.deleter
    def words_data(self) -> None:
        del self._words_data

    def load_texts(self, dir_path: str, encoding: str) -> None:
        self.text_data = ''
        for path in glob.glob(os.path.join(dir_path, '*.txt')):
            with open(path, 'r', encoding=encoding) as file:
                self.text_data += file.read()
        # получение уникального списка слов
        self.words_data = set(sorted(re.findall('[а-яё]{2,}', self.text_data.lower())))

    @staticmethod
    def __key_to_int(data: dict) -> dict:
        if isinstance(data, dict):
            return {int(k): v for k, v in data.items()}
        return data

    # дополнение длины слова до розмера N-граммы
    def __normalize(self, word: str) -> str:
        word = word.lower()
        if len(word) >= self.ngram_len:
            return word
        else:
            return word + '_' * abs(self.ngram_len - len(word))

    def __get_ngrams(self, word) -> list:
        word = word.lower()
        word_normalize = self.__normalize(word)
        n_gram_count = len(word_normalize) - self.ngram_len + 1
        return [word_normalize[pos:pos + self.ngram_len] for pos in range(n_gram_count)]

    # разбитие слов на N-граммы
    def __add_ngrams(self, word: str) -> None:
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
        self.dict_data = {}
        [self.__add_ngrams(word) for word in tqdm(self.words_data, desc=f"Создание словаря")]

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

    def load_texts(self, dir_path: str, encoding: str) -> DictAdapterBuilder:
        self.dictAdapter.load_texts(dir_path, encoding)
        return self

    def set_ngram_len(self, value: int) -> DictAdapterBuilder:
        self.dictAdapter.ngram_len = value
        return self

    def fit(self) -> DictAdapterBuilder:
        self.dictAdapter.fit()
        return self

    def save(self, file_name: str) -> DictAdapterBuilder:
        self.dictAdapter.save(file_name)
        return self

    def open(self, file_name) -> DictAdapterBuilder:
        self.dictAdapter.open(file_name)
        return self

    def build(self) -> DictAdapter:
        return self.dictAdapter
