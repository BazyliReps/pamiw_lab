from wtforms import Form, StringField, PasswordField, validators, ValidationError, IntegerField


class RegistrationForm(Form):
    username = StringField('Login', [validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField('Adres Email', [validators.Length(min=6, max=35), validators.DataRequired()])
    address = StringField('Adres', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('Hasło', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Hasło musi pasować')
    ])
    confirm = PasswordField('Powtórz Hasło')


class LoginForm(Form):
    username = StringField('Login', [validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('Hasło', [
        validators.DataRequired(),
    ])


class PackageForm(Form):
    recipient = StringField('Adresat', [validators.Length(min=4, max=25), validators.DataRequired()])
    mailbox_address = StringField('Adres Skrytki', [
        validators.Length(min=3, max=25, message='Adres skrytki musi składać się z 3 - 25 znaków.'),
        validators.DataRequired()])
    package_size = IntegerField('Rozmiar Paczki', [
        validators.NumberRange(min=0, max=10, message='Należy podać liczbę całkowitą z zakresu 0 - 10'),
        validators.DataRequired(message='Należy podać liczbę całkowitą z zakresu 0 - 10')])
