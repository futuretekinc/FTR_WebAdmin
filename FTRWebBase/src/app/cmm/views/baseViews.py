from flask import render_template, g, abort,jsonify
from flask.views import View, MethodView

from app import app, db, ma
from app.cmm.services.menu_handler import find_menu
from app.cmm.models import CM_CODED


class RenderTemplateView(View):
    def __init__(self,template_name):
        self.template_name = template_name
    def dispatch_request(self):
        return render_template(self.template_name)


class SCH_CM_CODED(ma.Schema):
    class Meta:
        fields = ('comm_code', 'comd_code', 'comd_cdnm')

cm_coded_many = SCH_CM_CODED(many=True)

class CM_CODED_VIEW(MethodView):
#     decorators = [user_required]
    def get(self):
        return self.post()
    
    def post(self):
        comm_code = 'ACTION_TYPE'
        data = db.session.query(CM_CODED).filter(CM_CODED.comm_code == comm_code, CM_CODED.use_yn == 'Y').all()
        result = cm_coded_many.dump(data)
        return jsonify({ 'data' : result.data }) 


