# coding: utf-8

import functools

import clang
from clang.cindex import TokenKind
from interface import Parser as BaseParser, Processor
from common import SourceCode, Token, Location

LIBCLANG_PATH = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib"
clang.cindex.Config.set_library_path(LIBCLANG_PATH)


class Parser(BaseParser):

    def __init__(self):
        super(Parser, self).__init__()
        self.cindex = clang.cindex.Index.create()
        self.source = SourceCode()

    def setup_prep(self):
        self.preps = []
        for p in self.prep_str.split('!'):
            prep = {
                'comment': comment_processor,
                'spec-keyword': spec_keyword_processor,
                'spec-punctuation': spec_punc_processor,
                'ast-cut': ASTCutProcessor(self),
            }.get(p, None)
            if not prep:
                print('Warning: no preprocessor {0}'.format(p))
            self.preps.append(prep)

    def parse(self, path):
        self.tu = self.cindex.parse(path)
        self.source.read_from_path(path)

    def get_tokens(self):
        tokens = [Token(t.kind, t.spelling, Location(t.location.line, t.location.column))
                  for t in self.tu.cursor.get_tokens()]
        for prep in self.preps:
            if prep:
                tokens = prep(tokens)
        return tokens

    def get_ast(self):
        pass

# 几种 processor 的声明和使用


comment_processor = functools.partial(filter, lambda t: t.kind != TokenKind.COMMENT)


def spec_keyword_processor(tokens):
    def f(token):
        if token.kind == TokenKind.KEYWORD:
            token = Token(token.value, token.value, token.location)
        return token
    return [f(t) for t in tokens]


def spec_punc_processor(tokens):
    def f(token):
        if token.kind == TokenKind.PUNCTUATION:
            token = Token(token.value, token.value, token.location)
        return token
    return [f(t) for t in tokens]


class ASTCutProcessor(Processor):

    def __init__(self, index):
        super(ASTCutProcessor, self).__init__()
        self.index = index

    def __call__(self, tokens):
        raise NotImplementedError()
