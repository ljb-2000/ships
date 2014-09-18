from flask.ext.wtf import Form, RecaptchaField
from werkzeug import secure_filename
from wtforms.ext.sqlalchemy.orm import model_form, QuerySelectField
from wtforms import (PasswordField, BooleanField, DateField, DateTimeField,
                    FileField, IntegerField, RadioField, SelectField,
                    SelectMultipleField, SubmitField, StringField, HiddenField,
                    TextAreaField, FormField, FieldList)
from wtforms.validators import (EqualTo, Email, DataRequired, IPAddress,
                                InputRequired, Length, MacAddress, NumberRange,
                                Optional, Regexp, URL, UUID, AnyOf, NoneOf)
from wtforms.widgets import (ListWidget, TableWidget, Input, TextInput,
                            PasswordInput, HiddenInput, CheckboxInput,
                            FileInput, SubmitInput, TextArea, Select)
from ..models import ShipType

#-----
class Login(Form):
    email = StringField(label='Email')
    password = StringField(label='Password')

#-----
class Register(Form):
    email = StringField(label='Email')
    password = PasswordField(label='Password')
    password_confirm = PasswordField(label='Confirm Password')
    submit = SubmitField(label='Submit')

#-----
class EditProfile(Form):
    handle = StringField(label='Handle', validators = [DataRequired()])
    rsi_profile = StringField(label='RSI Profile')
    tas_profile = StringField(label='TAS Profile')
    hide_email = BooleanField(label='Hide Email On Profile?')
    submit = SubmitField(label='Submit')

#-----
def ship_types():
    return ShipType.query.all()

class AddShip(Form):
    ship_type = QuerySelectField(query_factory=ship_types)
    ship_name = StringField(label='Ship Name')
    submit = SubmitField(label='Submit')