#!/usr/bin/env python
# -*-coding:utf-8 -*-


class Handler:

    def __init__(self):
        self._method_map = {
            'add': self._add,
            'len': self._len,
            'multi': self._multi,
            'sub': self._sub,
            'div': self._div,
        }

    def process(self, params):
        method_name = params.get('method_name')
        if method_name in self._method_map:
            return self._method_map[method_name](params.get('args'))
        else:
            return None

    def _add(self, args):
        if type(args[0]) == int:
            return [sum(args)]
        else:
            return [''.join(args)]

    def _len(self, args):
        return [len(arg) for arg in args]

    def _multi(self, args):
        result = 1
        for arg in args:
            result *= arg
        return [result]

    def _sub(self, args):
        return [args[0] - args[1]]

    def _div(self, args):
        return [args[0] / args[1]]
