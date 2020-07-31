from flask import Flask
from .config import Config
from .extensions import db, mail, migrate, jwt
from .users.controllers import user_api
from .auth.controllers import auth_api
from .reg.controllers import reg_api
from .products.controllers import product_api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  migrate.init_app(app, db)
  mail.init_app(app)
  jwt.init_app(app)


  app.register_blueprint(user_api)
  app.register_blueprint(auth_api)
  app.register_blueprint(reg_api)
  app.register_blueprint(product_api)

  return app