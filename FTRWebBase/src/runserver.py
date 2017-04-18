# -*- coding: utf-8 -*-
import os
from gevent.wsgi import WSGIServer

from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.web import FallbackHandler, RequestHandler, Application

from app import app

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

def WSGIApplication(app):
    tr = WSGIContainer(app)
    application = Application([(r".*", FallbackHandler, dict(fallback=tr))])
    return application

def runServer(app,port=80):
    application = WSGIApplication(app)
    application.listen(port)
    IOLoop.instance().start()

def runGevent(app,port=80):
    http_server = WSGIServer(('',port),app)
    http_server.serve_forever()

def runDebug(app):
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
#     runServer(app)
#     runGevent(app,port=80)
    runDebug(app)