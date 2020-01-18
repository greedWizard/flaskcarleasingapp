from flask import render_template, redirect, url_for, request, Blueprint, abort
from flaskcarleasing.models import Concern, Car
from flaskcarleasing.config import db
from concerns.forms import AddConcernForm
from flask import flash
from flask_login import current_user
import os
from utils.decorators import check_rights

concerns = Blueprint('concerns', __name__, template_folder='templates')


@concerns.route('/')
def index():
    concerns = Concern.query.all()
    return render_template('concerns/index.html', concerns=concerns)


@concerns.route('/add', methods=['GET', 'POST'])
@check_rights
def add():
    print(current_user)

    if not current_user.superuser:
        abort(403)
    
    form = AddConcernForm()

    if form.validate_on_submit():
        title = form.title.data

        if Concern.query.filter_by(title=title).first():
            return redirect(url_for('concerns.add'))

        concern = Concern(title=title)
        db.session.add(concern)

        db.session.commit()
        return redirect(url_for('concerns.index'))

    return render_template('concerns/add.html', form=form)


@concerns.route('/<string:title>/update', methods=['GET', 'POST'])
@check_rights
def update(title):
    if not current_user.superuser:
        abort(403)

    concern = Concern.query.filter_by(title=title).first_or_404()
    form = AddConcernForm()

    if request.method == 'GET':
        form.title.data = concern.title
    form.submit.label.text = 'Update'

    if form.validate_on_submit():
        concern.title = form.title.data
        db.session.commit()

        return redirect(url_for('concerns.index'))

    return render_template('concerns/update.html', form=form, title=title)


@concerns.route('/<string:title>/cars')
def view(title):
    page = request.args.get('page', 1, type=int)
    concern = Concern.query.filter_by(title=title).first()

    cs = Car.query.filter_by(concern=concern).paginate(page, 3, False)
    return render_template('cars/index.html', cars=cs)