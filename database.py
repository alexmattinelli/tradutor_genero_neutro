import sqlite3
import os

def criar_banco():
    # Remove o arquivo existente se estiver corrompido
    if os.path.exists("database.db"):
        os.remove("database.db")
        
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Cria a tabela de feedback
    cursor.execute("""
        CREATE TABLE feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original TEXT NOT NULL,
            traducao TEXT NOT NULL,
            correto BOOLEAN NOT NULL,
            correcao TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Cria tabela de vocabulário
    cursor.execute("""
        CREATE TABLE vocabulario (
            palavra_masc TEXT PRIMARY KEY,
            palavra_neutra TEXT NOT NULL,
            exemplos TEXT
        )
    """)
    
    # Insere alguns exemplos iniciais
    exemplos = [
        ("o", "ê"), ("a", "ê"),
        ("menino", "menine"), ("menina", "menine"),
        ("todos", "todes"), ("todas", "todes"),
        ("professor", "professore"), ("professora", "professore")
    ]
    
    cursor.executemany(
        "INSERT INTO vocabulario (palavra_masc, palavra_neutra) VALUES (?, ?)",
        exemplos
    )
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_banco()
    print("Banco de dados criado com sucesso!")