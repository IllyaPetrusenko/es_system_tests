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
from useful_functions import prepared_cpid, get_contract_period, get_new_period

contract_period = get_contract_period()
period = get_new_period()


class CNonPN:
    def __init__(self):
        self.access_token = get_access_token_for_platform_one()
        self.x_operation_id = get_x_operation_id(self.access_token)

    def create_pn_full_data_model(self, cpid, additional_value, identifier_scheme="MD-IDNO",
                                  procuring_entity_id="4"):
        self.cpid = cpid
        self.identifier_scheme = identifier_scheme
        self.procuring_entity_id = procuring_entity_id
        ei_id = prepared_cpid()
        pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value,
                                                      procuring_entity_identifier_scheme=self.identifier_scheme,
                                                      procuring_entity_id=self.procuring_entity_id, )
        return pn

    def create_pn_obligatory_data_model(self, cpid, additional_value, identifier_scheme="MD-IDNO",
                                        procuring_entity_id="4"):
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

    def enriching_payload(self, payload):
        self.payload = payload
        payload["tender"]["lots"] = [
            {
                "id": self.lot_list[0],
                "internalId": "internalId of lot",
                "title": "title of lot",
                "description": "description of lot",
                "value": {
                    "amount": 1500,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "street of placeOfPerformance",
                        "postalCode": "postalCode of placeOfPerformance",
                        "addressDetails": {
                            "country": {
                                "id": "MD"
                            },
                            "region": {
                                "id": "5700000"
                            },
                            "locality": {
                                "scheme": "CUATM",
                                "id": "5711001",
                                "description": "description of locality"
                            }
                        }
                    },
                    "description": "description of placeOfPerformance"
                },
                "hasOptions": True,
                "options": [
                    {
                        "description": "The buyer has the option to buy an additional hundred uniforms.",
                        "period": {
                            "durationInDays": 180,
                            "startDate": period[2],
                            "endDate": period[3],
                            "maxExtentDate": period[3]
                        }
                    }
                ],
                "hasRecurrence": True,
                "recurrence": {
                    "dates": [
                        {
                            "startDate": period[2]
                        },
                        {
                            "startDate": period[2]
                        }
                    ],
                    "description": "The duration of this contract and recurrent contracts will not exceed three years."
                },
                "hasRenewal": True,
                "renewal": {
                    "description": "The contracting authority reserves the right to extend the term for a period or "
                                   "periods of up to 1 year with a maximum of 2 such extensions on the same terms and "
                                   "conditions, subject to the contracting authority's obligations at law.",
                    "minimumRenewals": 2,
                    "maximumRenewals": 5,
                    "period": {
                        "durationInDays": 365,
                        "startDate": period[2],
                        "endDate": period[1],
                        "maxExtentDate": period[3]
                    }
                }
            },
            {
                "id": self.lot_list[1],
                "internalId": "internalId of lot",
                "title": "title of lot",
                "description": "description of lot",
                "value": {
                    "amount": 500,
                    "currency": "EUR"
                },
                "contractPeriod": {
                    "startDate": contract_period[0],
                    "endDate": contract_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "street of placeOfPerformance",
                        "postalCode": "postalCode of placeOfPerformance",
                        "addressDetails": {
                            "country": {
                                "id": "MD"
                            },
                            "region": {
                                "id": "5700000"
                            },
                            "locality": {
                                "scheme": "CUATM",
                                "id": "5711001",
                                "description": "description of locality"
                            }
                        }
                    },
                    "description": "description of placeOfPerformance"
                },
                "hasOptions": True,
                "options": [
                    {
                        "description": "The buyer has the option to buy an additional hundred uniforms.",
                        "period": {
                            "durationInDays": 180,
                            "startDate": period[2],
                            "endDate": period[3],
                            "maxExtentDate": period[3]
                        }
                    }
                ],
                "hasRecurrence": True,
                "recurrence": {
                    "dates": [
                        {
                            "startDate": period[2]
                        },
                        {
                            "startDate": period[2]
                        }
                    ],
                    "description": "The duration of this contract and recurrent contracts will not exceed three years."
                },
                "hasRenewal": True,
                "renewal": {
                    "description": "The contracting authority reserves the right to extend the term for a period or "
                                   "periods of up to 1 year with a maximum of 2 such extensions on the same terms and "
                                   "conditions, subject to the contracting authority's obligations at law.",
                    "minimumRenewals": 2,
                    "maximumRenewals": 5,
                    "period": {
                        "durationInDays": 365,
                        "startDate": period[2],
                        "endDate": period[1],
                        "maxExtentDate": period[3]
                    }
                }
            }

        ]
        payload["tender"]["items"] = [
            {
                "id": self.item_list[0],
                "internalId": "internalId of item",
                "classification": {
                    "id": "45112350-3",
                    "scheme": "CPV",
                    "description": "description"
                },
                "additionalClassifications": [
                    {
                        "id": self.additionalClassifications_list[0],
                        "scheme": "CPVS",
                        "description": "description"
                    }
                ],
                "quantity": 10,
                "unit": {
                    "id": "10",
                    "name": "name"
                },
                "description": "description of item",
                "relatedLot": self.lot_list[0]
            },
            {
                "id": self.item_list[1],
                "internalId": "internalId of item",
                "classification": {
                    "id": "45112360-6",
                    "scheme": "CPV",
                    "description": "description"
                },
                "additionalClassifications": [
                    {
                        "id": self.additionalClassifications_list[1],
                        "scheme": "CPVS",
                        "description": "description"
                    }
                ],
                "quantity": 10,
                "unit": {
                    "id": "10",
                    "name": "name"
                },
                "description": "description of item",
                "relatedLot": self.lot_list[1]
            }

        ]
        payload["tender"]["electronicAuctions"] = {
            "details": [
                {
                    "id": "1",
                    "relatedLot": self.lot_list[0],
                    "electronicAuctionModalities": [
                        {
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }
                    ]
                },
                {
                    "id": "2",
                    "relatedLot": self.lot_list[1],
                    "electronicAuctionModalities": [
                        {
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }
                    ]
                }
            ]
        }

        payload["tender"]["documents"][0]["id"] = self.document_list[0]
        payload["tender"]["documents"][0]["relatedLots"] = [self.lot_list[0]]
        payload["tender"]["documents"][1]["id"] = self.document_list[1]
        payload["tender"]["documents"][1]["relatedLots"] = [self.lot_list[1]]
        payload["tender"]["documents"][2]["relatedLots"] = [self.lot_list[0]]
        payload["tender"]["criteria"][1]["relatedItem"] = self.item_list[0]

        return self.payload

    def get_previous_ms_release(self, pn):
        self.pn = pn
        ms_release = requests.get(url=self.pn[0] + "/" + self.pn[1]).json()
        return ms_release

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
        time.sleep(3)
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
