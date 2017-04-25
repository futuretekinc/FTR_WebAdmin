from flask import render_template, g, abort, session, request, redirect, flash
from flask.views import View, MethodView
from sqlalchemy.orm import joinedload

from app import db, ma
from app.obm.forms import * 
from app.obm.models import *
from app.obm.services import *
from app.obm.services.gateway_service import ObGatewayHandler


class OB_GATEWAY_VIEW(MethodView):
    def get(self):
        form = OB_GATEWAY_FORM(request.form)
        return render_template('obm/gateway.html',form=form)
    
    def post(self):
        data = db.session.query(OB_GATEWAY).all()
        result = ob_gateway_many.dump(data)
        return fn_jsonify({ 'data' : result.data }) 

class OB_GATEWAY_SAVE(View):
    methods = ['POST']
    def dispatch_request(self):
        form = OB_GATEWAY_FORM(request.form)
        if form.validate():
            ret, msg = ObGatewayHandler.do_save(form.data)
            if ret is True:
                return redirect('/obm/gateway')  
            else:
                app.logger.debug('Except - ',msg)
                
        return render_template('obm/gateway.html',form=form)  