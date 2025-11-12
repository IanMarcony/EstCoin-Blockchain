# Script para iniciar o servidor backend no Windows
# Execute com: .\start.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Iniciando Backend EstCoin" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se Python esta instalado
Write-Host "Verificando Python..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "[ERRO] Python nao encontrado!" -ForegroundColor Red
    exit 1
}

# Verifica se as dependencias estao instaladas
Write-Host "Verificando dependencias..." -ForegroundColor Yellow
$pipList = pip list 2>$null
if ($pipList -match "Flask" -and $pipList -match "waitress") {
    Write-Host "[OK] Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "[AVISO] Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Dependencias instaladas com sucesso" -ForegroundColor Green
    } else {
        Write-Host "[ERRO] Falha ao instalar dependencias" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Iniciando Servidor" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Servidor rodando em: http://localhost:5000" -ForegroundColor Green
Write-Host "Pressione Ctrl+C para parar" -ForegroundColor Yellow
Write-Host ""

# Inicia o servidor com Waitress (funciona melhor no Windows)
python -m waitress --host=0.0.0.0 --port=5000 wsgi:app
