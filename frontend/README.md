# Frontend Documentation

## Overview
This project is a decentralized application (dApp) built on the Ethereum blockchain. It allows users to register, log in, and transfer tokens through a user-friendly interface. The frontend is developed using React and interacts with a backend REST API built with Python and Flask.

## Getting Started

### Prerequisites
- Node.js (v14 or later)
- npm (Node Package Manager)

### Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ethereum-blockchain-app/frontend
   ```

2. Install the dependencies:
   ```
   npm install
   ```

### Running the Application
To start the development server, run:
```
npm start
```
This will launch the application in your default web browser at `http://localhost:3000`.

### Folder Structure
- **public/**: Contains the static files, including the main HTML file.
- **src/**: Contains the React components and application logic.
  - **components/**: Contains individual React components for login, registration, transfer, and dashboard.
  - **services/**: Contains API service files for interacting with the backend and blockchain.
  - **utils/**: Contains utility functions for authentication.

### Components
- **Login.jsx**: User login interface.
- **Register.jsx**: User registration interface.
- **Transfer.jsx**: Interface for transferring tokens between users.
- **Dashboard.jsx**: Displays user information and transaction history.

### API Interaction
The frontend communicates with the backend REST API through the `api.js` service file. Ensure the backend is running to interact with the blockchain.

### Web3 Integration
The `web3.js` service file handles interactions with the Ethereum blockchain, allowing users to perform transactions and manage their tokens.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.