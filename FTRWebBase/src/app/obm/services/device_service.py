# -*- coding : utf-8 -*-
import json
from app import app, db
from app.obm.models import *
from app.cmm.utils.decimal_jsonizer import fn_jsonify
import pandas as pd

class ObDeviceHandler(object):
    
    @staticmethod
    def do_deviceDetail(param=None):
        ''' select [endpoint] where dev_id = param '''
        try:
            if 'dev_id' in param:
                dev_id = param.get('dev_id')
            else:
                dev_id = param
            eps = db.session.query(OB_ENDPOINT).join(OB_DEVICE_MAP, OB_DEVICE_MAP.ep_id == OB_ENDPOINT.ep_id).filter(OB_DEVICE_MAP.dev_id == dev_id).all()
            dev = db.session.query(OB_DEVICE).filter(OB_DEVICE.dev_id == dev_id).one()
            epts = db.session.query(OB_ENDPOINT_TYPE).all()
            dev = ob_device_single.dump(dev)
            eptypes = ob_eptype_many.dump(epts)
            result = ob_endpoint_many.dump(eps)
            return fn_jsonify({ 'data' : result.data, 'device' : dev.data, 'eptypes' : eptypes.data })
        except Exception as e:
            app.logger.debug(str(e))

        return fn_jsonify({'data' : []})
    
    @staticmethod
    def do_save(param=None):
        err_msg = ''
        if param is None:
            return (False,'param is null')
        try:
            saveObj = OB_DEVICE() 
            saveObj.dev_id = uuid_gen()
            for attr, value in param.items():
                setattr(saveObj, attr, str(value))
            
            dev_id = saveObj.dev_id
            dv_type = saveObj.dev_type

            rs = db.session.query(OB_ENDPOINT_TYPE) \
                    .join(OB_DEVICE_TYPE_MAP,OB_ENDPOINT_TYPE.ep_type == OB_DEVICE_TYPE_MAP.ep_type) \
                    .filter(OB_DEVICE_TYPE_MAP.dv_type == dv_type).all()
                                
            for x in rs:
                ep = OB_ENDPOINT()
                ep.dev_id = dev_id
                ep.ep_id = uuid_gen()
                print(x.__table__.c.items())
                for k, _ in x.__table__.c.items():
                    kval = getattr(x,k)
                    setattr(ep,k,kval)
                db.session.add(ep)
                
            db.session.add(saveObj)
            db.session.commit()
            return (True, 'success')
        except Exception as e:
            err_msg = str(e)

        return (False, err_msg)
    
    @staticmethod
    def do_save_type(param=None):
        err_msg = ''
        if param is None:
            return (False,'param is null')
        try:    
            dev_id = param.get('dev_id')
            ep_type = param.get('ep_type')
     
            rs = db.session.query(OB_ENDPOINT_TYPE) \
                    .filter(OB_ENDPOINT_TYPE.ep_type == ep_type) \
                    .first()     
                    
            ep = OB_ENDPOINT()
            ep.dev_id = dev_id
            ep.ep_id = uuid_gen()
            for k, _ in rs.__table__.c.items():
                kval = getattr(rs,k)
                setattr(ep,k,kval)
            db.session.add(ep)
            db.session.commit()
            return (True, 'success')
        except Exception as e:
            err_msg = str(e)
        return (False, err_msg)
    
    @staticmethod
    def do_read(param=None):
        err_msg = ''
        try:
            device = db.session.query(OB_DEVICE).all()
            result = ob_device_many.dump(device)
            for row in result.data:
                row['delete'] = '<span class="ftr_table_delete" key="{dev_id}"><i class="fa fa-trash-o"></i></span>'.format(dev_id=row.get('dev_id'))
                row['update'] = '<span class="ftr_table_delete" key="{dev_id}"><i class="fa fa-edit"></i></span>'.format(dev_id=row.get('dev_id'))
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
            if 'dev_id' in param:
                dev_id = param.get('dev_id')
            else:
                dev_id = param
            deleteObj = db.session.query(OB_DEVICE) \
                            .filter(OB_DEVICE.dev_id == dev_id) \
                            .one()
            db.session.delete(deleteObj)
            
            # endpoint - DELETE
            deleteEp = db.session.query(OB_ENDPOINT) \
                            .filter(OB_ENDPOINT.dev_id == dev_id) \
                            .all()
            for x in deleteEp:
                db.session.delete(x)

            db.session.commit()
            return (True, 'success')
        except Exception as e:
            err_msg = str(e)
            
        return (False, err_msg)        
        
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



class MD_OB_DEVICE(object):
    def get_entry(self,gw_id):
        err_msg = ''
        try:
            device = db.session.query(OB_DEVICE) \
                        .join(OB_GATEWAY_MAP,OB_GATEWAY_MAP.dev_id == OB_DEVICE.dev_id) \
                        .filter(OB_GATEWAY_MAP.gw_id == gw_id).all()
            result = ob_device_many.dump(device)
            for row in result.data:
                row['delete'] = '<span class="ftr_table_delete" key="{dev_id}"><i class="fa fa-trash-o"></i></span>'.format(dev_id=row.get('dev_id'))
                row['update'] = '<span class="ftr_table_update" key="{dev_id}"><i class="fa fa-edit"></i></span>'.format(dev_id=row.get('dev_id'))
            return fn_jsonify({ 'data' : result.data }) 
        except Exception as e:
            app.logger.error('Except - ',str(e))

        return fn_jsonify({'data' : []})
    def get_device(self,dev_id):
        dev = db.session.query(OB_DEVICE).filter(OB_DEVICE.dev_id == dev_id).one()
        return dev

    def update_edit_form(self,form, dev_id):
        try:
            if dev_id is not None and form is not None:
                dev = self.get_device(dev_id.strip())
                form.dev_id.data = dev.dev_id
                form.dev_name.data = dev.dev_name
                form.dev_location.data = dev.dev_location
        except Exception as e:
            print("ERROR>>",str(e))
            return
    
    def update_device(self,form, dev_id):
        try:
            if dev_id is not None:
                dev = self.get_device(dev_id.strip())
                dev.dev_name = form.dev_name.data
                dev.dev_location = form.dev_location.data
                db.session.commit()
        except Exception as e:
            print("ERROR>>",str(e))
            db.session.rollback()

class MD_KEEP_ALIVE():
    def get_status(self,email):
        query = self.get_status_query(email)
        df = pd.read_sql_query(query,con=db.engine, parse_dates={ 'expire_time' : '%Y-%m-%d %H:%M:%S'})
        df = df.fillna('')
        data = json.loads(df.to_json(orient='records'))
        return fn_jsonify({ 'data' : data })
    
    def get_status_query(self,email):
        return '''
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
    where d.email = '{}'
    order by a.gw_id, b.dev_id   
        '''.format(email)
        
if __name__ == '__main__':
    email = '1a@aaa.com'
    service = MD_KEEP_ALIVE()
    print(service.get_status(email))