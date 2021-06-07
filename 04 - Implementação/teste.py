from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def ola():
  return render_template('esqueci_senha.html')

@app.route('/1')
def x():
  return render_template('alterar_notas.html')

app.run()