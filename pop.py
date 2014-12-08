import pp
import time
def stat_pop(func, subname_depth = 1):
    def _wrapper(*args, **kwargs):
        name= func.__name__
        subname = '-'.join([name] + [ x for x in args[0:subname_depth] ])

        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            pp.pprint({'name':name, 'subname':subname})
            pp.pprint(result)
        except Exception, e:
            print e 
            total_time = int((time.time() - start_time) * 1000)
            pp.pprint( {'request_type':subname, 'name':name, 'response_time':total_time, 'exception':e.__dict__})
            #events.request_failure.fire(request_type=subname, name=name, response_time=total_time, exception=e)
        else:
            rslt_str = result if not isinstance(result, (tuple, list)) else result[0]
            if not rslt_str.startswith('+OK'):
                print "## Note: ng" 
                total_time = int((time.time() - start_time) * 1000)
                pp.pprint( {'request_type':subname, 'name':name, 'response_time':total_time, 'exception':None})
                #events.request_failure.fire(request_type=subname, name=name, response_time=total_time, exception=None)
                return result
            else:
                print "## Note: ok" 
                total_time = int((time.time() - start_time) * 1000)
                pp.pprint( {'request_type':subname, 'name':name, 'response_time':total_time, 'response_length':0})
                #events.request_success.fire(request_type="xmlrpc", name=name, response_time=total_time, response_length=0)
                return result
    return _wrapper

import poplib
def stat(self):  #original stat does not return +OK nor NG
    retval = self._shortcmd('STAT')
    rets = retval.split()
    if self._debugging: print '*stat*', repr(rets)
    numMessages = int(rets[1])
    sizeMessages = int(rets[2])
    return retval,(numMessages, sizeMessages)

poplib.POP3.stat=stat

class PopClient(poplib.POP3):
    def __init__(self,host,port,p_user,p_pswd, timeout=3000):
        target_cmds = [
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
        for cmd in target_cmds:
            setattr( self, cmd[0], stat_pop( getattr(self, cmd[0]) ,cmd[1]) )
        self.p_user = p_user
        self.p_pswd = p_pswd
        poplib.POP3.__init__(self,host, port)

 

    def dologin(self):
        self.user(self.p_user)
        self.pass_(self.p_pswd)

if __name__ == '__main__':

    client = PopClient(
        host = 'jpn-zaq50.openwave.com',
        port = 11110,
        p_user = 'pacmain0000001',
        p_pswd = 'pacmain0000001',
    )
    client.dologin()
    client.list(1)
    client.stat()
    client.quit()
