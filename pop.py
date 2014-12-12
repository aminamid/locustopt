# -*- coding: utf-8 -*-

import common

import poplib
superclass=poplib.POP3
excepts= (poplib.error_proto)

from socket import create_connection, _GLOBAL_DEFAULT_TIMEOUT

class Client(superclass): 
    def __init__(self, host, port=poplib.POP3_PORT,
                 timeout=_GLOBAL_DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.connect(host, port, timeout)

    def connect(self, host, port, timeout):
        self.sock = create_connection((host, port), timeout)
        self.file = self.sock.makefile('rb')
        self._debugging = 0
        self.welcome = self._getresp()
        return self.welcome

    def stat(self):  #original stat does not return +OK nor NG
        retval = self._shortcmd('STAT')
        rets = retval.split()
        if self._debugging: print '*stat*', repr(rets)
        numMessages = int(rets[1])
        sizeMessages = int(rets[2])
        return retval,(numMessages, sizeMessages)

def is_ok(result):
    return (result if not isinstance(result, (tuple, list)) else result[0]).startswith('+OK')


target_func = [
    ('connect',0),
    ('user',0),
    ('pass_',0),
    ('apop',0),
    ('rpop',0),
    ('stat',0),
    ('list',0),
    ('retr',0),
    ('dele',0),
    ('rset',0),
    ('noop',0),
    ('quit',0),
    ('top',0),
    ('uidl',0),
]

for cmd in target_func:
    setattr( Client, cmd[0],
        common.stat(
            modulename = superclass.__name__,
            method = getattr(Client, cmd[0]),
            is_ok = is_ok,
            excepts = excepts,
            num_arg_show = cmd[1]) )
