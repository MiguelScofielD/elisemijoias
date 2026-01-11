# Sistema de Vendas

## Passos para rodar o sistema no seu computador:

1. **Instale o Git e o Python (se não tiver instalado)**:
    - [Git](https://git-scm.com/downloads)
    - [Python](https://www.python.org/downloads/)

2. **Clone o repositório**:
    Abra o terminal ou prompt de comando e execute:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

3. **Crie um ambiente virtual**:
    Execute o seguinte comando no terminal:
    ```bash
    python -m venv venv
    ```

4. **Ative o ambiente virtual**:
    - **Windows**:
      ```bash
      venv\Scripts\activate
      ```
    - **Linux/macOS**:
      ```bash
      source venv/bin/activate
      ```

5. **Instale as dependências**:
    No terminal, execute:
    ```bash
    pip install -r requirements.txt
    ```

6. **Configure o banco de dados**:
    Execute as migrações do Django com o comando:
    ```bash
    python manage.py migrate
    ```

7. **Inicie o servidor**:
    Execute:
    ```bash
    python manage.py runserver
    ```

8. **Acesse o sistema**:
    Abra o navegador e digite:
    ```
    http://127.0.0.1:8000
    ```

Agora o sistema estará rodando localmente no seu computador.
