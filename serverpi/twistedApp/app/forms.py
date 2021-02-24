from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField


class PumpForm(FlaskForm):
    onLowAg = SubmitField('Turn Low Ag On')
    offLowAg = SubmitField('Turn Low Ag Off')
    onMedAg = SubmitField('Turn Med Ag On')
    offMedAg = SubmitField('Turn Med Ag Off')

def ValveForm(valvesState):
    """Dynamically creates a driver's schedule form"""

    # First we create the base form
    # Note that we are not adding any fields to it yet
    class ValveFormSub(FlaskForm):
        pass

    # Then we iterate over our ranges
    # and create a select field for each
    # item_{d}_{i} in the set, setting each field
    # *on our **class**.
    for valveTpl in valvesState:
        valve = valveTpl[0]
        state = valveTpl[1]
        label = valve
        if state == 'off':
            field = SubmitField('Turn On')
        else:
            field = SubmitField('Turn Off')
        setattr(ValveFormSub, label, field)

    # Finally, we return the *instance* of the class
    # We could also use a dictionary comprehension and then use
    # `type` instead, if that seemed clearer.  That is:
    # type('DriverTemplateScheduleForm', Form, our_fields)(**kwargs)
    return ValveFormSub()

def ScheduleBuilder(valveList):
    """Dynamically creates a driver's schedule form"""

    # First we create the base form
    # Note that we are not adding any fields to it yet
    class Schedule(FlaskForm):
        pass

    # Then we iterate over our ranges
    # and create a select field for each
    # item_{d}_{i} in the set, setting each field
    # *on our **class**.
    for valve in valveList:
        field = IntegerField('Number')
        setattr(Schedule, valve, field)

    setattr(Schedule, 'Submit', SubmitField('Submit'))

    # Finally, we return the *instance* of the class
    # We could also use a dictionary comprehension and then use
    # `type` instead, if that seemed clearer.  That is:
    # type('DriverTemplateScheduleForm', Form, our_fields)(**kwargs)
    return Schedule()


