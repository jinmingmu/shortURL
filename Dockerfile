FROM tiangolo/uwsgi-nginx-flask:flask

RUN rm -r /app

RUN git clone https://github.com/jinmingmu/shortURL.git /app 

WORKDIR "/app"

RUN git checkout docker-short

RUN pip install sqlalchemy

RUN export FLASK_APP=main.py && export FLASK_DEBUG=1 && flask run
