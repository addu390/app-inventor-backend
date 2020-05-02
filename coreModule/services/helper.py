import requests
from django.shortcuts import get_object_or_404

from ..constants import REFRESH_TOKEN, ACCESS_TOKEN, EXPIRES_IN
from ..models import User
from ..serializers import UserSerializer

API_ENDPOINT_V1 = "https://oauth2.googleapis.com/token"
API_ENDPOINT_V3 = "https://www.googleapis.com/oauth2/v3/tokeninfo"


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def token_refresh(user_id):
    user = get_object_or_404(User, user_id=user_id)
    data = UserSerializer(user).data
    # TODO: Move ClinetID to settings.py
    data = {
        "grant_type": "refresh_token",
        "client_id": "711972728828-0d3qme3mdba67l22k1q1dipg6ckdesoo.apps.googleusercontent.com",
        "refresh_token": data.get(REFRESH_TOKEN)
    }
    return requests.post(url=API_ENDPOINT_V1, data=data)


def is_valid_user(user_id, access_token, validate):
    is_valid = False
    user = get_object_or_404(User, user_id=user_id)
    data = UserSerializer(user).data
    print(data.get(ACCESS_TOKEN), access_token)
    if data.get(ACCESS_TOKEN) == access_token:
        response = requests.get(API_ENDPOINT_V3 + "?access_token=" + data.get(ACCESS_TOKEN))
        if response.status_code == 200 and (int(response.json().get(EXPIRES_IN)) or validate) > 0:
            is_valid = True
    return is_valid

