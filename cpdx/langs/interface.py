# coding: utf-8
""" 一些语言相关的接口
"""


class Parser(object):

    def __init__(self, preps=""):
        self.prep_strs = preps.split('!')
        self.preps = []
        self.setup_prep()

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

    def __call__(self, *arg, **kwargs):
        """ 可能是针对 token 的预处理, 也可能是针对 ast 的预处理/后处理.
        """
        raise NotImplementedError()