
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField, PasswordField, IntegerField, DateField)
from wtforms.fields.core import FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email


class AltaVehiculosForm(FlaskForm):
    vehiculo = StringField('Vehiculo', validators=[DataRequired('Complete el vehiculo aparecido')])
    rama = IntegerField('Rama', validators=[DataRequired('Complete el número de rama')])
    siniestro = IntegerField('Siniestro',validators=[DataRequired('Complete el número de siniestro')])
    fe_ocurrencia = DateField('Fecha de ocurrencia',format='%d/%m/%Y', validators=[DataRequired('Debe completar la fecha de ocurrencia')])
    fe_pago = DateField('Fecha de pago',format='%d/%m/%Y', validators=[DataRequired('Debe completar la fecha de vencimiento')])
    fe_aviso_aparicion = DateField('Aviso de aparicion',format='%d/%m/%Y', validators=[DataRequired('Debe completar la fecha de aparición')])
    importe_pagado = FloatField('Importe pagado', validators=[DataRequired('Complete el importe pagado')])
    asegurado = StringField('Asegurado / Razon social', validators=[DataRequired('Complete el nombre del asegurado/razon social')])
    submit = SubmitField('Enviar')