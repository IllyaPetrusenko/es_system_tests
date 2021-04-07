import allure
import requests
from config import host, platform_1


@allure.step('Get access token')
def get_access_token_for_platform_one():
    access_token = requests.get(
        url=host + '/auth/signin',
        headers={
            'Authorization': platform_1
        }).json()
    allure.attach(host + '/auth/signin', 'HOST')
    allure.attach(access_token, 'Response from auth service')
    access_token = access_token['data']['tokens']['access']
    allure.attach(platform_1, 'Platform credentials for authorization')
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

