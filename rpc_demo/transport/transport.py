#!/usr/bin/env python
# -*- coding:utf-8 -*-


import socket


class SocketTransport:

    def __init__(self, host, port, mode='server'):
        self._host = host
        self._port = port
        self._mode = mode
        self._init()

    def _init(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self._mode == 'server':
            self._s.bind((self._host, self._port))
            self._s.listen(5)
        else:
            self._s.connect((self._host, self._port))
            self._s.settimeout(5)

    def accept(self):
        self._conn, self._addr = self._s.accept()
        self._conn.settimeout(5)

    def read(self, buf_size=1024):
        while True:
            try:
                if self._mode == 'server':
                    data = self._conn.recv(buf_size)
                else:
                    data = self._s.recv(buf_size)
                if not data:
                    return
                yield data
            except Exception as e:
                yield ['2']
                return

    def write(self, data):
        if self._mode == 'server':
            self._conn.sendall(data)
        else:
            self._s.sendall(data)

    def close(self):
        if self._mode == 'server':
            self._conn.close()
        else:
            self._s.close()

    def shutdown(self):
        if self._mode == 'server':
            self._s.close()
