from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models import User, Music, Danmu
import json
import hashlib
import time
from sqlalchemy import text

# 创建蓝图
api_bp = Blueprint('api', __name__)

# ==================== 基础测试 ====================

@api_bp.route('/hello', methods=['GET'])
def hello():
    """基础测试接口"""
    return jsonify({
        'success': True,
        'message': '古典音乐API服务正常',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    })

# ==================== 用户认证 ====================

@api_bp.route('/auth/register', methods=['POST'])
def register():
    """用户注册"""
    print("📝 收到注册请求")
    
    try:
        data = request.get_json()
        print(f"注册数据: {data}")
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': '请提供用户名和密码'
            }), 400
        
        username = data['username'].strip()
        password = data['password'].strip()
        
        if len(username) < 3 or len(username) > 20:
            return jsonify({
                'success': False,
                'message': '用户名长度应为3-20个字符'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': '密码长度至少6个字符'
            }), 400
        
        # 检查用户名是否存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': '用户名已存在'
            }), 400
        
        # 创建新用户
        new_user = User(
            username=username,
            password=password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        print(f"✅ 用户注册成功: {username}")
        
        return jsonify({
            'success': True,
            'message': '注册成功',
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'created_at': new_user.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ 注册失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '注册失败',
            'error': str(e)
        }), 500

@api_bp.route('/auth/login', methods=['POST'])
def login():
    """用户登录"""
    print("📱 收到登录请求")
    
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': '请提供用户名和密码'
            }), 400
        
        username = data['username'].strip()
        password = data['password'].strip()
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({
                'success': False,
                'message': '用户名不存在'
            }), 401
        
        # 验证密码
        if user.password != password:
            return jsonify({
                'success': False,
                'message': '密码错误'
            }), 401
        
        print(f"✅ 登录成功: {username}")
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # 生成token
        token_str = f"{user.id}{user.username}{time.time()}"
        token = hashlib.md5(token_str.encode()).hexdigest()
        
        # 用户数据
        user_data = {
            'id': user.id,
            'username': user.username,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }
        
        return jsonify({
            'success': True,
            'message': '登录成功',
            'user': user_data,
            'token': token,
            'login_time': datetime.utcnow().isoformat()
        })
            
    except Exception as e:
        print(f"❌ 登录失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '登录失败',
            'error': str(e)
        }), 500

@api_bp.route('/auth/logout', methods=['POST'])
def logout():
    """用户退出"""
    print("🚪 收到退出请求")
    return jsonify({
        'success': True,
        'message': '退出成功'
    })

@api_bp.route('/auth/check', methods=['GET'])
def check_auth():
    """检查登录状态"""
    print("🔍 登录状态检查")
    return jsonify({
        'authenticated': False,
        'message': '请使用token验证'
    })

# ==================== 音乐相关 ====================

@api_bp.route('/music', methods=['GET'])
def get_music():
    """获取音乐列表"""
    genre = request.args.get('genre', 'all')
    
    if genre == 'all':
        music_list = Music.query.all()
    else:
        music_list = Music.query.filter_by(genre=genre).all()
    
    return jsonify({
        'success': True,
        'count': len(music_list),
        'music': [m.to_dict() for m in music_list]
    })

@api_bp.route('/music/init', methods=['GET'])
def init_music():
    """初始化测试音乐数据"""
    print("🎵 初始化音乐数据")
    
    # 先清空现有数据
    Music.query.delete()
    
    test_music = [
        {
            'title': '高山流水',
            'artist': '管平湖',
            'dynasty': '唐',
            'genre': 'guqin',
            'cover': 'image/gsls.jfif',
            'description': '古琴名曲，伯牙子期知音之曲'
        },
        {
            'title': '十面埋伏',
            'artist': '刘德海',
            'dynasty': '明',
            'genre': 'pipa',
            'cover': 'image/smmf.jfif',
            'description': '琵琶武曲，描绘楚汉垓下之战'
        },
        {
            'title': '春江花月夜',
            'artist': '王惠然',
            'dynasty': '清',
            'genre': 'pipa',
            'cover': 'image/cjhyy.jfif',
            'description': '琵琶文曲，描写江南春夜美景'
        }
    ]
    
    try:
        for item in test_music:
            music = Music(**item)
            db.session.add(music)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '测试数据添加成功',
            'count': len(test_music)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': '添加测试数据失败',
            'error': str(e)
        }), 500

# ==================== 弹幕相关 ====================

@api_bp.route('/danmu/sentences', methods=['GET'])
def get_danmu_sentences():
    """获取弹幕句子库"""
    sentences = [
        '礼乐之邦，华夏正音', '高山流水，知音难觅', '霓裳羽衣，盛世华章', '诗经三百，皆可弦歌',
        '周公制礼作乐，天下归心', '孔子闻韶，三月不知肉味', '老子大音希声，大象无形', '骨笛九千年，声声吹古今',
        '编钟十二律，一钟双音妙', '唐大曲霓裳，飘然转旋回雪轻', '宋詞牌蝶恋，浅斟低唱杨柳岸',
        '元杂剧西厢，花月影中共婵娟', '明清皮黄，京韵绕梁三日', '宫商角徵羽，五音调心', '三分损益，伶伦截竹',
        '律吕阴阳，六律六吕', '琴瑟友之，钟鼓乐之', '玉笛飞声，散入春风', '谁家玉笛暗飞声', '散入春风满洛城',
        '此夜曲中闻折柳', '何人不起故园情'
    ]
    
    return jsonify({
        'success': True,
        'count': len(sentences),
        'sentences': sentences
    })

@api_bp.route('/danmu', methods=['GET'])
def get_danmus():
    """获取弹幕列表 - 从数据库读取"""
    print("📥 收到弹幕列表请求")
    
    try:
        limit = request.args.get('limit', 50, type=int)
        
        # 从数据库获取最新的弹幕
        danmus = Danmu.query.order_by(Danmu.created_at.desc()).limit(limit).all()
        
        # 反转顺序，让最早的先显示
        danmus = danmus[::-1]
        
        print(f"✅ 从数据库获取 {len(danmus)} 条弹幕")
        
        return jsonify({
            'success': True,
            'count': len(danmus),
            'danmus': [d.to_dict() for d in danmus]
        })
        
    except Exception as e:
        print(f"❌ 获取弹幕失败: {str(e)}")
        # 失败时返回示例数据
        example_danmus = [
            {
                'id': 1,
                'text': '欢迎来到古典音乐世界',
                'color': '#FFFFFF',
                'size': 14,
                'position': 1,
                'speed': 15.0,
                'is_user': False,
                'created_at': datetime.utcnow().isoformat()
            }
        ]
        
        return jsonify({
            'success': True,
            'count': len(example_danmus),
            'danmus': example_danmus
        })

@api_bp.route('/danmu', methods=['POST'])
def create_danmu():
    """发送弹幕 - 保存到数据库"""
    print("📝 收到发送弹幕请求")
    
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'message': '请提供弹幕内容'
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                'success': False,
                'message': '弹幕内容不能为空'
            }), 400
        
        if len(text) > 20:
            return jsonify({
                'success': False,
                'message': '弹幕内容不能超过20字'
            }), 400
        
        # 从请求头获取token
        auth_header = request.headers.get('Authorization')
        user_id = None
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]
            # 简化处理：从token提取用户ID
            # token格式为 "user_{id}_{timestamp}" 的MD5
            # 这里我们直接从localStorage获取用户ID更简单
            pass
        
        # 也可以从前端直接传递用户ID
        user_id = data.get('user_id')
        
        # 创建弹幕记录
        danmu = Danmu(
            user_id=user_id,
            text=text,
            color=data.get('color', '#FFD700'),
            size=data.get('size', 14),
            position=data.get('position', 3),
            speed=data.get('speed', 15.0),
            is_user=user_id is not None
        )
        
        db.session.add(danmu)
        db.session.commit()
        
        print(f"✅ 弹幕已保存到数据库: {text} (ID: {danmu.id})")
        
        return jsonify({
            'success': True,
            'message': '弹幕发送成功',
            'danmu': danmu.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ 弹幕保存失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '弹幕发送失败',
            'error': str(e)
        }), 500

# ==================== 收藏相关 ====================

@api_bp.route('/collections', methods=['GET'])
def get_collections():
    """获取收藏列表"""
    # 需要token验证，现在返回示例数据
    example_collections = [
        {
            'type': 'theory',
            'key': 'theory-wuyin',
            'name': '五声调式',
            'icon': '🎵',
            'brief': '宫商角徵羽 · Do Re Mi Sol La',
            'collected_at': datetime.utcnow().isoformat()
        },
        {
            'type': 'work',
            'key': 'work-1',
            'name': '高山流水',
            'icon': '🎵',
            'brief': '管平湖 · 唐',
            'collected_at': datetime.utcnow().isoformat()
        }
    ]
    
    return jsonify({
        'success': True,
        'count': len(example_collections),
        'collections': example_collections
    })

@api_bp.route('/collections', methods=['POST'])
def add_collection():
    """添加收藏"""
    data = request.get_json()
    
    if not data or 'type' not in data or 'id' not in data:
        return jsonify({
            'success': False,
            'message': '请提供收藏类型和ID'
        }), 400
    
    return jsonify({
        'success': True,
        'message': '收藏成功',
        'collection': {
            'type': data['type'],
            'id': data['id'],
            'collected_at': datetime.utcnow().isoformat()
        }
    })

# ==================== 收藏相关 ====================

@api_bp.route('/favorites', methods=['GET'])
def get_favorites():
    """当前登录用户的收藏列表"""
    user_id = _get_user_id_from_request()
    if not user_id:
        return jsonify({'success': False, 'message': '请先登录'}), 401

    rows = db.session.execute(
        text("SELECT type, key_name, name, icon, brief, created_at "
             "FROM user_favorite WHERE user_id = :uid ORDER BY created_at DESC"),
        {'uid': user_id}
    ).fetchall()

    return jsonify({
        'success': True,
        'count': len(rows),
        'list': [{
            'type': r.type,
            'key': r.key_name,
            'name': r.name,
            'icon': r.icon,
            'brief': r.brief,
            'collected_at': r.created_at.isoformat()
        } for r in rows]
    })

@api_bp.route('/favorites', methods=['POST'])
def add_favorite():
    """添加收藏"""
    user_id = _get_user_id_from_request()
    if not user_id:
        return jsonify({'success': False, 'message': '请先登录'}), 401

    data = request.get_json() or {}
    required = ['type', 'key', 'name', 'icon', 'brief']
    if not all(k in data for k in required):
        return jsonify({'success': False, 'message': '缺少字段'}), 400

    try:
        db.session.execute(
            text("INSERT INTO user_favorite (user_id, type, key_name, name, icon, brief) "
                 "VALUES (:uid, :t, :k, :n, :i, :b) "
                 "ON DUPLICATE KEY UPDATE created_at=NOW()"),
            {'uid': user_id, 't': data['type'], 'k': data['key'],
             'n': data['name'], 'i': data['icon'], 'b': data['brief']}
        )
        db.session.commit()
        return jsonify({'success': True, 'message': '已收藏'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/favorites', methods=['DELETE'])
def del_favorite():
    """删除收藏"""
    user_id = _get_user_id_from_request()
    if not user_id:
        return jsonify({'success': False, 'message': '请先登录'}), 401

    data = request.get_json() or {}
    key_name = data.get('key')
    ftype = data.get('type')
    if not key_name or not ftype:
        return jsonify({'success': False, 'message': '缺少字段'}), 400

    db.session.execute(
        text("DELETE FROM user_favorite WHERE user_id=:uid AND type=:t AND key_name=:k"),
        {'uid': user_id, 't': ftype, 'k': key_name}
    )
    db.session.commit()
    return jsonify({'success': True, 'message': '已取消收藏'})

def _get_user_id_from_request():
    auth = request.headers.get('Authorization') or ''
    if auth.startswith('Bearer '):
        try:
            return int(auth[7:])
        except:
            pass
    return None

@api_bp.route('/favicon.ico')
def favicon():
    return '', 204          # 204 No Content