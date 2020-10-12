from flask import Flask, redirect, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anatolihalasny1969'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://aziveibtbozkbs:00213dc440bbea72e2bf91df6b64b1d5765c52c9def5e5e04a76f4aa81a0d4d1@ec2-54-217-213-79.eu-west-1.compute.amazonaws.com:5432/d8ei5c1vou2be0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.errorhandler(401)
def page_not_found(error):
    return redirect(url_for('error_401'))


# -----------------------Создаем базу данных-----------------------------------------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(250))

    def __init__(self, username, password):
        self.username = username
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
                 product_weight, product_material, product_term):
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


# ------------------------Главная страница-------------------------------------------------------------------
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная страница')


# -----------------------Создаем общую страницу с изделиями--------------------------------------------------
@app.route('/product')
def product():
    product = Product.query.filter_by().all()
    return render_template('product.html', title='Мои изделия', product=product)


# -----------------------Создаем общую страницу каждого изделиями--------------------------------------------
@app.route('/<int:prod_id>')
def prod(prod_id):
    prod = Product.query.filter_by(id=prod_id).one()
    return render_template('prod.html', prod=prod)


# -----------------------Страница создания каждого изделия---------------------------------------------------
@app.route('/create_product', methods=['GET', 'POST'])
@login_required
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


# -----------------------Страница редактирования изделий-----------------------------------------------------
@app.route('/edit_product')
@login_required
def edit_product():
    product = Product.query.all()
    return render_template('edit_product.html', title='Редактируем', product=product)


# -----------------------Страница редактирования каждого изделия---------------------------------------------
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
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


# -----------------------Функционал удаления отдельного изделия----------------------------------------------
@app.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    verse = Product.query.get_or_404(id)
    db.session.delete(verse)
    db.session.flush()
    db.session.commit()
    return redirect(url_for('product'))


# -----------------------Страница "Обо мне"------------------------------------------------------------------
@app.route('/about')
def about():
    return render_template('about.html', title='Контакты')


# -----------------------Страница "Доставка"-----------------------------------------------------------------
@app.route('/delivery')
def delivery():
    return render_template('delivery.html', title='Доставка и оплата')


# -----------------------Страница администратора-------------------------------------------------------------
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', title='Страница администратора')


# --------------------Регистрация---------------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password_hash = generate_password_hash(request.form["password"])
        register = User(username=username, password=password_hash)
        db.session.add(register)
        db.session.flush()
        db.session.commit()
        flash('Вы успешно зарегистрированы, теперь можете войти в систему!')
        return redirect(url_for("login"))
    return render_template("register.html", title='Регистрация')


#  --------------------Login-------------------------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()
        login_user(user)
        if user is None:
            flash('Неверная пара логин - пароль')
            return render_template("login.html")
        if not check_password_hash(user.password, request.form['password']):
            flash('Неверная пара логин - пароль')
            return render_template("login.html")
        flash(f'Вы успешно авторизованы под именем {username}!')
        return redirect(url_for("admin"))

    return render_template("login.html")


#  --------------------Logout------------------------------------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/error_401')
def error_401():
    return render_template('401.html', title='ОШИБКА 401')


if __name__ == '__main__':
    app.run()
