# coding: utf-8

from __future__ import division
import os


from .interface import Detector as BaseDetector
from .util import Sam, SamSearchBaseHandler


class SearchHandler(SamSearchBaseHandler):

    def __init__(self, t=4):
        super(SearchHandler, self).__init__()
        self.res = []
        self.cur_len = 0
        self.cur_state = None
        self.thre = t

    def read(self, v, state):
        self.cur_len += 1

    def fail(self, v):
        if self.cur_len > 0 and self.cur_len > self.thre:
            print 'fail and gen', (self.cur_state.r, self.pos-1, self.cur_len)
            self.res.append((self.cur_state.r, self.pos-1, self.cur_len))
        self.cur_len = 0

    def backtrack(self, v, state, pre_state):
        if self.cur_len > 0 and self.cur_len > self.thre:
            print 'backtrack and gen', (pre_state.r, self.pos-1, self.cur_len)
            self.res.append((pre_state.r, self.pos-1, self.cur_len))
        self.cur_len = state.max + 1

    def loop(self, state):
        self.cur_state = state

    @property
    def result(self):
        if self.cur_len > 0 and self.cur_len > self.thre:
            print('last gen')
            self.res.append((self.cur_state.r, self.pos, self.cur_len))
        return self.res


def cover_len(sam_res):
    """ 计算sam_res的覆盖长度
    """
    res = sam_res[0][2]
    pre = sam_res[0][1]
    for _, cp, le in sam_res[1:]:
        if cp - le < pre:
            res += cp - pre
        else:
            res += le
        pre = cp
    return res


def detect2(tokens_a, tokens_b, sam_a=None, sam_b=None, t=5):
    """ 由两个 tokens 进行比较, t 为 token 数量的阈值
    """
    # print 'tokens_a'
    # for token in tokens_a:
    #     print token.kind
    # print 'tokens_b'
    # for token in tokens_b:
    #     print token.kind

    if not isinstance(sam_a, Sam):
        sam_a = Sam(lambda t: t.kind)
        sam_a.build(tokens_a)
    if not isinstance(sam_b, Sam):
        sam_b = Sam(lambda t: t.kind)
        sam_b.build(tokens_b)
    sam_res_a = sam_a.search(tokens_b, SearchHandler(t))
    sam_res_b = sam_b.search(tokens_a, SearchHandler(t))
    similarity = (cover_len(sam_res_a) + cover_len(sam_res_b)) /\
                 (len(tokens_a) + len(tokens_b))
    pairs = []
    for ap, bp, tlen in sam_res_a:
        a_range = (tokens_a[ap-tlen+1].location.pos, tokens_a[ap].location.pos+len(tokens_a[ap]))
        b_range = (tokens_b[bp-tlen+1].location.pos, tokens_b[bp].location.pos+len(tokens_b[bp]))
        pairs.append((a_range, b_range, tlen))
    return {
        'similarity': similarity,
        'pairs': pairs,
    }


class Detector(BaseDetector):

    def run(self, files, len_t=5, sim_t=0.7):
        parsers = []
        filenames = [os.path.basename(f) for f in files]
        for f in files:
            parser = self.parser_cls()
            parser.parse(f)
            parsers.append(parser)
        tokens_list = []
        for p in parsers:
            tokens_list.append(p.get_tokens())
        sams = []
        for tokens in tokens_list:
            sam = Sam(lambda t: t.kind)
            sam.build(tokens)
            sams.append(sam)
        s = len(files)
        res = []
        for i in range(s):
            for j in range(i+1, s):
                r2 = detect2(tokens_list[i], tokens_list[j], sams[i], sams[j], len_t)
                # print('{0} - {1}:'.format(filenames[i], filenames[j]))
                # print(r2)
                if r2.get('similarity', 0.0) > sim_t:
                    res.append({
                        'src': filenames[i],
                        'dst': filenames[j],
                        'similarity': r2['similarity'],
                        'pairs': r2['pairs']
                    })
        res.sort(key=lambda x: x['similarity'], reverse=True)
        return res
