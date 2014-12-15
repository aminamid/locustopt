from time import time
from random import choice
from locust import TaskSet, task, HttpLocust, Locust

from common import measure
import pop
import smtp
import imap

cfg_popuser_list = [ 'pacmain{0:0>7}'.format(x) for x in range(10) ]
cfg_imapuser_list = [ 'pacmain{0:0>7}'.format(x) for x in range(10) ]
cfg_address_list = [ 'pacmain{0:0>7}@openwave.com'.format(x) for x in range(10) ]

class UserBehavior(TaskSet):
    def on_start(self):
        pass 

    @task(1)
    @measure
    def pop(self):
        cl=pop.Client('jpn-zaq50.openwave.com',11110)
        user = choice(cfg_popuser_list)
        cl.user(user)
        cl.pass_(user)
        cl.stat()
        cl.list()
        cl.quit()

    @task(1)
    @measure
    def smtp(self):
        cl=smtp.Client('jpn-zaq50.openwave.com',11025)
        user = choice(cfg_address_list)
        cl.sendmail(user, user, "test")

    @task(1)
    @measure
    def imap(self):
        cl=imap.Client('jpn-zaq50.openwave.com',11143)
        user = choice(cfg_imapuser_list)
        cl.login(user, user)
        cl.select('inbox')
        cl.uid('search',None,"all")
        cl.logout()



class MailUsers(Locust):
    task_set = UserBehavior
    min_wait=1
    max_wait=10
