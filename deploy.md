I used two docker to deploy this app. The first image will be the one we create, let's call it shortULR.
The second one will be called mysql.

steps(I assume you already installed docker):

go to my git directory

command: docker build -t short .

command: docker run --name mysqlcontainer -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=foo -d mysql 

command: docker run --name mycontainer -p 80:80 --link mysqlcontainer:mysql -d short 

command: docker exec mycontainer python -c 'import database.database;database.database.init_db()'
