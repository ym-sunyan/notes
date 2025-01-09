# 数据库模块，以mysql为例
# 首先在mysql中已经创建新数据库
from exts import db
from datetime import datetime

class Demo(db.Model):
    '''
    @Time    :   2024/02/18 14:47:38
    @Author  :   sunyan
    @Desc    :   None'''
    __tablename__ = "demo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc="唯一标识符")
    usename = db.Column(db.String(100), nullable=False, doc="用户名称")
    password = db.Column(db.String(100), nullable=False, doc="密码")
    email = db.Column(db.String(100), unique=True, nullable=False, doc="邮箱地址")
    # phone = db.Column(db.String(32), nullable=False)
    # address = db.Column(db.String(256))
    join_time = db.Column(db.DateTime, default=datetime.now, doc="创建时间")
    pass

class ask_copilot(db.Model):
    '''
    @Time    :   2024/02/18 14:47:38
    @Author  :   sunyan
    @Desc    :   None'''
    __tablename__ = "ask_copilot"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, doc="唯一标识符")
    ip = db.Column(db.String(15), nullable=False, doc="提问的ip地址")
    port = db.Column(db.String(5), nullable=False, doc="端口")
    question = db.Column(db.Text(5000), nullable=False, doc="问题")
    ask_model = db.Column(db.String(50),default="0",nullable=False, doc="提问模式。0：普通")
    answoer = db.Column(db.Text(5000), nullable=False, doc="答案")
    run_time = db.Column(db.String(10), nullable=False, doc="运行耗时")
    ask_time = db.Column(db.DateTime, default=datetime.now, doc="提问时间")
    pass