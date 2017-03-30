from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app,db
from app.cmm.models import CM_MENU_ITEM
from flask_admin.base import expose

admin = Admin(app, name='microblog', template_mode='bootstrap3')
# Add administrative views here
class MicroBlogModelView(ModelView):
    can_delete = False  # disable model deletion
    page_size = 50  # the number of entries to display on the list view
    @expose("/new/",methods=('GET','POST'))
    def create_view(self):
        return "CREATE!!!"

admin.add_view(MicroBlogModelView(CM_MENU_ITEM, db.session))

app.run()