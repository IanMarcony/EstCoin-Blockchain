# Script de configuracao da blockchain local no Windows
# Execute com: .\setup.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Setup Blockchain EstCoin" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se Node.js esta instalado
Write-Host "Verificando Node.js..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "[OK] Node.js instalado: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "[ERRO] Node.js nao encontrado!" -ForegroundColor Red
    Write-Host "Por favor, instale o Node.js de https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Verifica se npm esta instalado
Write-Host "Verificando npm..." -ForegroundColor Yellow
if (Get-Command npm -ErrorAction SilentlyContinue) {
    $npmVersion = npm --version
    Write-Host "[OK] npm instalado: $npmVersion" -ForegroundColor Green
} else {
    Write-Host "[ERRO] npm nao encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Instalando Dependencias" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Instala Truffle globalmente
Write-Host "Instalando Truffle..." -ForegroundColor Yellow
npm install -g truffle
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Truffle instalado com sucesso" -ForegroundColor Green
} else {
    Write-Host "[ERRO] Erro ao instalar Truffle" -ForegroundColor Red
}

# Instala Ganache CLI globalmente
Write-Host "Instalando Ganache CLI..." -ForegroundColor Yellow
npm install -g ganache-cli
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Ganache CLI instalado com sucesso" -ForegroundColor Green
} else {
    Write-Host "[ERRO] Erro ao instalar Ganache CLI" -ForegroundColor Red
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Configurando Projeto Truffle" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se ja existe um projeto Truffle inicializado
if (Test-Path "truffle-config.js") {
    Write-Host "[OK] Projeto Truffle ja inicializado" -ForegroundColor Green
} else {
    Write-Host "Inicializando projeto Truffle..." -ForegroundColor Yellow
    truffle init
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Projeto Truffle inicializado" -ForegroundColor Green
    } else {
        Write-Host "[ERRO] Erro ao inicializar Truffle" -ForegroundColor Red
    }
}

# Copia o contrato Token.sol para o diretorio de contratos do Truffle
Write-Host ""
Write-Host "Copiando contrato Token.sol..." -ForegroundColor Yellow
$sourcePath = "..\backend\contracts\Token.sol"
$destPath = "contracts\Token.sol"

if (Test-Path $sourcePath) {
    Copy-Item -Path $sourcePath -Destination $destPath -Force
    Write-Host "[OK] Token.sol copiado para contracts/" -ForegroundColor Green
} else {
    Write-Host "[ERRO] Arquivo Token.sol nao encontrado em $sourcePath" -ForegroundColor Red
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Compilando Contratos" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Compila os contratos
Write-Host "Compilando contratos..." -ForegroundColor Yellow
truffle compile
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Contratos compilados com sucesso" -ForegroundColor Green
} else {
    Write-Host "[ERRO] Erro ao compilar contratos" -ForegroundColor Red
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Proximos Passos" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Para iniciar a blockchain local:" -ForegroundColor Yellow
Write-Host "  1. Abra um novo terminal PowerShell" -ForegroundColor White
Write-Host "  2. Execute: ganache-cli" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para fazer deploy dos contratos:" -ForegroundColor Yellow
Write-Host "  1. Com Ganache rodando, execute:" -ForegroundColor White
Write-Host "  2. truffle migrate --network development" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para iniciar o backend Python:" -ForegroundColor Yellow
Write-Host "  1. cd ..\backend" -ForegroundColor White
Write-Host "  2. pip install -r requirements.txt" -ForegroundColor White
Write-Host "  3. python src\app.py" -ForegroundColor Cyan
Write-Host ""

Write-Host "[OK] Configuracao concluida!" -ForegroundColor Green
