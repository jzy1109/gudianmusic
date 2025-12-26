from datetime import datetime
from app import db

class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat()
        }

class Music(db.Model):
    """音乐作品表"""
    __tablename__ = 'music'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100))
    dynasty = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    cover = db.Column(db.String(200))
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'dynasty': self.dynasty,
            'genre': self.genre,
            'cover': self.cover,
            'description': self.description
        }
class Danmu(db.Model):
    """弹幕模型"""
    __tablename__ = 'danmus'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20), default='#FFFFFF')
    size = db.Column(db.Integer, default=14)
    position = db.Column(db.Integer, default=1)
    speed = db.Column(db.Float, default=15.0)
    is_user = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'color': self.color,
            'size': self.size,
            'position': self.position,
            'speed': self.speed,
            'is_user': self.is_user,
            'created_at': self.created_at.isoformat()
        }