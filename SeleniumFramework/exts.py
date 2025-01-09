# 扩展文件 exts 
# 该文件存在的意义就是为了解决循环引用导致的bug
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()