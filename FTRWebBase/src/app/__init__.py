# -*- coding:utf-8 -*-
from datetime import datetime
import logging
import os
import pickle
import sys
import time

from flask import *
from flask.sessions import SessionInterface, SessionMixin
from flask_apscheduler import APScheduler
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user , current_user
from flask_marshmallow import Marshmallow
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from sqlalchemy import MetaData, create_engine
from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy.pool import Pool
from uuid import uuid4



import numpy as np
import pandas as pd

def create_db(app,metadata):
    db = SQLAlchemy(app,metadata=metadata,session_options={'autocommit':False},use_native_unicode=True)
    return db

def init_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    app.debug_log_format = "%(levelname)s in %(module)s [%(lineno)d]: %(message)s"
    metadata = MetaData()
    db = create_db(app,metadata)
    ma = Marshmallow(app)
#     scheduler = APScheduler()
#     scheduler.init_app(app)
#     scheduler.start()
    return app, metadata,db, ma

app, metadata, db, ma = init_app()
# from app.cmm.forms import LoginForm

from app.cmm.controllers import cmm
from app.cmm.models import CM_CODEM, CM_CODED, FlaskSession
from app.cmm.services.menu_handler import find_menu

from app.cmm.utils.sqlalchemy_session import SQLAlchemySessionInterface
from app.evm.models import *
from app.obm.controllers import obm
from app.obm.models import *
from app.rtm.controllers import rtm

#app.session_interface = SQLAlchemySessionInterface()
@event.listens_for(Pool,"checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute('SELECT 1')
    except:
        raise exc.DisconnectionError()
    cursor.close()

@app.before_first_request
def before_first_request_handler():
    app.logger.debug("MENU 초기화")
    session['tree'] = find_menu()

@app.before_request
def before_request_handler():
    if 'tree' not in session:
        session['tree'] = find_menu()
    
# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404    

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403    

@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

@app.errorhandler(500)
def server_error(error):
#     app.logger.error(error)
    return render_template('500.html'), 500    

@app.teardown_appcontext
def shutdown_session(exception=None):
    #app.logger.debug('**************** SHUTDOWN SESSION ****************')
    #app.logger.debug('exception->',exception)
    db.session.remove()

# --------------------------------------------------
@app.route('/session_out')
def loginousst():
    session.clear()
    return 'session signout'

# --------------------------------------------------

# Import a module / component using its blueprint handler variable (mod_auth)

apimanager = APIManager(app,flask_sqlalchemy_db=db)
apimanager.create_api(CM_CODEM,methods=['GET']) 
# results_per_page [option] 
apimanager.create_api(CM_CODED,methods=['GET']) 
    
# Register blueprint(s) 
app.register_blueprint(cmm)
app.register_blueprint(obm)
app.register_blueprint(rtm)

# app.register_blueprint(xyz_module)
# .. 

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all() 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"

from app.cmm.services.service import MD_CM_USER
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    service = MD_CM_USER()
    profile = service.get_profile(email)
    if not profile:
        return 
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    service = MD_CM_USER()
    email = request.form.get('email')
    profile = service.get_profile(email)
    if not profile:
        return 
    user = User()
    user.id = email
    pwd = profile.get('passwd')
    user.is_authenticated = ( request.form['passwd'] == pwd )
    return user

# 
# @app.route('/')
# def index():
#     return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
@app.route('/login',methods=['GET','POST'])        
@app.route('/',methods=['GET','POST'])
def login_page():
    service = MD_CM_USER()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['passwd']
        profile = service.get_profile(email)
        if profile is None:
            return redirect(url_for('login_page'))

        if password == profile.get('passwd'):
            gw = profile.get('gateway')
            user = User()
            user.id = email
            login_user(user)
            session['tree'] = find_menu()
            if len(gw) > 0: 
                return redirect(url_for('obm.ob_gateway_view'))
            else:
                return redirect(url_for('obm.ob_gateway_add'))
        else:
            return redirect(url_for('login_page'))
    else:
        return render_template('cmm/login.html')
    
@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return "unauthorized"

@app.route("/img/<filename>")
def static_img(filename):
    return send_from_directory('static/img',filename=filename)



