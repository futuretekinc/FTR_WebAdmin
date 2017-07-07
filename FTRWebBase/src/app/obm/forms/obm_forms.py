#-*- conding: utf-8 -*-
from datetime import datetime

from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, StringField, PasswordField, validators, IntegerField, SelectField, TextAreaField, DateField, HiddenField, DateTimeField
from wtforms.validators import DataRequired, Required

from app import db
from app.cmm.models import CM_CODED
from app.obm.models.ob_resources import OB_ENDPOINT_TYPE, OB_DEVICE_TYPE, \
    OB_GATEWAY
from app.cmm.services.service import MD_CM_USER, MD_TIME_TYPE


class OB_RESOURCE_FORM(Form):
    rc_name = StringField(u'자원 명', [validators.required(),validators.Length(min=1,max=50)])
    
class OB_GATEWAY_FORM(Form):
    hd_gw_id = HiddenField(u'gw_id')
    gw_name = StringField(u'게이트웨이 명', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : 'Gateway Name','required':'required'})
    gw_location = StringField(u'설치위치', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : 'Gateway Location Info'})
    last_update = DateTimeField('last_update', format="%Y-%m-%dT%H:%M:%S",default=datetime.today,validators=[])
    
#     delete_enable = BooleanField('삭제권한', [validators.DataRequired()])
#     update_enable = BooleanField('수정권한', [validators.DataRequired()])

class OB_GATEWAY_SAVE_FORM(Form):
    gw_id = StringField(u'게이트웨이 ID', [validators.required(),validators.Length(min=1,max=32)],render_kw={'placeholder' : 'Gateway Id','required':'required'})
    last_update = DateTimeField('last_update', format="%Y-%m-%dT%H:%M:%S",default=datetime.today,validators=[])
#     gw_name = StringField(u'게이트웨이 명', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : 'Gateway Name','required':'required'})
#     gw_location = StringField(u'설치위치', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : 'Gateway Location Info'})
#     last_update = DateTimeField('last_update', format="%Y-%m-%dT%H:%M:%S",default=datetime.today,validators=[])
#     delete_enable = BooleanField('게이트웨이에서 정보 삭제 금지', [validators.DataRequired()])
#     update_enable = BooleanField('게이트웨이에서 정보 수정 금지', [validators.DataRequired()])
    def __init__(self,*args,**kwargs):
        Form.__init__(self,*args,**kwargs)
        self.dvtype = None
    
    def validate(self):
        rv = Form.validate(self)
        dvType = db.session.query(OB_GATEWAY) \
                    .filter(OB_GATEWAY.gw_id == str(self.gw_id.data)) \
                    .first()
        if dvType is not None:
            self.gw_id.errors.append('이미 존재하는 게이트웨이입니다.')
            return False
        self.gw_id = dvType
        return rv
      
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
    
    
class USER_GATEWAY_FROM(Form):    
    gateways = SelectField(u'게이트웨이', choices=[ ('-', '-' )],validators=[validators.optional()])
    timetypes = SelectField(u'시간간격', choices=[ ('-', '-' )],validators=[validators.optional()])
    ep_type = StringField(u'엔드포인트타입',validators=[validators.optional()])
    target_date = StringField(u'지정일',validators=[validators.optional()])
    def __init__(self,*args,**kwargs):
        Form.__init__(self,*args,**kwargs)
    def update_field(self,email):
        self.gateways.choices = self.gateway_choice(email)
        self.timetypes.choices = self.timetype_choice()
    def gateway_choice(self,email):
        cmUser = MD_CM_USER()
        gws = cmUser.get_gw_list(email)
        buf = []
        for gw in gws:
            buf.append((gw.gw_id, gw.gw_name))
        return buf
    def timetype_choice(self):
        tmType = MD_TIME_TYPE()
        return tmType.get_choice_entry()

class DisabledTextField(StringField):
  def __call__(self, *args, **kwargs):
    kwargs.setdefault('disabled', True)
    return super(DisabledTextField, self).__call__(*args, **kwargs) 
   
class OB_DEVICE_EDIT_FORM(Form):
    dev_id = DisabledTextField(u'디바이스 ID', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : u'디바이스 ID'})
    dev_name = StringField(u'디바이스 명', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : u'디바이스 명'})
    dev_location = StringField(u'설치위치', [validators.required(),validators.Length(min=1,max=50)],render_kw={'placeholder' : u'설치위치'})

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