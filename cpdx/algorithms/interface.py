# coding: utf-8
"""
    算法相关的接口
"""

from functools import partial

from cpdx.langs import parser_dispatch


class Detector(object):

    def __init__(self, lang, prep):
        self.parser_cls = partial(parser_dispatch(lang), prep)

    def run(self, files):
        raise NotImplementedError()