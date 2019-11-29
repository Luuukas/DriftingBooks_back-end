# 漂流图书：Django后端

### 运行环境

​	Ubuntu 18.04 LTS

​	Python 3.6.9

​	pip 9.0.1

​	Django 2.2.7

​	MySQL 5.7.28

### 运行

```bash
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
python -m pip install mysql-connector

# ModuleNotFoundError: No module named 'MySQLdb'
pip3 install mysqlclient
pip3 install pymysql

# mysql.connector.errors.ProgrammingError: 1698 (28000): Access denied for user 'root'@'localhost'
SELECT user,authentication_string,plugin,host FROM mysql.user;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<password>';
FLUSH PRIVILEGES;
SELECT user,authentication_string,plugin,host FROM mysql.user;

```

