# coding: utf-8
""" 一些语言相关的接口
"""


class Index(object):

    def __init__(self, preps=""):
        self.prep_str = preps
        self.preps = []

    def setup_prep(self):
        pass

    def parse(self, path):
        """ parse
        """
        raise NotImplementedError()

    def get_tokens(self):
        """ 获取 Tokens
        """
        raise NotImplementedError()

    def get_ast(self):
        """ 获取 AST
        """
        raise NotImplementedError()


class Processor(object):
    """ 预处理/后处理器
    """

    def __init__(self):
        pass

    def __call__(self, tokens):
        """ 接受 token 序列并返回处理后的 token 序列
        """
        raise NotImplementedError()