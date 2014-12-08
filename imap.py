import pp
import time
def stat_imap(func, subname_depth = 1):
    def _wrapper(*args, **kwargs):
        name= func.__name__
        subname = '-'.join([name] + [ x for x in args[0:subname_depth] ])

        start_time = time.time()
        try:
            print args
            print kwargs
            result = func(*args, **kwargs)
        except Exception, e:
            total_time = int((time.time() - start_time) * 1000)
            pp.pprint( {'request_type':subname, 'name':name, 'response_time':total_time, 'exception':e})
            #events.request_failure.fire(request_type=subname, name=name, response_time=total_time, exception=e)
        else:
            if not result[0] in ['OK', 'BYE']:
                total_time = int((time.time() - start_time) * 1000)
                pp.pprint( {'request_type':subname, 'name':name, 'response_time':total_time, 'exception':None})
                #events.request_failure.fire(request_type=subname, name=name, response_time=total_time, exception=None)
                return result
            else:
                total_time = int((time.time() - start_time) * 1000)
                pp.pprint( {'request_type':subname, 'name':name, 'response_time':total_time, 'response_length':0})
                #events.request_success.fire(request_type="xmlrpc", name=name, response_time=total_time, response_length=0)
                return result
    return _wrapper

import imaplib
class ImapClient(imaplib.IMAP4):
    def __init__(self,host,port,user,pswd, timeout=3000):
        target_cmds = [
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
            ('uid',1),
        ]
        for cmd in target_cmds:
            setattr( self, cmd[0], stat_imap( getattr(self, cmd[0]) ,cmd[1]) )
        self.user = user
        self.pswd = pswd
        imaplib.IMAP4.__init__(self,host, port)

    def dologin(self):
        self.login(self.user, self.pswd)

if __name__ == '__main__':

    client = ImapClient(
        host = 'jpn-zaq50-v3.openwave.com',
        port = 10143,
        user = 'pacmain0000001',
        pswd = 'pacmain0000001',
    )
    client.dologin()
    client.select('inbox')
    client.uid('search',None,"all")
    client.logout()
