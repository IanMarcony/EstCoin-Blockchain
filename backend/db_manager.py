"""
Script para gerenciar o banco de dados SQLite
"""
from src.models.user import init_db, SessionLocal, User, DB_PATH
import os

def create_database():
    """Cria o banco de dados e as tabelas"""
    print("🔄 Criando banco de dados...")
    init_db()
    print(f"✅ Banco criado em: {DB_PATH}")

def list_users():
    """Lista todos os usuários"""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        
        if not users:
            print("❌ Nenhum usuário encontrado")
            return
        
        print(f"\n📋 Total de usuários: {len(users)}\n")
        print("-" * 80)
        
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Ethereum Address: {user.ethereum_address}")
            print(f"Balance: {user.balance} EST")
            print("-" * 80)
            
    finally:
        db.close()

def delete_database():
    """Deleta o banco de dados"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"✅ Banco de dados deletado: {DB_PATH}")
    else:
        print("❌ Banco de dados não encontrado")

def reset_database():
    """Reseta o banco de dados (deleta e recria)"""
    print("🔄 Resetando banco de dados...")
    delete_database()
    create_database()
    print("✅ Banco resetado com sucesso!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("\n📚 Uso:")
        print("  python db_manager.py create    - Cria o banco de dados")
        print("  python db_manager.py list      - Lista todos os usuários")
        print("  python db_manager.py delete    - Deleta o banco de dados")
        print("  python db_manager.py reset     - Reseta o banco (deleta e recria)")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'create':
        create_database()
    elif command == 'list':
        list_users()
    elif command == 'delete':
        delete_database()
    elif command == 'reset':
        reset_database()
    else:
        print(f"❌ Comando desconhecido: {command}")
