import os

class Config:
    # 安全密钥
    SECRET_KEY = 'dev-secret-key-123456'
    
    # 数据库配置（使用SQLite）
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:123456@localhost:3306/gudianmusic?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 允许跨域请求
    CORS_ORIGINS = ['http://localhost:5173']

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}