import urllib
from datetime import datetime
from urllib.parse import urlunparse, urlencode
from django.shortcuts import HttpResponseRedirect, render
import requests
from django.conf import settings
from django.urls import reverse, reverse_lazy

from apps.authorization.models import HabrUserProfile, HabrUser


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        print('*' * 15, 'RESPONSE', '*' * 15)
        print(response)

        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(dict(fields=','.join(('first_name', 'last_name', 'career',
                                                              'sex', 'bdate', 'country', 'city', 'photo_max_orig')),
                                             access_token=response['access_token'],
                                             v='5.92')),
                              None
                              ))
        response_1 = requests.get(api_url)
        print(api_url)
        print(type(response))
        if response_1.status_code != 200:
            return
        data = response_1.json()['response'][0]
        print(data)
        if data.get('first_name'):
            user.habruserprofile.full_name = data["first_name"]
        if data.get('last_name'):
            user.habruserprofile.last_name = data["last_name"]
        if data.get('career'):
            user.habruserprofile.place_of_work = data['career'][-1]['company']
            user.habruserprofile.specialization = data['career'][-1]['position']
        if data.get('sex'):
            user.habruserprofile.gender = HabrUserProfile.MALE if data['sex'] == 2 else HabrUserProfile.FEMALE
        if data.get('bdate'):
            user.habruserprofile.birth_date = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        if data.get('country'):
            user.habruserprofile.country = data['country']['title']
        if data.get('city'):
            user.habruserprofile.city = data['city']['title']
        if data.get('photo_max_orig'):
            urllib.request.urlretrieve(data['photo_max_orig'], f'{settings.MEDIA_ROOT}/avatars/{user.pk}.jpg')
            user.habruserprofile.avatar = f'avatars/{user.pk}.jpg'
        username = response.get('screen_name')
        check_user = HabrUser.objects.filter(username=username)
        if check_user:
            return HttpResponseRedirect(reverse('articles:main_page'))
        user.save()
    elif backend.name == 'google-oauth2':
        print('*'*15, 'RESPONSE', '*'*15)
        print(response)
        if response.get('given_name'):
            user.habruserprofile.full_name = response['given_name']
        if response.get('family_name'):
            user.habruserprofile.last_name = response['family_name']
        if response.get('picture'):
            urllib.request.urlretrieve(response['picture'], f'{settings.MEDIA_ROOT}/avatars/{user.pk}.jpg')
            user.habruserprofile.avatar = f'avatars/{user.pk}.jpg'
        user.save()
    elif backend.name == 'github':
        print('*' * 15, 'RESPONSE', '*' * 15)
        print(response)
        if response.get('name'):
            user.habruserprofile.full_name = response['name']
        if response.get('avatar_url'):
            urllib.request.urlretrieve(response['avatar_url'], f'{settings.MEDIA_ROOT}/avatars/{user.pk}.jpg')
            user.habruserprofile.avatar = f'avatars/{user.pk}.jpg'
        user.save()
    else:
        return
