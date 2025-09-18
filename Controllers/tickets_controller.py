from flask import render_template, request, redirect, url_for, flash, session
from Models.tickets import Ticket
from Models.users import User
from datetime import datetime

class TicketsController:
    @staticmethod
    def index():
        if 'user_id' not in session:
            flash('Por favor inicie sesión primero, Acceso Denegado.', 'error')
            return redirect(url_for('index'))
        
        user = User.findByEmail(session.get('user_email'))
        if not user:
            return redirect(url_for('logout'))
        
        # Obtener tickets según el rol del usuario
        if user['role'] == 'ADMIN':
            tickets = Ticket.find_all()
        elif user['role'] == 'TEC':
            tickets = Ticket.find_by_technician(user['id'])
        else:  # USER
            tickets = Ticket.find_by_user(user['id'])
        
        # Obtener técnicos para el formulario de asignación (para ADMIN y USER)
        technicians = []
        if user['role'] in ['ADMIN', 'USER']:
            technicians = Ticket.get_technicians()
        
        return render_template('Home/tickets.html', 
                             user=user, 
                             tickets=tickets, 
                             technicians=technicians)

    @staticmethod
    def create():
        if 'user_id' not in session:
            flash('Por favor inicie sesión primero, Acceso Denegado.', 'error')
            return redirect(url_for('index'))
        
        user = User.findByEmail(session.get('user_email'))
        if not user:
            return redirect(url_for('logout'))
        
        if request.method == 'POST':
            # establecer prioridad por defecto
            data = {
                'titulo': request.form.get('titulo', '').strip(),
                'descripcion': request.form.get('descripcion', '').strip(),
                'estado': 'Abierto',
                'idUsuario': user['id'],
                'prioridad': 'Media',
                'departamento': request.form.get('departamento', 'Tecnología').strip(),
                'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Agregar idTecnico si se proporciona (solo para USER)
            if user['role'] == 'USER':
                id_tecnico = request.form.get('idTecnico')
                if id_tecnico and id_tecnico != '':
                    data['idTecnico'] = id_tecnico
            
            # Validaciones
            if not all([data['titulo'], data['descripcion']]):
                flash('Complete todos los campos obligatorios.', 'error')
                return redirect(url_for('tickets'))
            
            # Crear el ticket
            ticket_id = Ticket.create(data)
            if ticket_id:
                flash('Ticket creado exitosamente.', 'success')
            else:
                flash('Error al crear el ticket.', 'error')
            
            return redirect(url_for('tickets'))
        
        return redirect(url_for('tickets'))

    @staticmethod
    def delete(ticket_id):
        if 'user_id' not in session:
            flash('Por favor inicie sesión primero, Acceso Denegado.', 'error')
            return redirect(url_for('index'))
        
        user = User.findByEmail(session.get('user_email'))
        if not user:
            return redirect(url_for('logout'))
        
        # Verificar que el ticket existe
        ticket = Ticket.find_by_id(ticket_id)
        if not ticket:
            flash('Ticket no encontrado.', 'error')
            return redirect(url_for('tickets'))
        
        # Solo USER puede eliminar sus propios tickets
        if user['role'] != 'USER' or ticket['idUsuario'] != user['id']:
            flash('No tiene permisos para eliminar este ticket.', 'error')
            return redirect(url_for('tickets'))
        
        # Eliminar el ticket
        if Ticket.delete(ticket_id):
            flash('Ticket eliminado exitosamente.', 'success')
        else:
            flash('Error al eliminar el ticket.', 'error')
        
        return redirect(url_for('tickets'))

    @staticmethod
    def update(ticket_id):
        if 'user_id' not in session:
            flash('Por favor inicie sesión primero, Acceso Denegado.', 'error')
            return redirect(url_for('index'))
        
        user = User.findByEmail(session.get('user_email'))
        if not user:
            return redirect(url_for('logout'))
        
        # Verificar permisos
        ticket = Ticket.find_by_id(ticket_id)
        if not ticket:
            flash('Ticket no encontrado.', 'error')
            return redirect(url_for('tickets'))
        
        # USER solo puede ver sus propios tickets, no editarlos
        if user['role'] == 'USER' and ticket['idUsuario'] != user['id']:
            flash('No tiene permisos para editar este ticket.', 'error')
            return redirect(url_for('tickets'))
        
        # TEC solo puede editar tickets asignados a él
        if user['role'] == 'TEC' and ticket['idTecnico'] != user['id']:
            flash('No tiene permisos para editar este ticket.', 'error')
            return redirect(url_for('tickets'))
        
        if request.method == 'POST':
            data = {}
            
            # ADMIN puede editar todos los campos
            if user['role'] == 'ADMIN':
                if request.form.get('estado'):
                    data['estado'] = request.form.get('estado')
                if request.form.get('idTecnico'):
                    data['idTecnico'] = request.form.get('idTecnico')
                if request.form.get('prioridad'):
                    data['prioridad'] = request.form.get('prioridad')
                if request.form.get('departamento'):
                    data['departamento'] = request.form.get('departamento')
            
            # TEC solo puede cambiar el estado
            elif user['role'] == 'TEC':
                if request.form.get('estado'):
                    data['estado'] = request.form.get('estado')
            
            if data:
                if Ticket.update(ticket_id, data):
                    flash('Ticket actualizado exitosamente.', 'success')
                else:
                    flash('Error al actualizar el ticket.', 'error')
            
            return redirect(url_for('tickets'))
        
        return redirect(url_for('tickets'))