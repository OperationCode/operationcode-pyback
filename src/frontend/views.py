# Create your views here.
from typing import Tuple
from urllib import parse
import json
import logging
import os
import requests

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic import FormView, TemplateView
from django.conf import settings

from .forms import CodeSchoolForm

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'frontend/index.html'


class CodeschoolFormView(FormView):
    form_class = CodeSchoolForm
    template_name = 'frontend/codeschool-form.html'
    success_url = f'https://github.com/{settings.GITHUB_REPO}/issues'

    def form_valid(self, form):
        url_root = self.request.get_host()
        handle_submission(form.cleaned_data, url_root)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class BotMessagesView(TemplateView):
    template_name = 'frontend/messages.html'


def save_logo(logo: InMemoryUploadedFile):
    file_path = os.path.abspath(f'static/media/logos/{logo.name}')
    with open(file_path, 'wb+') as destination:
        for chunk in logo.chunks():
            destination.write(chunk)


def get_logo_and_users(logo: InMemoryUploadedFile, url_root: str) -> Tuple[str, str]:
    school_logo = parse.quote(logo.name)
    if settings.DEBUG:
        users = '@wimo7083 @AllenAnthes,'
        logo_url = f'https://pyback.ngrok.io/static/media/logos/{school_logo}'
    else:
        # users = '@hpjaj @wimo7083 @jhampton @kylemh @davidmolina @nellshamrell @hollomancer @maggi-oc'
        users = ''
        logo_url = f'{url_root}static/logos/{school_logo}'
    return logo_url, users


def handle_submission(form: dict, url_root: str):
    save_logo(form['logo'])
    repo_path = settings.GITHUB_REPO
    url = f"https://api.github.com/repos/{repo_path}/issues"
    headers = {"Authorization": f"Bearer {settings.GITHUB_JWT}"}

    params = make_params(**form, url_root=url_root)
    res = requests.post(url, headers=headers, data=json.dumps(params))


def make_params(logo, name, url, address1, city, state, zipcode, country, rep_name, rep_email, url_root, recaptcha='',
                address2=None, fulltime=False, hardware=False, has_online=False, only_online=False, accredited=False,
                housing=False, mooc=False):
    logo_url, notify_users = get_logo_and_users(logo, url_root)

    return ({
        'title': f'New Code School Request: {name}',
        'body': (
            f"Name: {name}\n"
            f"Website: {url}\n"
            f"Full Time: {fulltime}\n"
            f"Hardware Included: {hardware}\n"
            f"Has Online: {has_online}\n"
            f"Only Online: {only_online}\n"
            f"VA Accredited: {accredited}\n"
            f"Housing Included: {housing}\n"
            f"MOOC Only: {mooc}\n"

            f"Address: {address1} {address2}\n"
            f"City: {city}\n"
            f"State: {state}\n"
            f"Country: {country}\n"
            f"Zip: {zipcode}\n\n"
            f"Representative Name: {rep_name}\n"
            f"Representative Email: {rep_email}\n"

            f"logo: ![school-logo]({logo_url})\n"

            'This code school is ready to be added/updated:\n'
            f"{notify_users}\n"
            "Please close this issue once you've added/updated the code school."
        )
    })
