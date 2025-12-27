### **API接口文档**

##### 用户管理

##### &nbsp;	注册

##### &nbsp;	URL：/auth/register

##### &nbsp;	Method：POST

##### &nbsp;	Data：

##### &nbsp;		{

##### &nbsp;		  "username": "example",

##### &nbsp;		  "password": "password"

##### &nbsp;		}

##### &nbsp;	Response：

##### &nbsp;		{

##### &nbsp; 		"success": true,

##### &nbsp; 		"message": "注册成功",

##### &nbsp;		 "user": {

##### &nbsp;  		 "id": 1,

##### &nbsp;  		 "username": "example"

##### &nbsp;		 }

##### &nbsp;		}

##### &nbsp;	登录

##### &nbsp;	URL：/auth/login

##### &nbsp;	Method：POST

##### &nbsp;	Data：

##### &nbsp;		{

##### &nbsp; 		"username": "example",

##### &nbsp;		 "password": "password"

##### &nbsp;		}

##### &nbsp;	Response：

##### &nbsp;		{

##### &nbsp; 		"success": true,

##### &nbsp; 		"message": "登录成功",

##### &nbsp; 		"user": {

##### &nbsp;   		"id": 1,

##### &nbsp;   		"username": "example"

##### &nbsp;		 },

##### &nbsp; 		"token": "example\_token"

##### &nbsp;		}

##### &nbsp;	退出

##### &nbsp;		URL：/auth/logout

##### &nbsp;		Method：POST

##### &nbsp;		Response：

##### &nbsp;		{

##### &nbsp;		 "success": true,

##### &nbsp;		 "message": "退出成功"

##### &nbsp;		}

##### 音乐作品

##### &nbsp;	获取音乐列表

##### &nbsp;	URL：/music

##### &nbsp;	Method：GET

##### &nbsp;	Response：

##### &nbsp;		{

##### &nbsp; 		"success": true,

##### &nbsp; 		"count": 3,

##### &nbsp; 		"music": \[

##### &nbsp;   		{

##### &nbsp;     		"id": 1,

##### &nbsp;    		 "title": "高山流水",

##### &nbsp;     		"artist": "管平湖",

##### &nbsp;    		 "dynasty": "唐",

##### &nbsp;   		  "genre": "guqin",

##### &nbsp;   		  "cover": "image/gsls.jfif",

##### &nbsp;   		  "description": "古琴名曲，伯牙子期知音之曲"

##### &nbsp; 		  }

##### &nbsp;		 ]

##### &nbsp;		}

##### 

