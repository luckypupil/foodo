from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, FileField, StringField, IntegerField, validators
from wtforms.validators import Required, InputRequired, Length, Email

class RestSearch(Form):
    searchRest = TextField('restuarant',validators = [Required(message=(u'.'))])
    searchAddy = TextField('address',validators = [Required(message=(u'.'))])

class SubscribeForm(Form):
    email = StringField('email',validators = [InputRequired(message = (u'Email field required')),Email(),Length(min=2)])
    zipcd = IntegerField('zipcd',validators = [InputRequired(message = (u'Zip field required'))])
    first_name = TextField('first')
    last_name = TextField('last')