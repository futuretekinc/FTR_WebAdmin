from app import db

# from flask_wtf import FlaskForm as Form

from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField,SelectField,TextAreaField,DateField
from wtforms.validators import DataRequired, Required
from app.cmm.models import CM_USER


# Import Form validators
# Define the login form (WTForms)
# 
# class LoginForm(Form):
#     email    = TextField('Email Address', [Email(),
#                 Required(message='Forgot your email address?')])
#     password = PasswordField('Password', [
#                 Required(message='Must provide a password. ;-)')])
class LoginForm(Form):
    user_id = StringField('user_id', validators=[DataRequired()])
    password = PasswordField('Password', [Required(message='Must provide a password')])
    
class RegistrationrForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
#class="form-control" placeholder="Name" required=""
class RegistrationUserForm(Form):   
    email = StringField(u'Email', [validators.Length(min=1,max=50)], render_kw={'class' : 'form-control','placeholder' : 'Email', 'required' : '', 'type' : 'email'})
    username = StringField('Username', [validators.Length(min=1,max=50)],render_kw={'class' : 'form-control','placeholder' : 'Name', 'required' : '', 'type' : 'text'})
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ],render_kw={'class' : 'form-control','placeholder' : 'Password', 'required' : ''})
    confirm = PasswordField('Repeat Password',render_kw={'class' : 'form-control','placeholder' : 'Password', 'required' : '', })
    def __init__(self,*args,**kwargs):
        Form.__init__(self,*args,**kwargs)
        self.email_ = None
 
    def validate(self):
        print('validation -' , self.email.data)
        rv = Form.validate(self)
        if self.email.data is not None:
            user = db.session.query(CM_USER) \
                        .filter(CM_USER.email == str(self.email.data)) \
                        .first()
            if user is not None:
                email_ = user.email
                print('email ==>' , email_, '--', self.email.data)
                if email_ is not None:
                    self.email.errors.append('이미 존재하는 타입입니다.')
                    return False
                self.email_ = email_
        return rv     

    
    
class MasterCDForm(Form):
    comm_code = StringField(u'마스터코드', [validators.required(),validators.Length(min=1,max=30)])
    comm_cdnm = StringField(u'코드설명', [validators.required(),validators.Length(min=1,max=30)])
    re1f_desc = StringField(u'보조1', [validators.Length(min=0,max=30)])
    re2f_desc = StringField(u'보조2', [validators.Length(min=0,max=30)])
    re3f_desc = StringField(u'보조3', [validators.Length(min=0,max=30)])
    re4f_desc = StringField(u'보조4', [validators.Length(min=0,max=30)])
 
class DetailCDForm(Form):
    comm_code = StringField(u'마스터코드', [validators.required(),validators.Length(min=1,max=30)])
    comd_code = StringField(u'상세코드', [validators.required(),validators.Length(min=1,max=30)])
    comd_cdnm = StringField(u'코드설명', [validators.required(),validators.Length(min=1,max=30)])
    ref1_fild = StringField(u'보조1', [validators.Length(min=0,max=30)])
    ref2_fild = StringField(u'보조2', [validators.Length(min=0,max=30)])
    ref3_fild = StringField(u'보조3', [validators.Length(min=0,max=30)])
    ref4_fild = StringField(u'보조4', [validators.Length(min=0,max=30)])

