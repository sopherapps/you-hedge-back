FROM python:3.9.13-alpine3.16

COPY . /y_app

WORKDIR /y_app

RUN pip install -r requirements

CMD uwsgi --master \
  --workers 4 \
  --gevent 2000 \
  --protocol http \
  --socket 0.0.0.0:8000 \
  --module main:app
# uwsgi protocol is used with an nginx reverse proxy

EXPOSE 8000
STOPSIGNAL SIGQUIT