#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Server:

    def __init__(self, processor, ioprot):
        self._processor = processor
        self._ioprot = ioprot

    def run(self):
        while True:
            self._ioprot.trans.accept()
            while True:
                body = self._ioprot.read_body()
                if not body or body.get('close', False):
                    self._ioprot.trans.close()
                    break
                args = self._processor.process(body)
                self._ioprot.write_begin()
                for arg in args:
                    tp = type(arg)
                    if tp == int:
                        self._ioprot.write_int(arg)
                    elif tp == str:
                        self._ioprot.write_string(arg)
                self._ioprot.write_end()

    def shutdown(self):
        self._ioprot.trans.shutdown()
