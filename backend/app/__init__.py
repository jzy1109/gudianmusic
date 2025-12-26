from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

# 创建数据库对象
db = SQLAlchemy()

def create_app(config_name='default'):
    # 1. 创建Flask应用
    app = Flask(__name__,static_url_path='/image',static_folder='static')
    
    # 2. 加载配置
    app.config.from_object(config[config_name])
    
    # 3. 初始化数据库
    db.init_app(app)
    
    # 4. 允许跨域
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # 5. 导入路由（稍后创建）
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 6. 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app