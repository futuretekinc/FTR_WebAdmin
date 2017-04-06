import json
import decimal

from flask import jsonify

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(float(obj))
    raise TypeError

'''
USE -
json.dumps({},default=decimal_default)
'''

def fn_jsonify(obj):
    try:
        return jsonify(obj)
    except Exception as e:
        pass
    return json.dumps(obj,default=decimal_default)
