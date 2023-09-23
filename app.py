from flask import Flask, render_template, request, redirect, url_for, session, flash
#from flask_mail import Mail, Message
#import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

app = Flask(__name__, static_folder='static')
app.secret_key = 'sua_chave_secreta'  # Defina sua própria chave secreta para proteger a sessão.
app.config['PERMANENT_SESSION_LIFETIME'] = 900 

#app.config['MAIL_SERVER'] = '10.1.3.7'
#app.config['MAIL_PORT'] = 25
#app.config['MAIL_USERNAME'] = 'natanieln@gminuano.com.br'
#app.config['MAIL_PASSWORD'] = '142898'
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = False

#mail = Mail(app)

# Configuração do banco de dados
db = MySQLdb.connect(
  host= os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd= os.getenv("DB_PASSWORD"),
  db= os.getenv("DB_NAME"),
  autocommit = True,
  ssl_mode = "VERIFY_IDENTITY",
  #ssl      = {
  # "ca": "/etc/ssl/cert.pem"
  #}
)
cursor = db.cursor()

#def enviar_email(subject, sender, recipients, body):
#    msg = Message(subject, sender=sender, recipients=recipients)
#   msg.body = body
#    mail.send(msg)

# Função de autenticação básica (substitua pela lógica de autenticação real)
def autenticar_usuario(username, password):
    #Colocar a query aqui dentro
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username,password))
    user = cursor.fetchone()
    if user:
         session['id_user'] = user[0]
         session['username'] = user[1]
         session['funcao'] = user[4]
         session['negocio'] = user[5]
         session['setor'] = user[3]
         return True
    else: 
        return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if autenticar_usuario(username, password):
             return redirect(url_for('index'))
        else:
            error_message = 'Credenciais inválidas. Tente novamente.'
            return render_template('login.html', error_message=error_message) 
    return render_template('login.html')

@app.route('/')
def index():
    if 'username' in session:
        cursor.execute("""SELECT c.*,
	                      u.username,
	                      u.setor
                          FROM chamados c 
                          left join users u on c.user_id = u.user_id 
                          WHERE status = 'Aberto' or status = ''""")
        chamados = cursor.fetchall()
        return render_template('index.html', chamados=chamados)
    return redirect(url_for('login'))

@app.route('/chamado')
def chamado():
    id_chamado = request.args.get('id')
    if id_chamado:
        cursor.execute("""SELECT * FROM chamados WHERE id = %s""", (id_chamado,))
        chamado = cursor.fetchone()
        cursor.execute("SELECT i.*,u.username,u.setor,u.negocio FROM itens_chamados i LEFT JOIN users u on i.user_id = u.user_id WHERE i.id_chamado = %s order by i.data desc", (id_chamado,))
        itens = cursor.fetchall()
        return render_template('chamado.html', chamado=chamado, itens=itens)
    else:
        redirect(url_for('index'))

@app.route('/criar_item', methods=['POST']) 
def criar_item():
    if 'username' in session:
        id_chamado = request.form['id_chamado']
        user = session['id_user']
        observacao = request.form['observacao']
        setor = session['setor']
        cursor.execute("""INSERT INTO itens_chamados (id_chamado, user_id, observacao, setor) VALUES (%s, %s, %s, %s)""", (id_chamado, user, observacao, setor))
        db.commit()

        #subject = 'Assunto do E-mail'
        #sender = 'natanieln@gminuano.com.br'
        #recipients = ['natanieln@gminuano.com.br']
        #body = 'Corpo do E-mail'
        #enviar_email(subject, sender, recipients, body)

        return redirect(url_for('chamado', id=id_chamado))  
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/criar_chamado', methods=['GET', 'POST'])
def criar_chamado():
    if 'username' in session:
        if request.method == 'POST':
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            solucao = request.form['solucao']
            prioridade = request.form['prioridade']
            categoria = request.form['categoria']
            user_id = session['id_user']
            cursor.execute("INSERT INTO chamados (titulo, descricao, solucao, prioridade, categoria, user_id) VALUES (%s, %s, %s, %s, %s, %s)", (titulo, descricao, solucao, prioridade, categoria, user_id))
            cursor.execute("SELECT LAST_INSERT_ID()")
            novo_id_chamado = cursor.fetchone()[0]
            cursor.execute("""
    INSERT INTO itens_chamados (id_chamado, data, user_id, observacao, setor)
    SELECT
        c.id AS id_chamado,
        c.data_abertura AS data,
        c.user_id,
        CONCAT('Atividade gerada por ', u.username, '/', u.setor) AS observacao,
        u.setor
    FROM
        chamados c
    LEFT JOIN
        users u ON c.user_id = u.user_id
    WHERE
        c.id = %s
""", (novo_id_chamado,))
            db.commit()
            return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/editar_chamado', methods=['GET', 'POST'])
def editar_chamado():
    if 'username' in session:
        if request.method == 'POST':
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            id_chamado = request.form['id_chamado']
            status = request.form['status']
            cursor.execute("update chamados set titulo = %s, descricao = %s, status = %s where id = %s ", (titulo, descricao, status, id_chamado))
            db.commit()
            return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Registro Deletado Com Sucesso!")
    cursor.execute("DELETE FROM chamados WHERE id=%s", (id_data,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/atendimento')
def atendimento():
    if 'username' in session:
        cursor.execute("SELECT * FROM chamados where status = 'Em Desenvolvimento'")
        chamados = cursor.fetchall()
        return render_template('atendimento.html', chamados=chamados)
    return redirect(url_for('login'))

@app.route('/fechado')
def fechado():
    if 'username' in session:
        cursor.execute("SELECT * FROM chamados where status = 'Fechado'")
        chamados = cursor.fetchall()
        return render_template('fechado.html', chamados=chamados)
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug=True)
