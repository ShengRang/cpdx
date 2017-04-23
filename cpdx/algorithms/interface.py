# coding: utf-8
"""
    算法相关的接口
"""

from cpdx.langs.common import parser_dispatch


class Detector(object):

    def __init__(self, lang, prep):
        self.parser = parser_dispatch(lang, prep)

    def run(self, files):
        raise NotImplementedError()