#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing
import os

if not os.path.exists('log'):
    os.mkdir('log')

debug = True
# worker_class = 'gevent'
preload_app = True
reload = True
loglevel = 'debug'
threads = 20
# bind = '127.0.0.1:28000'
# pidfile = 'log/gunicorn.pid'
# logfile = 'log/debug.log'
# errorlog = 'log/error.log'
# accesslog = 'log/access.log'

# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'
