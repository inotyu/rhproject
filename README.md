# Sistema de Gestão de Recursos Humanos (RH) com Flask
<a href="https://lowproject.pythonanywhere.com/" target="_blank">RH Rosa</a>

[![Português](https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/45px-Flag_of_Brazil.svg.png)](#-instruções-em-português)

Este projeto é um sistema de gerenciamento de recursos humanos, desenvolvido em **Flask**, com funcionalidades como:

- Autenticação de usuários (login e registro)
- Cadastro, edição e remoção de funcionários
- Atribuição de trabalhos aos funcionários
- Upload de fotos para os funcionários
- Filtros para busca e visualização de funcionários por cargo e estado civil
- Dashboard com resumo de funcionários e cargos

⚠️ **Aviso:** o código está escrito em Português Brasileiro.

<!-- Exemplo de screenshot -->
<!-- <a href="https://ibb.co/vjGcy0z"><img src="" alt="Captura de Tela" border="0" /></a> -->

## Instruções

1. **Clone o projeto:**

   ```bash
   git clone <url-do-repositorio>
   cd rh
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências necessárias:**

   Este projeto requer as seguintes dependências em Python:
   - Flask
   - Flask-Login
   - Werkzeug
   - mysql-connector-python

   Instale todas de uma vez com:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**

   Crie as tabelas necessárias para funcionários e usuários. Exemplo:

   ```sql
   CREATE TABLE funcionarios (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nome VARCHAR(255) NOT NULL,
       cargo VARCHAR(100),
       salario DECIMAL(10,2),
       estado_civil VARCHAR(20),
       foto VARCHAR(255)
   );

   CREATE TABLE usuarios (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(150) UNIQUE NOT NULL,
       password_hash VARCHAR(255) NOT NULL
   );
   ```

   Configure a conexão MySQL no arquivo `db_utils.py`.

5. **Execute a aplicação Flask:**

   ```bash
   python app.py
   ```

6. **Uso:**

   - Acesse o app em [http://127.0.0.1:5000](http://127.0.0.1:5000) no seu navegador.
   - Utilize o sistema de login e registro para autenticar usuários.
   - Use o dashboard para gerenciar funcionários, cargos e muito mais.
   - Adicione, edite ou remova funcionários e atribua cargos a eles.
   - Os funcionários podem visualizar suas tarefas e informações de salário.

## Funcionalidades

- **Autenticação:** Sistema de login e registro de usuários
- **Cadastro de Funcionários:** Adição, edição e remoção de funcionários
- **Atribuição de Trabalhos:** Atribuição de tarefas a funcionários
- **Dashboard:** Resumo dos funcionários e cargos
- **Busca e Filtros:** Pesquisa de funcionários por cargo e estado civil
- **Upload de Fotos:** Possibilidade de adicionar fotos aos perfis dos funcionários

## Tecnologias Utilizadas

- **Flask:** Framework web em Python
- **MySQL:** Banco de dados para armazenamento de dados de funcionários
- **Flask-Login:** Extensão Flask para autenticação
- **Werkzeug:** Utilitário para segurança e senha
- **HTML/CSS/JavaScript:** Front-end da aplicação

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Funcionalidades
- Dashboard com estatísticas
- Cadastro, listagem, edição e remoção de funcionários (em memória)
- Upload de foto
- Busca e filtros
- Mensagens visuais de sucesso/erro
- Layout moderno, responsivo, tema rosa e branco

## Customização
- Para alterar o tema, edite os arquivos em `templates/` e `static/css/`.

## Observações
- Os dados são compartilhados.
- Meu objetivo com este projeto foi mostrar minhas skills com tecnológias como sql, python, html e css.

## Imagens

![Tela 1](rhsystem/static/images/Captura%20de%20tela%202025-05-08%20160536.png)
![Tela 2](rhsystem/static/images/Captura%20de%20tela%202025-05-08%20160519.png)

