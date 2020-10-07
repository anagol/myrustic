from flask import Flask, redirect, render_template, url_for, request

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
    product_code = db.Column(db.String(20), unique=False)
    product_name = db.Column(db.String(250), unique=False)
    product_photo = db.Column(db.String, unique=False)
    product_description = db.Column(db.Text, unique=False)
    product_price = db.Column(db.String(20), unique=False)
    product_size = db.Column(db.String(100), unique=False)
    product_weight = db.Column(db.String(100), unique=False)
    product_material = db.Column(db.String(200), unique=False)
    product_term = db.Column(db.String(200), unique=False)

    def __init__(self, product_code, product_name, product_photo, product_description, product_price, product_size,
                 product_weight,
                 product_material, product_term):
        self.product_code = product_code
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
    return render_template('product.html', title='Мои изделия', product=product)


@app.route('/<int:prod_id>')
def prod(prod_id):
    prod = Product.query.filter_by(id=prod_id).one()
    return render_template('prod.html', prod=prod)


@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if request.method == "POST":
        product_code = request.form["product_code"]
        product_name = request.form["product_name"]
        product_photo = request.form["product_photo"]
        product_description = request.form["product_description"]
        product_price = request.form["product_price"]
        product_size = request.form["product_size"]
        product_weight = request.form["product_weight"]
        product_material = request.form["product_material"]
        product_term = request.form["product_term"]
        prod = Product(product_code=product_code, product_name=product_name, product_photo=product_photo,
                       product_description=product_description, product_price=product_price, product_size=product_size,
                       product_weight=product_weight, product_material=product_material, product_term=product_term)
        db.session.add(prod)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('product'))
    return render_template('create_product.html', title='Добавляем изделие')


@app.route('/edit_product')
def edit_product():
    product = Product.query.all()
    return render_template('edit_product.html', title='Редактируем', product=product)


# @app.route('/edit')
# def edit():
#     return render_template('edit.html', title='Редактируем изделия')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    prod = Product.query.get_or_404(id)
    if request.method == 'POST':
        prod.product_code = request.form["product_code"]
        prod.product_name = request.form["product_name"]
        prod.product_photo = request.form["product_photo"]
        prod.product_description = request.form["product_description"]
        prod.product_price = request.form["product_price"]
        prod.product_size = request.form["product_size"]
        prod.product_weight = request.form["product_weight"]
        prod.product_material = request.form["product_material"]
        prod.product_term = request.form["product_term"]
        db.session.flush()
        db.session.commit()
        return redirect('/product')
    else:
        return render_template('edit.html', prod=prod)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    verse = Product.query.get_or_404(id)
    db.session.delete(verse)
    db.session.flush()
    db.session.commit()
    return redirect(url_for('product'))


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
