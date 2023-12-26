# 代码盒子 CodeBox



## 项目介绍

代码盒子是一个允许用户分享自己的 vue 代码片段的一个网站.

在代码盒子中, 用户可以将自己写好的包含各种效果的代码分享到网站中, 其他用户可以自由在线运行这些代码查看效果, 也可以复制这些代码为自己所用.

本项目意为用户可以分享自己的代码, 这样当别的程序员也需要实现同样的效果代码的时候, 就只需要将别人的代码拿过来直接使用即可.

项目类似于前端知名网站 codepen.io, 本网站正是模仿自该网站. 在此对该网站表示感谢.
但和 codepen.io 不一样的是, 本网站中的代码片段更注重于让广大程序员分享自己在日常实现功能时所需实现的各种代码, 而不是把更多精力放在实现各种样式效果上.

本项目只是本人在找工作时制作的一个演示性的网站, 只是用于展示自己的能力, 由于本人还只是前端初学者, 故而代码写的不会那么好, 还请各位多提意见. 如果我写的代码对你有帮助的话, 那这真的是我的荣幸了.

本项目开源 基于 MIT 协议.



## 项目使用的技术

前端使用 Vue3 全家桶(Vue3 + Vuex + VueRouter) 以及 TypeScript.
后端使用 Python 的 FastAPI 框架, 使用 MySQL 做数据库, 使用 Redis 做缓存, 使用 Docker 部署.



## 文件夹结构

- 根目录
  - client  前端页面代码
    - codebox_front  前台页面代码
      - notice.txt  一些注意事项 需要按其中记录的内容修改部分源码
      - ...
  - server  服务端代码
    - .assets  存储静态文件 用户创建的项目 用户上传的文件 服务端所使用的静态文件均存储于此
    - .mysqlData  存储 mysql 容器的数据
    - nginx  存储 nginx 容器的数据
    - depends  依赖注入代码
    - middlewares  中间件代码
    - models  数据库模型代码
    - schemas  响应模型代码
    - utils  工具代码
    - views  视图和路由的代码
    - API.md  后端 API 文档
    - 表.md  后端表设计文档
    - server.py  服务器入口文件
    - constants.py  服务端常量
    - genTortoiseSchemas.py  迁移数据库的代码
    - dockercmds.txt  构建容器所需执行的 docker 命令 可直接 ctrl+c/v 使用
    - require.txt  依赖记录文件
- README.md



## 运行项目

首先安装 docker 和 nodejs 环境

克隆项目后来到 server 文件夹下 执行如下命令以建立容器:

```shell
# 新建桥接网络
docker network create servernet

# 建立 mysql 容器
docker container run -it -d --name mysql --network servernet -v ${pwd}/.mysqlData/log:/var/log/mysql -v ${pwd}/.mysqlData/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=你的数据库密码 mysql:5.7

# 建立 redis 容器
docker container run --name redis -it -d --network servernet redis:7.2.3 --requirepass 你的redis密码

# 建立 python 容器
docker container run -it -d --network servernet -v ${pwd}:/serverCodes --name python python:3.11.7-alpine

# 建立 nginx 容器
docker run -p 80:80 --name nginx -v ${pwd}/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v ${pwd}/nginx/conf/conf.d:/etc/nginx/conf.d -v ${pwd}/nginx/log:/var/log/nginx -v ${pwd}/nginx/html:/usr/share/nginx/html -v ${pwd}/.assets:/assets -it -d --network servernet nginx

```

执行如下命令 进入到 python 容器中:

```shell
docker exec -it python bash
```

cd 到项目目录:

```shell
cd /serverCodes
```

安装依赖:

```shell
pip install -r require.txt
```

而后参考此链接来修改部分依赖的代码: https://blog.csdn.net/ViniJack/article/details/131809573

而后启动服务:

```shell
python ./server.py
```

这样后端服务就启动了 后端服务会占用 localhost 的 80 端口



而后启动前端项目 在安装好 nodejs 后 来到 client/codebox_front 文件夹下 执行:

```shell
yarn install
```

安装好项目依赖后 执行:

```shell
yarn serve
```

即可启动前端服务













