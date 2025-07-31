# Importamos lo necesario para crear la página web
from flask import Flask, render_template, request, redirect
# Importamos lo necesario para manejar la base de datos
import sqlite3

# Creamos la aplicación
app = Flask(__name__)

# Esta función se encarga de crear la base de datos y la tabla si no existen
def init_db():
    conn = sqlite3.connect('alumnos.db')  # Abrimos conexión con el archivo de base de datos
    cursor = conn.cursor()  # Creamos un objeto para enviar instrucciones a la base
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumno (  -- Creamos la tabla solo si no existe
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único que se crea solo
            nombre TEXT NOT NULL,  -- Nombre del alumno, obligatorio
            apellido TEXT NOT NULL,  -- Apellido del alumno, obligatorio
            edad INTEGER NOT NULL,  -- Edad, obligatoria
            activo INTEGER NOT NULL DEFAULT 1  -- Campo para saber si está activo o eliminado (1 = activo, 0 = eliminado)
        )
    ''')
    conn.commit()  # Guardamos los cambios
    conn.close()   # Cerramos la conexión

# Ruta principal, donde se muestran los alumnos activos
@app.route('/')
def index():
    try:
        conn = sqlite3.connect('alumnos.db')  # Abrimos la base de datos
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alumno WHERE activo=1")  # Solo se muestran los que no han sido eliminados
        alumnos = cursor.fetchall()  # Obtenemos todos los alumnos
        conn.close()
        return render_template('index.html', alumnos=alumnos)  # Mostramos los datos en la página
    except Exception as e:
        return f"Error al cargar los alumnos: {e}"  # Si algo falla, mostramos el error

# Ruta que muestra el formulario para agregar un nuevo alumno
@app.route('/agregar')
def agregar():
    return render_template('agregar.html')  # Muestra la página del formulario

# Ruta que guarda el nuevo alumno en la base de datos
@app.route('/guardar', methods=['POST'])
def guardar():
    # Tomamos los datos del formulario y los ponemos con la primera letra en mayúscula
    nombre = request.form['nombre'].capitalize()
    apellido = request.form['apellido'].capitalize()
    edad = request.form['edad']

    # Guardamos los datos en la base de datos
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alumno (nombre, apellido, edad, activo) VALUES (?, ?, ?, 1)", (nombre, apellido, edad))
    conn.commit()
    conn.close()
    return redirect('/')  # Volvemos a la página principal

# Ruta que muestra el formulario para editar un alumno
@app.route('/editar/<int:id>')
def editar(id):
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumno WHERE id=?", (id,))  # Buscamos al alumno por su ID
    alumno = cursor.fetchone()
    conn.close()
    return render_template('editar.html', alumno=alumno)  # Mostramos el formulario con los datos actuales

# Ruta que actualiza los datos del alumno después de editarlos
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nombre = request.form['nombre'].capitalize()
    apellido = request.form['apellido'].capitalize()
    edad = request.form['edad']

    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE alumno SET nombre=?, apellido=?, edad=? WHERE id=?", (nombre, apellido, edad, id))
    conn.commit()
    conn.close()
    return redirect('/')  # Regresamos a la lista principal

# Ruta que "elimina" un alumno marcándolo como inactivo (no se borra realmente)
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE alumno SET activo=0 WHERE id=?", (id,))  # Cambiamos el valor de activo a 0
    conn.commit()
    conn.close()
    return redirect('/')  # Volvemos a la página principal

# Este bloque se asegura de que todo inicie bien cuando ejecutamos el archivo
if __name__ == '__main__':
    init_db()  # Creamos la tabla si no existe
    app.run(debug=True)  # Iniciamos la aplicación
