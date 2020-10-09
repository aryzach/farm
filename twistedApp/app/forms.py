from flask_wtf import FlaskForm
from wtforms import SubmitField


class LowAgForm(FlaskForm):
    on = SubmitField('Turn Low Ag On')
    off = SubmitField('Turn Low Ag Off')

