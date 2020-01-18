from flask import render_template, redirect, url_for, request, Blueprint, abort
from flaskcarleasing.models import Car, Concern
from flaskcarleasing.config import db, delim, static_path
from cars.forms import AddCarForm
import hashlib
from flask import flash
from flask_login import current_user
import os
import secrets
from utils.functions import save_picture
from utils.decorators import check_rights


cars = Blueprint('cars', __name__, template_folder='templates')


@cars.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    cs = Car.query.order_by(Car.id).paginate(page, 3, False)
    return render_template('cars/index.html', cars=cs)


@cars.route('/add', methods=['GET', 'POST'])
@check_rights
def add():
    print(current_user)

    form = AddCarForm()

    if form.validate_on_submit():
        car = Car()
        car.concern_id = form.concern.data.id
        car.model = form.model.data
        car.price_per_day = form.price_per_day.data
        car.description = form.description.data

        if form.pic.data:
            car.pic = save_picture(form.pic.data)
            
        db.session.add(car)
        db.session.commit()

        print(car.pic)

        flash(f'{car.concern.title} {car.model} was successfully added to db!', 'info')
        return redirect(url_for('cars.index'))

    return render_template('cars/add.html', form=form)

@cars.route('/<int:car_id>/update', methods=['GET', 'POST'])
@check_rights
def update(car_id):
    car = Car.query.get_or_404(car_id)
    form = AddCarForm()

    if request.method == 'GET':
        form.concern.data = car.concern
        form.price_per_day.data = car.price_per_day
        form.model.data = car.model
        form.submit.label.text = 'Edit'
        form.description.data = car.description

    if form.validate_on_submit():
        if form.pic.data and car.pic != 'default.png':
            pic_path = os.path.join(static_path, f'pics{delim}{car.pic}')
            os.remove(pic_path)

            car.pic = save_picture(form.pic.data)

        car.model = form.model.data
        car.concern = form.concern.data
        car.price_per_day = form.price_per_day.data
        car.description = form.description.data
        
        db.session.commit()
        db.session.flush()

        flash(f'Successfully edited {car.concern.title} {car.model}')
        return redirect(url_for('cars.update', car_id=car.id))

    return render_template('cars/update.html', car=car, form=form)


@cars.route('/<int:car_id>/delete', methods=['GET', 'POST'])
@check_rights
def delete(car_id):
    car = Car.query.get_or_404(car_id)

    if request.method == 'POST':
        db.session.delete(car)

        db.session.commit()
        db.session.flush()

        if car.pic != 'default.png':
            pic_path = os.path.join(static_path, f'pics{delim}{car.pic}')
            os.remove(pic_path)

        flash(f'{car.concern.title} {car.model} was removed from the database!')
        return redirect(url_for('concerns.view', title=car.concern.title))

    return render_template('cars/delete.html', car=car)  