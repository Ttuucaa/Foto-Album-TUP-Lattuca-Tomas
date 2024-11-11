from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired

class PhotoForm(FlaskForm):
    title = StringField('Titulo', validators=[DataRequired()])
    description = TextAreaField('Descripcion') 
    image = FileField('Imagen', validators=[DataRequired()])
    submit = SubmitField('Enviar')
