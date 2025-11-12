# 🚀 Como Iniciar o Servidor Backend

Este guia mostra as diferentes formas de iniciar o servidor Flask do projeto EstCoin.

---

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **Dependências instaladas**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎯 Métodos de Inicialização

### **1️⃣ Modo Produção (Recomendado)** ✅

**Windows (PowerShell):**
```powershell
.\start.ps1
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```


---

### **2️⃣ Modo Desenvolvimento** 🔧

**Windows (PowerShell):**
```powershell
.\start-dev.ps1
```

**Linux/Mac:**
```bash
export FLASK_APP=src.app
export FLASK_ENV=development
export FLASK_DEBUG=1
python -m flask run --host=0.0.0.0 --port=5000 --reload
```
---

## 🌐 Endpoints Disponíveis

Após iniciar o servidor, você pode acessar:

- **API Base**: http://localhost:5000/
- **Autenticação**: http://localhost:5000/auth/
- **Transações**: http://localhost:5000/transactions/

---

## 📝 Exemplos de Uso

### Desenvolvimento Ativo (com auto-reload)
```powershell
# Edite seus arquivos e veja as mudanças instantaneamente
.\start-dev.ps1
```

### Demonstração
```powershell
# Servidor estável para apresentações
.\start.ps1
```
---

## 📚 Documentação Adicional

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Waitress Documentation](https://docs.pylonsproject.org/projects/waitress/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

**Desenvolvido para o projeto EstCoin Blockchain** 🔗
