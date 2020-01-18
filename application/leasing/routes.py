from flask import render_template, Blueprint, abort, redirect, url_for, flash, request
from flask_login import login_required, current_user
from leasing.forms import ContractForm
from flaskcarleasing.models import Car, Contract
from flaskcarleasing.config import db
import datetime


leasing = Blueprint('leasing', __name__, template_folder='templates')


@leasing.route('/<int:car_id>', methods=['GET', 'POST'])
def index(car_id):
    if not current_user.is_authenticated:
        abort(401)

    car = Car.query.get_or_404(car_id)
    form = ContractForm()
    
    if form.validate_on_submit():
        days_to_rent = form.days_to_rent.data

        user_id = current_user.id
        lease_date = datetime.datetime.utcnow()
        return_date = lease_date + datetime.timedelta(days=days_to_rent)

        price = days_to_rent * car.price_per_day
        
        contract = Contract(user_id=user_id, car_id=car_id, lease_date=lease_date,\
            return_date=return_date, price=price)

        db.session.add(contract)
        db.session.commit()

        flash('Thank you for leasing our car. Our manager will call you back and then we deliver that car to you! Enjoy!')
        return redirect(url_for('main.index'))

    return render_template('leasing/index.html', car=car, form=form)


@leasing.route('/endcontract/<int:contract_id>', methods=['GET', 'POST'])
def end_contract(contract_id):
    if not current_user.is_authenticated:
        return abort(401)

    contract = Contract.query.get_or_404(contract_id)

    if contract.actual_return_date:
        return abort(403)

    actual_return_date = datetime.datetime.utcnow()

    penalty = 0

    if actual_return_date > contract.return_date:
        delta = (actual_return_date - contract.return_date).days
        penalty = contract.car.price_per_day * delta

    total_price = contract.price + penalty

    contract.actual_return_date = actual_return_date
    contract.total_price = total_price
    contract.penalty = penalty

    if request.method == 'POST':
        db.session.commit()

        flash(f'Contract {contract.id} was successfully ended! Thank you for using our services!')
        return redirect(url_for('main.index'))

    return render_template('leasing/end_contract.html', contract=contract)