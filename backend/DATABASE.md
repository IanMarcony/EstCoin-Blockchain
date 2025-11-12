# 💾 Banco de Dados SQLite - EstCoin

## 📍 Localização do Banco

O arquivo do banco de dados será criado em:
```
backend/users.db
```

## 🚀 Inicialização Automática

O banco é criado automaticamente quando você inicia o servidor:

```powershell
.\start-dev.ps1
```

Você verá a mensagem:
```
🔄 Inicializando banco de dados...
✅ Banco de dados criado em: E:\...\backend\users.db
```

---

## 🛠️ Gerenciamento Manual do Banco

### **Criar o banco**
```bash
python db_manager.py create
```

### **Listar usuários**
```bash
python db_manager.py list
```

Saída:
```
📋 Total de usuários: 2

--------------------------------------------------------------------------------
ID: 1
Username: ian
Ethereum Address: 0x1234567890abcdef...
Balance: 10.0 EST
--------------------------------------------------------------------------------
ID: 2
Username: maria
Ethereum Address: 0xabcdef1234567890...
Balance: 10.0 EST
--------------------------------------------------------------------------------
```

### **Resetar banco (deleta tudo e recria vazio)**
```bash
python db_manager.py reset
```

### **Deletar banco**
```bash
python db_manager.py delete
```

---

## 📊 Estrutura da Tabela `users`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | INTEGER | ID único (auto-incremento) |
| `username` | VARCHAR(50) | Nome de usuário (único) |
| `password_hash` | VARCHAR(255) | Senha com bcrypt hash |
| `ethereum_address` | VARCHAR(42) | Endereço da carteira (único) |
| `private_key` | VARCHAR(66) | Chave privada (criptografada) |
| `balance` | FLOAT | Saldo em tokens EST |

---

## 🔍 Como Verificar se Está Funcionando

### 1. **Registre um usuário**
```bash
POST http://localhost:5000/api/auth/register
{
  "username": "teste",
  "password": "senha123"
}
```

### 2. **Liste os usuários**
```bash
python db_manager.py list
```
---

## 🔄 Backup do Banco

Para fazer backup:
```bash
# Windows
copy backend\users.db backup\users_backup.db

# Linux/Mac
cp backend/users.db backup/users_backup.db
```

Para restaurar:
```bash
# Windows
copy backup\users_backup.db backend\users.db

# Linux/Mac
cp backup/users_backup.db backend/users.db
```

---

**Agora seus dados estão sendo salvos permanentemente no SQLite!** 🎉
