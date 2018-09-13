from django import forms
from django.core.exceptions import ValidationError
from django.forms import CharField, BooleanField, ImageField
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.conf import settings

def image_validator(file):
    image = file.image
    if image.width != 200 or image.height != 200:
        raise ValidationError('Image must be 200x200')


class CodeSchoolForm(forms.Form):
    name = CharField(label='School Name')
    url = CharField(label='School website url')

    fulltime = BooleanField(label='Fulltime available?', required=False)
    hardware = BooleanField(label='Hardware included?', required=False)
    has_online = BooleanField(label='Online Offered?', required=False)
    only_online = BooleanField(label='Online only?', required=False)
    accredited = BooleanField(label='VA Accredited?', required=False)
    housing = BooleanField(label='Housing Included?', required=False)
    mooc = BooleanField(label='MOOC Only?', required=False)

    rep_name = CharField(label='School Representative')
    rep_email = CharField(label='Representative Email')
    address1 = CharField(label='Address Line 1')
    address2 = CharField(label='Address Line 2')
    city = CharField(label='City')
    state = CharField(label='State')
    zipcode = CharField(label='Zipcode')
    country = CharField(label='Country')

    logo = ImageField(label='Logo', validators=[image_validator])

    recaptcha = ReCaptchaField(private_key=settings.RECAPTCHA_PRIVATE_KEY, widget=ReCaptchaWidget())


