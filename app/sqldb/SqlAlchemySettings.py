from flask_sqlalchemy import SQLAlchemy
from Flask_App_Settings import app
from app.conf.conf import MYSQL_CONF

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}:{}/{}".format(MYSQL_CONF['user'],
                                                                                MYSQL_CONF['password'],
                                                                                MYSQL_CONF['host'], MYSQL_CONF['port'],
                                                                                MYSQL_CONF['dbname'])
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
