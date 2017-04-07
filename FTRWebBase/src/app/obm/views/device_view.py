from flask import render_template, g, abort, session, request, redirect, flash
from flask.views import View, MethodView
from sqlalchemy.orm import joinedload

from app import db, ma
from app.obm.forms import *  
from app.obm.models import *
from app.obm.services import *

'''
------------------------------------------------------------------------------------
OBM > DEVICE
------------------------------------------------------------------------------------
'''

class OB_DEVICE_VIEW(MethodView):
    def get(self):
        form = OB_DEVICE_FORM(request.form)
        return render_template('obm/devices.html',form=form)
    def post(self):
        return ObDeviceHandler.do_read()

class OB_DEVICE_SAVE(View): 
    methods = ['POST']
    def dispatch_request(self):
        form = OB_DEVICE_FORM(request.form)
        if form.validate():
            ret, msg = ObDeviceHandler.do_save(form.data)
            if ret is True:
                return redirect('/obm/devices')  
            else:
                app.logger.debug('Except - ',msg)
                
        return render_template('obm/devices.html',form=form) 

class OB_DEVICE_DELETE(View):
    methods = ['POST']
    def dispatch_request(self):
        dev_id = request.form.get('dev_id')
        if dev_id is not None:
            ret,msg = ObDeviceHandler.do_delete(dev_id)
            if ret is False:
                app.logger.debug('Except -', msg)
        return redirect('/obm/devices')  

class OB_DEVICE_DETAIL(View):
    methods = ['POST']
    def dispatch_request(self):
        dev_id = request.form.get('dev_id')
        return ObDeviceHandler.do_deviceDetail(dev_id)




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
        
    
    