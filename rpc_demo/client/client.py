#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Client:

    def __init__(self, ioprot):
        self._ioprot = ioprot

    def call(self, method_name, *args):
        self._ioprot.write_begin(method_name)
        for arg in args:
            tp = type(arg)
            if tp == int:
                self._ioprot.write_int(arg)
            elif tp == str:
                self._ioprot.write_string(arg)
        self._ioprot.write_end()
        body = self._ioprot.read_body()
        return body.get('args', [])

    def bye(self):
        self._ioprot.bye()
