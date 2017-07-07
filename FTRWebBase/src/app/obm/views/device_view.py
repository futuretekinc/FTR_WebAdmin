from flask import render_template, g, abort, session, request, redirect, flash
from flask.views import View, MethodView
from sqlalchemy.orm import joinedload

from app import db, ma
from app.obm.forms import *  
from app.obm.models import *
from app.obm.services import *
from flask_login.utils import current_user
from app.obm.forms.obm_forms import USER_GATEWAY_FROM

'''
------------------------------------------------------------------------------------
OBM > DEVICE
------------------------------------------------------------------------------------
'''

class OB_DEVICE_VIEW(MethodView):
    def get(self):
        form = OB_DEVICE_FORM(request.form)
        epForm = OB_ENDPOINT_FORM(request.form)
        email = current_user.id
        usrForm = USER_GATEWAY_FROM(request.form)
        usrForm.update_field(email)
        return render_template('obm/devices.html',form=form,epForm=epForm,usrForm=usrForm)
    def post(self):
        try:
            service = MD_OB_DEVICE()
            gw_id = request.form.get('gw_id')
            return service.get_entry(gw_id)
        except Exception as e:
            print('OB_DEVICE_VIEW-ERROR-',str(e))
            return fn_jsonify({})

class OB_DEVICE_DETAIL_VIEW(MethodView):
    def post(self):
        return ObDeviceHandler.do_deviceDetail(request.form)

class OB_DEVICE_SAVE(View): 
    methods = ['POST']
    def dispatch_request(self):
        form = OB_DEVICE_FORM(request.form)
        epForm = OB_DEVICE_FORM(request.form)
        if form.validate():
            ret, msg = ObDeviceHandler.do_save(form.data)
            if ret is True:
                return redirect('/obm/devices')  
            else:
                app.logger.debug('Except - ',msg)
                
        return render_template('obm/devices.html',form=form,epForm=epForm) 

class OB_ENDPOINT_SAVE_TYPE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_DEVICE_FORM(request.form)
        epForm = OB_DEVICE_FORM(request.form)
        dev_id = request.form.get('dev_id')
        ep_type = request.form.get('ep_type')
        param = { 'dev_id' : dev_id, 'ep_type' : ep_type }
        ret, msg = ObDeviceHandler.do_save_type(param)
        if ret is True:
            return fn_jsonify({ 'result' : 'success' })
        else:
            app.logger.debug('Except - ',msg)
            fn_jsonify({ 'result' : 'fail' , 'msg' : msg })
            
    
class OB_DEVICE_DELETE(View):
    methods = ['POST']
    def dispatch_request(self):
        dev_id = request.form.get('dev_id')
        if dev_id is not None:
            ret,msg = ObDeviceHandler.do_delete(dev_id)
            if ret is False:
                app.logger.debug('Except -', msg)
        return redirect('/obm/devices')  





'''
------------------------------------------------------------------------------------
OBM > DEVICE_TYPE
------------------------------------------------------------------------------------
'''

class OB_DEVTYPE_UPDATE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_DEVTYPE_FORM(request.form)
        if form.updateValidate():
            ret, msg = ObDeviceTypeHandler.do_update(form.data)
            if ret is True:
                return redirect('/obm/devtype')  
            else:
                app.logger.debug('Except - ', msg)
                
        return render_template('obm/devtype.html',form=form) 
    
class OB_DEVTYPE_SAVE(View): 
    methods = ['POST']
    def dispatch_request(self):
        form = OB_DEVTYPE_FORM(request.form)
        if form.validate():
            ret, msg = ObDeviceTypeHandler.do_save(form.data)
            if ret is True:
                return redirect('/obm/devtype')  
            else:
                app.logger.debug('Except - ',msg)
                
        return render_template('obm/devtype.html',form=form) 


class OB_DEVTYPE_VIEW(MethodView): 
    def get(self):
        form = OB_DEVTYPE_FORM(request.form) 
        epTypes = db.session.query(OB_ENDPOINT_TYPE).all()
        return render_template('obm/devtype.html',form=form, epTypes=epTypes)
    def post(self):
        return ObDeviceTypeHandler.do_read()
   
class OB_DEVTYPE_DELETE(View):
    methods = ['POST']
    def dispatch_request(self):
        dv_type = request.form.get('dv_type')
        if dv_type is not None:
            ret,msg = ObDeviceTypeHandler.do_delete(dv_type)
            if ret is False:
                app.logger.debug('Except -', msg)
        return redirect('/obm/devtype')  
  


'''
------------------------------------------------------------------------------------
OBM > DEVICE_TYPE_MAP
------------------------------------------------------------------------------------
'''

class OB_DEVTYPE_MAP_VIEW(MethodView):

    def get(self):
        dv_type = request.values.get('dv_type','',type=str)
        return ObDeviceTypeMapHandler.do_loadEntry(dv_type)

    def post(self):
        dv_type = request.values.get('dv_type','',type=str)
        ep_types = request.values.getlist('ep_types[]')
        
        return ObDeviceTypeMapHandler.do_mappingEntry(param={'dv_type' : dv_type, 'ep_types' : ep_types})
        
    
    