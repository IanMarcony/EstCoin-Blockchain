# Script para iniciar o servidor backend em modo desenvolvimento (com auto-reload)
# Execute com: .\start-dev.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Backend EstCoin - Modo DEV" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Define variaveis de ambiente para desenvolvimento
$env:FLASK_APP = "src.app:app"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
$env:PYTHONPATH = "$PWD"

Write-Host "[INFO] Modo: Desenvolvimento (auto-reload ativado)" -ForegroundColor Cyan
Write-Host "Servidor rodando em: http://localhost:5000" -ForegroundColor Green
Write-Host "Pressione Ctrl+C para parar" -ForegroundColor Yellow
Write-Host ""

# Inicia o servidor Flask em modo desenvolvimento
python -m flask run --host=0.0.0.0 --port=5000 --reload
