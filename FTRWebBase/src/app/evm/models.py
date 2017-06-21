# -*- coding: utf-8 -*-
from app import db,ma 
from app.cmm.utils.uuid_gen import uuid_gen
from sqlalchemy import func
from sqlalchemy.orm import joinedload

class EV_ACTION_PUSH(db.Model):
    __tablename__ = "EV_ACTION_PUSH"
    req_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    req_type = db.Column(db.NVARCHAR(32),nullable=False) # set_endpoint
    node_id = db.Column(db.NVARCHAR(32),nullable=False) 
    req_value = db.Column(db.NVARCHAR(50),nullable=False) 
    req_stat = db.Column(db.NVARCHAR(30),nullable=False)
    retry_id = db.Column(db.NVARCHAR(32),nullable=True) # confirm check msg_id
    retry = db.Column(db.Integer,nullable=True)
    next_retry = db.Column(db.DATETIME,nullable=True)
    create_dt = db.Column(db.TIMESTAMP,default=db.func.current_timestamp())
    
class EV_RULE(db.Model):
    __tablename__ = "EV_RULE"
    rule_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    rule_name = db.Column(db.NVARCHAR(50),nullable=False,unique=True)
    use_yn = db.Column(db.NVARCHAR(1),nullable=False,default='Y')

class EV_TRIGGER_RULE(db.Model):
    ''' 규칙에 속해 있는 트리거 정의 '''
    __tablename__ = "EV_TRIGGER_RULE"
    rule_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    trg_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    create_dt = db.Column(db.DATETIME,nullable=False,default=db.func.current_timestamp())

class EV_TRIGGER_ACTION(db.Model):
    __tablename__ = "EV_TRIGGER_ACTION"
    trg_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    act_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)


'''
# Trigger Type
1. above - 엔드포인트 값이 주어진 값(value) 이상인 경우
2. below - 엔드포인트 값이 주어진 값(value) 이하인 경우
3. change - 엔드포인트 값이 변경된 경우
4. include - 엔드포인트 값이 범위(upper ~ lower)내인 경우
5. except - 엔드포인트 값이 범위(upper ~ lower)를 벗어난 경우
'''
    
class EV_TRIGGER(db.Model):
    __tablename__ = "EV_TRIGGER"
    trg_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    ep_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    trg_type = db.Column(db.NVARCHAR(50),nullable=False) # above, below, include, except, change
    repeat_yn = db.Column(db.NVARCHAR(1),nullable=False,default='N')
    repeat_ms = db.Column(db.Integer,nullable=False,default=0)
    ep_id = db.Column(db.NVARCHAR(32),nullable=False)
    value = db.Column(db.DECIMAL(15,2),nullable=True)
    upper = db.Column(db.DECIMAL(15,2),nullable=True)
    lower = db.Column(db.DECIMAL(15,2),nullable=True)
    create_dt = db.Column(db.DATETIME,nullable=False,default=db.func.current_timestamp())

'''
Trigger Status
1. ACTIVE
2. DEACTIVE
'''
class EV_TRIGGER_MONITOR(db.Model):
    __tablename__ = "EV_TRIGGER_MONITOR"
    trg_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    trg_status = db.Column(db.Integer,nullable=False,primary_key=True)
    trg_type = db.Column(db.NVARCHAR(50),nullable=False) # above, below, include, except, change
    create_dt = db.Column(db.DATETIME,nullable=False,default=db.func.current_timestamp())

class EV_ACTION(db.Model):
    __tablename__ = "EV_ACTION"
    act_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    act_name = db.Column(db.NVARCHAR(50),nullable=False)
    act_interval = db.Column(db.Integer,nullable=False,default=0) # 0 : just one, 0 < : repeat
    param = db.Column(db.NVARCHAR(100),nullable=True) # param = JSON_TYPE
    result = db.Column(db.NVARCHAR(100),nullable=True) # param = JSON_TYPE
    status = db.Column(db.NVARCHAR(100),nullable=True)
    create_dt = db.Column(db.DATETIME,nullable=False,default=db.func.current_timestamp())

class EV_ACTION_DEFINE(db.Model):
    __tablename__ = "EV_ACTION_DEFINE"
    act_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    act_name = db.Column(db.NVARCHAR(50),nullable=False)
    param = db.Column(db.NVARCHAR(100),nullable=True) # param = JSON_TYPE
    create_dt = db.Column(db.DATETIME,nullable=False,default=db.func.current_timestamp())

class EV_EVENT(db.Model):
    __tablename__ = "EV_EVENT"
    rule_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    act_id = db.Column(db.NVARCHAR(32),nullable=False,primary_key=True)
    ev_stat = db.Column(db.NVARCHAR(30),nullable=False,default="ACTIVE") # ACTIVE, DEACTIVE
    create_dt = db.Column(db.DATETIME,nullable=False,default=db.func.current_timestamp())

class EV_EVENT_SNAP(db.Model):
    __tablename__ = "EV_EVENT_SNAP"
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    rule_id = db.Column(db.NVARCHAR(32),nullable=False)
    act_id = db.Column(db.NVARCHAR(32),nullable=False)
    ev_stat = db.Column(db.NVARCHAR(30),nullable=False,default="ACTIVE") # ACTIVE, DEACTIVE



