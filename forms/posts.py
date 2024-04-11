from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddPostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    about = TextAreaField("Содержание")
    submit = SubmitField('Опубликовать')
