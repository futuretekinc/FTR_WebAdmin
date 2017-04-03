from app import db, ma
from marshmallow_sqlalchemy import ModelSchema
from app.obm.models import *

class SCH_OB_RESOURCE(ModelSchema): 
    class Meta: model = OB_RESOURCE

class SCH_OB_GATEWAY(ModelSchema):
    class Meta:
        model = OB_GATEWAY

class SCH_OB_DEVICE(ModelSchema):
    class Meta:
        model = OB_DEVICE

class SCH_OB_ENDPOINT(ModelSchema):
    class Meta:
        model = OB_ENDPOINT

class SCH_OB_DEVTYPE(ModelSchema):
    class Meta:
        model = OB_DEVICE_TYPE

class SCH_OB_EPTYPE(ModelSchema):
    class Meta:
        model = OB_ENDPOINT_TYPE

class SCH_OB_DEVICE_TYPE_MAP(ModelSchema):
    class Meta:
        model = OB_DEVICE_TYPE_MAP

'''
SqlAlchemyObjectSerializer
'''
ob_resource_many         = SCH_OB_RESOURCE(many=True)
ob_gateway_many          = SCH_OB_GATEWAY(many=True)
ob_device_many           = SCH_OB_DEVICE(many=True)
ob_endpoint_many         = SCH_OB_ENDPOINT(many=True)
ob_eptype_many           = SCH_OB_EPTYPE(many=True)
ob_dvtype_many           = SCH_OB_DEVTYPE(many=True)
ob_devtype_single        = SCH_OB_DEVTYPE(many=False)
ob_device_type_map_many  = SCH_OB_DEVICE_TYPE_MAP(many=True)

