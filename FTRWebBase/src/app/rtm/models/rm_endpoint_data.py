# -*- coding: utf-8 -*-
from app import db,ma 
from app.cmm.utils.uuid_gen import uuid_gen
from sqlalchemy import func
from sqlalchemy.orm import joinedload

class RM_ENDPOINT_DATA(db.Model):
    __tablename__ = "RM_ENDPOINT_DATA"
    ep_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    ep_month = db.Column(db.NVARCHAR(6),nullable=False,primary_key=True) # yyyymmddhhmm
    ep_day = db.Column(db.NVARCHAR(8),nullable=False,primary_key=True) # yyyymmddhhmm
    ep_time = db.Column(db.NVARCHAR(4),nullable=False,primary_key=True) # yyyymmddhhmm
    ep_sec = db.Column(db.NVARCHAR(12),nullable=False,primary_key=True) # sss
    ep_unix = db.Column(db.NVARCHAR(15),nullable=False,primary_key=True)
    ep_data = db.Column(db.NVARCHAR(50),nullable=False)
    ep_offset = db.Column(db.Integer,nullable=False,default=0)
    ep_part = db.Column(db.Integer,nullable=False,default=0)
    create_dt = db.Column(db.DATETIME,default=db.func.current_timestamp())



