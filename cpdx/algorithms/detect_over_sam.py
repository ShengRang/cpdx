# coding: utf-8


from interface import Detector as BaseDetector
from util import Sam, SamSearchBaseHandler


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
            # print 'fail and gen', (self.cur_state.r, self.pos-1, self.cur_len)
            self.res.append((self.cur_state.r, self.pos-1, self.cur_len))
        self.cur_len = 0

    def backtrack(self, v, state, pre_state):
        if self.cur_len > 0 and self.cur_len > self.thre:
            # print 'backtrack and gen', (pre_state.r, self.pos-1, self.cur_len)
            self.res.append((pre_state.r, self.pos-1, self.cur_len))
        self.cur_len = state.max + 1

    def loop(self, state):
        self.cur_state = state

    @property
    def result(self):
        if self.cur_len > 0 and self.cur_len > self.thre:
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
        a_range = (tokens_a[ap-tlen+1].pos, tokens_a[ap].pos+len(tokens_a[ap]))
        b_range = (tokens_b[bp-tlen+1].pos, tokens_b[bp].pos+len(tokens_b[bp]))
        pairs.append((a_range, b_range, tlen))
    return {
        'similarity': similarity,
        'pairs': pairs,
    }


class Detector(BaseDetector):

    def run(self, files):
        pass