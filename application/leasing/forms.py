from flask_wtf import FlaskForm
from flask_wtf.html5 import NumberInput
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flaskcarleasing.models import Contract


class ContractForm(FlaskForm):
    days_to_rent = IntegerField('Days to lease', validators=[DataRequired()], \
        widget=NumberInput(min=1, max=20))
    user = HiddenField()

    submit = SubmitField('Lease')