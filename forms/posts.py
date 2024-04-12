from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired


class AddPostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    about = TextAreaField("Содержание", validators=[DataRequired()])
    is_public = BooleanField("Сделать публичным?")
    submit = SubmitField('Опубликовать')
