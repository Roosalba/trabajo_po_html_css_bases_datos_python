from flask_mysqldb import MySQL
from flask import Flask,render_template, request
from config import Config


app=Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'clave_secreta'
mysql=MySQL(app)


@app.route('/')
def index():
   cur=mysql.connection.cursor()
   cur.execute('select * from libro')
   resultados=cur.fetchall()
   cur.close()
   return render_template('libro.html', libros=resultados)



@app.route('/registrar', methods = ['GET', 'POST'])
def registro():
    if request.method == 'POST':
        ISBN = request.form['isbn']
        TITULO = request.form['titulo']
        AUTOR = request.form['autor']
        DISPONIBILIDAD = request.form['disponible']
        CATALOGO = request.form['catalogo']
        cur = mysql.connection.cursor()
        cur.execute('''insert into libro 
                       (isbn, titulo, autor, disponible, id_catalogo) 
                       values(%s, %s, %s,%s, %s)''', 
                    (ISBN, TITULO, AUTOR, DISPONIBILIDAD, CATALOGO))
        mysql.connection.commit()
        cur.close()
        return render_template('libro.html')





if __name__ == '__main__':
    app.run(debug= True)
