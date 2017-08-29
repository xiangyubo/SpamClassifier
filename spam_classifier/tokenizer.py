# -*- coding: UTF-8 -*-
import os
import re


class Tokenizer:
    '''split line to words'''

    _stopwords_set = set()

    _non_word_regexp = re.compile(r"(^\w|\s)*")

    def __init__(self):
        stopword_file = open('resources\stopword.txt', 'r')
        lines = stopword_file.readlines()
        for word in lines:
            self._stopwords_set.add(word.strip('\n'))
        stopword_file.close()


    def split_word(self, article):
        assert isinstance(article, basestring)
        temp_words_list = self._non_word_regexp.split(article)
        return [word for word in temp_words_list if len(word) > 0
                and word != '\n' and word != '\r' and word != '\t' and word != ''
                and (word not in self._stopwords_set)]