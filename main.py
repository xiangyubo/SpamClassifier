# -*- coding: UTF-8 -*-
import logging.config
import os

from spam_classifier.vocabulary_manager import VocabularyManager
from spam_classifier.trainer import Trainer

logging.config.fileConfig("conf\\logging.conf")  # 采用配置文件


def get_file_list(dir_path):
    dirs = os.listdir(dir_path)
    return [file for file in dirs]


def read_file_to_string(file_path):
    temp_list = []
    file = open(file_path, "r")
    lines = file.readlines()
    for line in lines:
        temp_list.append(line)
    return ''.join(temp_list)


def read_file_to_vocabulary(dir_path, vocabulary_manager):
    file_list = get_file_list(dir_path)
    for file in file_list:
        text = read_file_to_string(dir_path + '\\' + file)
        vocabulary_manager.append_article_to_vocabulary(text)


def read_file_to_trainer(dir_path, trainer, type):
    file_list = get_file_list(dir_path)
    for file in file_list:
        text = read_file_to_string(dir_path + '\\' + file)
        trainer.add_train_article(text, type)


def read_file_to_classify(dir_path, trainer):
    file_list = get_file_list(dir_path)
    total_count = 0
    correct_count = 0
    for file in file_list:
        text = read_file_to_string(dir_path + '\\' + file)
        type, p = trainer.classify(text)
        total_count += 1
        if file.find(type) != -1:
            correct_count += 1

    print "total test:%d corretc:%d %f" % (total_count, correct_count, 1.0 * correct_count / total_count)


if __name__ == '__main__':
    logger = logging.getLogger("main")
    logger.info("start build vocabulary")
    vocabulary_manager = VocabularyManager()
    read_file_to_vocabulary('data\\train\ham', vocabulary_manager)
    read_file_to_vocabulary('data\\train\spam', vocabulary_manager)
    vocabulary_manager.build_vocabulary()
    logger.info("end build vocabulary")
    logger.info("start add article for train")
    trainer = Trainer(vocabulary_manager)
    read_file_to_trainer('data\\train\ham', trainer, "ham")
    read_file_to_trainer('data\\train\spam', trainer, "spam")
    logger.info("end add article for train")
    logger.info("start train")
    model = trainer.train_bayes()
    logger.info("end train")
    print model
    read_file_to_classify('data\\test', trainer)
