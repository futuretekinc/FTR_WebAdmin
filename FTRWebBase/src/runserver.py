# -*- coding: utf-8 -*-

import os
from gevent.wsgi import WSGIServer
from app import app
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

if __name__ == '__main__x':
    http_server = WSGIServer(('',5000),app)
    http_server.serve_forever()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__z':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(80)
    IOLoop.instance().start()
