from flask import Flask
from ..app import app  # Importa seu app principal

def handler(request):
    with app.app_context():
        response = app.full_dispatch_request()()
        return response