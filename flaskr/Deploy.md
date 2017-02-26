#部署

##部署说明
因为想尝试一下用docker去简单部署一个服务器，我采用了两个docker容器通信的方法去部署我们的短连接服务。  
首先我们要从一个集成了uwsgi和nginx的docker镜像中加入我们的服务，然后我们再去创建mysql容器，然后把含有我们服务的容器在创建的时候跟mysql容器连接起来。

##部署步骤

* 先安装docker到本机，具体流程可参见 https://docs.docker.com/engine/installation/

* 先下载本github repo到本机

* 转换branch至docker-short

* 输入命令<pre> docker build -t short . </pre> (请注意不要忘记这个‘.’)

* 输入命令<pre> docker run --name mysqlcontainer -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=foo -d mysql
 </pre>

* 输入命令<pre> docker run --name mycontainer -p 80:80 --link mysqlcontainer:mysql -d short </pre>

* 输入命令<pre> docker exec mycontainer python -c 'import database.database;database.database.init_db()' </pre>(这条命令如果输入的太快可能会遇到mysql server没有完全启动导致失败，请再次输入 如果还是失败的话 有可能是ip配置的问题)


##命令说明

* 命令<pre> docker build -t short . </pre> 意思是按照本地的Dockerfile创建一个名字叫short的docker 镜像 如果本地没有响应的镜像，docker会从服务器下载

* 命令<pre> docker run --name mysqlcontainer -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=foo -d mysql
 </pre> 意思是创建mysql的容器，如果本地没有将会从服务器下载，将容器命名为mysqlcontainer 创建用户root的密码为admin 创建一个叫foo的表格

* 命令<pre> docker run --name mycontainer -p 80:80 --link mysqlcontainer:mysql -d short </pre> 意思是把刚才的short镜像创建为mycontainer的容器 开放端口80 并连接上刚才的mysql容器

* 命令<pre> docker exec mycontainer python -c 'import database.database;database.database.init_db()' </pre>意思是运行在mycontainer内部启动初始化数据库的命令，这个数据库命令在名字为foo的数据库内创建了一张空的URLTable表格

##问题说明
### ip配置的问题
* 如果无法初始化表格，遇到ip error那么说明mysqlcontainer容器的ip不是我这里的默认ip或端口：172.17.0.2:3306 
我们需要用<pre>docker inspect --format '{{ .NetworkSettings.IPAddress }}' mysqlcontainer</pre>去查看mysqlcontainer的ip，然后修改database/database.py 里面的代码去连接mysql
这个问题未来需要改变为动态取得ip
