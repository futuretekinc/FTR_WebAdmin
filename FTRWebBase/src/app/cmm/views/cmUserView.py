'''
[Ref.]
http://flask-docs-kr.readthedocs.io/ko/latest/views.html
'''

from flask import render_template, jsonify, g, abort,session
from flask.views import View, MethodView

from app import db, ma
from app.cmm.models import CM_USER, CM_MENU_ITEM, CM_USER_ROLE

def user_required(f):
    """Checks whether user is logged in or raises error 401."""
    def decorator(*args, **kwargs):
        if not g.user:
            abort(401)
        return f(*args, **kwargs)
    return decorator

class SCH_CM_USER(ma.Schema):
    class Meta:
        fields = ('user_id', 'company_id', 'username', 'phone','role_name','email')

class SCH_CM_MENU_ITEM(ma.Schema):
    class Meta:
        fields = ('menu_id', 'pmenu_id', 'category', 'name','url')

class SCH_CM_USER_ROLE(ma.Schema):
    class Meta:
        fields = ('role_name', 'menu_id', 'oper_C', 'oper_R','oper_U','oper_D')
        
user_many = SCH_CM_USER(many=True)
user_role_many = SCH_CM_USER_ROLE(many=True)
menu_many = SCH_CM_MENU_ITEM(many=True)

class CM_USER_VIEW(MethodView):
#     decorators = [user_required]
    def get(self):
        return render_template('cmm/users.html',title="사용자관리")
    
    def post(self):
        users = db.session.query(CM_USER).all()
        result = user_many.dump(users)
        return jsonify({ 'data' : result.data }) 

class CM_USER_ROLE_VIEW(MethodView):
#     decorators = [user_required]
    def get(self):
        return render_template('cmm/user_role.html',title="사용자권한관리")
    
    def post(self):
        users = db.session.query(CM_USER_ROLE).all()
        result = user_role_many.dump(users)
        return jsonify({ 'data' : result.data }) 



class CM_MENU_ITEM_VIEW(MethodView):
    def get(self):
        return render_template('cmm/menus.html',title="메뉴관리",tree=session['tree'])
    def post(self):
        menus = db.session.query(CM_MENU_ITEM).filter(CM_MENU_ITEM.use_yn == 'Y').all()
        result = menu_many.dump(menus)
        return jsonify({'data' : result.data})


