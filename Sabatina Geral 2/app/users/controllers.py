from flask import Blueprint, request, render_template, jsonify
from ..extensions import db, mail
from flask_mail import Message
from ..models import User
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, decode_token
)
import bcrypt

user_api = Blueprint('user_api', __name__)


@user_api.route('/users/', methods=['GET'])
def index():

    data = request.args

    idade = data.get('idade')

    if not idade:  
        users = User.query.all()
    else:
        idade = idade.split('-')

        if len(idade) == 1:
            users = User.query.filter_by(idade=idade[0])
        else:
            users = User.query.filter(db.and_(User.idade >= idade[0], User.idade <= idade[1]))

    return jsonify([user.json() for user in users]), 200


@user_api.route('/users/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def user_detail(id):

    user = User.query.get_or_404(id)

    if request.method == 'GET':
        return user.json(), 200

    if request.method == 'PUT':

        data = request.json

        if not data:
            return {'error': 'Requisição precisa de body'}, 400

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return {'error': 'Dados insuficientes'}, 400

        if User.query.filter_by(email=email).first() and email != user.email:
            return {'error': 'Email já cadastrado'}, 400

        user.name = name
        user.email = email

        db.session.add(user)
        db.session.commit()

        return user.json(), 200

    if request.method == 'PATCH':

        data = request.json

        if not data:
            return {'error': 'Requisição precisa de body'}, 400

        email = data.get('email')

        if User.query.filter_by(email=email).first() and email != user.email:
            return {'error': 'Email já cadastrado'}, 400

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.idade = data.get('idade', user.idade)

        db.session.add(user)
        db.session.commit()

        return user.json(), 200

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        return {}, 204