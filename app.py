from enum import unique
from re import template
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posti = db.Column(db.Integer)
    data_ora = db.Column(db.DateTime, nullable=False)
    gioco = db.Column(db.String(100), nullable=False)
    partecipazioni = db.relationship('Partecipazione', backref='evento')

class Partecipazione(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))
    nome = db.Column(db.String(35), nullable=False)
    nome_steam = db.Column(db.String(20), nullable=False)
    nome_telegram = db.Column(db.String(20), nullable=False)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id'))

@app.route('/')
def index():
    try:
        eventi = Evento.query.all()
        for evento in eventi:
            if evento.data_ora < datetime.datetime.today() - datetime.timedelta(days=1):
                db.session.delete(evento)
            db.session.commit()
        eventi = Evento.query.all()
        return render_template('index.html', eventi = eventi)
    except:
        return redirect('/')

    

@app.route('/crea', methods=['POST', 'GET'])
def crea():
    try:
        if request.method == 'POST':
            gioco = request.form['gioco']
            posti = request.form['posti']
            giorno = request.form['giorno']
            ora = request.form['ora']
            dataora = datetime.datetime.strptime(giorno + " " + ora,"%Y-%m-%d %H:%M")
            nuovo_evento = Evento(gioco=gioco, data_ora=dataora, posti=posti)
            
            db.session.add(nuovo_evento)
            db.session.commit()
            return redirect('/')
        else:
            return render_template('crea.html')
    except:
        return redirect('/')

@app.route('/partecipa/<int:id>', methods=['POST', 'GET'])
def partecipa(id):
    try:
        evento = Evento.query.get_or_404(id)
        if request.method == 'POST':
            nome = request.form['nome']
            nome_steam = request.form['nome_steam']
            nome_telegram = request.form['nome_telegram']
            tipo = request.form['tipo']
            nuova_partecipazione = Partecipazione(nome=nome, nome_steam=nome_steam, nome_telegram=nome_telegram, tipo=tipo, evento=evento)
            db.session.add(nuova_partecipazione)
            db.session.commit()
            return redirect('/')
        else:
            return render_template('partecipa.html', evento=evento)
    except:
        return redirect('/')

@app.route('/elimina/<int:id>', methods=['POST', 'GET'])
def elimina(id):
    try:
        evento = Evento.query.get_or_404(id)
        if request.method == 'POST':
            if request.form['conferma'] == 'conferma':
                db.session.delete(evento)
                db.session.commit()
            return redirect('/')
        else:
            return render_template('elimina.html', evento=evento)
    except:
        return redirect('/')

@app.route('/disiscrivi/<int:id>', methods=['POST', 'GET'])
def disiscrivi(id):
    try:
        partecipazione = Partecipazione.query.get_or_404(id)
        if request.method == 'POST':
            if request.form['conferma'] == 'conferma':
                db.session.delete(partecipazione)
                db.session.commit()
            return redirect('/')
        else:
            return render_template('disiscrivi.html', partecipazione=partecipazione)
    except:
        return redirect('/')