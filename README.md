# you-hedge-back

This is the back end of the YouHedge app that handles authentication of the client apps,
querying of the Youtube API as well as hosts the privacy policy and the terms of service documents.

## Dependencies

- [Python v3.9+](https://www.python.org/downloads/release/python-390/)
- [Flask v2.0+](https://flask.palletsprojects.com/en/2.1.x/)
- [gevent v21.12+](https://www.gevent.org/)
- [uwsgi v2.0+](https://uwsgi-docs.readthedocs.io/en/latest/)

## Quick Start

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

- Start the application

```shell
python main.py
```

- Open your browser at [http://localhost:8000](http://localhost:8000)

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

- Flask must be used. (This is part of an assessment)
- Flask however is a synchronous framework.
- Youtube API has daily quotas of around 10000

### Design Decisions

- There will be a cache for all requests except authentication requests
- Since this is basically a proxy, we need to be able to handle multiple requests concurrently.
  That means we will need to use uwsgi, gevent, and flask.

## License

Copyright (c) 2022 [Martin Ahindura](https://github.com/tinitto). Licensed under the [MIT License](./LICENSE)
