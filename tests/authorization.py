import allure
import requests
from config import host


def get_access_token_for_platform_one():
    access_token = requests.get(
        url=host + '/auth/signin',
        headers={
            'Authorization': 'Basic dXNlcjpwYXNzd29yZA=='
        }).json()['data']['tokens']['access']
    allure.attach(str(access_token), 'Access token')
    return access_token


def get_x_operation_id(platform_token):
    x_operation_id = requests.post(
        url=host + '/operations',
        headers={
            'Authorization': 'Bearer ' + platform_token
        }).json()['data']['operationId']
    allure.attach(str(x_operation_id), 'X-OPERATION-ID')
    return x_operation_id

