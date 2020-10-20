from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

class PumpForm(FlaskForm):
    onLowAg = SubmitField('Turn Low Ag On')
    offLowAg = SubmitField('Turn Low Ag Off')
    onMedAg = SubmitField('Turn Med Ag On')
    offMedAg = SubmitField('Turn Med Ag Off')

class ValveForm(FlaskForm):
    valve1 = SelectField('Valve 1', choices=[1,2,3], coerce=int)
    valve2 = SelectField('Valve 2', choices=[1,2,3], coerce=int)
    valve3 = SelectField('Valve 3', choices=[1,2,3], coerce=int)
    submit = SubmitField('Submit')

