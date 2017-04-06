# -*- coding : utf-8 -*-
from app import app, db
from app.obm.models import *
from app.cmm.utils.decimal_jsonizer import fn_jsonify

class ObDeviceTypeHandler(object):
    
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
        if param is None:
            return (False,'param is null')
        pass

    @staticmethod
    def do_delete(param=None):
        err_msg = ''
        if param is None:
            return (False,'param is null')
        pass

