I used two docker to deploy this app. The first image will be the one we create, let's call it shortULR.
The second one will be called mysql.

steps(I assume you already installed docker):

go to my git directory

command: docker build -t short .

command: docker run --name mysqlcontainer -e MYSQL_ROOT_PASSWORD=admin -d mysql

command: docker exec -it mysqlcontainer bash

command: mysql -u root -e "create database foo" -p

enter: admin

command: docker run --name mycontainer -p 80:80 --link mysqlcontainer:mysql -d short 

command: docker exec -it mycontainer bash

command: python -c 'import database.database;database.database.init_db()'

command: exit








