# 漂流图书：Django后端

### 运行环境

​	Ubuntu 18.04 LTS

​	Python 3.6.9

​	pip 9.0.1

​	Django 2.2.7

​	MySQL 5.7.28

### 运行

```bash
# DriftingBook/DriftingBook/register.py 填入<accessKeyId>和<accessSecret>
# DriftingBook/DriftingBook/settings.py 填写正确的DATABASES
# 完成数据库的建立
sudo python3 manage.py runserver 0.0.0.0:8000
```

### 文件结构

```bash
DriftingBook/BookModel	——	存储书目的数据库模型
DriftingBook/BottleModel	——	存储漂流瓶的数据库模型
DriftingBook/UserModel	——	存储用户信息的数据库模型

DriftingBook/book_handler.py	——	对数据库中书目相关操作进行封装
DriftingBook/bottle_handler.py	——	对数据库中漂流瓶相关操作进行封装
DriftingBook/user_handler.py	——	对数据库中用户相关操作进行封装
DriftingBook/ust_handler.py	——	负责用户唯一对应的star表的增删改查

DriftingBook/漂流图书.doc	——	数据库封装的相关接口函数

DriftingBook/DriftingBook/register.py	——	用户注册相关接口
```

### 建立数据库

```bash
# 首先要安装好mysql环境
sudo apt-get install mysql-server
sudo apt-get install mysql-client
sudo apt-get install libmysqlclient-dev

# 创建表结构，部署时仅需如下一句
python3 manage.py migrate

# 让 Django 知道我们在我们的模型有一些变更
python3 manage.py makemigrations TestModel
# 创建表结构
python3 manage.py migrate TestModel
```

### 注意问题

##### 	跨域问题：Forbidden (CSRF cookie not set.): /addUser/

```bash
pip3 install django-cors-headers
```

```bash
# DriftingBook/DriftingBook/settings.py：在INSTALLED_APPS里添加“corsheaders”
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

# DriftingBook/DriftingBook/settings.py：在MIDDLEWARE_CLASSES添加 ‘corsheaders.middleware.CorsMiddleware’, ‘django.middleware.common.CommonMiddleware’
MIDDLEWARE_CLASSES = (
    ...
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
)

# DriftingBook/DriftingBook/settings.py：在底部添加 
#  新增以下配置  #
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# Origin '*' in CORS_ORIGIN_WHITELIST is missing scheme 出现该错误则将其注释掉
# CORS_ORIGIN_WHITELIST = (
#   "*"
# )
CORS_ALLOW_METHODS = (
  'DELETE',
  'GET',
  'OPTIONS',
  'PATCH',
  'POST',
  'PUT',
  'VIEW',
)
CORS_ALLOW_HEADERS = (
  'XMLHttpRequest',
  'X_FILENAME',
  'accept-encoding',
  'authorization',
  'content-type',
  'dnt',
  'origin',
  'user-agent',
  'x-csrftoken',
  'x-requested-with',
  'Pragma',
)
```

##### 	其他问题

```bash
# ModuleNotFoundError: No module named 'mysql'
pip3 install mysql-connector
# or
python3 -m pip install mysql-connector

# import mysql.connector测试失败
# 如果你的 MySQL 是 8.0 版本，密码插件验证方式发生了变化，早期版本为 mysql_native_password，8.0 版本为 caching_sha2_password，所以需要做些改变：
# 登录mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourPassword';
FLUSH PRIVILEGES;

# ModuleNotFoundError: No module named 'MySQLdb'
pip3 install mysqlclient
pip3 install pymysql

# mysql.connector.errors.ProgrammingError: 1698 (28000): Access denied for user 'root'@'localhost'
SELECT user,authentication_string,plugin,host FROM mysql.user;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password>';
FLUSH PRIVILEGES;
SELECT user,authentication_string,plugin,host FROM mysql.user;

# django.db.utils.IntegrityError: (1048, "Column 'booid' cannot be null")
# 增加auto_increment 属性
alter table <tablename> modify <columnname> <type> auto_increment;
# 给自增值设置初始值
alter table <tablename> auto_increment = <value>; 

# django.db.utils.OperationalError: (1366, "Incorrect string value: '\\xE5\\xA5\\xBD\\xE7\\xAC\\x91...' for column 'bookname' at row 1")
alter table `tablename` convert to character set utf8;

# 安装阿里云短信服务所需要的包
pip3 install aliyun-python-sdk-core

# TypeError: the JSON object must be str, not 'bytes'
# python3.5 无法反序列化bytes数据必须decode成str才可以
# python3.6 无论bytes类型或者str类型都可以反序列化
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
# 调整Python3的优先级，使得3.6优先级较高
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2

# python3.6 下 pip install mysqlclient 报错
sudo apt-get install python3.6-dev libmysqlclient-dev
```

