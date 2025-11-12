# Blockchain Infrastructure Project

Este projeto implementa uma infraestrutura local de blockchain baseada no Ethereum, permitindo a criação de um sistema de transferência de fundos entre usuários. A aplicação é dividida em duas partes principais: um backend em Python com uma API REST e um frontend em React.

## Estrutura do Projeto

- **backend/**: Contém a lógica do servidor, incluindo rotas, controladores e modelos.
- **frontend/**: Contém a interface do usuário, construída com React.
- **blockchain/**: Contém a configuração e scripts para a rede blockchain local.

## Configuração da Blockchain

A blockchain é configurada para operar em um ambiente local, utilizando o arquivo `genesis.json` para definir o bloco gênese e o script `setup.sh` para iniciar a rede.

1. chainId: 1337 - ID único da sua rede privada
2. difficulty: "20000000000000" - Dificuldade de mineração (baixa para desenvolvimento)
3. gasLimit: "8000000" - Limite de gas por bloco (~400-500 transações)
4. alloc: {} - Contas pré-financiadas (vazio = nenhuma)

## Backend

O backend é construído com Flask e fornece as seguintes funcionalidades:

- **Cadastro de Usuários**: Permite que novos usuários se registrem.
- **Login de Usuários**: Autentica usuários existentes.
- **Transferência de Fundos**: Facilita a transferência de tokens entre usuários.

## Frontend

A aplicação frontend é construída com React e oferece uma interface amigável para os usuários interagirem com o sistema. As principais funcionalidades incluem:

- **Login**: Interface para usuários se autenticarem.
- **Cadastro**: Interface para novos usuários se registrarem.
- **Transferência**: Interface para usuários transferirem fundos.
- **Dashboard**: Exibe informações do usuário e histórico de transações.

## Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt` para o backend e no `package.json` para o frontend.

## Instruções de Uso

1. **Configurar a Blockchain**: Execute o script `setup.sh` para iniciar a rede blockchain local.
2. **Iniciar o Backend**: Navegue até o diretório `backend` e execute o servidor Flask.
3. **Iniciar o Frontend**: Navegue até o diretório `frontend` e inicie a aplicação React.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias e correções.