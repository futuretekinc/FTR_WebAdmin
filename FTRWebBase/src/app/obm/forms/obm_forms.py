#-*- conding: utf-8 -*-
from app import db
from datetime import datetime
from flask_wtf import Form
from wtforms import BooleanField, StringField, PasswordField, validators, IntegerField,SelectField,TextAreaField,DateField
from wtforms.validators import DataRequired, Required
from app.obm.models.ob_resources import OB_ENDPOINT_TYPE,OB_DEVICE_TYPE
from app.cmm.models import CM_CODED

class OB_RESOURCE_FORM(Form):
    rc_name = StringField(u'자원 명', [validators.required(),validators.Length(min=1,max=50)])
    
class OB_GATEWAY_FORM(Form):
    gw_name = StringField(u'게이트웨이 명', [validators.required(),validators.Length(min=1,max=50)])

class OB_DEVICE_FORM(Form):
    dev_name = StringField(u'디바이스 명', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : u'디바이스 명'})
    dev_type = SelectField(u'디바이스 타입',choices=[('','NONE')],render_kw={'style' : "text-transform:uppercase", 'placeholder' : 'required'})
    dev_inst = DateField(u'설치일자', format="%Y-%m-%d",default=datetime.today,validators=[validators.required()],render_kw={'type' : 'date' })
    dev_info = TextAreaField(u'설명', [validators.required(),validators.Length(min=1,max=300)],render_kw={'placeholder' : u'디바이스 설명'})
    def __init__(self,*args,**kwargs):
        Form.__init__(self,*args,**kwargs)
        self.dev_type.choices = self.dv_type_choice()

    def dv_type_choice(self):
        comm_code = 'DEV_PROTOCOL'
        rows = db.session.query(OB_DEVICE_TYPE).all()
        buf = []
        for x in rows:
            buf.append((x.dv_type, x.dv_name))
        return buf    
    
    
    
    
class OB_ENDPOINT_FORM(Form):
    ep_id = StringField(u'엔드포인트id',[validators.required(), validators.Length(min=32,max=32)]) 
    dev_id = StringField(u'디바이스id',[validators.required(), validators.Length(min=32,max=32)]) 
    ep_type = StringField(u'타입', [validators.required(),validators.Length(min=1,max=50)],render_kw={'style' : "text-transform:uppercase", 'placeholder' : 'required'})
    ep_name = StringField(u'엔드포인트명', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : 'unit'})
    ep_scale = StringField(u'스케일', [validators.required()],render_kw={'type' : 'number','value' : '1.0','step' : "0.001" })
    ep_unit = StringField(u'단위', [validators.Length(min=1,max=50)],render_kw={'placeholder' : 'required'}) # validators.required(),
    ep_pr_host = StringField(u'호스트 정보', [validators.required(),validators.Length(min=1,max=50)],default='127.0.0.1')
    ep_interval = IntegerField(u'실행주기(초)', [validators.NumberRange(min=0, max=100000)],render_kw={'type' : 'number','value' : 0 })
    ep_limit = SelectField(u'이벤트 설정  형태', choices=[ ('time', '시간(time)') , ( 'count', '횟수(count)' )])
    ep_hour = IntegerField(u'시간', [validators.NumberRange(min=0, max=24)],render_kw={'type' : 'number','value' : 0 })
    ep_day = IntegerField(label=u'일', validators=[validators.NumberRange(min=0, max=31)],render_kw={'type' : 'number','value' : 0 })
    ep_month = IntegerField(u'월', [validators.NumberRange(min=0, max=12)],render_kw={'type' : 'number','value' : 0 })
    ep_count = IntegerField(u'카운트', [validators.NumberRange(min=0, max=10000)],render_kw={'type' : 'number','value' : 0 })

class OB_DEVTYPE_FORM(Form):
    dv_type = StringField(u'타입', [validators.required(),validators.Length(min=1,max=50)],render_kw={'style' : "text-transform:uppercase", 'placeholder' : 'required'})
    dv_name = StringField(u'이름', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : 'required'})
    dv_desc = TextAreaField(u'설명', [validators.required(),validators.Length(min=1,max=300)],render_kw={'placeholder' : u'디바이스 설명'})
    dv_location = StringField(u'위치정보', [validators.Length(min=1,max=100)],render_kw={'placeholder' : u'위치정보'})
    dv_timeout = IntegerField(u'타임아웃',[validators.required()],render_kw={'type' : 'number','value' : 0 })
    #dv_option = StringField(u'옵션', [validators.Length(min=1,max=200)],render_kw={'placeholder' : u'옵션'})
    dv_protocol = SelectField(u'프로토콜', choices=[ ('-', '-' )],validators=[validators.optional()])
    
    def __init__(self,*args,**kwargs):
        Form.__init__(self,*args,**kwargs)
        self.dvtype = None
        self.dv_protocol.choices = self.protocol_choice()

    def protocol_choice(self):
        comm_code = 'DEV_PROTOCOL'
        rows = db.session.query(CM_CODED) \
                        .filter(CM_CODED.comm_code == comm_code
                                , CM_CODED.use_yn == 'Y' ).all()
        buf = []
        for x in rows:
            buf.append((x.comd_code, x.comd_code))
        return buf

    def validate(self):
        rv = Form.validate(self)
        dvType = db.session.query(OB_DEVICE_TYPE) \
                    .filter(OB_DEVICE_TYPE.dv_type == str(self.dv_type.data)) \
                    .first()
        if dvType is not None:
            self.dv_type.errors.append('이미 존재하는 타입입니다.')
            return False
        self.dvType = dvType
        return rv
    def updateValidate(self):
        return Form.validate(self)    


class OB_EPTYPE_FORM(Form):
    ep_type = StringField(u'타입', [validators.required(),validators.Length(min=1,max=50)],render_kw={'style' : "text-transform:uppercase", 'placeholder' : 'required'})
    ep_name = StringField(u'이름', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : 'unit'})
    ep_scale = StringField(u'스케일', [validators.required()],render_kw={'type' : 'number','value' : '1.0','step' : "0.001" })
    ep_unit = StringField(u'단위', [validators.Length(min=1,max=50)],render_kw={'placeholder' : 'required'}) # validators.required(),
    ep_pr_host = StringField(u'호스트 정보', [validators.required(),validators.Length(min=1,max=50)],default='127.0.0.1')
    ep_interval = IntegerField(u'실행주기(초)', [validators.NumberRange(min=0, max=100000)],render_kw={'type' : 'number','value' : 0 })
    ep_limit = SelectField(u'이벤트 설정  형태', choices=[ ('time', '시간(time)') , ( 'count', '횟수(count)' )])
    ep_hour = IntegerField(u'시간', [validators.NumberRange(min=0, max=24)],render_kw={'type' : 'number','value' : 0 })
    ep_day = IntegerField(label=u'일', validators=[validators.NumberRange(min=0, max=31)],render_kw={'type' : 'number','value' : 0 })
    ep_month = IntegerField(u'월', [validators.NumberRange(min=0, max=12)],render_kw={'type' : 'number','value' : 0 })
    ep_count = IntegerField(u'Count', [validators.NumberRange(min=0, max=10000)],render_kw={'type' : 'number','value' : 0 })
    
    def __init__(self,*args,**kwargs):
        Form.__init__(self,*args,**kwargs)
        self.etype = None

    def validate(self):
        rv = Form.validate(self)
        etype = db.session.query(OB_ENDPOINT_TYPE) \
                    .filter(OB_ENDPOINT_TYPE.ep_type == str(self.ep_type.data)) \
                    .first()
        print("etype-->",etype)
        if etype is not None:
            self.ep_type.errors.append('이미 존재하는 타입입니다.')
            return False
        self.etype = etype
        return rv
    def updateValidate(self):
        return Form.validate(self)
    
if __name__ == '__main__':
    obj = OB_EPTYPE_FORM()
    print(obj.__dict__)