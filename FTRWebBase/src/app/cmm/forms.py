 
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Required



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
    
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    
    
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
 
   