# -*- coding : utf-8 -*-
from app import app, db
from app.obm.models import *
from app.cmm.utils.decimal_jsonizer import fn_jsonify

class ObResourceHandler(object):
    
    @staticmethod
    def do_save(param=None):
        err_msg = ''
        if param is None:
            return (False,'param is null')
        try:
            saveObj = OB_RESOURCE()
            saveObj.rc_id = uuid_gen()
            for attr, value in param.items():
                setattr(saveObj, attr, str(value))
            
            db.session.add(saveObj)
            db.session.commit()
            return (True, 'success')
        except Exception as e:
            err_msg = str(e)

        return (False, err_msg)
    
