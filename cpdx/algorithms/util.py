# coding: utf-8

from collections import deque


class SamNode(object):
    # __slots__ = ('fail', 'max', 'next')

    def __init__(self, step=0):
        self.fail = None
        self.max = step
        self.next = dict()
        self.indeg = 0
        self.r = 0


class SamSearchBaseHandler(object):

    def __init__(self):
        """ sam: 当前自动机, string: 匹配串, pos: 当前匹配位置
        """
        self.sam = None
        self.string = ""
        self.pos = -1

    def loop(self, state):
        # 本轮状态转移完成执行, state表示转移之后的状态
        pass

    def read(self, v, state):
        # 成功读入字符v, 并转换到状态state
        pass

    def fail(self, v):
        # 读入字符v, 匹配失败. 状态回到初始状态
        pass

    def backtrack(self, v, state, pre_state):
        # 读入字符v, 直接匹配失败, 但是通过fail指针找到了存在转化的状态, 转移后的前一个为state
        # fail转移前为pre_state
        pass

    @property
    def result(self):
        return None


class Sam(object):

    def __init__(self, key=lambda x: x):
        self.nodes = []
        self.scnt = 0
        self.end = self.new_node(0)
        self.start = self.end
        self.key = key
        self.topos = []

    def new_node(self, step):
        node = SamNode(step)
        self.nodes.append(node)
        return node

    def insert(self, i, x):
        x = self.key(x)
        p = self.end
        np = self.new_node(0)
        np.r = i
        while (p is not None) and (p.next.get(x) is None):
            p.next[x] = np
            p = p.fail
        if p is None:
            np.fail = self.start
        else:
            q = p.next[x]
            if p.max+1 == q.max:
                np.fail = q
            else:
                nq = self.new_node(p.max+1)
                nq.r = i
                nq.next = {k: v for k, v in q.next.iteritems()}
                nq.fail = q.fail
                q.fail = nq
                np.fail = nq
                while p is not None and p.next[x] == q:
                    p.next[x] = nq
                    p = p.fail
        self.end = np

    def topo_sort(self):
        for node in self.nodes:
            if node.fail:
                node.fail.indeg += 1
        que = deque()
        for node in self.nodes:
            if node.indeg == 0:
                que.append(node)
        self.topos = []
        while que:
            t = que.popleft()
            self.topos.append(t)
            if t.fail:
                t.fail.indeg -= 1
            if t.fail.indeg == 0:
                que.append(t.fail)

    def build(self, string):
        """ 依次插入string的字符, 构建sam.
        注意string不一定是字符串, 是可迭代且元素不可变即可.
        """
        for i, x in enumerate(string):
            self.insert(i, x)
        # self.topo_sort()

    def search(self, string, handler):
        p = self.start
        handler.sam = self
        handler.string = string
        for _x in string:
            x = self.key(_x)
            handler.pos += 1
            pre = p
            if p.next.get(x) is not None:
                # 读入字符可以匹配
                handler.read(_x, p.next[x])
                p = p.next[x]
            else:
                while (p is not None) and (p.next.get(x) is None):
                    p = p.fail
                if p is None:
                    # 一直没有找到某个fail节点存在x弧转换
                    handler.fail(_x)
                    p = self.start
                else:
                    # 找到某个fail节点存在x弧转换
                    handler.backtrack(_x, p, pre)
                    p = p.next[x]
            handler.loop(p)
        return handler.result
