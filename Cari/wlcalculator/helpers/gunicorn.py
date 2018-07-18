bind = "unix:/vagrant/sockfile"
errorlog = '/vagrant/logs/gunicorn.err'
accesslog = '/vagrant/logs/gunicorn.acc'
loglevel = "debug"
workers = 3
worker_class = 'gevent'

max_requests = 1000
timeout = 30
keep_alive = 2

preload = True

