# Sistema de HelpDesk

# Sistema de despliegue 
Para este sistema se utilizo el deploy con RENDER en: https://si-helpdesk-tec.onrender.com

# Dificultades
La principal y unica dificultad fue el host de la base de datos, ya que se uso con MySQL, librerias y conectores en python, asi que para evitar una tediosa y larga migracion, se opto por usar Clever Cloud.

## Descripción General
Sistema de gestión de tickets de soporte técnico que permite a los usuarios crear, gestionar y dar seguimiento a incidencias técnicas. La aplicación está desarrollada con Flask y utiliza MySQL como base de datos.

## Estructura del Proyecto

```
HelpDesk/
├── Config/               # Configuración de la base de datos
├── Controllers/          # Controladores de la aplicación
├── Models/               # Modelos de datos
├── Static/               # Archivos estáticos (CSS, JS, imágenes)
├── templates/            # Plantillas HTML con jinja2
├── app.py                # Punto de entrada de la aplicación
└── requirements.txt      # Dependencias del proyecto
```

## Roles de Usuario
El sistema maneja tres roles de usuario:
- **ADMIN**: Acceso completo al sistema, puede gestionar usuarios y todos los tickets.
- **TEC** (Técnico): Puede ver y gestionar tickets asignados a él.
- **USER**: Puede crear tickets y ver el estado de sus propios tickets.

## Modelos de Datos

### Usuario (User)
Gestiona la información de los usuarios del sistema.
- **Atributos**: id, name, lastname, status, phone, email, password, DNI, role, creationDate
- **Métodos principales**:
  - `register()`: Registra un nuevo usuario
  - `findByEmail()`: Busca un usuario por su correo electrónico
  - `findById()`: Busca un usuario por su ID
  - `find_all()`: Obtiene todos los usuarios

### Ticket
Gestiona la información de los tickets de soporte.
- **Atributos**: id, titulo, descripcion, estado, idUsuario, idTecnico, prioridad, departamento, fecha_creacion
- **Métodos principales**:
  - `create()`: Crea un nuevo ticket
  - `delete()`: Elimina un ticket existente
  - `find_by_user()`: Encuentra tickets por usuario
  - `find_by_technician()`: Encuentra tickets asignados a un técnico
  - `find_all()`: Obtiene todos los tickets
  - `update()`: Actualiza la información de un ticket

## Controladores

### TicketsController
Maneja la lógica de negocio relacionada con los tickets.
- **Métodos**:
  - `index()`: Muestra la lista de tickets según el rol del usuario
  - `create()`: Crea un nuevo ticket
  - `update()`: Actualiza un ticket existente
  - `delete()`: Elimina un ticket

### UsersController
Maneja la lógica de negocio relacionada con los usuarios.
- **Métodos**:
  - `index()`: Muestra la lista de usuarios (solo para ADMIN)
  - `create()`: Crea un nuevo usuario
  - `update()`: Actualiza un usuario existente
  - `delete()`: Elimina un usuario

## Rutas Principales

### Autenticación
- `/`: Página de inicio de sesión
- `/signup`: Registro de nuevos usuarios
- `/logout`: Cierre de sesión

### Tickets
- `/tickets`: Visualización de tickets según el rol
- `/tickets/create`: Creación de tickets
- `/tickets/update/<id>`: Actualización de tickets
- `/tickets/delete/<id>`: Eliminación de tickets

### Usuarios (solo ADMIN)
- `/users`: Gestión de usuarios
- `/users/create`: Creación de usuarios
- `/users/update/<id>`: Actualización de usuarios
- `/users/delete/<id>`: Eliminación de usuarios

## Interfaz de Usuario
El sistema cuenta con una interfaz web responsive que permite:
- Inicio de sesión y registro de usuarios
- Dashboard principal con resumen de actividad
- Gestión de tickets con filtros y búsquedas
- Gestión de usuarios (para administradores)

## Tecnologías Utilizadas
- **Backend**: Python, Flask
- **Base de Datos**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Seguridad**: bcrypt para encriptación de contraseñas

## Instalación y Configuración

1. Clonar el repositorio
2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Configurar la base de datos en `Config/conection.py`
4. Ejecutar la aplicación:
   ```
   python app.py
   ```
5. Acceder a la aplicación en `http://localhost:5000` o el host al que se suba o con contenedores en docker

## Flujo de Trabajo

1. Los usuarios se registran en el sistema
2. Los usuarios pueden crear tickets especificando título, descripción y departamento
3. Los administradores pueden asignar tickets a técnicos
4. Los técnicos pueden actualizar el estado de los tickets
5. Los usuarios pueden ver el estado de sus tickets en todo momento

## Seguridad
- Contraseñas encriptadas con bcrypt
- Sesiones seguras con Flask
- Validación de permisos según rol de usuario