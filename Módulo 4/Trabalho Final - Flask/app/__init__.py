''' Módulo de __init__, responsável por importar os demais módulos e fazer configuração de ambiente '''

import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

########## Iniciando conexão com o banco ##########
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite+pysqlite:///microblog.db"
db = SQLAlchemy()
db.init_app(app) # Cria automaticamente uma pasta instance/ para o bannco
###################################################

login = LoginManager(app)
login.login_view = "login"
## O login_view redireciona o usário, passando uma flash message, para a 
# página de login quando esse tenta acessar páginas em que o login é
# necessário sem fazer o login
# Já as duas definições abaixo modificam a flash message exbida
login.login_message = "Você precisa fazer login para acessar essa página."
login.login_message_category = "error"

with open("key.json", "r") as fp:
    SECRET_KEY = json.load(fp)["secret_key"]

app.config["SECRET_KEY"] = SECRET_KEY

# A função básica do init do pacote é importar seus módulos (lembra?)
# Para evitar import circular (já que routes import app)
# fazemos isso no final do script
from app import routes, alquimias
from app.models import models

######### Criando as tabelas em models ##########
with app.app_context():
    db.create_all()

# from app.database import models

#run inplícito