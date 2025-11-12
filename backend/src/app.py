from flask import Flask
from flask_cors import CORS
from src.routes.auth import auth_bp
from src.routes.transactions import transactions_bp
from src.models.user import init_db

app = Flask(__name__)
CORS(app)

# Inicializa o banco de dados
print("🔄 Inicializando banco de dados...")
init_db()

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(transactions_bp, url_prefix='/api/transactions')

@app.route('/')
def home():
    return {
        "message": "Welcome to the EstCoin Blockchain API!",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth",
            "transactions": "/api/transactions"
        }
    }

if __name__ == '__main__':
    app.run(debug=True)