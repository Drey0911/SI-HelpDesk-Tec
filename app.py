from flask import Flask, render_template, request, redirect, url_for, flash, session
import bcrypt
from Models.users import User
from datetime import datetime
from Controllers.tickets_controller import TicketsController
from Controllers.users_controller import UsersController
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) # para mensajes flash

# Configuración de la carpeta estática
app.static_folder = 'Static'
app.static_url_path = '/Static'


# Ruta para la página de aterrizaje (login)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            flash('Complete todos los campos.', 'error')
            return redirect(url_for('index'))
        
        user = User.findByEmail(email)
        
        if not user:
            flash('Email o contraseña incorrectos.', 'error')
            return redirect(url_for('index'))
        
        # Verificar contraseña con bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            return redirect(url_for('home'))
        else:
            flash('Email o contraseña incorrectos.', 'error')
    
    return render_template('index.html')




# Ruta para la página de registro
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        repeat_password = request.form.get('repeat_password', '').strip()
        role = request.form.get('role', '').strip()
        
        if not all([email, password, repeat_password]):
            flash('Complete todos los campos.', 'error')
            return redirect(url_for('signup'))
            
        if password != repeat_password:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('signup'))
            
        data = {
            'name': request.form.get('name', '').strip(),
            'lastname': request.form.get('lastname', '').strip(),
            'status': 1,
            'phone': request.form.get('phone', '').strip(),
            'email': email,
            'password': password,
            'DNI': request.form.get('dni', '').strip(),
            'role': 'USER',
            'creationDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if User.register(data):
            flash('Usuario registrado exitosamente. Por favor inicie sesión.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Error al registrar usuario. El email ya podría estar en uso.', 'error')
    
    return render_template('sign-up.html')



# Ruta para la página de inicio del usuario
@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('Por favor inicie sesión primero, Acceso Denegado.', 'error')
        return redirect(url_for('index'))
    
    user = User.findByEmail(session.get('user_email'))
    if not user:
        return redirect(url_for('logout'))
    
    # Pasamos los datos del usuario a la plantilla
    return render_template('Home/home.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('index'))

# Rutas para tickets (ADMIN, USUARIO y TECNICO)

@app.route('/tickets')
def tickets():
    return TicketsController.index()

@app.route('/tickets/create', methods=['POST'])
def create_ticket():
    return TicketsController.create()

@app.route('/tickets/update/<int:ticket_id>', methods=['POST'])
def update_ticket(ticket_id):
    return TicketsController.update(ticket_id)

@app.route('/tickets/delete/<int:ticket_id>', methods=['POST'])
def delete_ticket(ticket_id):
    return TicketsController.delete(ticket_id)

# Rutas para usuarios (solo ADMIN)

@app.route('/users')
def users():
    return UsersController.index()

@app.route('/users/create', methods=['POST'])
def create_user():
    return UsersController.create()

@app.route('/users/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    return UsersController.update(user_id)

@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    return UsersController.delete(user_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)