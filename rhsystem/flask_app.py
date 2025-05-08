from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from db_utils import get_connection, init_db

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Upload
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Garante que a pasta de uploads exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Autenticação
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

init_db()


@app.route('/trabalho/novo/<int:func_id>', methods=['GET', 'POST'])
@login_required
def novo_trabalho(func_id):
    funcionario = get_funcionario_by_id(func_id)
    if not funcionario:
        flash("Funcionário não encontrado.", "error")
        return redirect(url_for('list_funcionarios'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        add_trabalho(func_id, titulo, descricao, data_inicio, data_fim)
        flash("Trabalho atribuído com sucesso!", "success")
        return redirect(url_for('detalhes_funcionario', emp_id=func_id))

    return render_template('trabalho_novo.html', funcionario=funcionario)


def get_funcionarios(filtros=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM funcionarios"
    params = []
    where = []
    if filtros:
        if filtros.get('busca'):
            where.append("(LOWER(nome) LIKE %s OR LOWER(cargo) LIKE %s)")
            busca = f"%{filtros['busca'].lower()}%"
            params.extend([busca, busca])
        if filtros.get('cargo'):
            where.append("cargo = %s")
            params.append(filtros['cargo'])
        if filtros.get('estado_civil'):
            where.append("estado_civil = %s")
            params.append(filtros['estado_civil'])
    if where:
        sql += " WHERE " + " AND ".join(where)
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_funcionario_by_id(emp_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM funcionarios WHERE id = %s", (emp_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def add_funcionario_db(func):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO funcionarios (nome, cargo, salario, estado_civil, foto) VALUES (%s, %s, %s, %s, %s)",
        (func['nome'], func['cargo'], func['salario'], func['estado_civil'], func['foto'])
    )
    conn.commit()
    cursor.close()
    conn.close()

def update_funcionario_db(emp_id, func):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE funcionarios SET nome=%s, cargo=%s, salario=%s, estado_civil=%s, foto=%s WHERE id=%s",
        (func['nome'], func['cargo'], func['salario'], func['estado_civil'], func['foto'], emp_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def delete_funcionario_db(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM funcionarios WHERE id=%s", (emp_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_positions_and_statuses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT cargo FROM funcionarios")
    positions = set(row[0] for row in cursor.fetchall())
    cursor.execute("SELECT DISTINCT estado_civil FROM funcionarios")
    statuses = set(row[0] for row in cursor.fetchall())
    cursor.close()
    conn.close()
    return positions, statuses

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def add_user_db(username, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    conn.commit()
    cursor.close()
    conn.close()

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return User(user['id'], user['username'], user['password_hash'])
    return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@login_required
def index():
    funcionarios = get_funcionarios()
    positions, _ = get_all_positions_and_statuses()
    total_employees = len(funcionarios)
    total_positions = len(positions)
    year = datetime.now().year
    return render_template('index.html', total_employees=total_employees, total_positions=total_positions, year=year)

@app.route('/funcionarios')
def list_funcionarios():
    busca = request.args.get('busca', '').strip().lower()
    cargo = request.args.get('cargo', '').strip()
    estado_civil = request.args.get('estado_civil', '').strip()
    filtros = {'busca': busca, 'cargo': cargo, 'estado_civil': estado_civil}
    funcionarios = get_funcionarios(filtros)
    positions, marital_statuses = get_all_positions_and_statuses()
    year = datetime.now().year
    return render_template('list.html', employees=funcionarios, positions=positions, marital_statuses=marital_statuses, year=year)

@app.route('/novo', methods=['GET', 'POST'])
def add_funcionario():
    errors = {}
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cargo = request.form.get('cargo', '').strip()
        salario = request.form.get('salario', '').strip()
        estado_civil = request.form.get('estado_civil', '').strip()
        foto = request.files.get('foto')

        if not nome:
            errors['nome'] = 'Nome é obrigatório.'
        if not cargo:
            errors['cargo'] = 'Cargo é obrigatório.'
        if not estado_civil:
            errors['estado_civil'] = 'Estado civil é obrigatório.'
        try:
            salario_val = float(salario)
            if salario_val < 0:
                errors['salario'] = 'Salário não pode ser negativo.'
        except:
            errors['salario'] = 'Salário inválido.'

        filename = ''
        if foto and foto.filename:
            if allowed_file(foto.filename):
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{foto.filename}")
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(save_path)
            else:
                errors['foto'] = 'Formato de imagem não permitido.'

        if not errors:
            funcionario = {
                'nome': nome,
                'cargo': cargo,
                'salario': salario_val,
                'estado_civil': estado_civil,
                'foto': filename
            }
            add_funcionario_db(funcionario)
            flash('Funcionário adicionado com sucesso!', 'success')
            return redirect(url_for('list_funcionarios'))
        else:
            flash('Erro ao adicionar funcionário.', 'error')

    year = datetime.now().year
    return render_template('add.html', errors=errors, year=year)

@app.route('/editar/<emp_id>', methods=['GET', 'POST'])
def edit_funcionario(emp_id):
    funcionario = get_funcionario_by_id(emp_id)
    if not funcionario:
        flash('Funcionário não encontrado.', 'error')
        return redirect(url_for('list_funcionarios'))

    errors = {}
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cargo = request.form.get('cargo', '').strip()
        salario = request.form.get('salario', '').strip()
        estado_civil = request.form.get('estado_civil', '').strip()
        foto = request.files.get('foto')

        if not nome:
            errors['nome'] = 'Nome é obrigatório.'
        if not cargo:
            errors['cargo'] = 'Cargo é obrigatório.'
        if not estado_civil:
            errors['estado_civil'] = 'Estado civil é obrigatório.'
        try:
            salario_val = float(salario)
            if salario_val < 0:
                errors['salario'] = 'Salário não pode ser negativo.'
        except:
            errors['salario'] = 'Salário inválido.'

        filename = funcionario['foto'] if funcionario['foto'] else ''
        if foto and foto.filename:
            if allowed_file(foto.filename):
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{foto.filename}")
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(save_path)
            else:
                errors['foto'] = 'Formato de imagem não permitido.'

        if not errors:
            funcionario_update = {
                'nome': nome,
                'cargo': cargo,
                'salario': salario_val,
                'estado_civil': estado_civil,
                'foto': filename
            }
            update_funcionario_db(emp_id, funcionario_update)
            flash('Funcionário editado com sucesso!', 'success')
            return redirect(url_for('list_funcionarios'))
        else:
            flash('Erro ao editar funcionário.', 'error')

    year = datetime.now().year
    return render_template('edit.html', funcionario=funcionario, errors=errors, year=year)

@app.route('/remover/<emp_id>', methods=['POST'])
def remover_funcionario(emp_id):
    funcionario = get_funcionario_by_id(emp_id)
    if funcionario:
        delete_funcionario_db(emp_id)
        flash('Funcionário removido com sucesso.', 'success')
    else:
        flash('Funcionário não encontrado.', 'error')
    return redirect(url_for('list_funcionarios'))

@app.route('/registro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user:
            flash('Usuário já existe.', 'error')
        else:
            password_hash = generate_password_hash(password)
            add_user_db(username, password_hash)
            flash('Registro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            login_user(User(user['id'], user['username'], user['password_hash']))
            flash('Login realizado com sucesso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
