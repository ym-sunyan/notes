from flask import Flask
# 导入配置文件
import config 
# 导入扩展
from exts import db
from db_model import ask_copilot
from flask_migrate import Migrate

# 导入蓝图
from blueprints.auth import bp as auto_bp
from blueprints.qa import bp as qa_bp
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)  #  这将允许所有来源的CORS请求
CORS(app, supports_credentials=True)
# 绑定配置文件
app.config.from_object(config)
# print(app.config['me']) # me不存在异常
# print(app.config.me) # me不存在异常
# print(app.config.get("me")) # me不存在返回None

# 绑定app
db.init_app(app)

migrate = Migrate(app, db)

# 绑定（注册）蓝图
# 蓝图作用，可以让每个模块的操作相互独立最后合成即可
app.register_blueprint(auto_bp)
app.register_blueprint(qa_bp)


if __name__ == '__main__':
    app.run(host=app.config.get("HOST"), port=app.config.get("PORT"), debug=True)
