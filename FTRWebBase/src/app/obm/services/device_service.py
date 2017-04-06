# -*- coding : utf-8 -*-
from app import app, db
from app.obm.models import *
from app.cmm.utils.decimal_jsonizer import fn_jsonify

class ObDeviceTypeMapHandler(object):

    @staticmethod
    def do_mappingEntry(param=None):
        try:
            dv_type = param.get('dv_type')
            ep_types = param.get('ep_types')
        except Exception as e:
            app.logger.debug(str(e))
            return fn_jsonify({'result' : [] })
        
        try:
            db.session.query(OB_DEVICE_TYPE_MAP) \
                .filter(OB_DEVICE_TYPE_MAP.dv_type == dv_type) \
                .delete() # CLEAR OLD MAPPING
            typeMap = []
            for ep_type in ep_types:
                map = OB_DEVICE_TYPE_MAP()
                map.dv_type = dv_type
                map.ep_type = ep_type
                typeMap.append(map)
            db.session.add_all(typeMap)
            db.session.commit()
            return fn_jsonify({'result' :  ep_types })
        except Exception as e:
            app.logger.debug(str(e))    
            db.session.rollback()
        
        return fn_jsonify({'result' : [] })
    
    @staticmethod
    def do_loadEntry(param=None):
        err_msg = ''
        query_ = '''
SELECT 
        a.ep_name, a.ep_type,a.ep_unit, b.dv_type 
FROM 
    OB_ENDPOINT_TYPE a 
    LEFT OUTER JOIN OB_DEVICE_TYPE_MAP b 
    ON a.ep_type = b.ep_type AND b.dv_type=:dv_type         
        '''
        if param is None:
            return (False, 'param is null')
        
        try:
            dv_type = param # request.values.get('dv_type', '', type=str)
            r = db.session.query(OB_ENDPOINT_TYPE, OB_DEVICE_TYPE_MAP) \
                            .from_statement(query_).params({'dv_type' : dv_type }).all()
            
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
                dvtypeObj = ob_devtype_single.dump(bufType).data 
            else:
                dvtypeObj = {}
            result = { 'dv_type' : dvtypeObj, 'selected' : selected , 'unselected' : unselected,'eptypes' : eptypes.data }
            return fn_jsonify(result)        
        except Exception as e:
            app.logger.error('Except - ',str(e))            
        
        return fn_jsonify({})

class ObDeviceTypeHandler(object):
    
    @staticmethod
    def do_update(param=None):
        err_msg = ''
        if param is None:
            return (False,'param is null')
        try:
            dv_type = param.get('dv_type')
            updateObj = db.session.query(OB_DEVICE_TYPE) \
                    .filter(OB_DEVICE_TYPE.dv_type == dv_type) \
                    .first()
            for attr, value in param.items():
                setattr(updateObj, attr, str(value))

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
            saveObj = OB_DEVICE_TYPE() 
            for attr, value in param.items():
                setattr(saveObj, attr, str(value))
            
            db.session.add(saveObj)
            db.session.commit()
            return (True, 'success')
        except Exception as e:
            err_msg = str(e)

        return (False, err_msg)

    @staticmethod
    def do_read(param=None):
        err_msg = ''
        try:
            dvType = db.session.query(OB_DEVICE_TYPE).all()
            result = ob_dvtype_many.dump(dvType)
            for row in result.data:
                row['dv_delete'] = '<span class="ftr_table_delete" key="{dv_type}"><i class="fa fa-trash-o"></i></span>'.format(dv_type=row.get('dv_type'))
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
            if 'dv_type' in param:
                dv_type = param.get('dv_type')
            else:
                dv_type = param
            deleteObj = db.session.query(OB_DEVICE_TYPE) \
                            .filter(OB_DEVICE_TYPE.dv_type == dv_type) \
                            .one()
            db.session.delete(deleteObj)
            db.session.commit()
            return (True, 'success')
        except Exception as e:
            err_msg = str(e)
            
        return (False, err_msg)

