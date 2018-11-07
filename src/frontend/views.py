import json
import logging
from typing import Tuple

import requests
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic import FormView, TemplateView

from .forms import CodeSchoolForm

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'frontend/index.html'


class CodeschoolFormView(FormView):
    form_class = CodeSchoolForm
    template_name = 'frontend/codeschool-form.html'
    success_url = f'https://github.com/{settings.GITHUB_REPO}/issues'

    def form_valid(self, form):
        form.save()
        handle_submission(form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class BotMessagesView(TemplateView):
    template_name = 'frontend/messages.html'


def get_logo_and_users(logo: InMemoryUploadedFile) -> Tuple[str, str]:
    school_logo = logo.name.replace(' ', '_')
    if settings.DEBUG or settings.PRE_PROD:
        users = '@wimo7083 @AllenAnthes,'
    else:
        users = '@wimo7083 @jhampton @kylemh'

    logo_url = f'{settings.MEDIA_URL}logos/{school_logo}'
    return logo_url, users


def handle_submission(form: dict):
    repo_path = settings.GITHUB_REPO
    url = f"https://api.github.com/repos/{repo_path}/issues"
    headers = {"Authorization": f"Bearer {settings.GITHUB_JWT}"}

    params = make_params(**form)
    res = requests.post(url, headers=headers, data=json.dumps(params))
    logger.info(f'response from github API call {res}')


def make_params(logo, name, url, address1, city, state, zipcode, country, rep_name, rep_email, recaptcha='',
                address2=None, fulltime=False, hardware=False, has_online=False, only_online=False, accredited=False,
                housing=False, mooc=False):
    logo_url, notify_users = get_logo_and_users(logo)

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
