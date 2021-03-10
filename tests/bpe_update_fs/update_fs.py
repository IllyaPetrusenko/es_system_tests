import requests, time
from config import host, update_fs
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.kafka_messages import get_message_from_kafka
from tests.bpe_create_ei.create_ei import bpe_create_ei


# def bpe_update_fs(ei_create_payload, fs_create_payload):
#     access_token = get_access_token_for_platform_one()
#     x_operation_id = get_x_operation_id(access_token)
#     create_ei_response = bpe_create_ei(ei_create_payload)
#     time.sleep(2)
#     request_to_create_fs = requests.post(
#         url=host + create_fs + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
#         headers={
#             'Authorization': 'Bearer ' + access_token,
#             'X-OPERATION-ID': x_operation_id,
#             'Content-Type': 'application/json'},
#         json=fs_create_payload)
#     time.sleep(2)
#     message_from_kafka = get_message_from_kafka(x_operation_id)
#     return request_to_create_fs, message_from_kafka, x_operation_id, create_ei_response[1]['data']['outcomes']['ei'][0][
#         'id']
from tests.presets import set_instance_for_request


def bpe_update_fs(cpid, fs_ocid, fs_update_payload, fs_token):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    time.sleep(2)
    host = set_instance_for_request()
    request_to_update_fs = requests.post(
        url=host + update_fs + cpid + "/" + fs_ocid,
        headers={
            'Authorization': 'Bearer ' + access_token,
            'X-OPERATION-ID': x_operation_id,
            'X-TOKEN': fs_token,
            'Content-Type': 'application/json'},
        json=fs_update_payload)
    time.sleep(2)
    message_from_kafka = get_message_from_kafka(x_operation_id)
    return request_to_update_fs, message_from_kafka, x_operation_id, fs_ocid
