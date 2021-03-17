import time
import requests
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.cassandra_inserts_into_Database import insert_into_db_create_pn_full_data_model, \
    insert_into_db_create_pn_obligatory_data_model
from tests.kafka_messages import get_message_from_kafka
from tests.presets import set_instance_for_request, create_pn, update_pn
from useful_functions import prepared_cpid


def get_some_id_of_pn_record(url):
    get_url = requests.get(url=url).json()["records"]
    record_list = list()
    item_list = list()
    lot_list = list()
    document_list = list()
    for d in get_url:
        for d_1 in d["compiledRelease"]["relatedProcesses"]:
            if d_1["relationship"] == ["planning"]:
                record_list.append(d_1)
    planning_notice = requests.get(url=record_list[0]["uri"]).json()
    if "releases" in planning_notice.keys() and "tender" in planning_notice["releases"][0].keys() and "items" in \
            planning_notice["releases"][0]["tender"].keys():

        for object in planning_notice["releases"][0]["tender"]["items"]:
            item_list.append(object["id"])

    if "releases" in planning_notice.keys() and "tender" in planning_notice["releases"][0].keys() and "lots" in \
            planning_notice["releases"][0]["tender"].keys():

        for object in planning_notice["releases"][0]["tender"]["lots"]:
            lot_list.append(object["id"])

    if "releases" in planning_notice.keys() and "tender" in planning_notice["releases"][0].keys() and "documents" in \
            planning_notice["releases"][0]["tender"].keys():
        for object in planning_notice["releases"][0]["tender"]["documents"]:
            document_list.append(object["id"])

    return item_list, lot_list, document_list


def bpe_update_pn_one_fs_if_pn_full(cpid, additional_value, pn_update_payload):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    time.sleep(2)
    ei_id = prepared_cpid()
    create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
    get_url = requests.get(url=create_pn[0]).json()["records"]
    ms_before_updating = list()
    for d in get_url:
        for d_1 in d["compiledRelease"]["relatedProcesses"]:
            if d_1["relationship"] == ["parent"]:
                ms_before_updating.append(d_1)
    ms_before_updating = requests.get(url=ms_before_updating[0]["uri"]).json()
    pn_before_updating = list()
    for d in get_url:
        for d_1 in d["compiledRelease"]["relatedProcesses"]:
            if d_1["relationship"] == ["planning"]:
                pn_before_updating.append(d_1)
    pn_before_updating = requests.get(url=pn_before_updating[0]["uri"]).json()
    host = set_instance_for_request()
    if "tender" in pn_update_payload.keys() and "lots" in pn_update_payload["tender"].keys():
        if "id" in pn_update_payload["tender"]["lots"][0].keys():
            enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
            pn_update_payload["tender"]["lots"][0]["id"] = enrich_payload[1][0]
        if "id" in pn_update_payload["tender"]["lots"][1].keys():
            enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
            pn_update_payload["tender"]["lots"][1]["id"] = enrich_payload[1][1]

    if "tender" in pn_update_payload.keys() and "items" in pn_update_payload["tender"].keys():
        if "id" in pn_update_payload["tender"]["items"][0].keys():
            enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
            pn_update_payload["tender"]["items"][0]["id"] = enrich_payload[0][0]
        if "relatedLot" in pn_update_payload["tender"]["items"][0].keys():
            enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
            pn_update_payload["tender"]["items"][0]["relatedLot"] = enrich_payload[1][0]
        if "id" in pn_update_payload["tender"]["items"][1].keys():
            enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
            pn_update_payload["tender"]["items"][1]["id"] = enrich_payload[0][1]
        if "relatedLot" in pn_update_payload["tender"]["items"][0].keys():
            enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
            pn_update_payload["tender"]["items"][1]["relatedLot"] = enrich_payload[1][1]

    if "tender" in pn_update_payload.keys() and "documents" in pn_update_payload["tender"].keys():
        if "id" in pn_update_payload["tender"]["documents"][0].keys():
            enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
            pn_update_payload["tender"]["documents"][0]["id"] = enrich_payload[2][0]
        if "relatedLots" in pn_update_payload["tender"]["documents"][0].keys():
            enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
            pn_update_payload["tender"]["documents"][0]["relatedLots"] = [enrich_payload[1][0]]
        if "id" in pn_update_payload["tender"]["documents"][1].keys():
            enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
            pn_update_payload["tender"]["documents"][1]["id"] = enrich_payload[2][1]
        if "relatedLots" in pn_update_payload["tender"]["documents"][1].keys():
            enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
            pn_update_payload["tender"]["documents"][1]["relatedLots"] = [enrich_payload[1][1]]

    request_to_update_pn = requests.post(
        url=host + update_pn + cpid + '/' + create_pn[3],
        headers={
            'Authorization': 'Bearer ' + access_token,
            'X-OPERATION-ID': x_operation_id,
            'X-TOKEN': create_pn[4],
            'Content-Type': 'application/json'},
        json=pn_update_payload)
    time.sleep(2)
    message_from_kafka = get_message_from_kafka(x_operation_id)

    return request_to_update_pn, message_from_kafka, x_operation_id, ms_before_updating, pn_before_updating, create_pn[3]


def bpe_update_pn_one_fs_if_pn_obligatory(cpid, additional_value, pn_update_payload):
    access_token = get_access_token_for_platform_one()
    x_operation_id = get_x_operation_id(access_token)
    time.sleep(2)
    ei_id = prepared_cpid()
    create_pn = insert_into_db_create_pn_obligatory_data_model(cpid, ei_id, additional_value)
    get_url = requests.get(url=create_pn[0]).json()["records"]
    ms_before_updating = list()
    for d in get_url:
        for d_1 in d["compiledRelease"]["relatedProcesses"]:
            if d_1["relationship"] == ["parent"]:
                ms_before_updating.append(d_1)
    ms_before_updating = requests.get(url=ms_before_updating[0]["uri"]).json()
    pn_before_updating = list()
    for d in get_url:
        for d_1 in d["compiledRelease"]["relatedProcesses"]:
            if d_1["relationship"] == ["planning"]:
                pn_before_updating.append(d_1)
    pn_before_updating = requests.get(url=pn_before_updating[0]["uri"]).json()
    host = set_instance_for_request()
    request_to_update_pn = requests.post(
        url=host + update_pn + cpid + '/' + create_pn[3],
        headers={
            'Authorization': 'Bearer ' + access_token,
            'X-OPERATION-ID': x_operation_id,
            'X-TOKEN': create_pn[4],
            'Content-Type': 'application/json'},
        json=pn_update_payload)
    time.sleep(2)
    message_from_kafka = get_message_from_kafka(x_operation_id)

    return request_to_update_pn, message_from_kafka, x_operation_id, ms_before_updating, pn_before_updating
