from flask.ext.wtf import Form, RecaptchaField
from werkzeug import secure_filename
from wtforms.ext.sqlalchemy.orm import model_form
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


class Login(Form):
    email = StringField(label='Email')
    username = StringField(label='Email')
    password = StringField(label='Password')
    submit = SubmitField(label='Submit')