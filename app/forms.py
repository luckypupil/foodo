
from wtforms import Form, TextField, BooleanField, FileField, StringField, IntegerField, validators
from wtforms.validators import Required

class RestSearch(Form):
    search = TextField('restuarant',validators = [Required()])

class SubscribeForm(Form):
    email = StringField('email',[validators.InputRequired(),validators.Email()])
    zipcd = IntegerField('zipcd',validators = [Required()])
    first_name = TextField('first')
    last_name = TextField('last')