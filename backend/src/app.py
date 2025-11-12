from flask import Flask
from flask_cors import CORS
from src.routes.auth import auth_bp
from src.routes.transactions import transactions_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(transactions_bp, url_prefix='/api/transactions')

@app.route('/')
def home():
    return "Welcome to the Ethereum Blockchain App API!"

if __name__ == '__main__':
    app.run(debug=True)