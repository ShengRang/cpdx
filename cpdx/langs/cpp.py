# coding: utf-8

import clang
from clang.cindex import TokenKind
from interface import Index as BaseIndex, Processor
from common import SourceCode, Token, Location

LIBCLANG_PATH = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib"
clang.cindex.Config.set_library_path(LIBCLANG_PATH)


class Index(BaseIndex):

    def __init__(self):
        super(Index, self).__init__()
        self.cindex = clang.cindex.Index.create()
        self.source = SourceCode()

    def setup_prep(self):
        self.preps = []
        for p in self.prep_str.split('!'):
            prep = {
                'comment': CommentProcessor,
                'spec-keyword': SpecKeywordProcessor,
                'spec-punctuation': SpecPuncProcessor,
            }.get(p, None)
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


class CommentProcessor(Processor):

    def __call__(self, tokens):
        return filter(lambda t: t.kind != TokenKind.COMMENT, tokens)


class SpecKeywordProcessor(Processor):

    def __call__(self, tokens):
        def f(token):
            if token.kind == TokenKind.KEYWORD:
                token = Token(token.value, token.value, token.location)
            return token
        return [f(t) for t in tokens]


class SpecPuncProcessor(Processor):

    def __call__(self, tokens):
        def f(token):
            if token.kind == TokenKind.PUNCTUATION:
                token = Token(token.value, token.value, token.location)
            return token
        return [f(t) for t in tokens]


