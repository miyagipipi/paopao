from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import *


class Base(DeclarativeBase):
  pass

engine = create_engine(
    f'mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    echo=False)

# 创建一个线程安全的会话
db_session = scoped_session(sessionmaker(bind=engine))
db = SQLAlchemy(model_class=Base)

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
    db.init_app(app)
    db.session = db_session # 绑定session到app
