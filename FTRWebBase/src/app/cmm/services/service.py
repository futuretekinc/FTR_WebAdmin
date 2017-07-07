# -*- coding: utf-8 -*-
import json
import pandas as pd
from app import db
from app.cmm.models import *
from app.obm.models import *
from app.cmm.utils.decimal_jsonizer import fn_jsonify

class SCH_CM_USER(ModelSchema): 
    class Meta: model = CM_USER

sch_cm_user_many          = SCH_CM_USER(many=True)
sch_cm_user_single        = SCH_CM_USER(many=False)

class MD_CM_USER(object):

    def get_entry(self):
        return db.session.query(CM_USER).all()
    
    def get_profile(self,email):
        try:
            stat = db.session.query(CM_USER).filter(CM_USER.email == email).one()
            result = sch_cm_user_single.dump(stat)
            profile = result.data
            profile['gateway'] = self.get_cm_user_gw(email)
            return profile
        except Exception as e:
            return None

    def get_gw_list(self,email):
        r = db.session.query(CM_USER_GATEWAY,OB_GATEWAY) \
            .join(OB_GATEWAY, CM_USER_GATEWAY.gw_id == OB_GATEWAY.gw_id) \
            .filter(CM_USER_GATEWAY.email == email).all()
        return [ x[1] for x in r ]

    def get_cm_user_gw(self,email):
#         r = db.session.query(CM_USER_GATEWAY,OB_GATEWAY) \
#             .join(OB_GATEWAY, CM_USER_GATEWAY.gw_id == OB_GATEWAY.gw_id) \
#             .filter(CM_USER_GATEWAY.email == email).all()
#         gw = [ x[1] for x in r ]
        gw = self.get_gw_list(email)
        result = ob_gateway_many.dump(gw)
        for x in result.data:
            r = u"등록완료" if x.get('register') == 'Y' else u"등록대기"
            x.update({'register' : r })
        return result.data        
        
    def save(self, email, name, passwd):
        try:
            user = CM_USER(email, name, passwd)
            db.session.add(user);
            db.session.commit()
            return True,'success'
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def save_user_gateway(self, email, gw_id):
        try:
            cug = CM_USER_GATEWAY()
            cug.email = email
            cug.gw_id = gw_id
            db.session.add(cug)
            db.session.commit()
            return True, 'success'
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def update(self,email, name, passwd):
        try:
            user = db.session.query(CM_USER).filter(CM_USER.email == email).one()
            user.name = name
            user.passwd = passwd
            db.session.commit()
            return True,'success'
        except Exception as e:
            db.session.rollback()
            return False, str(e)
        
    def delete(self, email):
        try:
            user = db.session.query(CM_USER).filter(CM_USER.email == email).one()
            db.session.delete(user)
            db.session.commit()
            return True,'success'
        except Exception as e:
            db.session.rollback()
            return False, str(e)
 
 
class MD_EP_TYPE(object): 
    def get_entry(self,gw_id):
        try:
            query = self.get_query(gw_id)
            df = pd.read_sql_query(query,con=db.engine)
            df = df.fillna('')
            data = json.loads(df.to_json(orient='records'))
            return fn_jsonify({ 'data' : data })
        except Exception as e:
            return fn_jsonify({'data' : []})
    
    def get_query(self,gw_id):
        return '''
SELECT 
    d.comd_code code, d.comd_cdnm name
FROM
    OB_GATEWAY_MAP a
        INNER JOIN
    OB_DEVICE_MAP b ON a.dev_id = b.dev_id
        INNER JOIN
    OB_ENDPOINT c ON b.ep_id = c.ep_id
        INNER JOIN
    CM_CODED d ON c.ep_type = d.comd_code
        AND d.use_yn = 'Y'
WHERE
    a.gw_id = '{}'
GROUP BY c.ep_type        
        '''.format(gw_id)
        

class MD_TIME_TYPE():        
    def get_choice_entry(self):
        rows = db.session.query(CM_CODED).filter(CM_CODED.comm_code == 'TIME_TYPE').all()
        buf = []
        for row in rows:
            buf.append((row.comd_code, row.comd_cdnm))
        return buf
        
        
if __name__ == '__main__x':
    r = db.session.query(CM_USER_GATEWAY,OB_GATEWAY).join(OB_GATEWAY, CM_USER_GATEWAY.gw_id == OB_GATEWAY.gw_id).filter(CM_USER_GATEWAY.email == '1a@aaa.com').all()
    gw = []
    for x in r:
        gw.append(x[1])
    result = ob_gateway_many.dump(gw)
    print(result.data)
if __name__ == '__main__xxx':
    service = MD_EP_TYPE()
    r = service.get_entry('FTM20170601012345678901234567894')
    print(r)


     