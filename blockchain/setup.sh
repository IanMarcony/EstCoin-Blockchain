#!/bin/bash

# Instala as dependências do Ethereum
npm install -g truffle
npm install -g ganache-cli

# Cria um novo projeto Truffle
truffle init

# Copia o contrato Token.sol para o diretório de contratos do Truffle
cp ../backend/contracts/Token.sol contracts/

# Inicia o Ganache para simular a rede Ethereum local
ganache-cli &

# Compila os contratos
truffle compile

# Migrate os contratos para a rede local
truffle migrate --network development

echo "Configuração da blockchain local concluída."