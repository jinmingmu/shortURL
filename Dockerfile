FROM tiangolo/uwsgi-nginx-flask:flask

RUN rm -r /app
RUN git clone https://github.com/jinmingmu/shortURL.git /app 

WORKDIR "/app"

RUN git checkout docker-short \

	&& pip install sqlalchemy \

	&& python -c 'import database.database;database.database.init_db()' \
	
	&& apt-get install mysql-server \
	
	&& pip install mysql
