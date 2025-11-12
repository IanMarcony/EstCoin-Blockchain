# Script para iniciar o frontend React no Windows
# Execute com: .\start.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Iniciando Frontend EstCoin" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Define variavel de ambiente para compatibilidade com Node.js 17+
$env:NODE_OPTIONS = "--openssl-legacy-provider"

Write-Host "[INFO] Iniciando servidor de desenvolvimento..." -ForegroundColor Cyan
Write-Host "Aguarde a compilacao..." -ForegroundColor Yellow
Write-Host ""

# Verifica se node_modules existe
if (-not (Test-Path "node_modules")) {
    Write-Host "[AVISO] Instalando dependencias..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha ao instalar dependencias" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Servidor estara disponivel em: http://localhost:3000" -ForegroundColor Green
Write-Host "Pressione Ctrl+C para parar" -ForegroundColor Yellow
Write-Host ""

# Inicia o servidor React
npm start
