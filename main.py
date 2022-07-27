"""Entry point for the server"""
from gevent import monkey
monkey.patch_all()

from services import create_app

app = create_app()
