# -*- coding: utf-8 -*-

import common

import smtplib
superclass=smtplib.SMTP
excepts= (smtplib.SMTPException)

class Client(superclass): pass

def is_ok(result):
    return 2 == result[0] // 100

target_func = [
    ('mail',0),
    ('rcpt',0),
    ('verify',0),
    ('connect',0),
    ('ehlo',0),
    ('helo',0),
    ('rset',0),
    ('noop',0),
    ('data',0),
    ('login',0),
    ('starttls',0),
    ('close',0),
    ('quit',0),
]


for cmd in target_func:
    setattr( Client, cmd[0],
        common.stat(
            modulename = superclass.__name__,
            method = getattr(Client, cmd[0]),
            is_ok = is_ok,
            excepts = excepts,
            num_arg_show = cmd[1]) )
