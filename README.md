
#Flask-Disk

## 简介
使用Flask开发的一个简单云盘系统，存储使用了Hadoop分布式文件系统，数据库使用到了ORM框架SQLAlchemy。
功能：
用户管理：注册、登录、资料编辑和修改密码
文件管理：文件上传下载、文件公开分享和密码分享、删除文件、恢复文件和重命名文件
管理员后台：查看用户个人信息、锁定普通用户、修改用户密码

## 安装使用
### Hadoop安装配置
首先需要安装Hadoop环境，参考http://www.powerxing.com/install-hadoop/
启用Hadoop回收站，修改conf/core-site.xml,增加以下内容
```
<property> 
<name>fs.trash.interval</name> 
<value>10080</value> 
</property>
```
其中10080为分钟，即7天。
[Python hdfs模块使用](http://seeicb.com/2017/02/21/python-hdfs%E6%A8%A1%E5%9D%97%E4%BD%BF%E7%94%A8/)

### 依赖安装

```
pip3 install virtualenv
virtualenv --no-site-packages venv
source venv/bin/activate
git clone git@github.com:seeicb/Flask-Disk.git
pip install -r requirements.txt
```

### 修改配置
配置文件config.py，其中

```
	# 最大上传限制，默认1024M
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024
	# Cookie 过期时间
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
	# HDFS回收站文件路径
    HDFS_TRASH = '/user/username/.Trash/Current/'
	# HDFS namenode
    HDFS_IP = "http://127.0.0.1:50070"
    # 网站地址，也可以是域名
    BASE_HOST='http://127.0.0.1:5000/'
```



### 数据库配置
```
python manage.py db init
python manage.py db migrate -m "init"
python manage.py db upgrade 
python manage.py deploy
```

## 启动
`python manage.py runserver`

打开：http://127.0.0.1:5000/

默认用户名admin，密码 password


