from flask import render_template, g, abort, session, request, redirect, flash
from flask.views import View, MethodView
from sqlalchemy.orm import joinedload

from app import db, ma
from app.obm.forms import * 
from app.obm.models import *
from app.obm.services import *

'''
------------------------------------------------------------------------------------
OBM > ENDPOINT
------------------------------------------------------------------------------------
'''
'''OB_ENDPOINT VIEW'''
class OB_ENDPOINT_VIEW(MethodView):
    def get(self):
        form = OB_ENDPOINT_FORM(request.form)
        return render_template('obm/endpoints.html',form=form)
    
    def post(self):
        return ObEndpointHandler.do_read() 
    
'''OB_ENDPOINT SAVE'''
class OB_ENDPOINT_SAVE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_ENDPOINT_FORM(request.form)
        if form.validate():
            ret, msg = ObEndpointHandler.do_save(form.data)
            if ret is True:
                return redirect('/obm/endpoints')
            else:
                app.logger.debug('Except - ',msg)
            
        return render_template('obm/endpoints.html',form=form)

class OB_ENDPOINT_UPDATE(View):
    methods = ['POST']
    def dispatch_request(self):
        param = request.form
        try:
            ep_id = param.get('ep_id')
            obj = db.session.query(OB_ENDPOINT) \
                    .filter(OB_ENDPOINT.ep_id == ep_id) \
                    .first()
            obj.ep_name = str(param.get('ep_name'))
            obj.ep_location = str(param.get('ep_location'))
            db.session.commit()
        except Exception as e:
            err_msg = str(e)
        return redirect('/obm/devices')


class OB_ENDPOINT_DELETE(View):
    methods = ['POST']
    def dispatch_request(self):
        ep_id = request.form.get('ep_id')
        return ObEndpointHandler.do_delete(ep_id)

'''
------------------------------------------------------------------------------------
OBM > ENDPOINT_TYPE 
------------------------------------------------------------------------------------
'''

class OB_EPTYPE_VIEW(MethodView): 
    def get(self):
        form = OB_EPTYPE_FORM(request.form)   
        return render_template('obm/eptype.html',form=form) 
    def post(self):
        return ObEndpointTypeHandler.do_read()
   
class OB_EPTYPE_UPDATE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_EPTYPE_FORM(request.form)
        if form.updateValidate():
            ret, msg = ObEndpointTypeHandler.do_update(form.data)
            if ret is True:
                return redirect('/obm/eptype')
            else:
                app.logger.debug('Except - ',msg)
        return render_template('obm/eptype.html',form=form) 

class OB_EPTYPE_SAVE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_EPTYPE_FORM(request.form)
        if form.validate():
            ret, msg = ObEndpointTypeHandler.do_save(form.data)
            if ret is True:
                return redirect('/obm/eptype')
            else:
                app.logger.debug('Except - ',msg)
            
        return render_template('obm/eptype.html',form=form) 

class OB_EPTYPE_DELETE(View):
    methods = ['POST']
    def dispatch_request(self):
        ep_type = request.form.get('ep_type')
        if ep_type is not None:
            ret, msg = ObEndpointTypeHandler.do_delete(ep_type)
            if ret is False:
                app.logger.debug('Except - ',msg)
        return redirect('/obm/eptype')  








    
    
  

    
 