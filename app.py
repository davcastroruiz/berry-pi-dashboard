from flask import Flask, render_template, redirect, url_for, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from apis import obtener_noticias_nba
from enums import NBA_Team

# Configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'  # Base de datos SQLite
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Inicializar Flask-Migrate
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Vista de login si el usuario no está autenticado

# Modelo de Usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    favorite_teams = db.Column(db.String(500), nullable=True)  # Guardamos los equipos como una cadena separada por comas

    def set_favorite_teams(self, teams):
        """Guarda los equipos favoritos como una cadena separada por comas"""
        self.favorite_teams = ",".join([team.value for team in teams])

    def get_favorite_teams(self):
        """Devuelve los equipos favoritos como una lista de enums"""
        if self.favorite_teams:
            return [NBA_Team(team) for team in self.favorite_teams.split(",")]
        return []

# Función para cargar el usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/select-favorites', methods=['GET', 'POST'])
@login_required
def select_favorites():
    if request.method == 'POST':
        selected_teams = request.form.getlist('favorite_teams')  # Lista con los equipos seleccionados
        user = User.query.get(current_user.id)  # Obtener usuario actual
        user.set_favorite_teams([NBA_Team(team) for team in selected_teams])  # Guardar en la DB
        db.session.commit()
        return redirect(url_for('dashboard'))  # Redirigir al dashboard

    return render_template('select_favorites.html', teams=NBA_Team)

# Ruta de Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, 'pbkdf2')  # Encriptamos la contraseña
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Ruta de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):  # Compara la contraseña con el hash
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

# Ruta de Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Ruta protegida (requiere login)
@app.route('/')
@login_required
def dashboard():
    favorite_teams = current_user.favorite_teams.split(",") if current_user.favorite_teams else []
    noticias = obtener_noticias_nba(favorite_teams)
    return render_template('dashboard.html', noticias=noticias,  user=current_user)

# Inicializar la base de datos si no existe
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)
