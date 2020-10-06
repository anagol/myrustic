from flask import Flask, redirect, render_template, url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(250))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), unique=False)
    product_photo = db.Column(db.String, unique=False)
    product_description = db.Column(db.Text, unique=False)
    product_price = db.Column(db.String(20), unique=False)
    product_size = db.Column(db.String(100), unique=False)
    product_weight = db.Column(db.String(100), unique=False)
    product_material = db.Column(db.String(200), unique=False)
    product_term = db.Column(db.String(200), unique=False)

    def __init__(self, product_name, product_photo, product_description, product_price, product_size, product_weight,
                 product_material, product_term):
        self.product_name = product_name
        self.product_photo = product_photo
        self.product_description = product_description
        self.product_price = product_price
        self.product_size = product_size
        self.product_weight = product_weight
        self.product_material = product_material
        self.product_term = product_term

    def __repr__(self):
        return '<Product %r>' % self.product_name


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница')


@app.route('/product')
def product():
    product = Product.query.filter_by().all()
    return render_template('product.html', title='Мои изделия', time=time, product=product)


@app.route('/<int:prod_id>')
def prod(prod_id):
    prod = Product.query.filter_by(id=prod_id).one()
    return render_template('prod.html', prod=prod)


@app.route('/about')
def about():
    return render_template('about.html', title='Обо мне')


@app.route('/delivery')
def delivery():
    return render_template('delivery.html', title='Доставка')


@app.route('/payment')
def payment():
    return render_template('payment.html', title='Оплата')


if __name__ == '__main__':
    app.run()
