from wtforms import Form, BooleanField, StringField, PasswordField, validators

class editResult(Form):
    result = StringField('Result')
