# you-hedge-back

This is the back end of the YouHedge app that handles authentication of the client apps,
querying of the Youtube API as well as hosts the privacy policy and the terms of service documents.
The front end can be found at [https://github.com/sopherapps/you-hedge](https://github.com/sopherapps/you-hedge).

## Dependencies

- [Python v3.9+](https://www.python.org/downloads/release/python-390/)
- [Flask v2.0+](https://flask.palletsprojects.com/en/2.1.x/)
- [gevent v21.12+](https://www.gevent.org/)
- [uwsgi v2.0+](https://uwsgi-docs.readthedocs.io/en/latest/)

## Quick Start

- To get to know what kind of requests the API can handler can be found in
  the [API docs](https://documenter.getpostman.com/view/17998957/UzXPwGN8)
- Ensure you have [Python v3.9+](https://www.python.org/downloads/release/python-390/) installed.
- Clone the repo

```shell
git clone git@github.com:sopherapps/you-hedge-back.git
```

- Copy the `example.config.json` file to `config.json` file and update the variables in the `config.json` file.

```shell
cp example.config.json config.json
```

- Create a virtual environment and activate it.

```shell
python3 -m venv env
source env/bin/activate # for unix
```

- Install dependencies

```shell
pip install -r requirements.txt
```

- Start the uwsgi application

```shell
uwsgi --master \
  --workers 4 \
  --gevent 2000 \
  --protocol http \
  --socket 0.0.0.0:8000 \
  --module main:app
```

- Open your browser at [http://localhost:8000](http://localhost:8000)

## In Production

- You can run the app as a systemd service and expose it via an Nginx reverse proxy.
- The service file (e.g. /etc/systemd/system/youhedge.service) can look like:

```
[Unit]
Description=youhedge backend uwsgi daemon
After=network.target

[Service]
User=<your-user>
Group=www-data
WorkingDirectory=/path-to-your-projects-folder/you-hedge-back
ExecStart=/path-to-your-projects-folder/you-hedge-back/env/bin/uwsgi --master \
          --workers 4 \
          --gevent 2000 \
          --protocol uwsgi \
          --socket 127.0.0.1:8000 \
          --module main:app

[Install]
WantedBy=multi-user.target
```

- Be sure to add the following config in the Nginx server config (e.g. /etc/nginx/sites-available/youhedge_api) for this app.

```
server {
    server_name your-domain; # e.g. server_name example.com

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
       alias /path-to-your-projects-folder/you-hedge-back/services/website/static/;
    }

    location / {
       include uwsgi_params;
       uwsgi_pass uwsgi://127.0.0.1:8000;
       # these increased timeouts are for the sake of long-polling for google authentication status
       uwsgi_read_timeout 300s;
       proxy_read_timeout 300s;
       proxy_connect_timeout 300s;
       proxy_send_timeout 300s;
    }
}
```

## Running tests

- Ensure you have [Python v3.9+](https://www.python.org/downloads/release/python-390/) installed.
- Clone the repo

```shell
git clone git@github.com:sopherapps/you-hedge-back.git
```

- Copy the `example.config.json` file to `config.json` file and update the variables in the `config.json` file.

```shell
cp example.config.json config.json
```

- Create a virtual environment and activate it.

```shell
python3 -m venv env
source env/bin/activate # for unix
```

- Install dependencies

```shell
pip install -r requirements.txt
```

- Install dependencies

```shell
pip install -r requirements.txt
```

- Run the test command

```shell
python -m unittest
```

## Design

### Constraints

- Flask must be used.
- Flask however is a synchronous framework.
- Youtube API has daily quotas of around 10000

### Design Decisions

- There will be a cache for all requests except authentication requests
- Since this is basically a proxy, we need to be able to handle multiple requests concurrently.
  That means we will need to use uwsgi, gevent, and flask.

## License

Copyright (c) 2022 [Martin Ahindura](https://github.com/tinitto). Licensed under the [MIT License](./LICENSE)
