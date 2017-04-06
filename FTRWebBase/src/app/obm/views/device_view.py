from flask import render_template, g, abort, session, request, redirect, flash
from flask.views import View, MethodView
from sqlalchemy.orm import joinedload

from app import db, ma
from app.obm.forms import *  
from app.obm.models import *
from app.obm.services import *


class OB_DEVICE_VIEW(MethodView):
    def get(self):
        form = OB_DEVICE_FORM(request.form)
        return render_template('obm/devices.html',form=form)
    def post(self):
        users = db.session.query(OB_DEVICE).all()
        result = ob_device_many.dump(users)
        return fn_jsonify({ 'data' : result.data }) 

class OB_DEVICE_SAVE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_DEVICE_FORM(request.form)
        if form.validate():
            device = OB_DEVICE()
            device.dev_name = str(form.dev_name.data)
            db.session.add(device)
            db.session.commit()
            flash('Thanks for registering')
        return redirect('/obm/devices')  

class OB_DEVTYPE_VIEW(MethodView): 
    def get(self):
        form = OB_DEVTYPE_FORM(request.form) 
        epTypes = db.session.query(OB_ENDPOINT_TYPE).all()
        return render_template('obm/devtype.html',form=form, epTypes=epTypes)
    def post(self):
        dvType = db.session.query(OB_DEVICE_TYPE).all()
        result = ob_dvtype_many.dump(dvType)
        for row in result.data:
            row['dv_delete'] = '<span class="ftr_table_delete" key="{dv_type}"><i class="fa fa-trash-o"></i></span>'.format(dv_type=row.get('dv_type'))
        return fn_jsonify({ 'data' : result.data }) 
   
class OB_DEVTYPE_SAVE(View): 
    methods = ['POST']
    def dispatch_request(self):
        form = OB_DEVTYPE_FORM(request.form)
        if form.validate():
            dtype = OB_DEVICE_TYPE()
            dtype.dv_type = str(form.dv_type.data).upper()
            dtype.dv_name = str(form.dv_name.data)
            dtype.dv_desc = str(form.dv_desc.data)
            dtype.dv_location = str(form.dv_location.data)
            dtype.dv_timeout = str(form.dv_timeout.data)
#             dtype.dv_option = str(form.dv_option.data)
            dtype.dv_protocol = str(form.dv_protocol.data)
            db.session.add(dtype)
            db.session.commit()
            return redirect('/obm/devtype')  
        return render_template('obm/devtype.html',form=form) 

class OB_DEVTYPE_DELETE(View):
    methods = ['POST']
    def dispatch_request(self):
        dv_type = request.form.get('dv_type')
        if dv_type is not None:
            delObj = db.session.query(OB_DEVICE_TYPE).filter(OB_DEVICE_TYPE.dv_type == dv_type).first()
            db.session.delete(delObj)
            db.session.commit()
        return redirect('/obm/devtype')  
  

class OB_DEVTYPE_UPDATE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_DEVTYPE_FORM(request.form)
        if form.updateValidate():
            dv_type = str(form.dv_type.data)
            dtype = db.session.query(OB_DEVICE_TYPE).filter(OB_DEVICE_TYPE.dv_type == dv_type).first()
            if dtype is not None:
                dtype.dv_name = str(form.dv_name.data)
                dtype.dv_desc = str(form.dv_desc.data)
                dtype.dv_location = str(form.dv_location.data)
                dtype.dv_timeout = str(form.dv_timeout.data)
                dtype.dv_protocol = str(form.dv_protocol.data)
                db.session.commit()
                return redirect('/obm/devtype')  
        return render_template('obm/devtype.html',form=form) 
    


class OB_DEVTYPE_MAP_VIEW(MethodView):
    loadEntryQuery = '''
SELECT 
        a.ep_name, a.ep_type,a.ep_unit, b.dv_type 
FROM 
    OB_ENDPOINT_TYPE a 
    LEFT OUTER JOIN OB_DEVICE_TYPE_MAP b 
    
    ON a.ep_type = b.ep_type AND b.dv_type=:dv_type    
    '''
    def get(self):
        dv_type = request.values.get('dv_type','',type=str)
        r = db.session.query(OB_ENDPOINT_TYPE, OB_DEVICE_TYPE_MAP)
        r = r.from_statement(self.loadEntryQuery).params({'dv_type': dv_type }).all()
        selected = []
        unselected = []
        buf = []
        try:
            bufType = db.session.query(OB_DEVICE_TYPE).filter(OB_DEVICE_TYPE.dv_type == dv_type).one()
        except Exception as e:
            bufType = None
        for (x,y) in r:
            if y.dv_type is None:
                unselected.append(x.ep_type)
            else:
                selected.append(x.ep_type)
                buf.append(x)
        
        eptypes = ob_eptype_many.dump(buf)
        if bufType:
            dvtype = ob_devtype_single.dump(bufType).data 
        else:
            dvtype = {}
        result = { 'dv_type' : dvtype, 'selected' : selected , 'unselected' : unselected,'eptypes' : eptypes.data }
        return fn_jsonify(result)

    def post(self):
        dv_type = request.values.get('dv_type','',type=str)
        ep_types = request.values.getlist('ep_types[]')
        try:
            db.session.query(OB_DEVICE_TYPE_MAP).filter(OB_DEVICE_TYPE_MAP.dv_type == dv_type).delete()
            typeMap = []
            for ep_type in ep_types:
                map = OB_DEVICE_TYPE_MAP()
                map.dv_type = dv_type
                map.ep_type = ep_type
                typeMap.append(map)
            db.session.add_all(typeMap)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return fn_jsonify({'result' :  ep_types })
    