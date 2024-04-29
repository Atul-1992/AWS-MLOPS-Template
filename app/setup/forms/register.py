from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email


class RegisterForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "User Name", validators=[DataRequired(), EqualTo("confirm_pass")]
    )
    confirm_pass = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
