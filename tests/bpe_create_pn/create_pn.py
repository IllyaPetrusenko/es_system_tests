import time

import requests

from tests.authorization import get_access_token_for_platform_one, get_x_operation_id

from tests.cassandra_inserts_into_Database import insert_into_db_create_fs
from tests.kafka_messages import get_message_from_kafka
from tests.presets import set_instance_for_request, create_pn


def bpe_create_pn_one_fs(cpid, pn_create_payload, pmd):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    time.sleep(2)
    test_create_fs = insert_into_db_create_fs(cpid)
    if "planning" in pn_create_payload.keys() and "budget" in pn_create_payload[
        "planning"].keys() and "budgetBreakdown" in pn_create_payload["planning"][
        "budget"].keys() and "id" in pn_create_payload["planning"]["budget"]["budgetBreakdown"][0].keys():
        pn_create_payload["planning"]["budget"]["budgetBreakdown"][0]["id"] = test_create_fs[2]
        host = set_instance_for_request()
        request_to_create_pn = requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": pmd},
            json=pn_create_payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
    else:
        host = set_instance_for_request()
        request_to_create_pn = requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": pmd},
            json=pn_create_payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
    return request_to_create_pn, message_from_kafka, x_operation_id


def bpe_create_pn_two_fs(cpid_1, buyer_1, payer_1, funder_1, cpid_2, buyer_2, payer_2, funder_2, pn_create_payload,
                         pmd, seconds=0):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    time.sleep(2)
    test_create_fs_1 = insert_into_db_create_fs(cpid=cpid_1, buyer=buyer_1, payer=payer_1, funder=funder_1)
    time.sleep(seconds)
    test_create_fs_2 = insert_into_db_create_fs(cpid=cpid_2, buyer=buyer_2, payer=payer_2, funder=funder_2)
    if "planning" in pn_create_payload.keys() and "budget" in pn_create_payload[
        "planning"].keys() and "budgetBreakdown" in pn_create_payload["planning"][
        "budget"].keys() and "id" in pn_create_payload["planning"]["budget"]["budgetBreakdown"][0].keys() and "id" in \
            pn_create_payload["planning"]["budget"]["budgetBreakdown"][1].keys():

        pn_create_payload["planning"]["budget"]["budgetBreakdown"][0]["id"] = test_create_fs_1[2]

        pn_create_payload["planning"]["budget"]["budgetBreakdown"][1]["id"] = test_create_fs_2[2]
        host = set_instance_for_request()
        request_to_create_pn = requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": pmd},
            json=pn_create_payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
    else:
        host = set_instance_for_request()
        request_to_create_pn = requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": pmd},
            json=pn_create_payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
    return request_to_create_pn, message_from_kafka, x_operation_id
