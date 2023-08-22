from flask import Flask, render_template, redirect, url_for, request, session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, functions
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/cars'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['SECRET_KEY'] = 'aaaa'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ALLOWED_EXTESION = {'png', 'jpg', 'jpeg'}


class Type(db.Model):
    __tablename = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo = Column(String)
    car = db.relationship("Car", backref="type", order_by="Car.id")
    model = db.relationship("Categoris", backref="type", order_by="Categoris.id")


class Categoris(db.Model):
    id = Column(Integer, primary_key=True)
    model = Column(String)
    type_id = Column(Integer, ForeignKey('type.id'))


class Car(db.Model):
    __tablename = "car"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    about = Column(String)
    body = Column(String)
    seat = Column(String)
    doors = Column(String)
    looggage = Column(String)
    fuel_type = Column(String)
    engine = Column(String)
    year = Column(String)
    milieage = Column(String)
    transmission = Column(String)
    drive = Column(String)
    fuel_econmy = Column(String)
    exterior_color = Column(String)
    interir_color = Column(String)
    horse = Column(String)
    prise = Column(String)
    photo = Column(String)
    photo2 = Column(String)
    photo3 = Column(String)
    photo4 = Column(String)
    model = Column(String)
    type_id = Column(Integer, ForeignKey('type.id'))
    car = db.relationship("Orders", backref="car", order_by="Orders.id")


class Orders(db.Model):
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('car.id'))
    username = Column(String)
    pic_locatin = Column(String)
    take_locatin = Column(String)
    pic_data = Column(String)
    take_data = Column(String)
    status = Column(String)
    gmail = Column(String)


class Users(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    photo = Column(String)
    gmail = Column(String)
    admin = Column(Boolean)


class News(db.Model):
    id = Column(Integer, primary_key=True)
    by = Column(String)
    data = Column(String)
    type = Column(String)
    name = Column(String)
    photo = Column(String)
    caption = Column(String)
    text = Column(String)


def current_user():
    user_now = None
    if 'username' in session:
        user_get = Users.query.filter(Users.username == session['username']).first()
        user_now = user_get

    return user_now


def users_folder():
    upload_folder = 'static/img/'
    return upload_folder


def checkFile(filename):
    value = '.' in filename
    type_file = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTESION
    return value and type_file


@app.route('/')
def hello_world():
    cars = Car.query.order_by(Car.id.desc()).all()
    news = News.query.limit(3).all()
    user = current_user()
    return render_template('index.html', user=user, news=news, car=cars)


@app.route('/header')
def header():
    user = current_user()
    return render_template('header.html', user=user)


@app.route('/order/<int:id>', methods=["POST", "GET"])
def orderss(id):
    user = current_user()
    order = Orders.query.all()
    if request.method == "POST":
        status = request.form.get('status')
        Orders.query.filter(Orders.id == id).update({
            'status': status,
        })
        db.session.commit()
    return render_template('admin_orders.html', user=user, order=order)


@app.route('/order')
def order():
    user = current_user()
    order = Orders.query.all()
    return render_template('admin_orders.html', user=user, order=order)


@app.route('/cars_edit/<int:ids>', methods=["POST", "GET"])
def cars_edit(ids):
    filter = Car.query.filter(Car.id == ids).first()
    types = Type.query.all()
    classe = Categoris.query.all()
    user = current_user()
    if request.method == "POST":
        name = request.form.get('name')
        type = request.form.get('type')
        info = request.form.get('info')
        body = request.form.get('body')
        seats = request.form.get('seats')
        doors = request.form.get('doors')
        luggage = request.form.get('luggage')
        engine = request.form.get('engine')
        year = request.form.get('year')
        mileage = request.form.get('mileage')
        transmission = request.form.get('transmission')
        drive = request.form.get('drive')
        fuel_economy = request.form.get('fuel_economy')
        exterior_color = request.form.get('exterior_color')
        interior_color = request.form.get('interior_color')
        horse = request.form.get('horse')
        fuel = request.form.get('fuel')
        prise = request.form.get('prise')
        classs = request.form.get('classs')
        photo = request.files['photo']
        photo2 = request.files['photo2']
        photo3 = request.files['photo3']
        photo4 = request.files['photo4']
        folder = users_folder()
        if photo and checkFile(photo.filename) and photo2 and checkFile(photo2.filename) and photo3 and checkFile(
                photo3.filename) and photo4 and checkFile(photo4.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            photo_file2 = secure_filename(photo2.filename)
            photo_url2 = '/' + folder + photo_file2
            photo_file3 = secure_filename(photo3.filename)
            photo_url3 = '/' + folder + photo_file3
            photo_file4 = secure_filename(photo4.filename)
            photo_url4 = '/' + folder + photo_file4
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            photo2.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file2))
            photo3.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file3))
            photo4.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file4))
        Car.query.filter(Car.id == ids).update({
            'name': name,
            'about': info,
            'type_id': type,
            'body': body,
            'seat': seats,
            'doors': doors,
            'looggage': luggage,
            'fuel_type': fuel,
            'engine': engine,
            'year': year,
            'milieage': mileage,
            'transmission': transmission,
            'drive': drive,
            'fuel_econmy': fuel_economy,
            'exterior_color': exterior_color,
            'interir_color': interior_color,
            'horse': horse,
            'prise': prise,
            'model': classs,
            'photo': photo_url,
            'photo2': photo_url2,
            'photo3': photo_url3,
            'photo4': photo_url4
        })
        db.session.commit()
        return redirect(url_for('cars'))
    return render_template('edit_car.html', user=user, car=filter, types=types, clas=classe)


@app.route('/cars_add', methods=["POST", "GET"])
def cars_add():
    user = current_user()
    types = Type.query.all()
    classe = Categoris.query.all()
    if request.method == "POST":
        name = request.form.get('name')
        type = request.form.get('type')
        info = request.form.get('info')
        body = request.form.get('body')
        seats = request.form.get('seats')
        doors = request.form.get('doors')
        luggage = request.form.get('luggage')
        engine = request.form.get('engine')
        year = request.form.get('year')
        mileage = request.form.get('mileage')
        transmission = request.form.get('transmission')
        drive = request.form.get('drive')
        fuel_economy = request.form.get('fuel_economy')
        exterior_color = request.form.get('exterior_color')
        interior_color = request.form.get('interior_color')
        horse = request.form.get('horse')
        classs = request.form.get('classs')
        fuel = request.form.get('fuel')
        prise = request.form.get('prise')
        photo = request.files['photo1']
        photo2 = request.files['photo2']
        photo3 = request.files['photo3']
        photo4 = request.files['photo4']
        folder = users_folder()
        if photo and checkFile(photo.filename) and photo2 and checkFile(photo2.filename) and photo3 and checkFile(
                photo3.filename) and photo4 and checkFile(photo4.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            photo_file2 = secure_filename(photo2.filename)
            photo_url2 = '/' + folder + photo_file2
            photo_file3 = secure_filename(photo3.filename)
            photo_url3 = '/' + folder + photo_file3
            photo_file4 = secure_filename(photo4.filename)
            photo_url4 = '/' + folder + photo_file4
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            photo2.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file2))
            photo3.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file3))
            photo4.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file4))
            add = Car(name=name, about=info, type_id=type, body=body, seat=seats, doors=doors, looggage=luggage,
                      fuel_type=fuel,
                      engine=engine, year=year, milieage=mileage, transmission=transmission, drive=drive,
                      fuel_econmy=fuel_economy, exterior_color=exterior_color, interir_color=interior_color,
                      horse=horse, prise=prise, photo=photo_url, photo2=photo_url2, photo3=photo_url3,
                      photo4=photo_url4,
                      model=classs)
            db.session.add(add)
            db.session.commit()
            return redirect(url_for('cars'))
    return render_template('add_car.html', user=user, types=types, clas=classe)


@app.route('/deletes/<int:id>')
def deletes(id):
    filter = News.query.filter(News.id == id).delete()
    db.session.commit()
    return redirect(url_for("news"))


@app.route('/delete/<int:id>')
def delete(id):
    filter = Car.query.filter(Car.id == id).delete()
    db.session.commit()
    return redirect(url_for("cars"))


@app.route('/news/<int:ids>', methods=["POST", "GET"])
def news_edit(ids):
    user = current_user()
    news = News.query.all()
    if request.method == "POST":
        by = request.form.get('name')
        data = request.form.get('time')
        type = request.form.get('type')
        news_name = request.form.get('news_name')
        text = request.form.get('text')
        caption = request.form.get('caption')
        photo = request.files['photo']
        folder = users_folder()
        News.query.filter(News.id == ids).update({
            "by": by,
            "data": data,
            "type": type,
            "name": news_name,
            "text": text,
            "caption": caption
        })
        db.session.commit()
        return redirect(url_for('news'))
    return render_template('news_edit.html', id=ids, user=user)


@app.route('/news', methods=["POST", "GET"])
def news():
    user = current_user()
    news = News.query.order_by(News.id.desc()).all()
    if request.method == "POST":
        by = request.form.get('name')
        data = request.form.get('time')
        type = request.form.get('type')
        news_name = request.form.get('news_name')
        text = request.form.get('text')
        caption = request.form.get('caption')
        photo = request.files['photo']
        folder = users_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            add = News(by=by, data=data, type=type, photo=photo_url, name=news_name, text=text, caption=caption)
            db.session.add(add)
            db.session.commit()
            return redirect(url_for('news'))
    return render_template('news_page.html', user=user, news=news)


@app.route('/new/<int:id>', methods=["POST", "GET"])
def new(id):
    filter = News.query.filter(News.id == id).first()
    user = current_user()
    return render_template('new.html', user=user, new=filter)


@app.route('/profile', methods=["POST", "GET"])
def profile():
    user = current_user()
    if request.method == "POST":
        name = request.form.get('name')
        surname = request.form.get('surname')
        usernames = request.form.get('username')
        password = request.form.get('password')
        photo = request.files['photo']
        folder = users_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            hashed = generate_password_hash(password=password, method='sha256')
            Users.query.filter(Users.id == user.id).update({
                "name": name,
                "surname": surname,
                "password": hashed,
                "username": usernames,
                "photo": photo_url,
            })
            db.session.commit()
            return redirect(url_for('profile'))
    return render_template('profile.html', user=user)


@app.route('/orders')
def orders():
    user = current_user()
    order = Orders.query.filter(Orders.username == user.username).all()
    return render_template('orders.html', user=user, order=order)


@app.route('/liked')
def liked():
    user = current_user()
    return render_template('like.html', user=user)


@app.route('/signout')
def singout():
    user = current_user()
    session['username'] = ""
    return redirect(url_for('login'))


@app.route('/cars')
def cars():
    Cars = Car.query.order_by(Car.prise.desc()).all()
    types = Type.query.all()
    user = current_user()
    return render_template('cars.html', user=user, types=types, cars=Cars)


@app.route('/car/<int:id>', methods=["POST", "GET"])
def car(id):
    filter = Car.query.filter(Car.id == id).first()
    user = current_user()
    order = Orders.query.filter(Orders.username == user.username).all()
    if request.method == "POST":
        pic_locatin = request.form.get('pic_loc')
        take_locatin = request.form.get('drop_loc')
        pic_data = request.form.get('pic_data')
        take_data = request.form.get('ret_data')
        add = Orders(pic_locatin=pic_locatin, take_locatin=take_locatin, pic_data=pic_data, take_data=take_data,
                     username=user.username, car_id=id, gmail=user.gmail, status='scheduled')
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('orders', order=order))
    return render_template('car.html', user=user, car=filter, id=id)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        username = Users.query.filter(Users.username == name).first()
        if username:
            if check_password_hash(username.password, password):
                session["username"] = username.username
                return redirect(url_for('hello_world'))
            else:
                return render_template('login.html', error='Username or password incorect')
    return render_template('login.html')


@app.route('/regstration', methods=["POST", "GET"])
def reg():
    if request.method == "POST":
        name = request.form.get('name')
        surname = request.form.get('surname')
        usernames = request.form.get('username')
        gmail = request.form.get('gmail')
        password = request.form.get('password')
        photo = request.files['photo']
        folder = users_folder()
        username = Users.query.filter(Users.username == usernames).first()
        if username:
            return render_template('reg.html', eror="This username already used")
        else:
            if photo and checkFile(photo.filename):
                photo_file = secure_filename(photo.filename)
                photo_url = '/' + folder + photo_file
                app.config['UPLOAD_FOLDER'] = folder
                photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
                hashed = generate_password_hash(password=password, method='sha256')
                add = Users(name=name, surname=surname, password=hashed, photo=photo_url, username=usernames,
                            gmail=gmail)
                db.session.add(add)
                db.session.commit()
                return redirect(url_for('reg'))
    return render_template('reg.html')


@app.route('/filter')
def filter():
    Cars = Car.query.order_by(Car.id.desc()).all()
    types = Type.query.all()
    user = current_user()
    return render_template('types.html', user=user, types=types, cars=Cars)


@app.route('/brands', methods=["POST", "GET"])
def brands():
    Cars = Car.query.order_by(Car.id.desc()).all()
    types = Type.query.all()
    user = current_user()
    if request.method == "POST":
        name = request.form.get("name")
        photo = request.files['photo']
        folder = users_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
            add = Type(name=name, photo=photo_url)
            db.session.add(add)
            db.session.commit()
        return redirect(url_for('brands'))
    return render_template('brands.html', user=user, types=types, cars=Cars)


@app.route('/brands/<string:id>', methods=["POST", "GET"])
def brand(id):
    types = Type.query.filter(Type.name == id).first()
    Cars = Car.query.filter(Car.type_id == types.id).all()
    classe = Categoris.query.all()
    user = current_user()
    filter = Type.query.filter(Type.id == types.id).first()
    if request.method == "POST":
        seria = request.form.get("seria")
        add = Categoris(model=seria, type_id=types.id)
        db.session.add(add)
        db.session.commit()
        return render_template('types.html', user=user, types=types, cars=Cars, id=types.id, clas=classe, name=id,
                               model=filter.model)
    return render_template('types.html', user=user, types=types, cars=Cars, id=types.id, clas=classe, name=id,
                           model=filter.model)


@app.route('/brands/<string:id>/<string:model>', methods=["POST", "GET"])
def bran(id, model):
    types = Type.query.filter(Type.name == id).first()
    Cars = Car.query.filter(Car.type_id == types.id, Car.model == model).all()
    classe = Categoris.query.all()
    user = current_user()
    filter = Type.query.filter(Type.id == types.id).first()
    if request.method == "POST":
        froms = request.form.get("from")
        to = request.form.get("to")
        Transmission = request.form.get("Transmission")
        Cars2 = Car.query.filter(Car.type_id == types.id, Car.model == model, Car.transmission == Transmission,
                                 Car.prise >= froms, Car.prise <= to).all()
        print(Cars2)
        return render_template('types.html', user=user, types=types, cars=Cars2, id=types.id, clas=classe, name=id,
                               model=filter.model, model1=model)
    return render_template('types.html', user=user, types=types, cars=Cars, id=types.id, clas=classe, name=id,
                           model=filter.model, model1=model)


if __name__ == '__main__':
    app.run()
