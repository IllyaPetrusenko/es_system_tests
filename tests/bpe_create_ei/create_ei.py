import json

import requests, time
from config import host, create_ei
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.kafka_messages import get_message_from_kafka
from tests.presets import set_instance_for_request


def bpe_create_ei(payload):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    host = set_instance_for_request()
    request_to_create_ei = requests.post(
        url=host + create_ei,
        headers={
            'Authorization': 'Bearer ' + access_token,
            'X-OPERATION-ID': x_operation_id,
            'Content-Type': 'application/json'},
        params={
            'country': 'MD',
            'lang': 'ro'
        },
        json=payload)
    time.sleep(0.2)
    message_from_kafka = get_message_from_kafka(x_operation_id)
    print(message_from_kafka)
    return request_to_create_ei, message_from_kafka, x_operation_id

