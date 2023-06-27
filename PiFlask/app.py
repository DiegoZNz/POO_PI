from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask import flash
import bcrypt


app = Flask(__name__, static_folder='static')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_cafeteria'
mysql = MySQL(app)
app.secret_key = "mi_clave_secreta"



@app.route('/')
def index():
    # Ejecutar una consulta SQL simple
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()

    if result:
        return render_template('login.html')
    else:
        return "No se pudo conectar a la base de datos"

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        Vmatricula = request.form['txtMatricula_login']
        Vpassword = request.form['txtContrasena_login']

        CS = mysql.connection.cursor()
        CS.execute("SELECT COUNT(*) FROM tbusuarios WHERE matricula=%s", (Vmatricula,))
        userCount = CS.fetchone()[0]
        if userCount == 0:
            flash(f"El usuario {Vmatricula} NO existe", 'error')
            return redirect('/login')

        CS.execute("SELECT contrasena FROM tbusuarios WHERE matricula=%s", (Vmatricula,))
        conEncriptada = CS.fetchone()[0]

        if bcrypt.checkpw(Vpassword.encode(), conEncriptada.encode()):
            CS.execute("SELECT nombre from tbusuarios WHERE matricula =%s", (Vmatricula,))
            nombre = CS.fetchone()[0]
            flash(f'Bienvenido {nombre}!')
        else:
            flash("Contraseña incorrecta", 'error')
        
        

    return redirect(url_for('index'))

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        Vnombre = request.form['txtNombre_guardar']
        VapellidoPaterno = request.form['txtApellidoPaterno_guardar']
        VapellidoMaterno = request.form['txtApellidoMaterno_guardar']
        Vmatricula = request.form['txtMatricula_guardar']
        VcorreoElectronico = request.form['txtCorreoElectronico_guardar']
        Vcontrasena = request.form['txtContrasena_guardar'] 
        
        conH=encriptarContrasena(Vcontrasena)
        
        CS = mysql.connection.cursor()
        CS.execute("SELECT * FROM tbusuarios WHERE matricula=%s", (Vmatricula,))
        usuario_existente = CS.fetchone()
        if usuario_existente is not None:
            flash(f"El usuario {Vmatricula} ya existe", 'error')
            return redirect('/login')
        else:
            CS.execute('INSERT INTO tbusuarios (nombre, ap, am, matricula, correo, contrasena) values (%s, %s, %s, %s, %s, %s)', (Vnombre, VapellidoPaterno, VapellidoMaterno, Vmatricula, VcorreoElectronico, conH))
            mysql.connection.commit()
            flash('El usuario se ha agregado correctamente.')
    return redirect(url_for('index'))


def encriptarContrasena(password):
    sal = bcrypt.gensalt()
    conHa = bcrypt.hashpw(password.encode(), sal)
    return conHa



@app.route('/login')
def dashboard():
    return render_template('main.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/pedidos')
def pedidos():
    return render_template('navbar.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
