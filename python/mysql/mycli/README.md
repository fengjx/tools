# mycli辅助工具

### 用途

更方便的通过ssh tunnel远程服务器端口转发来使用MySQL命令行客户端mycli连接远程MySQL。

mycli的详细使用方法可以查看官网说明 <https://www.mycli.net/>

### 网络拓扑

![mycli-helper-network](mycli-helper.png)

通常我们无法连接线上生产环境数据库，需要一台服务器作为中转，我们可以登录这台中转服务器，通过中转服务器访问MySQL

### 环境依赖

- [python3](https://www.python.org/)
- [mycli](https://www.mycli.net/)
- [sshtunnel](https://github.com/pahaz/sshtunnel)

安装依赖

mycli <https://www.mycli.net/install>
```bash
pip install mycli 
```

sshtunnel <https://github.com/pahaz/sshtunnel>
```bash
pip install sshtunnel
```

ps: 推荐你使用[pyenv](https://github.com/pyenv/pyenv)或者其他python依赖管理工具来管理你的依赖


### 配置文件

```ini mycli.ini
[user-mysql]
desc=用户数据库
remote_host=192.168.1.106
remote_port=22
remote_username=fengjx
remote_password=
remote_pkey=~/.ssh/id_rsa
remote_pkey_password=

mysql_host=192.168.1.106
mysql_port=3306
mysql_user=root
mysql_password=1234
```

remote 是ssh登录代理端口转发的服务器配置，remote_password和remote_pkey、remote_pkey_password两个可以按实际情况选择使用密码登录还是秘钥登录。

mysql 是远程MySQL登录配置

### 使用方法

只有一个可选参数，`-c` 指定配置文件路径，如果没有指定则会使用当前目录下的mycli.ini配置文件。
```bash
python mycli-helper.py -h
usage: mycli helper [-h] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        配置文件，默认当前目录下的 mycli.ini
```

### 示例

```bash
python mycli-helper.py -c mycli.ini
加载配置： mycli.ini
情输入连接的MySQL实例编号
[0] - user-mysql, 用户数据库
[1] - order-mysql, 订单数据库
1
connect to order-mysql, bind local port 64069
mycli mysql://root:1234@localhost:64069
mysql 5.7.28
mycli 1.20.1
Chat: https://gitter.im/dbcli/mycli
Mail: https://groups.google.com/forum/#!forum/mycli-users
Home: http://mycli.net
Thanks to the contributor - Frederic Aoustin
mysql root@localhost:(none)>
mysql root@localhost:(none)> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mydb               |
| mysql              |
| performance_schema |
| sys                |
| test               |
+--------------------+
6 rows in set
Time: 0.026s
mysql root@localhost:(none)> use mydb;
You are now connected to database "mydb" as user "root"
Time: 0.004s
mysql root@localhost:mydb> show tables;
+----------------+
| Tables_in_mydb |
+----------------+
| t1             |
+----------------+
1 row in set
Time: 0.050s
mysql root@localhost:mydb>
mysql root@localhost:mydb> insert into t1(id, c) values (1, 1024);
Query OK, 1 row affected
Time: 0.013s
mysql root@localhost:mydb> select * from t1;
+----+------+
| id | c    |
+----+------+
| 1  | 1024 |
+----+------+
1 row in set
Time: 0.033s
```









