import pp
import time
def stat_smtp(func, subname_depth = 1):
    def _wrapper(*args, **kwargs):
        name= func.__name__
        subname = '-'.join([name] + [ x for x in args[0:subname_depth] ])
        try:
            start_time = time.time()
            result = func(*args, **kwargs)
        except Exception, e:
            pp.pprint(e)
            total_time = int((time.time() - start_time) * 1000)
            pp.pprint( {'request_type':subname, 'name':name, 'response_time':total_time, 'exception':e})
            #events.request_failure.fire(request_type=subname, name=name, response_time=total_time, exception=e)
        else:
            if not (200 <= result[0] <= 299):
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

import smtplib
class SmtpClient(smtplib.SMTP):
    def __init__(self,host,port,localhost,user,pswd,timeout=3000):
        target_cmds = [
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
        for cmd in target_cmds:
            setattr( self, cmd[0], stat_smtp( getattr(self, cmd[0]) ,cmd[1]) )
        self.user = user
        self.pswd = pswd
        smtplib.SMTP.__init__(self,host, port, localhost)


if __name__ == '__main__':

    client = SmtpClient(
        host = 'jpn-zaq50.openwave.com',
        port = 11025,
        localhost = 'jpn-zaq50.openwave.com',
        user = 'pacmain0000001',
        pswd = 'pacmain0000001',
    )
    client.sendmail("pacmain0000001@openwave.com", "pacmain0000001@openwave.com", "test"*5000000)
    client.quit()
