# 🔐 Documentação do Módulo de Autenticação

## Funções Implementadas em `auth_utils.py`

### 1. **`generate_token(user_id, username, ethereum_address)`**

Gera um token JWT (JSON Web Token) para autenticação do usuário.

**Parâmetros:**
- `user_id` (int): ID do usuário no banco de dados
- `username` (str): Nome de usuário
- `ethereum_address` (str): Endereço da carteira Ethereum

**Retorno:** Token JWT (string)

**Exemplo de uso:**
```python
token = generate_token(1, "joao_silva", "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
# Retorna: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### 2. **`verify_token(token)`**

Verifica se um token JWT é válido e não está expirado.

**Parâmetros:**
- `token` (str): Token JWT a ser verificado

**Retorno:** 
- `dict`: Payload do token se válido
- `None`: Se inválido ou expirado

**Exemplo de uso:**
```python
payload = verify_token(token)
if payload:
    user_id = payload['user_id']
    username = payload['username']
else:
    print("Token inválido!")
```

---

### 3. **`hash_password(password)`**

Cria um hash seguro da senha usando bcrypt.

**Parâmetros:**
- `password` (str): Senha em texto plano

**Retorno:** Hash da senha (string)

**Exemplo de uso:**
```python
hashed = hash_password("minhaSenha123")
# Retorna: "$2b$12$KIXx8Z9p..."
```

**🔒 Segurança:**
- Usa bcrypt com 12 rounds (recomendado)
- Gera um salt único para cada senha
- Proteção contra rainbow tables

---

### 4. **`check_password(hashed_password, password)`**

Verifica se uma senha corresponde ao hash armazenado.

**Parâmetros:**
- `hashed_password` (str): Hash armazenado no banco
- `password` (str): Senha fornecida pelo usuário

**Retorno:** `bool` (True se corresponde, False se não)

**Exemplo de uso:**
```python
is_valid = check_password(user.password, "minhaSenha123")
if is_valid:
    print("Login bem-sucedido!")
```

---

### 5. **`@token_required` (Decorator)**

Decorator para proteger rotas que requerem autenticação.

**Exemplo de uso:**
```python
from utils.auth_utils import token_required

@app.route('/api/user/profile')
@token_required
def get_profile(current_user):
    return jsonify({
        'user_id': current_user['user_id'],
        'username': current_user['username'],
        'ethereum_address': current_user['ethereum_address']
    })
```

**Como funciona:**
1. Extrai o token do header `Authorization: Bearer <token>`
2. Verifica se o token é válido
3. Passa os dados do usuário para a função
4. Retorna erro 401 se o token for inválido

---

### 6. **`extract_token_from_request()`**

Extrai o token JWT do header da requisição HTTP.

**Retorno:** Token (string) ou None

**Exemplo de uso:**
```python
token = extract_token_from_request()
if token:
    user_data = verify_token(token)
```

---

### 7. **`validate_password_strength(password)`**

Valida se a senha atende aos requisitos de segurança.

**Regras:**
- Mínimo 6 caracteres
- Máximo 128 caracteres
- Pelo menos uma letra
- Pelo menos um número

**Retorno:** `(bool, str)` - (é válida, mensagem)

**Exemplo de uso:**
```python
is_valid, message = validate_password_strength("senha123")
if is_valid:
    # Pode criar o usuário
else:
    return jsonify({'error': message}), 400
```

---

## 🔑 Configuração

### Variável de Ambiente

Para maior segurança, defina a chave secreta JWT como variável de ambiente:

**Windows PowerShell:**
```powershell
$env:SECRET_KEY = "sua-chave-super-secreta-aqui"
```

**Linux/Mac:**
```bash
export SECRET_KEY="sua-chave-super-secreta-aqui"
```

---

## 📦 Dependências Necessárias

```
PyJWT==2.8.0
bcrypt==4.1.1
Flask==2.1.1
```

Instalar com:
```bash
pip install -r requirements.txt
```

---

## 🛡️ Segurança

### Token JWT
- **Expiração:** 24 horas por padrão
- **Algoritmo:** HS256 (HMAC SHA-256)
- **Payload inclui:** user_id, username, ethereum_address, exp, iat

### Senhas
- **Hashing:** bcrypt com 12 rounds
- **Salt:** Gerado automaticamente
- **Proteção:** Contra ataques de força bruta e rainbow tables

---

## 📝 Exemplo Completo: Rota de Login

```python
from flask import Flask, request, jsonify
from utils.auth_utils import check_password, generate_token
from models.user import User

app = Flask(__name__)

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Busca usuário no banco
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    # Verifica senha
    if not check_password(user.password, password):
        return jsonify({'error': 'Senha incorreta'}), 401
    
    # Gera token
    token = generate_token(user.id, user.username, user.ethereum_address)
    
    return jsonify({
        'message': 'Login bem-sucedido',
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'ethereum_address': user.ethereum_address
        }
    }), 200
```

---

## 🧪 Testando

```python
# Teste de hash de senha
password = "minhasenha123"
hashed = hash_password(password)
print(f"Hash: {hashed}")
print(f"Válida: {check_password(hashed, password)}")

# Teste de token
token = generate_token(1, "teste", "0x123...")
payload = verify_token(token)
print(f"Payload: {payload}")
```

---

## 🚨 Tratamento de Erros

Todas as funções incluem tratamento de exceções:

- **Token expirado:** Retorna `None`
- **Token inválido:** Retorna `None`
- **Erro no hash:** Captura exceção e retorna `False`
- **Erro na geração:** Lança exceção com mensagem descritiva
