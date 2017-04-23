# coding: utf-8
""" 通用, 如源码位置操作, token等
"""

import functools

import cpp
import c


class SourceCode(object):
    """
    source code manipulation
    """

    def __init__(self):
        self.source_lines = []
        self.source = ''
        self.pre_lens = []

    def read_from_path(self, path):
        f = open(path, 'r')
        self.source_lines = f.readlines()
        self.source = ''.join(self.source_lines)
        self.pre_lens = [0, len(self.source_lines[0])]    # 除去\n
        for line in self.source_lines[1:]:
            self.pre_lens.append(len(line) + self.pre_lens[-1])

    def get_range(self, start, stop):
        """ 源代码的[start, stop)子串
        """
        if isinstance(start, Location):
            start = self.pos(start.line, start.col)
        if isinstance(stop, Location):
            stop = self.pos(stop.line, stop.col)
        return self.source[start:stop]

    def pos(self, row, column):
        """ 给出row行column列在整个code字符串里的位置, 行号从1开始
        """
        return self.pre_lens[row-1] + column - 1


class Location(object):
    """
    location of source code
    """

    def __init__(self, line=1, col=1, pos=0):
        self.line = line
        self.col = col
        self.pos = pos


class Token(object):
    """
    Token
    """

    def __init__(self, kind, value, location=None):
        self.kind = kind
        self.value = value
        self.location = location

    def __len__(self):
        return len(self.value)


def parser_dispatch(lang="cpp", prep="comment!spec-keyword"):
    """ Return an instance of spec parser
    """
    parser_cls = {
        "cpp": cpp.Parser,
        "c": c.Parser,
    }.get(lang)
    return parser_cls(prep)

