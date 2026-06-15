from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for 
from config import Config
from MySQLdb.cursors import DictCursor # <-- Importante para usar diccionarios

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'clave_secreta'


mysql = MySQL(app)
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

@app.route('/')
def index():
    return render_template('libro.html')

@app.route('/listado') 
def listado():
    cur = mysql.connection.cursor()
    # CORREGIDO: 'bibliotecas' en plural y seleccionamos las columnas exactas
    cur.execute(''' 
        SELECT 
            li.isbn, 
            li.titulo, 
            li.autor, 
            li.disponible, 
            li.id_catalogo, 
            cat.id_biblioteca, 
            bib.nombre 
        FROM libro li
        JOIN catalogo cat ON li.id_catalogo = cat.id_catalogo
        JOIN bibliotecas bib ON cat.id_biblioteca = bib.id_biblioteca
    ''')
    resultados = cur.fetchall()
    cur.close()
    return render_template('listado.html', libros=resultados)

@app.route('/editar/<id>')
def obtener(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libro WHERE isbn = %s', (id,))
    resultados = cur.fetchall()
    
    cur.execute('SELECT * FROM catalogo')
    catalogos = cur.fetchall()
    cur.close()
  
    if resultados:
        return render_template('editar.html', catalogo=catalogos, libro=resultados[0])
    return redirect(url_for('listado'))

@app.route('/actualizar/<isbn>', methods=['POST'])
def actualizar(isbn):
    if request.method == 'POST':
        TITULO = request.form['titulo']
        AUTOR = request.form['autor']
        DISPONIBILIDAD = request.form['disponible']
        CATALOGO = request.form['catalogo']
        
        cur = mysql.connection.cursor()
      
        cur.execute('''
            UPDATE libro 
            SET titulo=%s, autor=%s, disponible=%s, id_catalogo=%s 
            WHERE isbn=%s
        ''', (TITULO, AUTOR, DISPONIBILIDAD, CATALOGO, isbn))
        
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listado'))

@app.route('/registrar', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM catalogo")
        resultados = cur.fetchall()
        cur.close()
        return render_template('libro.html', catalogo=resultados)
        
    if request.method == 'POST':
        ISBN = request.form['isbn']
        TITULO = request.form['titulo']
        AUTOR = request.form['autor']
        DISPONIBILIDAD = request.form['disponible']
        CATALOGO = request.form['catalogo']
        
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO libro (isbn, titulo, autor, disponible, id_catalogo) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (ISBN, TITULO, AUTOR, DISPONIBILIDAD, CATALOGO))
        mysql.connection.commit()
        cur.close()
    
        return redirect(url_for('listado'))

if __name__ == '__main__':
    app.run(debug=True)