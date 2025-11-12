# Backend Documentation

Este diretório contém a implementação do backend da aplicação de blockchain baseada em Ethereum. A aplicação é construída utilizando Flask e oferece uma API REST para gerenciar usuários e transações.

## Estrutura do Projeto

- **src/**: Contém o código-fonte da aplicação.
  - **app.py**: Ponto de entrada da aplicação, inicializa o servidor Flask e configura as rotas.
  - **config.py**: Contém as configurações da aplicação, como variáveis de ambiente e configurações do banco de dados.
  - **routes/**: Define as rotas da API.
    - **auth.py**: Rotas relacionadas à autenticação de usuários (cadastro e login).
    - **transactions.py**: Rotas para a funcionalidade de transferência de fundos entre usuários.
  - **controllers/**: Contém a lógica de controle para operações relacionadas a usuários e transações.
    - **user_controller.py**: Lógica de controle para operações de usuários.
    - **transaction_controller.py**: Lógica de controle para operações de transferência.
  - **models/**: Define os modelos de dados utilizados na aplicação.
    - **user.py**: Modelo de dados para os usuários.
  - **blockchain/**: Contém a lógica para interagir com a blockchain Ethereum.
    - **contract.py**: Definição do contrato inteligente em Solidity.
    - **web3_client.py**: Configuração da conexão com a rede Ethereum.
  - **utils/**: Funções utilitárias para a aplicação.
    - **auth_utils.py**: Funções para autenticação, como geração de tokens.

## Instalação

1. Clone o repositório:
   ```
   git clone <URL_DO_REPOSITORIO>
   cd ethereum-blockchain-app/backend
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```
   python src/app.py
   ```

## Uso

A API REST está disponível em `http://localhost:5000`. As seguintes rotas estão disponíveis:

- **POST /auth/register**: Cadastro de um novo usuário.
- **POST /auth/login**: Login de um usuário existente.
- **POST /transactions/transfer**: Transferência de fundos entre usuários.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.