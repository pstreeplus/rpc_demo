#!/usr/bin/env python
# -*-coding:utf-8 -*-


from rpc_demo import SocketTransport
from rpc_demo import IOProt
from rpc_demo import Processor
from rpc_demo import Server

from handler import Handler

processor = Processor(Handler())
ioprot = IOProt(SocketTransport('localhost', 8080))
server = Server(processor, ioprot)
server.run()
