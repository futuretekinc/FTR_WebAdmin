# -*- coding : utf-8 -*-
from app import app, db
from app.obm.models import *
from app.cmm.utils.decimal_jsonizer import fn_jsonify

class ObEndpointTypeHandler(object):
    
    def __init__(self):
        pass
    
    '''
    Wtfform -> form.data => dict => param

a = {'ep_limit': 'time'
, 'ep_day': 0
, 'ep_pr_host': '127.0.0.1'
, 'ep_name': ''
, 'ep_type': ''
, 'ep_interval': 0
, 'csrf_token': 'ImU5YTQ0ODgzY2EwNzdhYWVhOWZlZTg1N2VmNzIyMjM0YjcwZDM4NTci.C8dpXA.BSH46HaU_5ObNh43Pl4l7Wls_wY'
, 'ep_unit': ''
, 'ep_month': 0
, 'ep_count': 0
, 'ep_scale': '1.0', 'ep_hour': 0}
    '''
    @staticmethod
    def do_update(param=None):
        err_msg = ''
        if param is None:
            return (False,'param is null')
        try:
            ep_type = param.get('ep_type')
            epTypeObj = db.session.query(OB_ENDPOINT_TYPE) \
                    .filter(OB_ENDPOINT_TYPE.ep_type == ep_type) \
                    .first()
            for attr, value in param.items():
                setattr(epTypeObj, attr, str(value))

            db.session.commit()
            return (True, 'success')
        except Exception as e:
            err_msg = str(e)

        return (False, err_msg)

    @staticmethod
    def do_save(param=None):
        err_msg = ''
        if param is None:
            return (False,'param is null')
        try:
            epTypeObj = OB_ENDPOINT_TYPE() 
            for attr, value in param.items():
                setattr(epTypeObj, attr, str(value))
            
            db.session.add(epTypeObj)
            db.session.commit()
            return (True, 'success')
        except Exception as e:
            err_msg = str(e)

        return (False, err_msg)

    @staticmethod
    def do_read(param=None):
        err_msg = ''
        try:
            etypes = db.session.query(OB_ENDPOINT_TYPE).all()
            result = ob_eptype_many.dump(etypes)
            for row in result.data:
                row['delete'] = '<span class="ftr_table_delete" key="{ep_type}"><i class="fa fa-trash-o"></i></span>'.format(ep_type=row.get('ep_type'))
            return fn_jsonify({ 'data' : result.data })
        except Exception as e:
            app.logger.error('Except - ',str(e))

        return fn_jsonify({'data' : []})

    @staticmethod
    def do_delete(param=None):
        err_msg = ''
        if param is None:
            return (False,'param is null')
        try:
            if 'ep_type' in param:
                ep_type = param.get('ep_type')
            else:
                ep_type = param
            epTypeObj = db.session.query(OB_ENDPOINT_TYPE) \
                            .filter(OB_ENDPOINT_TYPE.ep_type == ep_type) \
                            .one()
            db.session.delete(epTypeObj)
            db.session.commit()
            return (True, 'success')
        except Exception as e:
            err_msg = str(e)
            
        return (False, err_msg)

