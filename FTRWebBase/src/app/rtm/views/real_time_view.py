from flask import render_template, jsonify, g, abort,session,request,redirect,flash
from flask.views import View, MethodView

from app import db, ma
from app.rtm.models.rm_endpoint_data import *
from app.obm.forms.obm_forms import USER_GATEWAY_FROM
from flask_login.utils import current_user
from app.cmm.utils.decimal_jsonizer import fn_jsonify
from app.rtm.services.chart_service import MD_HIGHCHARTS

class RM_REAL_TIME_VIEW(MethodView):
    def get(self):
        form = USER_GATEWAY_FROM()
        email = current_user.id
        form.update_field(email)
        return render_template('rtm/realtime.html',form=form)
    def post(self):
        target_date = request.form['target_date']
        ep_day = target_date.replace('-','')
        email = current_user.id
        gw_id = request.form['gateway']
        timetype = request.form['timetype']
        ep_type = request.form['ep_type']
        service = MD_HIGHCHARTS()
        d = service.get_type_entry(timetype, ep_day,email,ep_type,gw_id)
        return fn_jsonify({'data' : d})        

'''
SELECT 
    (select gw_name from OB_GATEWAY where gw_id = a.gw_id) gw_name,
    (select dev_name from OB_DEVICE where dev_id = b.dev_id) dev_name,
    (select ep_name from OB_ENDPOINT where ep_id = b.ep_id) ep_name,
    CASE when ISNULL(c.expire_time) OR c.expire_time < NOW() then 'OFF'
    ELSE 'ON' END status
    , c.expire_time
FROM
    OB_GATEWAY_MAP a
        INNER JOIN
    OB_DEVICE_MAP b ON a.dev_id = b.dev_id
        LEFT OUTER JOIN
    CM_KEEP_ALIVE c ON c.dtype = 'endpoint' AND c.did = b.ep_id 
    inner join CM_USER_GATEWAY d on d.gw_id = a.gw_id
    where d.email = '1a@aaa.com'
    order by a.gw_id, b.dev_id
    ;   
'''