import logging

from tokenizer import Tokenizer

class VocabularyManager:
    # create logger
    logger = logging.getLogger("main")

    _vocabulary_set = set()

    _vocabulary_dict = {}

    _vocabulary_list = list()

    _tokenizer = Tokenizer()

    def __init__(self):
        file = None
        try:
            file = open("resources\\vocabulary.txt", "r")
            lines = file.readlines()
            for word in lines:
                self._vocabulary_set.add(word.strip('\n'))
        except IOError, e:
            self.logger.error("read vocabulary failed " + e.message)
        finally:
            if file is not None:
                file.close()

    def append_article_to_vocabulary(self, article):
        assert isinstance(article, basestring)
        self._vocabulary_set |= set(self._tokenizer.split_word(article))

    def build_vocabulary(self):
        self._vocabulary_list = list(self._vocabulary_set)
        for i in range(0, len(self._vocabulary_list)):
            self._vocabulary_dict[self._vocabulary_list[i]] = i
        file = None
        try:
            file = open("resources\\vocabulary.txt", "w")
            for word in self._vocabulary_list:
                file.write(word + '\n')
        except IOError, e:
            self.logger.error("write vocabulary failed " + e.message)
        finally:
            if file is not None:
                file.close()

    def convert_article_2_word_list(self, article):
        assert isinstance(article, basestring)
        word_list = self._tokenizer.split_word(article)
        ret = [0] * len(self._vocabulary_list)
        for word in word_list:
            if word in self._vocabulary_set:
                ret[self._vocabulary_dict[word]] += 1
            # else:
                # print "word: %s not in vocabulary" % word
        return ret