# -*- coding : utf-8 -*-
from app import db, render_template, send_from_directory
from flask import Response, jsonify, request,Blueprint,flash,redirect
from app.cmm.services.menu_handler import find_menu
from app.cmm.views.baseViews import RenderTemplateView, CM_CODED_VIEW
from app.cmm.views.cmUserView import CM_USER_VIEW, CM_MENU_ITEM_VIEW,\
    CM_USER_ROLE_VIEW
from app.cmm.forms import MasterCDForm, DetailCDForm
from app.cmm.models import CM_CODEM, CM_CODED
from app.cmm.views.cmCodeView import CM_FIND_COMM_VIEW


cmm = Blueprint('cmm', __name__, url_prefix='/cmm')

# cmm.add_url_rule('/about', view_func=RenderTemplateView.as_view('about_page', template_name='about.html'))
userView = CM_USER_VIEW().as_view('user_view')
userRoleView = CM_USER_ROLE_VIEW().as_view('user_role_view')
userRoleMenuView = CM_USER_VIEW().as_view('user_role_menu')
cmCodeView = CM_CODED_VIEW().as_view('cm_coded_view')
# 
cmm.add_url_rule('/coded',view_func=cmCodeView)
cmm.add_url_rule('/users', view_func=userView)
cmm.add_url_rule('/user_role', view_func=userRoleView)
cmm.add_url_rule('/menus',view_func=CM_MENU_ITEM_VIEW().as_view('menu_view'))


cmm.add_url_rule('/find_code',view_func=CM_FIND_COMM_VIEW().as_view('cm_find_comm_view'))

@cmm.route('/editcode',methods=['GET','POST'])
def editcode():
    mform = MasterCDForm(request.form)
    dform = DetailCDForm(request.form)

    code = { 'result' : [] }
    rs = db.session.query(CM_CODEM).all()
    for x in rs:
        code['result'].append({'comm_code':x.comm_code, 'comm_cdnm' : x.comm_cdnm })
    return render_template('cmm/editcode.html',mform=mform,dform=dform,mcode=code, title='시스템코드등록',username='FutureTeK')    

@cmm.route('/master_code',methods=['GET','POST'])
def masterCode():
    form = MasterCDForm(request.form)
    if request.method == 'POST' and form.validate():
        mcode = CM_CODEM()
        mcode.comm_code = str(form.comm_code.data).upper()
        mcode.comm_cdnm = form.comm_cdnm.data
        mcode.re1f_desc = form.re1f_desc.data
        mcode.re2f_desc = form.re2f_desc.data
        mcode.re3f_desc = form.re3f_desc.data
        mcode.re4f_desc = form.re4f_desc.data
        db.session.add(mcode)
        db.session.commit()
        flash('Thanks for registering')
    code = db.session.query(CM_CODEM).all()
    return redirect('/cmm/editcode')    

@cmm.route('/detail_code',methods=['GET','POST'])
def detailCode():
    
    form = DetailCDForm(request.form)
    if request.method == 'POST' and form.validate():
        code = CM_CODED()
        code.comm_code = str(form.comm_code.data).upper()
        code.comd_code = str(form.comd_code.data).upper()
        code.comd_cdnm = str(form.comd_cdnm.data)
        code.ref1_fild = form.ref1_fild.data
        code.ref2_fild = form.ref2_fild.data
        code.ref3_fild = form.ref3_fild.data
        code.ref4_fild = form.ref4_fild.data
        db.session.add(code)
        db.session.commit()
        flash('Thanks for registering')
    code = db.session.query(CM_CODEM).all()
    return redirect('/cmm/editcode')    
        

@cmm.route('/CMMAA001')
def CMMAA001():
    pass

@cmm.route('/CMMAA002')
def CMMAA002():
    pass

@cmm.route("/page/<filename>")
def page(filename):
    return render_template('cmm/{}'.format(filename),title='FTOM',username='FutureTek')

@cmm.route('/menu')
def menu(id=4):
    '''system code '''
    tree = find_menu()
    return render_template('cmm/menu.html',tree=tree)

