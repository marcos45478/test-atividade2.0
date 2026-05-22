import sqlite3
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / 'teste.sqlite'
LOGS_DB_FILE = BASE_DIR / 'log.sqlite'

@pytest.fixture(scope='function')
def db_produtos():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    cursor.execute('''
            CREATE TABLE produtos(
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                preco REAL NOT NULL
            )
        ''')
    
    yield conn
    conn.close()


@pytest.fixture(scope='function')
def db_logs():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE logs(
                id INTEGER PRIMARY KEY,
                mensagem TEXT NOT NULL
            )
        ''')

    yield conn
    conn.close()


def registrar_log(conn, mensagem):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (mensagem) VALUES (?)", (mensagem,))
    conn.commit()


def test_inserir_produto(db_produtos):
    cursor = db_produtos.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", ("Ford GT 40 mk IV", 35000.0))
    db_produtos.commit()

    cursor.execute("SELECT nome, preco FROM produtos")
    produto = cursor.fetchone()

    assert produto == ("Ford GT 40 mk IV", 35000.0)


def test_retorna_produto_inserido(db_produtos):
    cursor = db_produtos.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", ("Ford GT 40 mk IV", 35000.0))
    db_produtos.commit()

    cursor.execute("SELECT nome, preco FROM produtos WHERE nome = ?", ("Ford GT 40 mk IV",))
    produto = cursor.fetchone()

    assert produto == ("Ford GT 40 mk IV", 35000.0)


def test_banco_produtos_vazio(db_produtos):
    cursor = db_produtos.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total = cursor.fetchone()[0]

    assert total == 0


def test_registrar_log(db_logs):
    registrar_log(db_logs, "Produto criado")

    cursor = db_logs.cursor()
    cursor.execute("SELECT mensagem FROM logs")
    log = cursor.fetchone()

    assert log == ("Produto criado",)


def test_logs_compartilhados(db_logs):
    registrar_log(db_logs, "Log 1")
    registrar_log(db_logs, "Log 2")

    cursor = db_logs.cursor()
    cursor.execute("SELECT mensagem FROM logs ORDER BY id")
    logs = cursor.fetchall()

    assert logs == [("Log 1",), ("Log 2",)]
