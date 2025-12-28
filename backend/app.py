from flask import Flask
from app import create_app

# 创建Flask应用
app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("🎵 古典音乐后端服务启动")
    print("=" * 50)
    print("主页地址: http://localhost:5000")
    print("API测试: http://localhost:5000/api/hello")
    print("音乐列表: http://localhost:5000/api/music")
    print("初始化数据: http://localhost:5000/api/music/init")
    print("=" * 50)
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    # 启动服务器
    app.run(debug=True, port=5000)