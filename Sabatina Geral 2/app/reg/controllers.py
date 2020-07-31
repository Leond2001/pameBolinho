from flask import Blueprint, request, render_template, jsonify
from ..extensions import db, mail
from flask_mail import Message
from ..models import User
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, decode_token
)
import bcrypt

reg_api = Blueprint('reg_api', __name__)

@reg_api.route('/register/', methods=['GET', 'POST'])
def create():
  error = None
  if request.method == 'POST':     #O método será post quando o usuário enviar as informações do formulário para se registrar

    name = request.form['name']
    email = request.form['email']     #armazena o usuário na varíavel username
    idade = request.form['idade']
    password = request.form['password']     #armazena a senha na variável password

    if not name or not password or not email:
      return 'Dados insuficientes', 400          #Verifica se um dos dois é vazio
    
    user_check = User.query.filter_by(email=email).first()                 #Verifica no BD se já existe um usuário com esse nome

    if user_check: 
      return 'Usuário já cadastrado', 400                    #Se não for vazio, existe um usuário com esse nome. Então, um arquivo html é aberto dizendo "usuário já cadastrado" e com um link de volta ao início

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())                   #Faz hash na senha

    user = User(name=name, email=email, idade=idade, password_hash=password_hash)

    db.session.add(user)
    db.session.commit()

    # msg = Message(sender='lnrdgas@hotmail.com',
    #               recipients=[email],
    #               subject='Bem Vindo!',
    #               body='Bem vindo a nossa comunidade!')
    # mail.send(msg)

    return {'Cadastro realizado!'}, 200
  else:
    return render_template('register.html', error=error)                  #Caso o método não for o post, o usuário irá para a tela de inicio



@reg_api.route('/register/activate/<token>', methods=['GET'])
def activate(token):

    data = decode_token(token)

    user = User.query.get_or_404(data['identity'])

    if user.active == False:
        user.active = True
        db.session.add(user)
        db.session.commit()

    return {'Cadastro confirmado!'}