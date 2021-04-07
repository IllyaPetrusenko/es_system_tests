import allure, json
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
    allure.attach(platform_1, 'Platform credentials for authorization')
    allure.attach(json.dumps(access_token), 'Response from auth service')
    access_token = access_token['data']['tokens']['access']
    allure.attach(str(access_token), 'Access token')
    return access_token


@allure.step('Get X-OPERATION-ID')
def get_x_operation_id(platform_token):
    x_operation_id = requests.post(
        url=host + '/operations',
        headers={
            'Authorization': 'Bearer ' + platform_token
        }).json()
    allure.attach(host + '/operations', 'HOST')
    allure.attach(platform_token, 'Platform access token')
    allure.attach(json.dumps(x_operation_id), 'Response from auth service')
    x_operation_id = x_operation_id['data']['operationId']
    allure.attach(str(x_operation_id), 'X-OPERATION-ID')
    return x_operation_id

