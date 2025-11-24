

echo "════════════════════════════════════════════════════════════════════"
echo "  🚀 SETUP INICIAL ESTCOIN - SISTEMA COMPLETO"
echo "════════════════════════════════════════════════════════════════════"
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

print_step() {
    echo -e "\n${BLUE}▶ $1${NC}"
}


print_step "Instalando dependências Python..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --break-system-packages
    if [ $? -eq 0 ]; then
        print_success "Dependências instaladas"
    else
        print_error "Erro ao instalar dependências"
        exit 1
    fi
else
    print_error "requirements.txt não encontrado"
    exit 1
fi

print_step "Verificando conexão com Ethereum..."
python3 -c "
from web3 import Web3
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
if web3.is_connected():
    print('✅ Conectado ao Ethereum')
    exit(0)
else:
    print('❌ Não conectado ao Ethereum em http://127.0.0.1:8545')
    print('   Inicie o servidor Ethereum primeiro!')
    exit(1)
"
if [ $? -ne 0 ]; then
    exit 1
fi

print_step "Verificando contrato compilado..."
CONTRACT_PATH="../blockchain/build/contracts/Token.json"
if [ -f "$CONTRACT_PATH" ]; then
    print_success "Contrato compilado encontrado"
else
    print_error "Contrato não compilado!"
    print_info "Execute: cd ../blockchain && truffle compile"
    exit 1
fi

print_step "Fazendo deploy do contrato (1 milhão de ESTCOIN)..."
python3 deploy_contract.py
if [ $? -eq 0 ]; then
    print_success "Contrato deployado com sucesso"
else
    print_error "Erro no deploy do contrato"
    exit 1
fi


print_step "Verificando configuração..."
python3 -c "
from src.config import Config
if Config.TOKEN_CONTRACT_ADDRESS:
    print(f'✅ Contrato configurado: {Config.TOKEN_CONTRACT_ADDRESS}')
else:
    print('❌ Contrato não configurado no config.py')
    exit(1)
"
if [ $? -ne 0 ]; then
    exit 1
fi
