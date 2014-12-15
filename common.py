# -*- coding: utf-8 -*-

import time
from locust import events, task, TaskSet

def stat(modulename, method, is_ok, excepts, num_arg_show):

    def _wrapper(*args, **kwargs):
        subname = '-'.join([method.__name__] + [ x for x in args[1:num_arg_show+1] ])

        start_time = time.time()
        try:
            result = method(*args, **kwargs)
        except excepts as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type=modulename, name=subname, response_time=total_time, exception=e)
        else:
            if is_ok(result):
                total_time = int((time.time() - start_time) * 1000)
                events.request_success.fire(request_type=modulename, name=subname, response_time=total_time, response_length=0)
                return result
            else:
                total_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(request_type=modulename, name=subname, response_time=total_time, exception=None)
                return result
    return _wrapper

def measure(func):
    def _wrapper(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        total_time = int((time.time() - start_time) * 1000)
        events.request_success.fire(request_type='TASK', name=func.__name__, response_time=total_time, response_length=0)
        return result
    return _wrapper
    
        
