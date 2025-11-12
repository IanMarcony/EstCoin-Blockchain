#!/bin/bash

# Script para iniciar o servidor backend no Linux/Mac
# Execute com: ./start.sh

echo "=================================="
echo "  Iniciando Backend EstCoin"
echo "=================================="
echo ""

# Verifica se Python esta instalado
echo "Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "[OK] $PYTHON_VERSION"
else
    echo "[ERRO] Python nao encontrado!"
    exit 1
fi

# Verifica se as dependencias estao instaladas
echo "Verificando dependencias..."
if pip3 list | grep -q "Flask" && pip3 list | grep -q "gunicorn"; then
    echo "[OK] Dependencias instaladas"
else
    echo "[AVISO] Instalando dependencias..."
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "[OK] Dependencias instaladas com sucesso"
    else
        echo "[ERRO] Falha ao instalar dependencias"
        exit 1
    fi
fi

echo ""
echo "=================================="
echo "  Iniciando Servidor"
echo "=================================="
echo ""
echo "Servidor rodando em: http://localhost:5000"
echo "Pressione Ctrl+C para parar"
echo ""

# Inicia o servidor com Gunicorn (funciona melhor no Linux/Mac)
gunicorn --bind 0.0.0.0:5000 --workers 4 --reload wsgi:app
