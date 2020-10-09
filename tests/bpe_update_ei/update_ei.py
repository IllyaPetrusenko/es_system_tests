import copy

import requests, time
from config import host, create_ei, update_ei
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.kafka_messages import get_message_from_kafka
from tests.bpe_create_ei.payloads import ei_full
from tests.bpe_create_ei.create_ei import bpe_create_ei

def bpe_update_ei(payload):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    ei = copy.deepcopy(ei_full)
    create_ei_response = bpe_create_ei(ei)
    request_to_create_ei = requests.post(
        url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
        headers={
            'Authorization': 'Bearer ' + access_token,
            'X-OPERATION-ID': x_operation_id,
            'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
            'Content-Type': 'application/json'},
        json=payload)
    time.sleep(1)
    message_from_kafka = get_message_from_kafka(x_operation_id)
    return request_to_create_ei, message_from_kafka, x_operation_id

# ei=copy.deepcopy(ei_full)
# xc = bpe_update_ei(ei)
# print(xc)
# url = xc[1]['data']['url']
# print(url)