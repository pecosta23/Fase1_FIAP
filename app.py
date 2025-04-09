from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#configurando banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#importando modelos
import models 

if __name__ == '__main__':
    #criando o db
    app.run(debug=True)


