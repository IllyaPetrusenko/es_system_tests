import requests, time
from config import host, create_fs
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.kafka_messages import get_message_from_kafka
from tests.bpe_create_ei.create_ei import bpe_create_ei


def bpe_create_fs(ei_create_payload, fs_create_payload):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    create_ei_response = bpe_create_ei(ei_create_payload)
    time.sleep(2)
    request_to_create_fs = requests.post(
        url=host + create_fs + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
        headers={
            'Authorization': 'Bearer ' + access_token,
            'X-OPERATION-ID': x_operation_id,
            'Content-Type': 'application/json'},
        json=fs_create_payload)
    time.sleep(2)
    message_from_kafka = get_message_from_kafka(x_operation_id)
    return request_to_create_fs, message_from_kafka, x_operation_id, create_ei_response[1]['data']['outcomes']['ei'][0][
        'id']
