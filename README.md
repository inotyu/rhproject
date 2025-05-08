# Sistema de Gestão de Recursos Humanos (RH) com Flask

Este projeto é um sistema de gerenciamento de recursos humanos, desenvolvido em **Flask**, com funcionalidades como:

- Autenticação de usuários (login e registro).
- Cadastro, edição e remoção de funcionários.
- Atribuição de trabalhos aos funcionários.
- Upload de fotos para os funcionários.
- Filtros para busca e visualização de funcionários por cargo e estado civil.
- Dashboard com resumo de funcionários e cargos.

## Tecnologias Utilizadas

- **Flask**: Framework web em Python.
- **Flask-Login**: Gerenciamento de sessão de usuários.
- **MySQL**: Banco de dados para armazenar informações de funcionários e usuários.
- **Werkzeug**: Utilizado para segurança e manipulação de arquivos.

## Funcionalidades

- **Cadastro de Funcionários**: Permite adicionar novos funcionários com informações como nome, cargo, estado civil, salário e foto.
- **Edição de Funcionários**: Edita os dados de um funcionário existente, permitindo modificar todas as informações.
- **Remoção de Funcionários**: Exclui um funcionário do sistema.
- **Atribuição de Trabalhos**: Permite atribuir um trabalho a um funcionário, com informações sobre o título, descrição e datas de início e fim.
- **Login e Registro**: Sistema de autenticação com registro de novos usuários e login com verificação de senha.
- **Filtro de Funcionários**: Busca de funcionários por nome, cargo e estado civil.

## Como Rodar o Projeto

1. Clone este repositório para sua máquina local:

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Crie e configure o banco de dados MySQL conforme a estrutura abaixo:

Tabelas principais:

funcionarios

usuarios

trabalhos

Exemplo de criação da tabela de funcionários:

sql
Copiar
Editar
CREATE TABLE funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cargo VARCHAR(100),
    salario DECIMAL(10,2),
    estado_civil VARCHAR(20),
    foto VARCHAR(255)
);
Configure o arquivo de banco de dados para conectar ao MySQL no arquivo db_utils.py.

Rode o servidor Flask:

bash
Copiar
Editar
python app.py
Acesse o sistema através do navegador em http://127.0.0.1:5000.

Considerações
Este sistema foi criado para fins de aprendizado e pode ser adaptado para empresas de diferentes portes. Algumas melhorias que podem ser feitas:

Implementar controle de acesso para diferentes tipos de usuários (admin, gerente, etc).

Adicionar relatórios detalhados sobre salários, departamentos e cargos.

Criar um sistema de feedback para os funcionários.

Implementar funcionalidades de notificação.

Contribuições
Contribuições são bem-vindas! Se você tiver alguma sugestão ou melhoria, fique à vontade para abrir uma issue ou enviar um pull request.

Projeto criado por Seu Nome.
