import time
import requests
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.cassandra_inserts_into_Database import insert_into_db_create_pn_full_data_model
from tests.kafka_messages import get_message_from_kafka
from tests.presets import set_instance_for_request, create_pn, update_pn
from useful_functions import prepared_cpid


def bpe_update_pn_one_fs(cpid, additional_value, pn_update_payload):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    time.sleep(2)
    cpid_ei = prepared_cpid()
    test_create_pn = insert_into_db_create_pn_full_data_model(cpid, cpid_ei, additional_value)
    pn_update_payload["tender"]["lots"][0]["id"] = test_create_pn[5]
    pn_update_payload["tender"]["lots"][1]["id"] = test_create_pn[6]
    pn_update_payload["tender"]["items"][0]["relatedLot"] = test_create_pn[5]
    pn_update_payload["tender"]["items"][1]["relatedLot"] = test_create_pn[6]
    pn_update_payload["tender"]["items"][0]["id"] = test_create_pn[7]
    pn_update_payload["tender"]["items"][1]["id"] = test_create_pn[8]
    pn_update_payload["tender"]["documents"][0]["relatedLots"] = [test_create_pn[5]]
    pn_update_payload["tender"]["documents"][1]["relatedLots"] = [test_create_pn[6]]
    pn_update_payload["tender"]["documents"][0]["id"] = test_create_pn[9]
    pn_update_payload["tender"]["documents"][1]["id"] = test_create_pn[10]
    host = set_instance_for_request()
    request_to_update_pn = requests.post(
        url=host + update_pn + cpid + '/' + test_create_pn[3],
        headers={
            'Authorization': 'Bearer ' + access_token,
            'X-OPERATION-ID': x_operation_id,
            'X-TOKEN': test_create_pn[4],
            'Content-Type': 'application/json'},
        json=pn_update_payload)
    time.sleep(2)
    message_from_kafka = get_message_from_kafka(x_operation_id)

    return request_to_update_pn, message_from_kafka, x_operation_id, test_create_pn[0], test_create_pn[1], \
           test_create_pn[2], test_create_pn[3], test_create_pn[4]
