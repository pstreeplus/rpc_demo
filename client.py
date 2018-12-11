#!/usr/bin/env python
# -*-coding:utf-8 -*-

from rpc_demo import IOProt
from rpc_demo import Client
from rpc_demo import SocketTransport

ioprot = IOProt(SocketTransport('localhost', 8080, 'client'))
client = Client(ioprot)

print client.call('add', 1, 2, 3, 4)[0]
print client.call('add', 'hello', ' world!')[0]
print client.call('len', 'rpc demo')[0]


"""
output:

10
hello world!
8
"""

client.bye()
