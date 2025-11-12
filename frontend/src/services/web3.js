import Web3 from 'web3';

let web3;

if (window.ethereum) {
    web3 = new Web3(window.ethereum);
    window.ethereum.request({ method: 'eth_requestAccounts' });
} else {
    console.error('Please install MetaMask!');
}

export const getAccounts = async () => {
    const accounts = await web3.eth.getAccounts();
    return accounts;
};

export const getBalance = async (address) => {
    const balance = await web3.eth.getBalance(address);
    return web3.utils.fromWei(balance, 'ether');
};

export const sendTransaction = async (from, to, amount) => {
    const transactionParameters = {
        to: to,
        from: from,
        value: web3.utils.toHex(web3.utils.toWei(amount, 'ether')),
    };

    return await web3.eth.sendTransaction(transactionParameters);
};