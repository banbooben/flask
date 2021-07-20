"""
Created on 2020年2月7日

@author: jianzhihua
"""

# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
BaseModel = declarative_base()

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)





def init_db(app):
    # from config.server_conf import current_config
    app.logger.info("MYSQL_CONNECT_URL: " + app.config.SQLALCHEMY_DATABASE_URI)
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_BINDS"] = dict(db=app.config.SQLALCHEMY_DATABASE_URI)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    # app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

    # if current_config.USE_DB_POOL:
    #     app.config["SQLALCHEMY_ENGINE_OPTIONS"] = current_config.SQLALCHEMY_ENGINE_OPTIONS

    # db = SQLAlchemy()
    # db.init_app(app)
    # session = db.session
    # migrate = Migrate(app, db, compare_type=True, compare_server_default=True)
