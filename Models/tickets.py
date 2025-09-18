from Config.conection import db
from datetime import datetime

class Ticket:
    @staticmethod
    def create(data):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                
                # Verificar si se proporciona idTecnico 
                if 'idTecnico' in data:
                    query = """
                    INSERT INTO tickets (titulo, descripcion, estado, idUsuario, idTecnico, prioridad, departamento, fecha_creacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        data['titulo'],
                        data['descripcion'],
                        data.get('estado', 'Abierto'),
                        data['idUsuario'],
                        data['idTecnico'],  
                        data.get('prioridad', 'Media'),
                        data['departamento'],
                        data['fecha_creacion']
                    )
                else:
                    query = """
                    INSERT INTO tickets (titulo, descripcion, estado, idUsuario, prioridad, departamento, fecha_creacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        data['titulo'],
                        data['descripcion'],
                        data.get('estado', 'Abierto'),
                        data['idUsuario'],
                        data.get('prioridad', 'Media'),
                        data['departamento'],
                        data['fecha_creacion']
                    )
                
                cursor.execute(query, values)
                connection.commit()
                return cursor.lastrowid
            except Exception as e:
                print(f"Error creating ticket: {e}")
                return False
            finally:
                if cursor:
                    cursor.close()
        return False

    @staticmethod
    def delete(ticket_id):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor()
                query = "DELETE FROM tickets WHERE id = %s"
                cursor.execute(query, (ticket_id,))
                connection.commit()
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error deleting ticket: {e}")
                return False
            finally:
                if cursor:
                    cursor.close()
        return False

    @staticmethod
    def find_by_user(user_id):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = """
                SELECT t.*, u.name as usuario_nombre, u.lastname as usuario_apellido, 
                       tec.name as tecnico_nombre, tec.lastname as tecnico_apellido
                FROM tickets t
                LEFT JOIN user u ON t.idUsuario = u.id
                LEFT JOIN user tec ON t.idTecnico = tec.id
                WHERE t.idUsuario = %s
                ORDER BY t.fecha_creacion DESC
                """
                cursor.execute(query, (user_id,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error finding tickets by user: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
        return []

    @staticmethod
    def find_by_technician(technician_id):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = """
                SELECT t.*, u.name as usuario_nombre, u.lastname as usuario_apellido, 
                       tec.name as tecnico_nombre, tec.lastname as tecnico_apellido
                FROM tickets t
                LEFT JOIN user u ON t.idUsuario = u.id
                LEFT JOIN user tec ON t.idTecnico = tec.id
                WHERE t.idTecnico = %s
                ORDER BY t.fecha_creacion DESC
                """
                cursor.execute(query, (technician_id,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error finding tickets by technician: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
        return []

    @staticmethod
    def find_all():
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = """
                SELECT t.*, u.name as usuario_nombre, u.lastname as usuario_apellido, 
                       tec.name as tecnico_nombre, tec.lastname as tecnico_apellido
                FROM tickets t
                LEFT JOIN user u ON t.idUsuario = u.id
                LEFT JOIN user tec ON t.idTecnico = tec.id
                ORDER BY t.fecha_creacion DESC
                """
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error finding all tickets: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
        return []

    @staticmethod
    def find_by_id(ticket_id):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = """
                SELECT t.*, u.name as usuario_nombre, u.lastname as usuario_apellido, 
                       tec.name as tecnico_nombre, tec.lastname as tecnico_apellido
                FROM tickets t
                LEFT JOIN user u ON t.idUsuario = u.id
                LEFT JOIN user tec ON t.idTecnico = tec.id
                WHERE t.id = %s
                """
                cursor.execute(query, (ticket_id,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error finding ticket by ID: {e}")
                return None
            finally:
                if cursor:
                    cursor.close()
        return None

    @staticmethod
    def update(ticket_id, data):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                # Construir la consulta dinámicamente 
                set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
                values = list(data.values())
                values.append(ticket_id)
                
                query = f"UPDATE tickets SET {set_clause} WHERE id = %s"
                cursor.execute(query, values)
                connection.commit()
                return True
            except Exception as e:
                print(f"Error updating ticket: {e}")
                return False
            finally:
                if cursor:
                    cursor.close()
        return False

    @staticmethod
    def get_technicians():
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT id, name, lastname FROM user WHERE role = 'TEC'"
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error getting technicians: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
        return []