# -*- coding : utf-8 -*-
from flask import Response, jsonify, request, Blueprint, flash, redirect

from app import db, render_template, send_from_directory
from app.rtm.views import *
from app.rtm.views.real_time_view import RM_REAL_TIME_VIEW
from app.obm.services.device_service import MD_KEEP_ALIVE
from flask_login.utils import current_user, login_required

rtm = Blueprint('rtm', __name__, url_prefix='/rtm')

rtm.add_url_rule('/realtime',view_func=login_required(RM_REAL_TIME_VIEW().as_view('rm_real_time_view')))

@rtm.route('/keep_alive',methods=['GET','POST'])
@login_required
def keep_alive():
    if request.method == 'POST':
        email = current_user.id
        service = MD_KEEP_ALIVE()
        return service.get_status(email)
    
    return render_template('rtm/keep_alive.html')