#!/bin/bash
# Script de recuperação rápida quando o Ganache é reiniciado

echo "════════════════════════════════════════════════════════════════════"
echo "  🔄 RECUPERAÇÃO RÁPIDA - REDEPLOY E REDISTRIBUIÇÃO"
echo "════════════════════════════════════════════════════════════════════"
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
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
    echo -e "\n${GREEN}▶ $1${NC}"
}

# 1. Deploy do contrato
print_step "1/3 - Fazendo deploy do contrato Token..."
python3 deploy_contract.py
if [ $? -ne 0 ]; then
    print_error "Falha no deploy do contrato"
    exit 1
fi

# 2. Distribuir ETH
print_step "2/3 - Distribuindo ETH (gás) para usuários..."
python3 distribute_eth.py
if [ $? -ne 0 ]; then
    print_error "Falha na distribuição de ETH"
    exit 1
fi

# 3. Distribuir Tokens
print_step "3/3 - Distribuindo ESTCOIN para usuários..."
python3 distribute_tokens.py
if [ $? -ne 0 ]; then
    print_error "Falha na distribuição de tokens"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
print_success "RECUPERAÇÃO CONCLUÍDA COM SUCESSO!"
echo "════════════════════════════════════════════════════════════════════"
echo ""
print_info "Próximos passos:"
echo "  1. Reinicie o backend: ./start.sh"
echo "  2. Reinicie o frontend (se necessário)"
echo "  3. Faça login novamente"
echo ""
