from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CharField, BooleanField, ImageField
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.conf import settings


def image_validator(file):
    image = file.file.image
    if image.width != 200 or image.height != 200:
        raise ValidationError('Image must be 200x200')


class CodeSchool(models.Model):
    name = CharField(max_length=100, verbose_name='School Name')
    url = CharField(max_length=100, verbose_name='School website url')

    fulltime = BooleanField(verbose_name='Fulltime available?', blank=True)
    hardware = BooleanField(verbose_name='Hardware included?', blank=True)
    has_online = BooleanField(verbose_name='Online Offered?', blank=True)
    only_online = BooleanField(verbose_name='Online only?', blank=True)
    accredited = BooleanField(verbose_name='VA Accredited?', blank=True)
    housing = BooleanField(verbose_name='Housing Included?', blank=True)
    mooc = BooleanField(verbose_name='MOOC Only?', blank=True)

    rep_name = CharField(max_length=100, verbose_name='School Representative')
    rep_email = CharField(max_length=100, verbose_name='Representative Email')
    address1 = CharField(max_length=100, verbose_name='Address Line 1')
    address2 = CharField(max_length=100, verbose_name='Address Line 2', blank=True)
    city = CharField(max_length=100, verbose_name='City')
    state = CharField(max_length=100, verbose_name='State')
    zipcode = CharField(max_length=100, verbose_name='Zipcode')
    country = CharField(max_length=100, verbose_name='Country')

    logo = ImageField(verbose_name='Logo', validators=[image_validator], upload_to='logos')


class RecaptchaForm(forms.Form):
    recaptcha = ReCaptchaField(private_key=settings.RECAPTCHA_PRIVATE_KEY, widget=ReCaptchaWidget())


class CodeSchoolModelForm(forms.ModelForm):
    class Meta:
        model = CodeSchool
        fields = '__all__'


class CodeSchoolForm(CodeSchoolModelForm, RecaptchaForm):
    pass
