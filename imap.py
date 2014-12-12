# -*- coding: utf-8 -*-

import common

import imaplib
superclass=imaplib.IMAP4
excepts= (imaplib.IMAP4.error)


from random import randint
import re
class Client(superclass):
    def __init__(self, host = '', port = imaplib.IMAP4_PORT):
        self.debug = imaplib.Debug
        self.state = 'LOGOUT'
        self.literal = None             # A literal argument to a command
        self.tagged_commands = {}       # Tagged commands awaiting response
        self.untagged_responses = {}    # {typ: [data, ...], ...}
        self.continuation_response = '' # Last continuation response
        self.is_readonly = False        # READ-ONLY desired state
        self.tagnum = 0

        # Create unique tag for this session,
        # and compile tagged response matcher.

        
        self.tagpre = imaplib.Int2AP(randint(4096, 65535))
        self.tagre = re.compile(r'(?P<tag>'
                        + self.tagpre
                        + r'\d+) (?P<type>[A-Z]+) (?P<data>.*)')

        self.connect(host,port)

        typ, dat = self.capability()
        if dat == [None]:
            raise self.error('no CAPABILITY response from server')
        self.capabilities = tuple(dat[-1].upper().split())

        if __debug__:
            if self.debug >= 3:
                self._mesg('CAPABILITIES: %r' % (self.capabilities,))

        for version in imaplib.AllowedVersions:
            if not version in self.capabilities:
                continue
            self.PROTOCOL_VERSION = version
            return

        raise self.error('server not IMAP4 compliant')

    def connect(self, host, port):
        # Open socket to server.

        self.open(host, port)

        # Get server welcome message,
        # request and store CAPABILITY response.

        if __debug__:
            self._cmd_log_len = 10
            self._cmd_log_idx = 0
            self._cmd_log = {}           # Last `_cmd_log_len' interactions
            if self.debug >= 1:
                self._mesg('imaplib version %s' % __version__)
                self._mesg('new IMAP4 connection, tag=%s' % self.tagpre)

        self.welcome = self._get_response()
        if 'PREAUTH' in self.untagged_responses:
            self.state = 'AUTH'
            return 'OK', self.untagged_responses
        elif 'OK' in self.untagged_responses:
            self.state = 'NONAUTH'
            return 'OK', self.untagged_responses
        else:
            raise self.error(self.welcome)
            return 'NO', self.welcome

 
def is_ok(result):
    return result[0] in ['OK', 'BYE']

target_func = [
    ('login',0),
    ('logout',0),
    ('select',0),
    ('fetch',0),
    ('close',0),
    ('getquota',0),
    ('expunge',0),
    ('lsub',0),
    ('list',0),
    ('search',0),
    ('capability',0),
    ('connect',0),
    ('uid',1),
]
  
for cmd in target_func:
    setattr( Client, cmd[0],
        common.stat(
            modulename = superclass.__name__,
            method = getattr(Client, cmd[0]),
            is_ok = is_ok,
            excepts = excepts,
            num_arg_show = cmd[1]) )


