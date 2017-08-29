import logging
import numpy as np
import math
import cPickle as pickle

from tokenizer import Tokenizer
from vocabulary_manager import VocabularyManager

class Trainer:
    # create logger
    logger = logging.getLogger("main")

    _TYPE_COUNT_KEY = "type_count"

    _WORD_VECTOR_KEY = "word_array"

    _WORD_COUNT_KEY = "word_count"

    _tokenizer = Tokenizer()

    _vocabulary_manager = None

    # _type_info_set = {"type" : {"word_vector" : np.array(), "word_count" : 0}}
    _type_info_dict = {}

    _article_count = 0

    _model = {}

    def __init__(self, vocabulary_manager):
        assert isinstance(vocabulary_manager, VocabularyManager)
        self._vocabulary_manager = vocabulary_manager
        # try:
        #     self._model = pickle.load(open("resources\model.txt", "rb"))
        # except BaseException, e:
        #     self.logger.warn("load model failed " + e.message)

    def add_train_article(self, article, type):
        assert isinstance(article, basestring)
        word_list = self._vocabulary_manager.convert_article_2_word_list(article)
        type_info = self._type_info_dict.get(type, None)
        if type_info == None:
            type_info = {self._WORD_VECTOR_KEY: np.ones(len(word_list)), \
                          self._WORD_COUNT_KEY: 1, \
                          self._TYPE_COUNT_KEY: 0}
            self._type_info_dict[type] = type_info
        type_info[self._WORD_VECTOR_KEY] += np.array(word_list)
        type_info[self._WORD_COUNT_KEY] += sum(word_list)
        type_info[self._TYPE_COUNT_KEY] += 1
        self._article_count += 1

    def train_bayes(self):
        for (type, type_info) in self._type_info_dict.items():
            word_probability_array = np.log(type_info[self._WORD_VECTOR_KEY] / type_info[self._WORD_COUNT_KEY])
            type_probability = 1.0 * type_info[self._TYPE_COUNT_KEY] / self._article_count
            self._model[type] = (word_probability_array, type_probability)
        # try:
        #     pickle.dump(self._model, open('resources\model.txt', 'wb'), 0)
        # except BaseException, e:
        #     self.logger.error("dump model failed " + e.message)
        return self._model

    def classify(self, article):
        assert isinstance(article, basestring)
        word_list = self._vocabulary_manager.convert_article_2_word_list(article)
        max_type = None
        max_p = float("-inf")
        for (type, model_info) in self._model.items():
            p = sum(word_list * model_info[0]) + math.log(model_info[1])
            if max_p < p:
                max_p = p
                max_type = type
        return max_type, max_p