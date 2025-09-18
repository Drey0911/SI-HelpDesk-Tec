import bcrypt
from Config.conection import db
from datetime import datetime

# Clase de modelo de usuario
class User:
    
    # Método estático para registrar un usuario
    @staticmethod
    def register(data):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = """
                INSERT INTO user (name, lastname, status, phone, email, password, DNI, role, creationDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                # Hash password con bcrypt
                hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                values = (
                    data['name'],
                    data['lastname'],
                    data['status'],
                    data['phone'],
                    data['email'],
                    hashed_password.decode('utf-8'),
                    data['DNI'],
                    data.get('role', 'USER'),
                    data['creationDate']
                )
                cursor.execute(query, values)
                connection.commit()
                return True
            except Exception as e:
                print(f"Error registering user: {e}")
                return False
            finally:
                if cursor:
                    cursor.close()
        return False
    
    # Método estático para encontrar un usuario por su email
    @staticmethod
    def findByEmail(email):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM user WHERE email = %s"
                cursor.execute(query, (email,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error finding user by email: {e}")
                return None
            finally:
                if cursor:
                    cursor.close()
        return None

    # Método estático para encontrar un usuario por su ID
    @staticmethod
    def findById(user_id):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM user WHERE id = %s"
                cursor.execute(query, (user_id,))
                return cursor.fetchone()
            except Exception as e:
                print(f"Error finding user by ID: {e}")
                return None
            finally:
                if cursor:
                    cursor.close()
        return None

    # Método estático para obtener todos los usuarios
    @staticmethod
    def find_all():
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM user ORDER BY creationDate DESC"
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                print(f"Error finding all users: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
        return []

    # Método estático para actualizar un usuario
    @staticmethod
    def update(user_id, data):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                
                # Construir la consulta dinámicamente
                set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
                values = list(data.values())
                values.append(user_id)
                
                query = f"UPDATE user SET {set_clause} WHERE id = %s"
                cursor.execute(query, values)
                connection.commit()
                return True
            except Exception as e:
                print(f"Error updating user: {e}")
                return False
            finally:
                if cursor:
                    cursor.close()
        return False

    # Método estático para eliminar un usuario
    @staticmethod
    def delete(user_id):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = "DELETE FROM user WHERE id = %s"
                cursor.execute(query, (user_id,))
                connection.commit()
                return True
            except Exception as e:
                print(f"Error deleting user: {e}")
                return False
            finally:
                if cursor:
                    cursor.close()
        return False

    # Método estático para obtener usuarios por rol
    @staticmethod
    def findByRole(role):
        connection = db.get_connection()
        if connection:
            cursor = None
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM user WHERE role = %s ORDER BY name"
                cursor.execute(query, (role,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Error finding users by role: {e}")
                return []
            finally:
                if cursor:
                    cursor.close()
        return []