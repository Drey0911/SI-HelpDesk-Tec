from flask import render_template, request, redirect, url_for, flash, session
from Models.users import User
import bcrypt

class UsersController:
    @staticmethod
    def index():
        # Verificar que el usuario sea ADMIN
        if 'user_id' not in session:
            flash('Por favor inicie sesión primero.', 'error')
            return redirect(url_for('index'))
        
        user = User.findByEmail(session.get('user_email'))
        if not user or user['role'] != 'ADMIN':
            flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
            return redirect(url_for('home'))
        
        # Obtener todos los usuarios
        users = User.find_all()
        return render_template('Home/usuarios.html', user=user, users=users)

    @staticmethod
    def create():
        # Verificar que el usuario sea ADMIN
        if 'user_id' not in session:
            flash('Por favor inicie sesión primero.', 'error')
            return redirect(url_for('index'))
        
        user = User.findByEmail(session.get('user_email'))
        if not user or user['role'] != 'ADMIN':
            flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            data = {
                'name': request.form.get('name', '').strip(),
                'lastname': request.form.get('lastname', '').strip(),
                'status': int(request.form.get('status', 1)),
                'phone': request.form.get('phone', '').strip(),
                'email': request.form.get('email', '').strip(),
                'password': request.form.get('password', '').strip(),
                'DNI': request.form.get('dni', '').strip(),
                'role': request.form.get('role', 'USER').strip(),
                'creationDate': request.form.get('creationDate', '')
            }
            
            # Validaciones
            if not all([data['name'], data['lastname'], data['email'], data['password']]):
                flash('Complete todos los campos obligatorios.', 'error')
                return redirect(url_for('users'))
            
            if User.findByEmail(data['email']):
                flash('El email ya está registrado.', 'error')
                return redirect(url_for('users'))
            
            # Si no se proporciona fecha, usar la actual
            if not data['creationDate']:
                from datetime import datetime
                data['creationDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if User.register(data):
                flash('Usuario creado exitosamente.', 'success')
            else:
                flash('Error al crear el usuario.', 'error')
            
            return redirect(url_for('users'))
        
        return redirect(url_for('users'))

    @staticmethod
    def update(user_id):
        # Verificar que el usuario sea ADMIN
        if 'user_id' not in session:
            flash('Por favor inicie sesión primero.', 'error')
            return redirect(url_for('index'))
        
        user = User.findByEmail(session.get('user_email'))
        if not user or user['role'] != 'ADMIN':
            flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            data = {}
            
            # Campos editables
            editable_fields = ['name', 'lastname', 'status', 'phone', 'role']
            for field in editable_fields:
                if request.form.get(field):
                    data[field] = request.form.get(field)
            
            # Campo de password (opcional)
            if request.form.get('password'):
                hashed_password = bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt())
                data['password'] = hashed_password.decode('utf-8')
            
            if data:
                if User.update(user_id, data):
                    flash('Usuario actualizado exitosamente.', 'success')
                else:
                    flash('Error al actualizar el usuario.', 'error')
            
            return redirect(url_for('users'))
        
        return redirect(url_for('users'))

    @staticmethod
    def delete(user_id):
        # Verificar que el usuario sea ADMIN
        if 'user_id' not in session:
            flash('Por favor inicie sesión primero.', 'error')
            return redirect(url_for('index'))
        
        user = User.findByEmail(session.get('user_email'))
        if not user or user['role'] != 'ADMIN':
            flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
            return redirect(url_for('home'))
        
        # No permitir auto-eliminación
        if int(user_id) == user['id']:
            flash('No puede eliminarse a sí mismo.', 'error')
            return redirect(url_for('users'))
        
        if User.delete(user_id):
            flash('Usuario eliminado exitosamente.', 'success')
        else:
            flash('Error al eliminar el usuario.', 'error')
        
        return redirect(url_for('users'))