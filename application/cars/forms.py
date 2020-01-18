from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from flaskcarleasing.models import Concern


def get_concern_pk(obj):
    return str(obj)


class AddCarForm(FlaskForm):
    model = StringField('Model', validators=[DataRequired()])
    concern = QuerySelectField(u'Concern', query_factory=lambda: Concern.query, \
        allow_blank=False, get_label='title', get_pk=get_concern_pk)

    price_per_day = FloatField('Price per day', validators=[DataRequired()])
    description = TextAreaField('Description')

    pic = FileField('Load Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Add')