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
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        if result:
            return render_template('index.html')
        else:
            return "No se pudo conectar a la base de datos"
    except Exception as e:
        return f"Error de conexión a la base de datos: {str(e)}"
    
@app.route('/login', methods=['POST'])
def login():
    Vmatricula = request.form['txtMatricula_login']
    Vpassword = request.form['txtContrasena_login']

    CS = mysql.connection.cursor()
    CS.execute("SELECT COUNT(*) FROM tbusuarios WHERE matricula=%s", (Vmatricula,))
    userCount = CS.fetchone()[0]
    if userCount == 0:
        flash(f"El usuario {Vmatricula} NO existe", 'error')
        return redirect('/')

    CS.execute("SELECT contrasena, id_tipo_permiso FROM tbusuarios WHERE matricula=%s", (Vmatricula,))
    result = CS.fetchone()
    if result:
        conEncriptada = result[0]
        idTipoPermiso = result[1]

        if bcrypt.checkpw(Vpassword.encode(), conEncriptada.encode()):
            CS.execute("SELECT nombre FROM tbusuarios WHERE matricula=%s", (Vmatricula,))
            nombre = CS.fetchone()[0]
            flash(f'Bienvenido {nombre}!')

            if idTipoPermiso == 1:
                return redirect('/clientes')  # Ruta del administrador
            elif idTipoPermiso == 2:
                return redirect('/usrmenu')  # Ruta del cliente
        else:
            flash("Contraseña incorrecta", 'error')
    else:
        flash("Error al obtener datos del usuario", 'error')

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



@app.route('/clientes')
def menu():
    return render_template('clientes.html')

@app.route('/pedidos')
def pedidos():
    return render_template('pedidos.html')

@app.route('/agregar-admin')
def clientes():
    return render_template('adm_add.html')

@app.route('/usuarios-penalizados')
def upena():
    return render_template('adm_Upenalizados.html')

@app.route('/cerrar-sesion')
def LogO():
    return render_template('index.html')

@app.route('/usrmenu')
def userp():
    return render_template('usr_menu.html')

@app.route('/usrpedidos')
def userMenu():
    return render_template('usr_pedidos.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
