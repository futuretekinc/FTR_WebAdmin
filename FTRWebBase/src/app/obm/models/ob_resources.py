# -*- coding: utf-8 -*-
from app import db,ma 
from app.cmm.utils.uuid_gen import uuid_gen
from sqlalchemy import func
from sqlalchemy.orm import joinedload

    
class OB_RESOURCE(db.Model):
    __tablename__ = "OB_RESOURCE"
    res_id = db.Column(db.Integer,primary_key=True)
    res_name = db.Column(db.NVARCHAR(50),nullable=False)

class OB_GATEWAY(db.Model):
    __tablename__ = "OB_GATEWAY"
    gw_id = db.Column(db.Integer,primary_key=True)
    gw_name = db.Column(db.NVARCHAR(50),nullable=False)

class OB_DEVICE(db.Model):
    __tablename__ = "OB_DEVICE"
    dev_id = db.Column(db.NVARCHAR(32),nullable=False,default=uuid_gen(),primary_key=True)
    dev_name = db.Column(db.NVARCHAR(50),nullable=False)
    dev_type = db.Column(db.NVARCHAR(50),nullable=False)
    dev_inst = db.Column(db.DATETIME)
    dev_info = db.Column(db.NVARCHAR(200))
    
class OB_ENDPOINT(db.Model):
    __tablename__ = "OB_ENDPOINT"
    ep_id = db.Column(db.NVARCHAR(32),nullable=False,default=uuid_gen(),primary_key=True)
    ep_type = db.Column(db.NVARCHAR(50),nullable=False,primary_key=True)
    ep_name = db.Column(db.NVARCHAR(50),nullable=False)
    ep_unit = db.Column(db.NVARCHAR(20),nullable=True)
    ep_pr_host = db.Column(db.NVARCHAR(20),nullable=False,default='127.0.0.1') # parent domain(connection info)
    ep_interval = db.Column(db.Integer,nullable=False,default=10)
    ep_limit = db.Column(db.NVARCHAR(10),nullable=False) # time  / count
    ep_hour = db.Column(db.Integer)
    ep_day = db.Column(db.Integer)
    ep_month = db.Column(db.Integer) 
    ep_count = db.Column(db.Integer)
    
class OB_ENDPOINT_TYPE(db.Model): 
    __tablename__ = "OB_ENDPOINT_TYPE"
    ep_type = db.Column(db.NVARCHAR(50),nullable=False,primary_key=True)
    ep_name = db.Column(db.NVARCHAR(50),nullable=False)
    ep_scale = db.Column(db.Numeric(precision=15,scale=3,asdecimal=False),default=1.0)
#     ep_scale = db.Column(db.NVARCHAR(15),default='1.0')
    ep_unit = db.Column(db.NVARCHAR(20),nullable=True)
    ep_pr_host = db.Column(db.NVARCHAR(60),nullable=False,default='127.0.0.1') # parent domain(connection info)
    ep_interval = db.Column(db.Integer,nullable=False,default=10)
    ep_limit = db.Column(db.NVARCHAR(10),nullable=False) # time  / count
    ep_hour = db.Column(db.Integer)
    ep_day = db.Column(db.Integer)
    ep_month = db.Column(db.Integer)
    ep_count = db.Column(db.Integer)

class OB_DEVICE_TYPE(db.Model):
    __tablename__ = "OB_DEVICE_TYPE"
    dv_type = db.Column(db.NVARCHAR(50),nullable=False,primary_key=True)
    dv_name = db.Column(db.NVARCHAR(50),nullable=False)
    dv_desc = db.Column(db.NVARCHAR(300))
    dv_location = db.Column(db.NVARCHAR(100))
    dv_timeout = db.Column(db.Integer,nullable=False,default=10)
    dv_protocol = db.Column(db.NVARCHAR(100))

class OB_DEVICE_TYPE_MAP(db.Model):
    __tablename__ = "OB_DEVICE_TYPE_MAP"
    dv_type = db.Column(db.NVARCHAR(50),nullable=False,primary_key=True)
    ep_type = db.Column(db.NVARCHAR(50),nullable=False,primary_key=True)
    

