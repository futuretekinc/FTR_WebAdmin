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

class OB_ENDPOINT_VIEW(MethodView):
    def get(self):
        form = OB_ENDPOINT_FORM(request.form)
        return render_template('obm/endpoint.html',form=form)
    
    def post(self):
        data = db.session.query(OB_ENDPOINT).all()
        result = ob_endpoint_many.dump(data)
        return fn_jsonify({ 'data' : result.data }) 

class OB_ENDPOINT_SAVE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_ENDPOINT_FORM(request.form)
        if form.validate():
            endpoint = OB_ENDPOINT()
            endpoint.ep_name = str(form.ep_name.data)
            db.session.add(endpoint)
            db.session.commit()
            flash('Thanks for registering')
        return redirect('/obm/endpoints')  


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
        eptypes = db.session.query(OB_ENDPOINT_TYPE).all() 
        result = ob_eptype_many.dump(eptypes)
        for row in result.data:
            row['delete'] = '<span class="ftr_table_delete" key="{ep_type}"><i class="fa fa-trash-o"></i></span>'.format(ep_type=row.get('ep_type'))
        return fn_jsonify({ 'data' : result.data }) 

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
            delObj = db.session.query(OB_ENDPOINT_TYPE).filter(OB_ENDPOINT_TYPE.ep_type == ep_type).first()
            db.session.delete(delObj)
            db.session.commit()
        return redirect('/obm/eptype')  









    
    
  

    
 