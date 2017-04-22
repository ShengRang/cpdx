# coding: utf-8
"""
    算法相关的接口
"""


class Detector(object):

    def __init__(self, lang, prep):
        self.lang = lang
        self.prep = prep

    def run(self, files):
        pass