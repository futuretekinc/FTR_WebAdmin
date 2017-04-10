# -*- coding: utf-8 -*-
import os

from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.web import FallbackHandler, RequestHandler, Application

from app import app

def WSGIApplication(app):
    tr = WSGIContainer(app)
    application = Application([(r".*", FallbackHandler, dict(fallback=tr))])
    return application

def runServer(app):
    application = WSGIApplication(app)
    application.listen(80)
    IOLoop.instance().start()

def runDebug(app):
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
#     runServer(app)
    runDebug(app)