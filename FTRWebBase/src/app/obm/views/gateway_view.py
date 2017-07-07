from flask import render_template, g, abort, session, request, redirect, flash
from flask.views import View, MethodView
from flask_login import current_user
from sqlalchemy.orm import joinedload

from app import db, ma
from app.cmm.services.service import MD_CM_USER
from app.obm.forms import * 
from app.obm.forms.obm_forms import OB_GATEWAY_SAVE_FORM
from app.obm.models import *
from app.obm.services import *
from app.obm.services.gateway_service import ObGatewayHandler, MD_OB_GATEWAY
from app.cmm.models import CM_USER_GATEWAY


class OB_GATEWAY_VIEW(MethodView):
    def get(self):
        form = OB_GATEWAY_FORM(request.form)
        return render_template('obm/gateway.html',form=form)
    
    def post(self):
        email = current_user.id
        service = MD_CM_USER()
        profile = service.get_profile(email)
        gw = profile.get('gateway')
        return fn_jsonify({ 'data' : gw }) 

class OB_GATEWAY_UPDATE(View):
    methods = ['POST']
    def dispatch_request(self):
        service = MD_OB_GATEWAY()
        form = OB_GATEWAY_FORM(request.form)
        
        print("[VALIDATION]---------------------->" + str(form.validate()))
        print(form.data)
        if form.validate():
            ret = service.do_update(form.data)
            if ret is True:
                return redirect('/obm/gateway')  
                
        return render_template('obm/gateway.html',form=form)  

class OB_GATEWAY_SAVE(View):
    methods = ['POST']
    def dispatch_request(self):
        service = MD_OB_GATEWAY()
        form = OB_GATEWAY_SAVE_FORM(request.form)
        if form.validate():
            service.do_save(form.data)
            return redirect('/obm/gateway')
#             service.do_update(form.data)
#             ret, msg = ObGatewayHandler.do_save(form.data)
#             if ret is True:
#                 return redirect('/obm/add_gateway')  
#             else:
#                 app.logger.debug('Except - ',msg)
                
        return render_template('obm/add_gateway.html',form=form)  

class OB_GATEWAY_ADD(MethodView):
    def get(self):
        form = OB_GATEWAY_SAVE_FORM(request.form)
        return render_template('obm/add_gateway.html',form=form)
    
    def post(self):
        email = current_user.id
        service = MD_OB_GATEWAY()
        form = OB_GATEWAY_SAVE_FORM(request.form)
        try:
            if form.validate():
                service.do_save(form.data)
                cmUser = CM_USER_GATEWAY()
                cmUser.email = email
                cmUser.gw_id = form.data.get('gw_id')
                db.session.add(cmUser)
                db.session.commit()
                return redirect('/obm/gateway')
        except Exception as e:
            db.session.rollback()
        return render_template('obm/add_gateway.html',form=form)
            