import decimal
import json
from flask import render_template, jsonify, g, abort,session,request,redirect,flash
from flask.views import View, MethodView

from app import db, ma
from app.obm.models import *
from app.obm.forms import * 
from sqlalchemy.orm import joinedload
from app.cmm.models import CM_CODED,CM_CODEM
from marshmallow_sqlalchemy.schema import ModelSchema


class SCH_CM_CODED(ModelSchema):
    class Meta:
        model = CM_CODED

sch_cm_coded = SCH_CM_CODED(many=True)



class CM_FIND_COMM_VIEW(MethodView):
    '''
    def get(self):
        form = OB_RESOURCE_FORM(request.form)
        return render_template('obm/resources.html',form=form)
    '''
    def get(self):
        comm_code = request.values.get('code','',type=str)
        return self.find_comm_code(comm_code)
    def post(self):
        comm_code = request.values.get('code','',type=str)
        #comm_code = 'DEV_PROTOCOL'
        return self.find_comm_code(comm_code)
    
    def find_comm_code(self,comm_code): 
        try:
            rows = db.session.query(CM_CODED) \
                        .join(CM_CODEM, CM_CODEM.comm_code == CM_CODED.comm_code) \
                        .filter(CM_CODED.comm_code == comm_code,CM_CODEM.use_yn == 'Y').all()
            
            result = sch_cm_coded.dump(rows)
            return jsonify({ 'data' : result.data })
        except Exception as e:
            print(e)
            return jsonify({'data' : []})



if __name__ == '__main__':
    r = db.session.query(CM_CODED).join(CM_CODEM, CM_CODEM.comm_code == CM_CODED.comm_code).filter(CM_CODED.comm_code == 'DEV_PROTOCOL').all()
    for x in r:
        print(x.comm_code)
        print(x.comd_code)
        print(x.comd_cdnm)
        
'''
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
'''