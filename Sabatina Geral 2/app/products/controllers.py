from flask import request, Blueprint, jsonify, render_template
from ..models import User, Product
from flask_jwt_extended import jwt_required
from ..extensions import db

product_api = Blueprint('product_api', __name__)

@product_api.route('/users/<int:id>/products/', methods=['GET', 'POST'])
#@jwt_required
def create_products(id):
    if request.method == 'POST':
        # data = request.json

        # name = data.get('name')
        # description = data.get('description')

        name = request.form['name']
        description = request.form['description']

        if not name or not description:
            return {'error': 'Dados insuficientes'}, 400

        owner = User.query.get_or_404(id) #O usuário com a ID fornecida será o dono do produto

        product = Product(name=name, description=description, owner_id=owner.id) #Aqui, a variável product recebe um nome, seus detalhes e seu proprietário

        db.session.add(product)
        db.session.commit()

        return render_template('product_success.html'), 200

    else:
        return render_template('produtos.html'), 200


    