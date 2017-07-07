# -*- coding : utf-8 -*-
from flask import Response, jsonify, request, Blueprint, flash, redirect
from flask_login import login_required

from app import db, render_template, send_from_directory
from app.obm.forms.obm_forms import OB_DEVICE_EDIT_FORM
from app.obm.views import *


obm = Blueprint('obm', __name__, url_prefix='/obm')


@obm.route("/device_edit/<dev_id>", methods=['GET','POST'])
@login_required
def device_edit(dev_id):
    service = MD_OB_DEVICE()
    form = OB_DEVICE_EDIT_FORM(request.form)
    if request.method == 'POST':
        service.update_device(form, dev_id)
        return redirect("/obm/devices")
    
    service.update_edit_form(form,dev_id)
    return render_template("obm/device_edit.html",form=form)

ob_gateway_view = login_required(OB_GATEWAY_VIEW().as_view('ob_gateway_view'))
ob_gateway_add = login_required(OB_GATEWAY_ADD().as_view('ob_gateway_add'))
obm.add_url_rule('/gateway_update',view_func=login_required(OB_GATEWAY_UPDATE().as_view('ob_gateway_update')))

ob_resource_view = OB_RESOURCE_VIEW().as_view('ob_resource_view')
ob_endpoint_view = OB_ENDPOINT_VIEW().as_view('ob_endpoint_view')
ob_device_detail_view = OB_DEVICE_DETAIL_VIEW().as_view('ob_device_detail_view')
ob_eptype_view = OB_EPTYPE_VIEW().as_view('ob_eptype_view')  

# obm.add_url_rule('/resources',view_func=ob_resource_view)
# obm.add_url_rule('/resources_save',view_func=OB_RESOURCE_SAVE().as_view('ob_resources_save'))

obm.add_url_rule('/gateway',view_func=ob_gateway_view)
obm.add_url_rule('/add_gateway',view_func=ob_gateway_add)

obm.add_url_rule('/gateway_save',view_func=login_required(OB_GATEWAY_SAVE().as_view('ob_gateway_save')))

# -------------------------------------------------------------------------------------------

ob_device_view = OB_DEVICE_VIEW().as_view('ob_device_view')
obm.add_url_rule('/devices',view_func=ob_device_view) 
obm.add_url_rule('/devices_save',view_func=OB_DEVICE_SAVE().as_view('ob_device_save'))

obm.add_url_rule('/devices_save_ep',view_func=OB_ENDPOINT_SAVE_TYPE().as_view('ob_endpoint_save_type'))

obm.add_url_rule('/device_delete',view_func=OB_DEVICE_DELETE().as_view('ob_device_delete'))
obm.add_url_rule('/device_detail',view_func=ob_device_detail_view)
 
# -------------------------------------------------------------------------------------------


obm.add_url_rule('/devtype_map',view_func=OB_DEVTYPE_MAP_VIEW().as_view('ob_devtype_map_view'))

# -------------------------------------------------------------------------------------------

ob_devtype_view = OB_DEVTYPE_VIEW().as_view('ob_devtype_view')   
# -------------------------------------------------------------------------------------------

obm.add_url_rule('/devtype',view_func=ob_devtype_view)
obm.add_url_rule('/devtype_save',view_func=OB_DEVTYPE_SAVE().as_view('ob_devtype_save'))
obm.add_url_rule('/devtype_update',view_func=OB_DEVTYPE_UPDATE().as_view('ob_devtype_update')) 
obm.add_url_rule('/devtype_delete',view_func=OB_DEVTYPE_DELETE().as_view('ob_devtype_delete')) 


# -------------------------------------------------------------------------------------------

obm.add_url_rule('/endpoints',view_func=ob_endpoint_view)
obm.add_url_rule('/endpoints_save',view_func=OB_ENDPOINT_SAVE().as_view('ob_endpoint_save'))
obm.add_url_rule('/endpoints_update',view_func=OB_ENDPOINT_UPDATE().as_view('ob_endpoint_update')) 
obm.add_url_rule('/endpoints_delete',view_func=OB_ENDPOINT_DELETE().as_view('ob_endpoint_delete'))   


# -------------------------------------------------------------------------------------------
obm.add_url_rule('/eptype',view_func=ob_eptype_view)
obm.add_url_rule('/eptype_save',view_func=OB_EPTYPE_SAVE().as_view('ob_eptype_save'))
obm.add_url_rule('/eptype_update',view_func=OB_EPTYPE_UPDATE().as_view('ob_eptype_update')) 
obm.add_url_rule('/eptype_delete',view_func=OB_EPTYPE_DELETE().as_view('ob_eptype_delete'))  


# -------------------------------------------------------------------------------------------