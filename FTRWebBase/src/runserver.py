# -*- coding: utf-8 -*-
import os
from gevent.wsgi import WSGIServer
from app import app

if __name__ == '__main__x':
    http_server = WSGIServer(('',5000),app)
    http_server.serve_forever()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
    
