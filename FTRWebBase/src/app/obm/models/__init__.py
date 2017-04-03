from app import db,ma 
from datetime import datetime
from app.cmm.utils import uuid_gen 

from app.obm.models.ob_resources import *
from app.obm.models.sch_ob_resources import *

__all__ = [ 
            "OB_RESOURCE"
            , "OB_GATEWAY"
            , "OB_DEVICE"
            , "OB_DEVICE_TYPE"
            , "OB_DEVICE_TYPE_MAP"
            , "OB_ENDPOINT"
            , "OB_ENDPOINT_TYPE"
            , 'ob_resource_many'
            , 'ob_gateway_many'
            , 'ob_device_many'
            , 'ob_endpoint_many'
            , 'ob_eptype_many'
            , 'ob_dvtype_many'
            , 'ob_device_type_map_many'
            , 'ob_devtype_single'
        ]

