from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')


class ChangeSettingsForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField('О себе')
    submit = SubmitField('Подтвердить')


class BecomeAuthorForm(FlaskForm):
    display_name = StringField('Отображаемый ник', validators=[DataRequired()])
    about = TextAreaField('О себе', validators=[DataRequired()])
    submit = SubmitField('Стать автором!')
