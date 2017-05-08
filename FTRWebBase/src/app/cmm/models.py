import os
import bcrypt 
from sqlalchemy.inspection import inspect
from app import db,ma 

from datetime import datetime
from app.cmm.utils import uuid_gen 
from sqlalchemy.sql.expression import text
 
# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True

# __all__ = ["app.config"]
class FlaskSession(db.Model):
    __tablename__ = 'CM_FLASK_SESSION'
    sid = db.Column(db.NVARCHAR(100),primary_key=True)
    value = db.Column(db.PickleType)
    create_dt = db.Column(db.DATETIME,nullable=False,default=db.func.current_timestamp())
    update_dt = db.Column(db.DATETIME,nullable=False,default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    @classmethod
    def change(cls,sid,value):
        rec = db.session.query(cls).filter(cls.sid == sid).first()  # @UndefinedVariable
        if not rec:
            rec = cls()
            rec.sid = sid
        rec.value = value 
        return rec
               

class CM_MENU_ITEM(db.Model):
    __tablename__ = "CM_MENU_ITEM"
    menu_id = db.Column(db.Integer,primary_key=True)
    pmenu_id = db.Column(db.Integer,nullable=False,default=0)
    depth = db.Column(db.Integer,nullable=False,default=0)
    category = db.Column(db.NVARCHAR(50),nullable=False,default="CMM")
    name = db.Column(db.NVARCHAR(30),nullable=False,default="_undefined_")
    url = db.Column(db.NVARCHAR(30),nullable=False,default="#")
    use_yn = db.Column(db.NVARCHAR(1),nullable=False,default="Y")
    sort_order = db.Column(db.Integer)
    def as_dict(self):
        return {
            'menu_id' : self.menu_id
            ,'pmenu_id' : self.pmenu_id
            ,'depth' : self.depth
            , 'name' : self.name
            , 'url' : self.url
        }
    
class CM_USER_ROLE(db.Model):
    __tablename__ = "CM_USER_ROLE"
    role_name = db.Column(db.NVARCHAR(50),primary_key=True)
    menu_id = db.Column(db.Integer,primary_key=True) 
    oper_C = db.Column(db.NVARCHAR(1),nullable=False,default="Y")
    oper_R = db.Column(db.NVARCHAR(1),nullable=False,default="Y")
    oper_U = db.Column(db.NVARCHAR(1),nullable=False,default="Y")
    oper_D = db.Column(db.NVARCHAR(1),nullable=False,default="Y")
    
class CM_COMPANY(db.Model):
    __tablename__ = "CM_COMPANY"
    company_id = db.Column(db.Integer,primary_key=True)
    company_name = db.Column(db.NVARCHAR(50),nullable=False)
    company_addr = db.Column(db.NVARCHAR(50),nullable=False)
    
class CM_USER(db.Model):
    __tablename__ = "CM_USER"
    user_id = db.Column(db.NVARCHAR(50),primary_key=True)
    company_id = db.Column(db.Integer,nullable=False)
    role_name = db.Column(db.NVARCHAR(50),nullable=False)
    auth_key = db.Column(db.NVARCHAR(32),nullable=False,default=uuid_gen)
    username = db.Column(db.NVARCHAR(50),nullable=False)
    password = db.Column(db.NVARCHAR(50))
    email = db.Column(db.NVARCHAR(50))
    phone = db.Column(db.NVARCHAR(50))

class CM_CODEM(db.Model):
    __tablename__ = "CM_CODEM"
    comm_code = db.Column(db.NVARCHAR(50), primary_key=True, nullable=False)
    comm_cdnm = db.Column(db.NVARCHAR(100),nullable=False)
    use_yn = db.Column(db.NVARCHAR(1),nullable=False,default='Y')
    re1f_desc = db.Column(db.NVARCHAR(100))
    re2f_desc = db.Column(db.NVARCHAR(100))
    re3f_desc = db.Column(db.NVARCHAR(100))
    re4f_desc = db.Column(db.NVARCHAR(100))
    inst_usid = db.Column(db.NVARCHAR(30),default="ADMIN",nullable=False)
    inst_date = db.Column(db.DATETIME,default=db.func.current_timestamp())
    updt_usid = db.Column(db.NVARCHAR(30),default="ADMIN",nullable=False)
    updt_date = db.Column(db.DATETIME,nullable=False,default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
#     tm_coded      = db.relationship('CM_CODED', backref="CM_CODEM")
'''    
class CM_CODEM_SCH(ma.Schema):
    class Meta:
        fields = ('comm_code','comm_cdnm','inst_usid','inst_date')

codem_many = CM_CODEM_SCH(many=True)
'''



class CM_CODED(db.Model):
    __tablename__ = "CM_CODED"
    comm_code = db.Column(db.NVARCHAR(50), primary_key=True)
    comd_code = db.Column(db.NVARCHAR(50), primary_key=True, nullable=False)
    comd_cdnm = db.Column(db.NVARCHAR(200),nullable=False)
    use_yn = db.Column(db.NVARCHAR(1),nullable=False,default='Y')
    ref1_fild = db.Column(db.NVARCHAR(100))
    ref2_fild = db.Column(db.NVARCHAR(100))
    ref3_fild = db.Column(db.NVARCHAR(100))
    ref4_fild = db.Column(db.NVARCHAR(100))
    sort_ordr = db.Column(db.Integer)
    inst_usid = db.Column(db.NVARCHAR(30),default="ADMIN",nullable=False)
    inst_date = db.Column(db.DATETIME,default=db.func.current_timestamp(type_=db.Time))
    updt_usid = db.Column(db.NVARCHAR(30),default="ADMIN",nullable=False)
    updt_date = db.Column(db.DATETIME,nullable=False,default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class CM_TIME(db.Model):
    __tablename__ = "CM_TIME"
    time_type = db.Column(db.NVARCHAR(10),primary_key=True)
    time_key = db.Column(db.NVARCHAR(4),primary_key=True)
