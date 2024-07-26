# paopao 匹配系统
## 项目介绍
一个快速帮助用户找到娱乐伙伴的移动端H5网站（APP风格）。
包含用户注册-登录-退出、更新个人信息、按标签搜索用户、组建房间、进入房间、发布任务计划、推荐相似用户等功能。
前端使用VUE框架实现，后端使用 python-flask 实现的restfull风格。
## 项目技术
### 前端
vue3 + vant4 + element plus + vue-router + pinia + vite + axios + vue-virtual-scrolling + vue-infinite-scroll
### 后端
python3 + flask + flask-restx + SQLAlchemy + APScheduler + Flask-Session + MySQL + redis
## 体验网页
[泡泡活动匹配系统](http://110.41.66.229:5173/user/login)
## 如何使用
- git clone https://github.com/miyagipipi/paopao.git
- 命令行执行 npm install 安装前端相关的 node_modules
- 在 ./backend 目录下找到 requirements.txt 文件，执行 pip install -r requirements.txt 安装 python 相关的依赖包（建议使用虚拟环境安装）。
