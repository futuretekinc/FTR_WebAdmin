from flask import render_template, jsonify, g, abort,session,request,redirect,flash
from flask.views import View, MethodView

from app import db, ma
from app.obm.models import *
from app.obm.forms import OB_RESOURCE_FORM, OB_GATEWAY_FORM, OB_DEVICE_FORM, OB_ENDPOINT_FORM

class RM_REAL_TIME_VIEW(MethodView):
    def get(self):
        return render_template('rtm/realtime.html')
'''
    def post(self):
        data = db.session.query(OB_RESOURCE).all() 
        result = ob_resource_many.dump(data)
        return jsonify({ 'data' : result.data }) 
'''
