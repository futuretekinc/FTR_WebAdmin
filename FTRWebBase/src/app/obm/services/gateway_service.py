# -*- coding : utf-8 -*-
from app import app, db
from app.obm.models import *
from app.cmm.utils.decimal_jsonizer import fn_jsonify

class ObGatewayHandler(object):
    
    @staticmethod
    def do_save(param=None):
        err_msg = ''
        if param is None:
            return (False,'param is null')
        try:
            saveObj = OB_GATEWAY() 
            saveObj.gw_id = uuid_gen()
            for attr, value in param.items():
                setattr(saveObj, attr, str(value))
            
            db.session.add(saveObj)
            db.session.commit()
            return (True, 'success')
        except Exception as e:
            err_msg = str(e)

        return (False, err_msg)
    
class MD_OB_GATEWAY():
    def do_update(self,param):
        try:
            gw_id = param.get('hd_gw_id')
            gw_name = param.get('gw_name')
            gw_location = param.get('gw_location')
            print("@@-----------------------------------------@@@")
            print(param.get('register'))
            print(param.get('last_update'))
            gw = db.session.query(OB_GATEWAY).filter(OB_GATEWAY.gw_id == gw_id).one()
            gw.gw_name = gw_name
            gw.gw_location = gw_location
            gw.last_update = db.func.current_timestamp()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
        
    def do_save(self,param):
        try:
            gw = OB_GATEWAY()
            gw.gw_id = param.get('gw_id')
            gw.gw_name = 'no name'
            gw.gw_location = 'not yet'
            gw.gw_type = 'no type'
            gw.register = 'N'
            db.session.add(gw)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
if __name__ == '__main__':
    
    service = MD_OB_GATEWAY()
    gw_id = 'FTM20170601012345678901234567894'
    service.do_update(gw_id, 'test', '방제실')
        
        
