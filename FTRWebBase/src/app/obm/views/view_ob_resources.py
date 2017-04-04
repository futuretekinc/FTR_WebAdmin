import decimal
import json
from flask import render_template, jsonify, g, abort,session,request,redirect,flash
from flask.views import View, MethodView

from app import db, ma
from app.obm.models import *
from app.obm.forms import * 
from sqlalchemy.orm import joinedload

def decimal_default(obj):
    if isinstance(obj,decimal.Decimal):
        return str(float(obj))
    raise TypeError

class OB_RESOURCE_VIEW(MethodView):
    def get(self):
        form = OB_RESOURCE_FORM(request.form)
        return render_template('obm/resources.html',form=form)

    def post(self):
        data = db.session.query(OB_RESOURCE).all() 
        result = ob_resource_many.dump(data)
        return jsonify({ 'data' : result.data }) 

class OB_RESOURCE_SAVE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_RESOURCE_FORM(request.form)
        if form.validate():
            resource = OB_RESOURCE()
            resource.res_name = str(form.res_name.data)
            db.session.add(resource)
            db.session.commit()
            flash('Thanks for registering')
        return redirect('/obm/resources')  

class OB_GATEWAY_VIEW(MethodView):
    def get(self):
        form = OB_GATEWAY_FORM(request.form)
        return render_template('obm/gateway.html',form=form)
    
    def post(self):
        data = db.session.query(OB_GATEWAY).all()
        result = ob_gateway_many.dump(data)
        return jsonify({ 'data' : result.data }) 

class OB_GATEWAY_SAVE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_GATEWAY_FORM(request.form)
        if form.validate():
            gw = OB_GATEWAY()
            gw.gw_name = str(form.gw_name.data)
            db.session.add(gw)
            db.session.commit()
            flash('Thanks for registering')
        return redirect('/obm/gateway')  

class OB_DEVICE_VIEW(MethodView):
    def get(self):
        form = OB_DEVICE_FORM(request.form)
        return render_template('obm/devices.html',form=form)
    def post(self):
        users = db.session.query(OB_DEVICE).all()
        result = ob_device_many.dump(users)
        return jsonify({ 'data' : result.data }) 

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
        return jsonify({ 'data' : result.data }) 
   
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
        return json.dumps(result,default=decimal_default)
#         return jsonify(result)

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
        return jsonify({'result' :  ep_types })
    


class OB_ENDPOINT_VIEW(MethodView):
    def get(self):
        form = OB_ENDPOINT_FORM(request.form)
        return render_template('obm/endpoint.html',form=form)
    
    def post(self):
        data = db.session.query(OB_ENDPOINT).all()
        result = ob_endpoint_many.dump(data)
        return jsonify({ 'data' : result.data }) 
    
class OB_EPTYPE_VIEW(MethodView): 
    def get(self):
        form = OB_EPTYPE_FORM(request.form)   
        return render_template('obm/eptype.html',form=form) 
    def post(self):
        eptypes = db.session.query(OB_ENDPOINT_TYPE).all() 
        result = ob_eptype_many.dump(eptypes)
        for row in result.data:
            row['delete'] = '<span class="ftr_table_delete" key="{ep_type}"><i class="fa fa-trash-o"></i></span>'.format(ep_type=row.get('ep_type'))
        return json.dumps({ 'data' : result.data },default=decimal_default)
#         return jsonify({ 'data' : result.data }) 
    
class OB_EPTYPE_SAVE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_EPTYPE_FORM(request.form)
        if form.validate():
            etype = OB_ENDPOINT_TYPE()
            etype.ep_type = str(form.ep_type.data).upper()
            etype.ep_name = str(form.ep_name.data)
            etype.ep_scale = str(form.ep_scale.data)
            etype.ep_unit = str(form.ep_unit.data) if form.ep_unit.data is not None else ''
            etype.ep_pr_host = str(form.ep_pr_host.data)
            etype.ep_interval = str(form.ep_interval.data)
            etype.ep_limit = str(form.ep_limit.data)
            etype.ep_hour = str(form.ep_hour.data)
            etype.ep_day = str(form.ep_day.data)
            etype.ep_month = str(form.ep_month.data) 
            etype.ep_count = str(form.ep_count.data)
            db.session.add(etype)
            db.session.commit()
            return redirect('/obm/eptype')  
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
  

class OB_EPTYPE_UPDATE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_EPTYPE_FORM(request.form)
        if form.updateValidate():
            ep_type = str(form.ep_type.data)
            etype = db.session.query(OB_ENDPOINT_TYPE).filter(OB_ENDPOINT_TYPE.ep_type == ep_type).first()
            if etype is not None:
                etype.ep_name = str(form.ep_name.data)
                etype.ep_scale = str(form.ep_scale.data)
                etype.ep_unit = str(form.ep_unit.data) if form.ep_unit.data is not None else ''
                etype.ep_pr_host = str(form.ep_pr_host.data)
                etype.ep_interval = str(form.ep_interval.data)
                etype.ep_limit = str(form.ep_limit.data)
                etype.ep_hour = str(form.ep_hour.data)
                etype.ep_day = str(form.ep_day.data)
                etype.ep_month = str(form.ep_month.data)
                etype.ep_count = str(form.ep_count.data)
                db.session.commit()
                return redirect('/obm/eptype')  
        return render_template('obm/eptype.html',form=form) 
    
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
 