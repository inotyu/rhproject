import mysql.connector
from mysql.connector import Error

# Configure these as needed or use environment variables
DB_CONFIG = {
    'host': 'lowproject.mysql.pythonanywhere-services.com',
    'user': 'lowproject',
    'password': '2024debe',  # Altere para sua senha
    'database': 'lowproject$default'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cargo VARCHAR(255) NOT NULL,
            salario DECIMAL(10,2) NOT NULL,
            estado_civil VARCHAR(50) NOT NULL,
            foto VARCHAR(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(150) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def get_trabalhos_by_funcionario(func_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trabalhos WHERE funcionario_id = %s", (func_id,))
    trabalhos = cursor.fetchall()
    cursor.close()
    conn.close()
    return trabalhos

def add_trabalho(funcionario_id, titulo, descricao, data_inicio, data_fim):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trabalhos (funcionario_id, titulo, descricao, data_inicio, data_fim)
        VALUES (%s, %s, %s, %s, %s)
    """, (funcionario_id, titulo, descricao, data_inicio, data_fim))
    conn.commit()
    cursor.close()
    conn.close()
