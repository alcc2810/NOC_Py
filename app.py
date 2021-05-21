from flask import Flask, render_template, request, redirect
from flask import url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime
from flask_csv import send_csv

app = Flask(__name__)

#Conexion a la DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASS'] = ''
app.config['MYSQL_DB']   = 'noc_db'
mysql_conn = MySQL(app)

#Configuracion de la sesion (guardamos dentro de la memoria de la aplicacion)
app.secret_key = 'mysecretkey'

#ruta principal
@app.route('/')
def index():
    return render_template('index.html')

#ruta pagina de actividades SES
@app.route('/actividades_ses')
def actividades_ses():
    return ('show SES activities')

#Ruta para guardar en la tabla de SES
@app.route("/add_attention", methods=["POST"])
def add_attention():
    if (request.method == "POST"):
        tecnico_ses       = request.form["tecnico_ses"]
        descripcion_ses   = request.form["descripcion_ses"]
        requerimiento_ses = request.form["requerimiento_ses"]
        fecha_atencion    = request.form["fecha_atencion"]
        hora_atencion     = request.form["hora_atencion"]
        espec_atencion    = request.form["espec_atencion"]

        #inserta datos en la base
        if fecha_atencion == "":
            fecha_atencion = datetime.today().strftime('%Y%m%d')

        cursordb = mysql_conn.connection.cursor()
        cursordb.execute('INSERT INTO atenciones_ses (tecnico_ses, descripcion_ses, requerimiento_HPSM, fecha_atencion, hora_atencion, espec_atencion) VALUES (%s, %s, %s, %s, %s, %s)',
        (tecnico_ses,descripcion_ses,requerimiento_ses,fecha_atencion,hora_atencion,espec_atencion))
        mysql_conn.connection.commit()
        flash ('Asistencia asignada')

        return redirect(url_for('agrega_atencion'))

#Ruta de la página para agregar datos
@app.route('/agrega_atencion')
def agrega_atencion():
    return render_template('agrega_atencion.html')

#Ruta para exportar a csv
@app.route("/exporta_atencion")
def exporta_atencion():
    return send_csv([{"id": 42, "foo": "bar"}, {"id": 91, "foo": "baz"}], "test.csv", ["id", "foo"])

#Ruta para eliminar atenciones ses
@app.route("/elimina_atencion/<string:id>")
def elimina_atencion(id):
    cursordb = mysql_conn.connection.cursor()
    cursordb.execute("DELETE FROM atenciones_ses WHERE id_ses = {0}".format(id))
    mysql_conn.connection.commit()
    flash("Atención eliminada")
    return redirect(url_for('admin_atencion'))

#Ruta para completar atenciones ses
@app.route("/completa_atencion/<string:id>")
def completa_atencion(id):
    cursordb = mysql_conn.connection.cursor()
    cursordb.execute("UPDATE atenciones_ses SET estado_atencion=0 WHERE id_ses= {0}".format(id))
    mysql_conn.connection.commit()
    flash("Atención completa")
    return redirect(url_for('admin_atencion'))

#Ruta de la página de Standby mensual
@app.route("/muestra_sby")
def muestra_sby():
    return render_template('muestra_sby.html')

#Ruta de la pagina administrador  de la consulta de atenciones SES
@app.route("/admin_atencion")
def admin_atencion():
    cursordb = mysql_conn.connection.cursor()

    consulta = """SELECT tecnico_ses, descripcion_ses, requerimiento_hpsm, 
                  DATE_FORMAT(fecha_atencion, %s), 
                  TIME_FORMAT(hora_atencion, %s), espec_atencion, id_ses
                  FROM atenciones_ses WHERE estado_atencion = 1 
                  ORDER BY fecha_atencion DESC, hora_atencion ASC;"""

    formato_fecha= "%d/%m/%Y"
    formato_hora = "%H:%i"

    cursordb.execute(consulta,[formato_fecha,formato_hora])
    atenciones_ses = cursordb.fetchall()

    return render_template('admin_atencion.html', atenciones_ses = atenciones_ses)

#Ruta de la pagina que muestra las atenciones SES
@app.route('/muestra_atencion')
def muestra_atencion():
    cursordb = mysql_conn.connection.cursor()

    consulta = """SELECT tecnico_ses, descripcion_ses, requerimiento_hpsm, 
                  DATE_FORMAT(fecha_atencion, %s), 
                  TIME_FORMAT(hora_atencion, %s), espec_atencion 
                  FROM atenciones_ses WHERE estado_atencion = 1 
                  ORDER BY fecha_atencion DESC, hora_atencion ASC;"""

    formato_fecha= "%d/%m/%Y"
    formato_hora = "%H:%i"

    cursordb.execute(consulta,[formato_fecha,formato_hora])
    atenciones_ses = cursordb.fetchall()

    return render_template('muestra_atencion.html', atenciones_ses = atenciones_ses)

#Ruta de la pagina que muestra los numeros de cedula de TEUNO
@app.route('/muestra_ced')
def muestra_ced():
    cursordb = mysql_conn.connection.cursor()

    consulta = 'SELECT * FROM cedula_teuno'

    cursordb.execute(consulta)
    cedulas_teuno = cursordb.fetchall()

    return render_template('muestra_ced.html', lista_cedulas = cedulas_teuno)



#Ruta de la pagina que muestra los pilotos de CNT
@app.route('/muestra_tagcnt')
def muestra_tagcnt():
    cursordb = mysql_conn.connection.cursor()

    consulta = 'SELECT * FROM tag_cnt'

    cursordb.execute(consulta)
    tags_cnt = cursordb.fetchall()

    return render_template('muestra_tagcnt.html', logins_cnt = tags_cnt)



#Ruta de la pagina que muestra los pilotos de Telconet
@app.route('/muestra_tagtnt')
def muestra_tagtnt():
    cursordb = mysql_conn.connection.cursor()

    consulta = 'SELECT * FROM tag_telconet'

    cursordb.execute(consulta)
    tags_tnt = cursordb.fetchall()

    return render_template('muestra_tagtnt.html', logins_tnt = tags_tnt)



if __name__ == '__main__':
    app.run(port=3000, debug=True)
    # app.run(port=3000)