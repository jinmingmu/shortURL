FROM tiangolo/uwsgi-nginx-flask:flask

RUN rm -r /app
RUN git clone https://github.com/jinmingmu/shortURL.git /app 

WORKDIR "/app"

RUN git checkout working \
    && mv flaskr/* . \
    && mv flaskr.py main.py \
	&& pip install -r requirements.txt
