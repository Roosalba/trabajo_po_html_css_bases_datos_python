from flask_mysqldb import MySQL
from flask import Flask,render_template, request , redirect , url_for 
from config import Config


app=Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'clave_secreta'
mysql=MySQL(app)


@app.route('/')
def index():
  
   return 'mi primera pagina'



@app.route('/registrar', methods = ['GET', 'POST'])
def registro():
    if request.method=='GET':
        cur=mysql.connection.cursor()
        cur.execute("select * from catalogo")
        resultados=cur.fetchall()
        cur.close()
        return render_template('libro.html', catalogo=resultados)
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
        return redirect(url_for('listar'))



@app.route('/listado')
def listar():
   cur=mysql.connection.cursor()
   cur.execute('select * from libro')
   resultados=cur.fetchall()
   cur.close()
   return render_template('listado.html', libros=resultados)






if __name__ == '__main__':
    app.run(debug= True)
