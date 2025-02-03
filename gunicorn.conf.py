import multiprocessing
import os

bind = "0.0.0.0:8000"
backlog = 2048
workers = 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2
accesslog = '-'
errorlog = '-'
loglevel = 'info'
proc_name = 'flowai'
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None
keyfile = None
certfile = None