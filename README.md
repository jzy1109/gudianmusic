### **\[古典音乐] - 软件工程综合实践项目**

##### 项目信息

#####  	组号：\[21]

#####  	学生：\[金紫怡] (\[21])

#####  	学生：\[江雪兰] (\[36])

#####  	学生：\[柯奕晴] (\[43])

#####  	课程：《软件工程综合实践》

#####  	技术栈：Vue3 (前端) + Flask (后端) + MySQL (数据库)

#####  	项目周期：\[11.6] - \[12.28]



##### 快速启动



##### 我们提供了两种方式快速运行本项目：



#####  	方式一：使用 Docker Compose (推荐)

#####  		前提：确保本地已安装 Docker 和 Docker Compose。

#####  		# 1. 克隆或解压项目

#####  		# 2. 进入项目根目录

#####  		cd \[gudianmusic]

#####  		# 3. 一键启动所有服务 (前端、后端、数据库)

#####  		docker-compose up -d

#####  		# 4. 访问应用

#####  		# - 前端：http://localhost:8080

#####  		# - 后端 API：http://localhost:5000

#####  		# - MySQL：localhost:3306 (root 密码见 docker-compose.yml)

#####  	方式二：手动启动 

#####  		详细步骤见\[部署手册](./docs/部署手册.md)

##### 项目结构

#####  	21组-古典音乐/ # 项目根目录（压缩包解压后应见此结构）

##### &nbsp;	├── 📁 frontend/ # 【必需】Vue3前端项目

##### &nbsp;	│ ├── public/

##### &nbsp;	│ ├── src/

##### &nbsp;	│ ├── package.json # 必须包含运行脚本

##### &nbsp;	│ ├── vite.config.js # 或 vue.config.js

##### &nbsp;	│ └── README-frontend.md # 前端专属说明（可选）

##### &nbsp;	│

##### &nbsp;	├── 📁 backend/ # 【必需】Flask后端项目

##### &nbsp;	│ ├── app/

##### &nbsp;	│ │ ├── \_\_init\_\_.py

##### &nbsp;	│ │ ├── models.py # 数据模型

##### &nbsp;	│ │ ├── routes.py # API路由

##### &nbsp;	│ │ └── utils.py # 工具函数

##### &nbsp;	│ ├── migrations/ # 数据库迁移（如使用Flask-Migrate）

##### &nbsp;	│ ├── requirements.txt # 【必需】Python依赖清单

##### &nbsp;	│ ├── config.py # 配置文件

##### &nbsp;	│ └── run.py # 【必需】应用启动入口

##### &nbsp;	│

##### &nbsp;	├── 📁 database/ # 【必需】数据库相关

##### &nbsp;	│ ├── schema.sql # 数据库建表SQL脚本

##### &nbsp;	│ ├── dummy\_data.sql # 模拟数据脚本（用于演示、可选）

##### &nbsp;	│ └── er\_diagram.png # 数据库ER图（强烈建议）

##### &nbsp;	│

##### &nbsp;	├── 📁 docs/ # 【必需】项目文档

##### &nbsp;	│ ├── 需求规格说明书.md

##### &nbsp;	│ ├── API接口文档.md

##### &nbsp;	│ ├── 部署手册.md

##### &nbsp;	│ └── 演示视频.mp4 # 5-10分钟功能演示

##### &nbsp;	│

##### &nbsp;	└── 📄 README.md # 【必需】项目总README（最重要！）

##### 技术架构说明

#####  	前端 (Vue3)

#####  		构建工具：Vite

#####  		核心框架：Vue 3 + Composition API

#####  		状态管理：Pinia

#####  		UI 组件库：Element Plus

#####  		路由：Vue Router 4

#####  	HTTP 客户端：Axios

#####  	后端 (Flask)

#####  	Web 框架：Flask + Blueprint

#####  	数据库ORM：SQLAlchemy

#####  	身份认证：JWT

#####  	API 文档：Swagger

#####  	部署服务：Gunicorn (生产环境)

##### 数据库 (MySQL)

#####  	版本：MySQL /8.0

#####  	设计工具：MySQL Workbench

##### 开发环境搭建

#####  	前端：进入 frontend/，执行 npm install

#####  	后端：进入 backend/，创建虚拟环境后执行 pip install -r requirements.txt

#####  	数据库：执行 database/schema.sql 和 database/dummy\_data.sql

##### API 接口

#####  	本地文档：\[API 接口文档](./docs/API接口文档.md)

#####  	基础 URL：http://localhost:5000/api

#####  	健康检查：GET /api/health

##### 项目亮点

#####  	工程化：完整的前后端分离、模块化设计、规范的 Git 提交。

#####  	技术深度：使用 Vue 3 Composition API 实现响应式数据流，Flask 结合 SQLAlchemy 实现复杂查询。

#####  	用户体验：前端界面友好，加载流畅，错误处理完善。

#####  	代码质量：代码有清晰注释，关键函数有文档字符串，遵循 PEP 8/ESLint 规范。

##### 问题与解决

#####  	跨域问题：通过 Flask-CORS 中间件解决。

#####  	前端路由刷新 404：配置 Nginx/Vite 的 history 模式回退。

#####  	数据库连接池：使用 SQLAlchemy 的连接池管理，避免性能瓶颈。

##### 演示与截图

#####  	演示视频

##### 文档清单

#####  	\[需求规格说明书](./docs/需求规格说明书.md)

#####  	\[API 接口文档](./docs/API接口文档.md)

#####  	\[部署手册](./docs/部署手册.md)

