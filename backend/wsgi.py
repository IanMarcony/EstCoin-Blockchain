"""
WSGI Entry Point para o servidor Flask
Este arquivo e usado pelo Gunicorn/Waitress para iniciar a aplicacao
"""
from src.app import app

if __name__ == "__main__":
    app.run()
