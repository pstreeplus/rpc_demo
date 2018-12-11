#!/use/bin/env python
# -*- coding:utf-8 -*-


class Processor:

    def __init__(self, handler):
        self._handler = handler

    def process(self, args):
        return self._handler.process(args)
