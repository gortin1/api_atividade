from flask import Flask
from database import db
from api.atividade.atividade_route import atividades_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atividades.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(atividades_blueprint)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5003, debug=True)