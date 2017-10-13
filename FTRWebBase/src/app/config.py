# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
from datetime import timedelta
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


APP_SALT= b'$2b$05$frugyJd.fV8zeGjNk4MVJO'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example

SQLITE3 = "sqlite:///D:/tmp/single_db.db"
AZURE_APP_DB = "mssql+pyodbc://devweb:Qvbcuxpr#123456@ftiotdb1.database.windows.net/appdb?driver=ODBC+Driver+13+for+SQL+Server"
MYSQL_DB='mysql+pymysql://ftrdb:4rnekd9wkd@ftrdb.japanwest.cloudapp.azure.com/ftrapp?charset=utf8'
MYSQL_OPER='mysql+pymysql://root:4rnekd9wkd@ftr-app.japanwest.cloudapp.azure.com/ftr_app_db?charset=utf8'
# ORACLE_TEST="oracle+cx_oracle://HMUSER:HMUSER@hmtidc.iptime.org/JARG"
ORACLE_TEST="oracle+cx_oracle://HMUSER:HMUSER@hmtidc.iptime.org/JARG"
ORACLE_REAL='oracle+cx_oracle://HMUSER:HMUSER@localhost:1521/JARG?charset=utf8'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_DATABASE_URI = MYSQL_DB

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = DEBUG
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_POOL_SIZE = 30
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 500


DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
#THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

WTF_CSRF_ENABLED = True

# Secret key for signing cookies
# SECRET_KEY = "secret"
SECRET_KEY = '#2kajsd9jdj3kd93911-2023'
SESSION_COOKIE_NAME='futuretek_cookies'
PERMANENT_SESSION_LIFETIME=timedelta(31) # 31days


SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 40}
}
SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 15
}
SCHEDULER_API_ENABLED = True
SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
}
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]








