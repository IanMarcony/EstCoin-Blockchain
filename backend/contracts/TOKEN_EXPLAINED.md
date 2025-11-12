# 📜 Token.sol - Smart Contract EstCoin

## 🎯 O que é este arquivo?

**Token.sol** é um **Smart Contract** (contrato inteligente) escrito em **Solidity** que implementa o token **EstCoin (ESTC)** no padrão **ERC-20** simplificado. Este contrato roda na blockchain Ethereum e controla toda a lógica de criação, transferência e gerenciamento dos tokens do projeto.

---

## 🏗️ Estrutura do Contrato

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
```

### **Licença e Versão**
- **MIT License**: Código open source, pode ser usado livremente
- **Solidity ^0.8.0**: Requer versão 0.8.0 ou superior do compilador
  - Proteção automática contra overflow/underflow
  - Recursos modernos de segurança

---

## 📋 Variáveis de Estado

### **Informações do Token**

```solidity
string public name = "EstCoin";
string public symbol = "ESTC";
uint8 public decimals = 18;
uint256 public totalSupply;
```

| Variável | Tipo | Valor | Descrição |
|----------|------|-------|-----------|
| `name` | string | "EstCoin" | Nome completo do token |
| `symbol` | string | "ESTC" | Símbolo/ticker (como BTC, ETH) |
| `decimals` | uint8 | 18 | Casas decimais (padrão Ethereum) |
| `totalSupply` | uint256 | Variável | Quantidade total de tokens existentes |

**Por que 18 decimais?**
- Padrão do Ethereum
- Permite divisões precisas: 0.000000000000000001 ESTC
- 1 ESTC = 1 × 10¹⁸ unidades menores (Wei)

---

### **Armazenamento de Dados**

```solidity
mapping(address => uint256) public balanceOf;
```

**`balanceOf`** - Mapeamento de saldos:
- Chave: Endereço Ethereum (0x...)
- Valor: Quantidade de tokens
- Exemplo: `balanceOf[0x123...] = 100` = endereço tem 100 tokens

```solidity
mapping(address => mapping(address => uint256)) public allowance;
```

**`allowance`** - Permissões de gasto:
- Mapeia: Dono → Gastador → Quantidade permitida
- Exemplo: `allowance[Alice][Bob] = 50` = Alice permite Bob gastar até 50 tokens dela
- Usado para delegação (DEXs, contratos automáticos)

---

## 📢 Eventos (Event Logs)

```solidity
event Transfer(address indexed from, address indexed to, uint256 value);
event Approval(address indexed owner, address indexed spender, uint256 value);
```

### **Por que usar eventos?**
- ✅ Registram ações importantes na blockchain
- ✅ Baratos (custo baixo de gas)
- ✅ Frontend pode "ouvir" e reagir em tempo real
- ✅ `indexed` permite filtrar/buscar eventos específicos

### **Event Transfer**
Emitido quando tokens são transferidos:
```javascript
// Exemplo de evento
Transfer(from: "0xAlice...", to: "0xBob...", value: 10000000000000000000)
```

### **Event Approval**
Emitido quando permissão é concedida:
```javascript
// Exemplo de evento
Approval(owner: "0xAlice...", spender: "0xBob...", value: 50000000000000000000)
```

---

## 🏗️ Constructor (Criação do Contrato)

```solidity
constructor(uint256 _initialSupply) {
    totalSupply = _initialSupply * (10 ** uint256(decimals));
    balanceOf[msg.sender] = totalSupply;
}
```

### **O que faz?**
Executado **UMA VEZ** quando o contrato é deployado na blockchain.

### **Parâmetros:**
- `_initialSupply`: Quantidade inicial de tokens (ex: 1000000 = 1 milhão)

### **Processo:**
1. **Calcula total supply**: `1000000 × 10¹⁸` = 1000000000000000000000000
2. **Atribui ao criador**: Todo o supply vai para `msg.sender` (quem fez o deploy)

### **Exemplo de Deploy:**
```python
# Python com Web3.py
contract = web3.eth.contract(abi=abi, bytecode=bytecode)
tx = contract.constructor(1000000).transact({'from': owner_address})

# Resultado:
# - totalSupply = 1.000.000 ESTC
# - balanceOf[owner] = 1.000.000 ESTC
# - Todos os outros endereços = 0 ESTC
```

---

## 💸 Funções Públicas

### **1. transfer() - Transferência Simples**

```solidity
function transfer(address _to, uint256 _value) public returns (bool success) {
    require(_to != address(0), "Invalid address");
    require(balanceOf[msg.sender] >= _value, "Insufficient balance");

    balanceOf[msg.sender] -= _value;
    balanceOf[_to] += _value;
    emit Transfer(msg.sender, _to, _value);
    return true;
}
```

#### **O que faz?**
Permite enviar tokens diretamente do seu endereço para outro.

#### **Parâmetros:**
- `_to`: Endereço do destinatário
- `_value`: Quantidade de tokens (em Wei)

#### **Validações:**
1. ✅ Endereço destinatário não pode ser 0x0...0
2. ✅ Remetente deve ter saldo suficiente

#### **Fluxo:**
```
1. Valida endereço e saldo
2. Subtrai tokens do remetente
3. Adiciona tokens ao destinatário
4. Emite evento Transfer
5. Retorna true (sucesso)
```

#### **Exemplo de Uso:**
```javascript
// JavaScript/Web3.js
await contract.methods.transfer(
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", // destinatário
    web3.utils.toWei("10", "ether")               // 10 ESTC
).send({ from: userAddress });
```

```python
# Python/Web3.py
contract.functions.transfer(
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",  # destinatário
    10 * 10**18                                     # 10 ESTC
).transact({'from': user_address})
```

#### **Custo de Gas:**
~51.000 gas (~$2-5 dependendo do preço do gas)

---

### **2. approve() - Dar Permissão**

```solidity
function approve(address _spender, uint256 _value) public returns (bool success) {
    allowance[msg.sender][_spender] = _value;
    emit Approval(msg.sender, _spender, _value);
    return true;
}
```

#### **O que faz?**
Permite que outro endereço gaste seus tokens em seu nome.

#### **Quando usar?**
- **DEXs (exchanges descentralizadas)**: Autorizar contrato a mover seus tokens
- **Contratos automáticos**: Delegar permissões
- **Pagamentos recorrentes**: Permitir cobranças automáticas

#### **Parâmetros:**
- `_spender`: Endereço que receberá permissão
- `_value`: Quantidade máxima que pode gastar

#### **Exemplo:**
```javascript
// Alice permite que um contrato DEX gaste até 100 ESTC
await contract.methods.approve(
    dexContractAddress,
    web3.utils.toWei("100", "ether")
).send({ from: aliceAddress });

// Agora allowance[Alice][DEX] = 100 ESTC
```

#### **Custo de Gas:**
~45.000 gas

---

### **3. transferFrom() - Transferência Delegada**

```solidity
function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
    require(_from != address(0), "Invalid address");
    require(_to != address(0), "Invalid address");
    require(balanceOf[_from] >= _value, "Insufficient balance");
    require(allowance[_from][msg.sender] >= _value, "Allowance exceeded");

    balanceOf[_from] -= _value;
    balanceOf[_to] += _value;
    allowance[_from][msg.sender] -= _value;
    emit Transfer(_from, _to, _value);
    return true;
}
```

#### **O que faz?**
Permite transferir tokens **de outra pessoa** (se você tem permissão via `approve`).

#### **Parâmetros:**
- `_from`: Endereço de origem dos tokens
- `_to`: Endereço de destino
- `_value`: Quantidade a transferir

#### **Validações:**
1. ✅ Endereços de origem e destino válidos
2. ✅ Origem tem saldo suficiente
3. ✅ Você tem permissão (`allowance`) suficiente

#### **Fluxo:**
```
1. Valida endereços, saldo e permissão
2. Transfere tokens: from → to
3. Reduz a permissão usada
4. Emite evento Transfer
5. Retorna true
```

#### **Exemplo Completo:**
```javascript
// Passo 1: Alice aprova Bob gastar 50 ESTC
await contract.methods.approve(bobAddress, web3.utils.toWei("50", "ether"))
    .send({ from: aliceAddress });

// allowance[Alice][Bob] = 50 ESTC

// Passo 2: Bob transfere 30 ESTC de Alice para Carol
await contract.methods.transferFrom(
    aliceAddress,
    carolAddress,
    web3.utils.toWei("30", "ether")
).send({ from: bobAddress });

// Resultado:
// - balanceOf[Alice] -= 30
// - balanceOf[Carol] += 30
// - allowance[Alice][Bob] = 20 (50 - 30)
```

#### **Custo de Gas:**
~65.000 gas

---

## 🔐 Segurança Implementada

### ✅ **Proteções Ativas:**

1. **Validação de Endereços**
   ```solidity
   require(_to != address(0), "Invalid address");
   ```
   - Previne envio para endereço vazio (queima acidental)

2. **Verificação de Saldo**
   ```solidity
   require(balanceOf[msg.sender] >= _value, "Insufficient balance");
   ```
   - Impossível gastar mais do que tem

3. **Overflow/Underflow Protection**
   - Solidity 0.8+ tem proteção automática
   - Operações aritméticas revertem se houver overflow

4. **Verificação de Allowance**
   ```solidity
   require(allowance[_from][msg.sender] >= _value, "Allowance exceeded");
   ```
   - Impossível gastar mais do que foi aprovado

### ⚠️ **O que FALTA (mas poderia ter):**

- ❌ **Pausar/Congelar**: Não tem função para pausar transferências
- ❌ **Mint/Burn**: Não pode criar ou destruir tokens após deploy
- ❌ **Ownership**: Não tem controle de dono do contrato
- ❌ **Blacklist**: Não pode bloquear endereços específicos
- ❌ **Taxa de Transferência**: Não cobra comissão nas transferências
- ❌ **Limite por Transação**: Não limita quantidade por transferência

---

## 📊 Fluxo de Uso no Projeto

### **1. Deploy do Contrato**
```python
# Backend (Python)
contract = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor(1000000).transact({'from': owner_address})

# Resultado:
# - 1.000.000 ESTC criados
# - Owner recebe 100% dos tokens
```

### **2. Novo Usuário se Registra**
```python
# Backend transfere 10 ESTC para novo usuário
contract.functions.transfer(
    user_ethereum_address,
    10 * 10**18  # 10 ESTC
).transact({'from': owner_address})

# Resultado:
# - balanceOf[owner] -= 10
# - balanceOf[new_user] = 10
```

### **3. Usuário Transfere para Outro**
```javascript
// Frontend (React)
await contract.methods.transfer(
    recipientAddress,
    amount * 10**18
).send({ from: userAddress });

// Resultado:
// - balanceOf[user] -= amount
// - balanceOf[recipient] += amount
// - Evento Transfer emitido
```

### **4. Backend Consulta Saldo**
```python
# Leitura (não custa gas)
balance_wei = contract.functions.balanceOf(user_address).call()
balance_estc = balance_wei / 10**18

# Retorna para frontend exibir
```

### **5. Histórico de Transações**
```javascript
// Frontend escuta eventos Transfer
contract.events.Transfer({
    filter: { from: userAddress },
    fromBlock: 0
}).on('data', (event) => {
    console.log('Transferência:', {
        from: event.returnValues.from,
        to: event.returnValues.to,
        value: event.returnValues.value / 10**18
    });
});
```

---

## 🎓 Conceitos de Blockchain

### **Smart Contract**
- Código imutável que roda na blockchain
- Execução determinística (mesmo input = mesmo output)
- Não pode ser alterado após deploy
- Cobra gas para executar

### **ERC-20**
- Padrão mais usado para tokens no Ethereum
- Define interface comum: `transfer`, `balanceOf`, `approve`, etc.
- Compatível com wallets (MetaMask, Trust Wallet)
- Compatível com exchanges (Uniswap, PancakeSwap)

### **Gas**
- "Combustível" para executar operações
- Medido em unidades (ex: 51.000 gas)
- Custo em ETH/Wei
- Previne loops infinitos e spam

### **Wei**
- Menor unidade do Ethereum (como centavos)
- 1 ETH = 10¹⁸ Wei
- 1 ESTC = 10¹⁸ unidades menores

### **Events (Logs)**
- Registros permanentes na blockchain
- Baratos (~2.000 gas)
- Não ocupam espaço em variáveis de estado
- Podem ser consultados offline

---

## 💰 Exemplo Prático: Economia do Token

### **Supply Inicial:**
```
1.000.000 ESTC criados
├─ Owner: 1.000.000 ESTC (100%)
└─ Outros: 0 ESTC
```

### **Após 100 Usuários Registrados:**
```
Owner: 999.000 ESTC (99.9%)
└─ 100 usuários: 1.000 ESTC (0.1%)
   ├─ User1: 10 ESTC
   ├─ User2: 10 ESTC
   └─ ... (98 usuários)
```

### **Após Transações:**
```
Owner: 999.000 ESTC
├─ User1: 5 ESTC (enviou 5 para User2)
├─ User2: 15 ESTC (recebeu 5)
├─ User3: 8 ESTC (enviou 2 para User4)
└─ User4: 12 ESTC (recebeu 2)

Total Supply: Sempre 1.000.000 ESTC (fixo)
```

---

## 🧪 Testando o Contrato

### **1. Deploy Local (Ganache)**
```bash
ganache-cli --networkId 1337
```

### **2. Compilar Contrato**
```bash
# Com Truffle
truffle compile

# Com Hardhat
npx hardhat compile

# Com Solc
solc --abi --bin Token.sol -o build/
```

### **3. Deploy**
```javascript
const Token = artifacts.require("Token");

module.exports = function(deployer) {
  deployer.deploy(Token, 1000000); // 1 milhão
};
```

### **4. Interagir**
```javascript
const token = await Token.deployed();

// Verifica supply
const supply = await token.totalSupply();
console.log(supply.toString()); // 1000000000000000000000000

// Verifica saldo
const balance = await token.balanceOf(accounts[0]);
console.log(balance.toString());

// Transfere tokens
await token.transfer(accounts[1], web3.utils.toWei("10", "ether"));
```

---

## 🚀 Melhorias Futuras (Opcional)

### **1. Adicionar Função Mint**
```solidity
function mint(address _to, uint256 _amount) public onlyOwner {
    totalSupply += _amount;
    balanceOf[_to] += _amount;
    emit Transfer(address(0), _to, _amount);
}
```

### **2. Adicionar Função Burn**
```solidity
function burn(uint256 _amount) public {
    require(balanceOf[msg.sender] >= _amount);
    totalSupply -= _amount;
    balanceOf[msg.sender] -= _amount;
    emit Transfer(msg.sender, address(0), _amount);
}
```

### **3. Adicionar Pausable**
```solidity
bool public paused = false;

modifier whenNotPaused() {
    require(!paused, "Contract is paused");
    _;
}

function transfer(...) public whenNotPaused returns (bool) { ... }
```

---

## 📚 Recursos Adicionais

- [Solidity Documentation](https://docs.soliditylang.org/)
- [ERC-20 Standard](https://eips.ethereum.org/EIPS/eip-20)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)
- [Ethereum.org - Smart Contracts](https://ethereum.org/en/developers/docs/smart-contracts/)

---
