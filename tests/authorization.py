import requests, allure
from config import host


@allure.step('Get access token')
def get_access_token_for_platform_one():
    access_token = requests.get(
        url=host + '/auth/signin',
        headers={
            'Authorization': 'Basic dXNlcjpwYXNzd29yZA=='
        }).json()['data']['tokens']['access']
    return access_token


@allure.step('Get x-operation-id')
def get_x_operation_id(platform_token):
    x_operation_id = requests.post(
        url=host + '/operations',
        headers={
            'Authorization': 'Bearer ' + platform_token
        }).json()['data']['operationId']
    return x_operation_id

