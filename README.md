# Relatório de Testes de Integração

## Visão Geral

Este relatório descreve os testes de integração implementados no projeto e sua relação com o código atual em [TEST/test_produto.py](TEST/test_produto.py).

## Ambiente e Ferramentas

- **Framework de teste:** Pytest
- **Banco de dados:** SQLite
- **Interpretador utilizado:** `.venv\Scripts\python.exe`
- **Arquivo de testes:** [TEST/test_produto.py](TEST/test_produto.py)

## Componentes Cobertos

| Componente | Descrição |
| --- | --- |
| `db_produtos` | Fixture de escopo `function` que cria um banco em memória para testes de produtos |
| `db_logs` | Fixture de escopo `function` que cria um banco em memória para testes de logs |
| `registrar_log` | Função utilitária que insere registros na tabela `logs` |
| Tabela `produtos` | Armazena os registros de produtos utilizados nos testes |
| Tabela `logs` | Armazena entradas de log utilizadas nos testes de persistência de mensagens |

## Casos de Teste

### CT-01 — Inserção de produto

- **Objetivo:** validar que um produto pode ser inserido e recuperado corretamente.
- **Pré-condição:** fixture `db_produtos` disponível.
- **Passos:**
  1. Inserir um produto na tabela `produtos`.
  2. Consultar o registro inserido.
- **Resultado esperado:** o registro retornado corresponde ao produto inserido.

```python
def test_inserir_produto(db_produtos):
    cursor = db_produtos.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", ("Ford GT 40 mk IV", 35000.0))
    db_produtos.commit()

    cursor.execute("SELECT nome, preco FROM produtos")
    produto = cursor.fetchone()

    assert produto == ("Ford GT 40 mk IV", 35000.0)
```

### CT-02 — Consulta de produto inserido

- **Objetivo:** validar a recuperação de um produto específico a partir do banco.
- **Pré-condição:** fixture `db_produtos` disponível.
- **Passos:**
  1. Inserir um produto na tabela `produtos`.
  2. Consultar o produto pelo campo `nome`.
- **Resultado esperado:** o produto consultado deve ser exatamente o produto inserido.

```python
def test_retorna_produto_inserido(db_produtos):
    cursor = db_produtos.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", ("Ford GT 40 mk IV", 35000.0))
    db_produtos.commit()

    cursor.execute("SELECT nome, preco FROM produtos WHERE nome = ?", ("Ford GT 40 mk IV",))
    produto = cursor.fetchone()

    assert produto == ("Ford GT 40 mk IV", 35000.0)
```

### CT-03 — Banco de produtos vazio

- **Objetivo:** garantir que o banco de produtos comece sem registros.
- **Pré-condição:** fixture `db_produtos` disponível.
- **Passos:**
  1. Consultar a contagem de registros da tabela `produtos`.
- **Resultado esperado:** contagem igual a `0`.

```python
def test_banco_produtos_vazio(db_produtos):
    cursor = db_produtos.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total = cursor.fetchone()[0]

    assert total == 0
```

### CT-04 — Registro de log

- **Objetivo:** validar que a função de registro insere uma mensagem na tabela `logs`.
- **Pré-condição:** fixture `db_logs` disponível.
- **Passos:**
  1. Registrar uma mensagem usando `registrar_log`.
  2. Consultar a tabela `logs`.
- **Resultado esperado:** a mensagem registrada deve ser retornada corretamente.

```python
def test_registrar_log(db_logs):
    registrar_log(db_logs, "Produto criado")

    cursor = db_logs.cursor()
    cursor.execute("SELECT mensagem FROM logs")
    log = cursor.fetchone()

    assert log == ("Produto criado",)
```

### CT-05 — Logs compartilhados

- **Objetivo:** validar que múltiplos registros de log são preservados e recuperados na ordem esperada.
- **Pré-condição:** fixture `db_logs` disponível.
- **Passos:**
  1. Registrar duas mensagens consecutivas.
  2. Consultar todos os registros do banco.
- **Resultado esperado:** as mensagens devem ser retornadas na ordem de inserção.

```python
def test_logs_compartilhados(db_logs):
    registrar_log(db_logs, "Log 1")
    registrar_log(db_logs, "Log 2")

    cursor = db_logs.cursor()
    cursor.execute("SELECT mensagem FROM logs ORDER BY id")
    logs = cursor.fetchall()

    assert logs == [("Log 1",), ("Log 2",)]
```

## Resultados de Execução

A suíte foi executada com o comando abaixo:

```powershell
pytest -s -v TEST/test_produto.py
```

**Resultado verificado:** 5 testes executados com sucesso.

## Observações

- Os testes utilizam bancos SQLite em memória, garantindo isolamento entre testes.
- O arquivo atual de testes está centralizado em [TEST/test_produto.py](TEST/test_produto.py).
- O relatório foi alinhado com a implementação real do projeto e com os cenários efetivamente cobertos pela suíte.
    
