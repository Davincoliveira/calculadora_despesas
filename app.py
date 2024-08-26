from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///despesas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Despesas(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.String(200), nullable = False)
    valor = db.Column(db.Float, nullable = False)
    categoria = db.Column(db.String(100), nullable = False)
    data = db.Column(db.Date, nullable = False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    despesas = Despesas.query.all()
    return render_template('despesas.html', despesas = despesas)

@app.route('/adicionar_despesa', methods=['POST'])
def adicionar_despesa():
    descricao = request.form['descricao']
    valor = float(request.form['valor'])
    categoria = request.form['categoria']
    data = datetime.datetime.strptime(request.form['data'], '%Y-%m-%d').date()

    nova_despesa = Despesas(descricao = descricao, valor = valor, categoria = categoria, data = data)
    db.session.add(nova_despesa)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/editar_despesa/<int:id>', methods=['GET', 'POST'])
def editar_despesa(id):
    despesa = Despesas.query.get(id)
    if request.method == 'POST':
        despesa.descricao = request.form['descricao']
        despesa.valor = float(request.form['valor'])
        despesa.categoria = request.form['categoria']
        despesa.data = datetime.datetime.strptime(request.form['data'], '%Y-%m-%d').date()

        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('editar_despesa.html', despesa = despesa)

@app.route('/excluir_depesa/<int:id>')
def excluir_despesa(id):
    despesa = Despesas.query.get(id)
    db.session.delete(despesa)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)