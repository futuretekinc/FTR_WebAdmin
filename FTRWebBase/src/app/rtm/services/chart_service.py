# -*- coding : utf-8 -*-
import pandas as pd
from app import app, db
from app.obm.models import *
from app.cmm.utils.decimal_jsonizer import fn_jsonify
import json
from app.cmm.models import CM_USER_GATEWAY
from app.obm.models.ob_resources import OB_GATEWAY

class MD_HIGHCHARTS():
 
    def get_query(self, ep_day, ep_id, email):
        return '''
SELECT 
    (select gw_name from OB_GATEWAY where gw_id = d.gw_id) gw_name
    , (SELECT ep_name FROM OB_ENDPOINT WHERE ep_id = d.ep_id) ep_name
    , (select comd_cdnm from CM_CODED where comd_code = d.ep_type) ep_type
    , if(ISNULL(d.ep_data), null, d.ep_data*1) ep_data
    , unix_timestamp(str_to_date(concat(d.ep_day, d.ep_time),'%%Y%%m%%d%%H%%i')) ep_unix    
    , d.ep_day
    , d.ep_time
FROM 
CM_USER_GATEWAY a 
INNER JOIN OB_GATEWAY_MAP b ON a.gw_id = b.gw_id 
INNER JOIN OB_DEVICE_MAP c ON b.dev_id = c.dev_id 
INNER JOIN RM_GET_DATA d ON c.ep_id = d.ep_id and a.gw_id = d.gw_id
AND d.ep_day = '{0}' 
WHERE 
    d.ep_id = '{1}'
    AND a.email = '{2}'
    AND d.ep_data is not null
    order by ep_name, ep_time desc
        '''.format( ep_day, ep_id, email )
        
    def get_chart_query(self,time_type, ep_day, ep_id, email):
        sub_query = self.get_query(ep_day, ep_id, email)
        return '''
            select t1.time_key times, t2.ep_data, t2.ep_unix
            from 
            CM_TIME t1 left outer join (
             {0}
            ) t2 on t1.time_key = t2.ep_time where  t1.time_type = '{1}'
        '''.format(sub_query, time_type)

    def get_type_query(self, email, ep_type, gw_id):
        return '''
select 
    b.gw_id
    , (select gw_name from OB_GATEWAY where gw_id = b.gw_id) gw_name    
    , d.ep_id
    , d.ep_type
    , (select comd_cdnm from CM_CODED where comd_code = d.ep_type) ep_type_kor
    , d.ep_name
from 
    CM_USER_GATEWAY a 
    inner join OB_GATEWAY_MAP b on a.gw_id = b.gw_id 
    inner join OB_DEVICE_MAP c on b.dev_id = c.dev_id 
    inner join OB_ENDPOINT d on c.ep_id = d.ep_id
    where 
        a.email = '{0}' 
        and d.ep_type='{1}'
        and b.gw_id = '{2}'        
        '''.format(email, ep_type, gw_id)

    def get_type_entry(self,time_type, ep_day, email, ep_type,gw_id):
        try:
            query = self.get_type_query(email, ep_type,gw_id)
            df = pd.read_sql_query(query, con=db.engine)
            records = df.to_dict(orient='records')
            for record in records:
                ep_id = record.get('ep_id')
                ca = self.get_chart_entry(time_type, ep_day, email, ep_type,ep_id)
                record.update(ca)
            return records
        except Exception as e:
            print("ERROR-->", str(e))
            return {}

    def get_chart_entry(self,time_type, ep_day, email, ep_type,ep_id): 
        query = self.get_query(ep_day, ep_id, email)
        ct_query= self.get_chart_query(time_type, ep_day, ep_id, email)
        df = pd.read_sql_query(query,con=db.engine)
        cdf = pd.read_sql_query(ct_query,con=db.engine)
        cdf = cdf.where((pd.notnull(cdf)),None)
        json_str = df.to_json(orient='records')
        return {
            'table_data' : json.loads(json_str) 
            , 'chart_data' :  {'times' : cdf.times.tolist(),'unix' : cdf.ep_unix.tolist(), 'values' : cdf.ep_data.tolist() }
        }        
    
if __name__ == '__main__':
    
    service = MD_HIGHCHARTS()
    d = service.get_type_entry('MIN_5', '20170630','1a@aaa.com','ep_s_temperature','FTM20170601012345678901234567894')
    
    
    from pprint import pprint
    pprint(d)
        
    print(fn_jsonify({'data' : d}))
        

























