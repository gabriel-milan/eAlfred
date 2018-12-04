#
#   Imports
#
from settings import *
from flask_wtf import FlaskForm
from wtforms.validators import Length, InputRequired
from wtforms import StringField, IntegerField, BooleanField

#
#   Registration form
#
class RegistrationForm (FlaskForm):
    identificacao = StringField('identificacao', validators = [InputRequired(), Length(max = MAX_DEVICE_NAME)])
    porta = IntegerField('porta', validators = [InputRequired()])
    tipo_porta = BooleanField('tipo_porta')
    tipo_dispositivo = BooleanField('tipo_dispositivo')

#
#   Write form
#
class WriteForm (FlaskForm):
    pwm = BooleanField('pwm')
    value = IntegerField('value')