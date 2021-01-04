from flask_wtf import FlaskForm
from wtforms import SubmitField


class PumpForm(FlaskForm):
    onLowAg = SubmitField('Turn Low Ag On')
    offLowAg = SubmitField('Turn Low Ag Off')
    onMedAg = SubmitField('Turn Med Ag On')
    offMedAg = SubmitField('Turn Med Ag Off')


