import copy
import json
import time

import requests

from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.bpe_create_cnonpn.payloads import payload_cnonpn_auction_full_data_model
from tests.cassandra_inserts_into_Database import insert_into_db_create_pn_full_data_model, \
    insert_into_db_create_pn_obligatory_data_model
from tests.iStorage import Document
from tests.kafka_messages import get_message_from_kafka
from tests.presets import create_cn, set_instance_for_request
from useful_functions import prepared_cpid


class CNonPN:
    def __init__(self):
        self.access_token = get_access_token_for_platform_one()
        self.x_operation_id = get_x_operation_id(self.access_token)

    def create_pn_full_data_model(self, cpid, additional_value):
        self.cpid = cpid
        ei_id = prepared_cpid()
        pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
        return pn

    def create_pn_obligatory_data_model(self, cpid, additional_value, identifier_scheme="MD-IDNO",
                                        procuring_entity_id="2"):
        self.cpid = cpid
        self.identifier_scheme = identifier_scheme
        self.procuring_entity_id = procuring_entity_id
        ei_id = prepared_cpid()
        pn = insert_into_db_create_pn_obligatory_data_model(cpid, ei_id, additional_value,
                                                            procuring_entity_identifier_scheme=self.identifier_scheme,
                                                            procuring_entity_id=self.procuring_entity_id, )
        return pn

    def get_some_id_of_pn_record(self, pn):
        self.pn = pn
        self.item_list = list()
        self.lot_list = list()
        self.document_list = list()
        self.additionalClassifications_list = list()
        get_url = requests.get(url=self.pn[0]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        if "releases" in planning_notice.keys() and "tender" in planning_notice["releases"][0].keys() and "items" in \
                planning_notice["releases"][0]["tender"].keys():
            for object in planning_notice["releases"][0]["tender"]["items"]:
                self.item_list.append(object["id"])

        if "releases" in planning_notice.keys() and "tender" in planning_notice["releases"][0].keys() and "lots" in \
                planning_notice["releases"][0]["tender"].keys():

            for object in planning_notice["releases"][0]["tender"]["lots"]:
                self.lot_list.append(object["id"])

        if "releases" in planning_notice.keys() and "tender" in planning_notice["releases"][0].keys() and "documents" \
                in planning_notice["releases"][0]["tender"].keys():
            for object in planning_notice["releases"][0]["tender"]["documents"]:
                self.document_list.append(object["id"])

        if "releases" in planning_notice.keys() and "tender" in planning_notice["releases"][0].keys() and "items" in \
                planning_notice["releases"][0]["tender"].keys() and "additionalClassifications" in \
                planning_notice["releases"][0]["tender"]["items"][0].keys():
            for object in planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"]:
                self.additionalClassifications_list.append(object["id"])

        if "releases" in planning_notice.keys() and "tender" in planning_notice["releases"][0].keys() and "items" in \
                planning_notice["releases"][0]["tender"].keys() and "additionalClassifications" in \
                planning_notice["releases"][0]["tender"]["items"][0].keys():
            for object in planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"]:
                self.additionalClassifications_list.append(object["id"])

        return self.item_list, self.lot_list, self.document_list, self.additionalClassifications_list

    def preparing_payload(self, payload):
        self.payload = payload
        if "tender" in payload.keys() and "lots" in payload["tender"].keys():
            if "tender" in payload.keys() and "lots" in payload["tender"].keys() and \
                    "id" in payload["tender"]["lots"][0].keys():
                payload["tender"]["lots"][0]["id"] = self.lot_list[1][0]
            if "id" in payload["tender"]["lots"][1].keys():
                payload["tender"]["lots"][1]["id"] = self.lot_list[1][1]

        if "tender" in payload.keys() and "items" in payload["tender"].keys():
            if "id" in payload["tender"]["items"][0].keys():
                payload["tender"]["items"][0]["id"] = self.item_list[0][0]
            if "relatedLot" in payload["tender"]["items"][0].keys():
                payload["tender"]["items"][0]["relatedLot"] = self.item_list[1][0]
            if "id" in payload["tender"]["items"][1].keys():
                payload["tender"]["items"][1]["id"] = self.item_list[0][1]
            if "relatedLot" in payload["tender"]["items"][1].keys():
                payload["tender"]["items"][1]["relatedLot"] = self.item_list[1][1]

        if "tender" in payload.keys() and "documents" in payload["tender"].keys():
            if "id" in payload["tender"]["documents"][0].keys():
                payload["tender"]["documents"][0]["id"] = self.document_list[2][0]
            if "relatedLots" in payload["tender"]["documents"][0].keys():
                payload["tender"]["documents"][0]["relatedLots"] = [self.lot_list[1][0]]
            if "id" in payload["tender"]["documents"][1].keys():
                payload["tender"]["documents"][1]["id"] = [self.document_list[2][1]]
            if "relatedLots" in payload["tender"]["documents"][1].keys():
                payload["tender"]["documents"][1]["relatedLots"] = [self.lot_list[1][1]]

        if "tender" in payload.keys() and "items" in payload["tender"].keys() and "additionalClassifications" in \
                payload["tender"]["items"][0].key():
            if "id" in payload["tender"]["items"][0]["additionalClassifications"][0].keys():
                payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = \
                    self.additionalClassifications_list[3][0]

        if "tender" in payload.keys() and "items" in payload["tender"].keys() and "additionalClassifications" in \
                payload["tender"]["items"][1].key():
            if "id" in payload["tender"]["items"][1]["additionalClassifications"][0].keys():
                payload["tender"]["items"][1]["additionalClassifications"][0]["id"] = \
                    self.additionalClassifications_list[3][1]
        return self.payload

    def create_request_cnonpn(self, cpid, pn, payload):
        self.cpid = cpid
        self.pn = pn
        self.payload = payload
        host = set_instance_for_request()
        cnonpn = requests.post(
            url=host + create_cn + cpid + '/' + pn[3],
            headers={
                'Authorization': 'Bearer ' + self.access_token,
                'X-OPERATION-ID': self.x_operation_id,
                'X-TOKEN': pn[4],
                'Content-Type': 'application/json'},
            json=payload)
        return cnonpn

    def get_message_from_kafka(self):
        time.sleep(3.6)
        message_from_kafka = get_message_from_kafka(self.x_operation_id)
        return message_from_kafka

# This is example of creating CNonPn
# c = CNonPN()
# cpid = prepared_cpid()
# pn = c.create_pn_obligatory_data_model(cpid=cpid, additional_value="TEST_OT")
# get_some_value = c.get_some_id_of_pn_record(pn)
# print(get_some_value)
# payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
#
# # payload_was_enriched = c.preparing_payload(payload)
# # print(json.dumps(payload_was_enriched))
# cnonpn = c.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
# time.sleep(1.3)
# message_from_kafka = c.get_message_from_kafka()
# print(message_from_kafka)
