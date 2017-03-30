# -*- coding : utf-8 -*-
from flask import Response, jsonify, request, Blueprint, flash, redirect

from app import db, render_template, send_from_directory
from app.rtm.views import *
from app.rtm.views.real_time_view import RM_REAL_TIME_VIEW

rtm = Blueprint('rtm', __name__, url_prefix='/rtm')

rtm.add_url_rule('/realtime',view_func=RM_REAL_TIME_VIEW().as_view('rm_real_time_view'))
 