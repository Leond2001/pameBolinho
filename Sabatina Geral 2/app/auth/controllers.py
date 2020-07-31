from flask import Blueprint, request, render_template, jsonify
from flask_jwt_extended import create_access_token
from ..models import User
from ..extensions import db
import bcrypt

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/login/', methods=['GET', 'POST'])
def login():
  error = None

  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    if not email:
      return jsonify({"msg":"Usuário em branco"}), 400
    if not password:
      return jsonify({'msg':'Senha em branco'})

    user_check = User.query.filter_by(email=email).first()

    if user_check:
      password_unhash = bcrypt.checkpw(password.encode(), user_check.password_hash) #Caso o usuário seja encontrado

      if password_unhash:
        access_token = create_access_token(identity=email) # A senha bateu
        return render_template('login_success.html', token=access_token), 200
      
      else:
        return jsonify({'msg':'Usuário ou senha errados'}) #Caso a senha não bata

    else:
      return jsonify({'msg':'Usuário ou senha errados'}) #Caso o usuário não bata

  if request.method == 'GET':
    return render_template('login.html', error=error)