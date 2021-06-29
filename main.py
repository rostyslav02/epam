from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SECRET_KEY'] = 'agregehwreh'
db = SQLAlchemy(app)


from view import views
app.register_blueprint(views, url_prefix='/')


if __name__ == '__main__':
    app.run()

