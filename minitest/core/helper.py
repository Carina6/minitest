#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2018/12/11 14:10
# @Author: hlliu
import functools
import inspect

import time
import traceback


# def logwrap(logger):
#
#     def Logwrap(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             start = time.time
#
#             m = inspect.getcallargs(func, *args, **kwargs)
#             fndata = {'name': func.__name__, 'call_args': m, 'start_time': start}
#             # LOGGER.running_stack.append(fndata)
#             logger.info(fndata)
#
#             try:
#                 res = func(*args, **kwargs)
#                 time.sleep(2)
#             except Exception as e:
#                 data = {"traceback": traceback.format_exc(), "end_time": time.time()}
#                 fndata.update(data)
#                 raise
#             finally:
#                 logger.info(fndata)
#
#             return res
#
#         return wrapper
#
#     return Logwrap


def logwrap(logger):

    def Logwrap(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info('{}.{}() is starting'.format(func.__module__, func.__qualname__))

            start = time.time()
            m = inspect.getcallargs(func, *args, **kwargs)
            fndata = {'name': func.__name__, 'call_args': m, 'start_time': start}
            # LOGGER.running_stack.append(fndata)

            logger.info(fndata)

            try:
                res = func(*args, **kwargs)
                time.sleep(2)
            except Exception as e:
                data = {"traceback": traceback.format_exc(), "end_time": time.time()}
                fndata.update(data)
                raise
            finally:
                logger.info(fndata)

            logger.info('{}.{}() is end'.format(func.__module__, func.__qualname__))
            return res

        return wrapper

    return Logwrap


# def ready_method(func):
#     @functools.wraps(func)
#     def ready(inst, *args, **kwargs):
#         key = "_%s_ready" % func.__name__
#         res = func(inst, *args, **kwargs)
#         setattr(inst, key, True)
#
#         return res
#     return ready


def on_method_ready(method):
    def method_ready(func):
        @functools.wraps(func)
        def ready(inst, *args, **kwargs):
            m = getattr(inst, method)
            m()
            res = func(inst, *args, **kwargs)
            return res
        return ready
    return method_ready


class G(object):
    DEVICE = None