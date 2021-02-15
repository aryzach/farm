from flask_wtf import FlaskForm
from wtforms import SubmitField


class PumpForm(FlaskForm):
    onLowAg = SubmitField('Turn Low Ag On')
    offLowAg = SubmitField('Turn Low Ag Off')
    onMedAg = SubmitField('Turn Med Ag On')
    offMedAg = SubmitField('Turn Med Ag Off')


def valve_form(valves, **kwargs):
    """Dynamically creates a driver's schedule form"""

    # First we create the base form
    # Note that we are not adding any fields to it yet
    class ValveForm(FlaskForm):
        pass

    # Then we iterate over our ranges
    # and create a select field for each
    # item_{d}_{i} in the set, setting each field
    # *on our **class**.
    for i in range(len(valves)):
        #label = 'valve_{:d}'.format(i)
        label = 'valve1'
        field = SubmitField('Turn On')
        setattr(ValveForm, label, field)

    # Finally, we return the *instance* of the class
    # We could also use a dictionary comprehension and then use
    # `type` instead, if that seemed clearer.  That is:
    # type('DriverTemplateScheduleForm', Form, our_fields)(**kwargs)
    return ValveForm(**kwargs)
