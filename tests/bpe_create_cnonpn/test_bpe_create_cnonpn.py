import copy
import json
import time
from uuid import uuid4

import requests
from pytest_testrail.plugin import pytestrail

from tests.Cassandra_session import execute_cql_from_orchestrator_operation_step_by_oper_id, \
    execute_cql_from_orchestrator_operation_step
from tests.authorization import get_x_operation_id, get_access_token_for_platform_one
from tests.bpe_create_cnonpn.create_cnonpn import CNonPN
from tests.bpe_create_cnonpn.payloads import payload_cnonpn_auction_full_data_model, \
    payload_cnonpn_obligatory_data_model
from tests.iStorage import get_hash_md5, get_weught, Document
from tests.kafka_messages import get_message_from_kafka
from tests.presets import create_cn, set_instance_for_request
from useful_functions import prepared_cpid, get_human_date_in_utc_format, is_it_uuid, get_access_token_for_platform_two


class TestBpeCreateCN(object):
    @pytestrail.case("27194")
    def test_27194_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        create_cn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        cn.delete_auction_from_database(cpid)
        assert create_cn_response.text == "ok"
        assert create_cn_response.status_code == 202

    @pytestrail.case("27194")
    def test_27194_2_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert message_from_kafka["data"]["ocid"] == cpid
        assert message_from_kafka["data"]["url"] == f"http://dev.public.eprocurement.systems/tenders/{cpid}"

    @pytestrail.case("27194")
    def test_27194_3_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["status"] == "active"
        assert ev_release["releases"][0]["tender"]["statusDetails"] == "clarification"

    @pytestrail.case("27194")
    def test_27194_4_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tag"] == ["tender"]

    @pytestrail.case("27194")
    def test_27194_5_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()

        ev_release_id = ev_release['releases'][0]['id']
        ev_release_timestamp = int(ev_release_id[46:59])
        date_from_timestamp = get_human_date_in_utc_format(ev_release_timestamp)
        cn.delete_auction_from_database(cpid)
        assert ev_release_id[0:45] == message_from_kafka["data"]["outcomes"]["ev"][0]["id"]
        assert ev_release['releases'][0]['date'] == date_from_timestamp[0]
        assert ev_release['releases'][0][
                   'id'] == f'{message_from_kafka["data"]["outcomes"]["ev"][0]["id"]}' + f'-{str(ev_release_timestamp)}'

    @pytestrail.case("27195")
    def test_27195_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_obligatory_data_model)
        create_cn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        cn.delete_auction_from_database(cpid)
        assert create_cn_response.text == "ok"
        assert create_cn_response.status_code == 202

    @pytestrail.case("27195")
    def test_27195_2_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_obligatory_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert message_from_kafka["data"]["ocid"] == cpid
        assert message_from_kafka["data"]["url"] == f"http://dev.public.eprocurement.systems/tenders/{cpid}"

    @pytestrail.case("27195")
    def test_27195_3_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_obligatory_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = "test_id"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
            "scheme"] = "test_scheme"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
            "description"] = "test_description"
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["awardCriteria"] == payload["tender"]["awardCriteria"]
        assert \
            ev_release["releases"][0]["tender"]["awardCriteriaDetails"] == payload["tender"]["awardCriteriaDetails"]
        assert \
            ev_release["releases"][0]["tender"]["tenderPeriod"]["endDate"] == payload["tender"]["tenderPeriod"][
                "endDate"]
        assert \
            ev_release["releases"][0]["tender"]["enquiryPeriod"]["endDate"] == payload["tender"]["enquiryPeriod"][
                "endDate"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["title"] == payload["tender"]["lots"][0]["title"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["description"] == payload["tender"]["lots"][0][
                "description"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["value"]["amount"] == payload["tender"]["lots"][0][
                "value"]["amount"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["value"]["currency"] == payload["tender"]["lots"][0][
                "value"]["currency"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["contractPeriod"]["startDate"] == \
            payload["tender"]["lots"][0]["contractPeriod"]["startDate"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["contractPeriod"]["endDate"] == \
            payload["tender"]["lots"][0]["contractPeriod"]["endDate"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"] == \
            payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "country"][
                "id"] == payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"][
                "id"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "region"]["id"] == payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "region"]["id"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "locality"]["id"] == payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "locality"]["id"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "locality"]["scheme"] == \
            payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "locality"]["scheme"]
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "locality"]["description"] == payload["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"]["locality"]["description"]
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["classification"]["id"] == payload["tender"]["items"][0][
                "classification"]["id"]
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["quantity"] == payload["tender"]["items"][0]["quantity"]
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["unit"]["id"] == payload["tender"]["items"][0]["unit"]["id"]
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["description"] == payload["tender"]["items"][0][
                "description"]
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["relatedLot"] == ev_release["releases"][0]["tender"][
                "lots"][0]["id"]
        assert \
            ev_release["releases"][0]["tender"]["documents"][0]["documentType"] == payload["tender"]["documents"][0][
                "documentType"]
        assert \
            ev_release["releases"][0]["tender"]["documents"][0]["title"] == payload["tender"]["documents"][0][
                "title"]

    @pytestrail.case("27206")
    def test_27206_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        create_cn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        cn.delete_auction_from_database(cpid)
        assert create_cn_response.text == "ok"
        assert create_cn_response.status_code == 202

    @pytestrail.case("27206")
    def test_27206_2_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert message_from_kafka["data"]["ocid"] == cpid
        assert message_from_kafka["data"]["url"] == f"http://dev.public.eprocurement.systems/tenders/{cpid}"

    @pytestrail.case("27206")
    def test_27206_3_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["title"] == "Evaluation"

    @pytestrail.case("27206")
    def test_27206_4_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["description"] == "Evaluation stage of contracting process"

    @pytestrail.case("27206")
    def test_27206_5_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["procurementMethodRationale"] == payload["tender"][
            "procurementMethodRationale"]

    @pytestrail.case("27206")
    def test_27206_6_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["procurementMethodRationale"] == payload["tender"][
            "procurementMethodRationale"]

    @pytestrail.case("27206")
    def test_27206_7_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["awardCriteria"] == payload["tender"][
            "awardCriteria"]

    @pytestrail.case("27206")
    def test_27206_8_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["awardCriteriaDetails"] == payload["tender"][
            "awardCriteriaDetails"]

    @pytestrail.case("27206")
    def test_27206_9_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["tenderPeriod"]["endDate"] == \
               payload["tender"]["tenderPeriod"]["endDate"]

    @pytestrail.case("27206")
    def test_27206_10_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["enquiryPeriod"]["endDate"] == \
               payload["tender"]["enquiryPeriod"]["endDate"]

    @pytestrail.case("27206")
    def test_27206_11_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["electronicAuctions"]["details"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_12_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(
            ev_release["releases"][0]["tender"]["electronicAuctions"]["details"][0]["relatedLot"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_13_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
                "eligibleMinimumDifference"]["amount"] == \
            payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
                "eligibleMinimumDifference"]["amount"]

    @pytestrail.case("27206")
    def test_27206_14_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
                "eligibleMinimumDifference"]["currency"] == \
            payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
                "eligibleMinimumDifference"]["currency"]

    @pytestrail.case("27206")
    def test_27206_15_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["id"] == payload["tender"]["procuringEntity"]["id"]

    @pytestrail.case("27206")
    def test_27206_16_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["persones"][0]["title"] == payload["tender"]["procuringEntity"]["persones"][0][
            "title"]

    @pytestrail.case("27206")
    def test_27206_17_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["persones"][0]["name"] == payload["tender"]["procuringEntity"]["persones"][0][
            "name"]

    @pytestrail.case("27206")
    def test_27206_18_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["persones"][0]["identifier"]["scheme"] == \
               payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["scheme"]

    @pytestrail.case("27206")
    def test_27206_19_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["persones"][0]["identifier"]["id"] == \
               payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["id"]

    @pytestrail.case("27206")
    def test_27206_20_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["persones"][0]["identifier"]["uri"] == \
               payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["uri"]

    @pytestrail.case("27206")
    def test_27206_21_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["persones"][0]["businessFunctions"][0]["id"] == \
               payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["id"]

    @pytestrail.case("27206")
    def test_27206_22_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["persones"][0]["businessFunctions"][0]["type"] == \
               payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["type"]

    @pytestrail.case("27206")
    def test_27206_23_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["persones"][0]["businessFunctions"][0]["jobTitle"] == \
               payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["jobTitle"]

    @pytestrail.case("27206")
    def test_27206_24_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["persones"][0]["businessFunctions"][0]["period"]["startDate"] == \
               payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["period"]["startDate"]

    @pytestrail.case("27206")
    def test_27206_25_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert procuring_entity_obj[0]["persones"][0]["businessFunctions"][0]["documents"][0]["id"] == \
               payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["id"]

    @pytestrail.case("27206")
    def test_27206_26_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert \
            procuring_entity_obj[0]["persones"][0]["businessFunctions"][0]["documents"][0]["documentType"] == \
            payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["documentType"]

    @pytestrail.case("27206")
    def test_27206_27_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert \
            procuring_entity_obj[0]["persones"][0]["businessFunctions"][0]["documents"][0]["title"] == \
            payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["title"]

    @pytestrail.case("27206")
    def test_27206_28_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        cn.delete_auction_from_database(cpid)
        assert \
            procuring_entity_obj[0]["persones"][0]["businessFunctions"][0]["documents"][0]["description"] == \
            payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["description"]

    @pytestrail.case("27206")
    def test_27206_29_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["criteria"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_30_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["criteria"][0]["title"] == payload["tender"]["criteria"][0]["title"]

    @pytestrail.case("27206")
    def test_27206_31_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["criteria"][0]["relatesTo"] == payload["tender"]["criteria"][0][
            "relatesTo"]

    @pytestrail.case("27206")
    def test_27206_32_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["criteria"][0]["classification"]["id"] == \
               payload["tender"]["criteria"][0]["classification"]["id"]

    @pytestrail.case("27206")
    def test_27206_33_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["criteria"][0]["classification"]["scheme"] == \
               payload["tender"]["criteria"][0]["classification"]["scheme"]

    @pytestrail.case("27206")
    def test_27206_34_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["criteria"][0]["description"] == \
               payload["tender"]["criteria"][0]["description"]

    @pytestrail.case("27206")
    def test_27206_35_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_36_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(
            ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_37_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["title"] \
               == payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["title"]

    @pytestrail.case("27206")
    def test_27206_38_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["dataType"] \
            == payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["dataType"]

    @pytestrail.case("27206")
    def test_27206_39_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                "expectedValue"] == payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                "expectedValue"]

    @pytestrail.case("27206")
    def test_27206_40_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0][
                "minValue"] == payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0][
                "minValue"]

    @pytestrail.case("27206")
    def test_27206_41_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0][
                "maxValue"] == payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0][
                "maxValue"]

    @pytestrail.case("27206")
    def test_27206_42_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                "eligibleEvidences"][0]["id"] == \
            payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0]["id"]

    @pytestrail.case("27206")
    def test_27206_43_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                "eligibleEvidences"][0]["title"] == \
            payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0]["title"]

    @pytestrail.case("27206")
    def test_27206_44_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                "eligibleEvidences"][0]["description"] == \
            payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0][
                "description"]

    @pytestrail.case("27206")
    def test_27206_45_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                "eligibleEvidences"][0]["type"] == \
            payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0][
                "type"]

    @pytestrail.case("27206")
    def test_27206_46_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                "eligibleEvidences"][0]["relatedDocument"]["id"] == \
            payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0][
                "relatedDocument"]["id"]

    @pytestrail.case("27206")
    def test_27206_47_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0][
                "period"]["startDate"] == \
            payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0]["period"]["startDate"]

    @pytestrail.case("27206")
    def test_27206_48_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0][
                "period"]["endDate"] == \
            payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0]["period"]["endDate"]

    @pytestrail.case("27206")
    def test_27206_49_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["conversions"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_50_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["conversions"][0]["relatesTo"] == \
            payload["tender"]["conversions"][0]["relatesTo"]

    @pytestrail.case("27206")
    def test_27206_51_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["conversions"][0]["relatedItem"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_52_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["conversions"][0]["rationale"] == \
            payload["tender"]["conversions"][0]["rationale"]

    @pytestrail.case("27206")
    def test_27206_53_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["conversions"][0]["description"] == \
            payload["tender"]["conversions"][0]["description"]

    @pytestrail.case("27206")
    def test_27206_54_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["conversions"][0]["coefficients"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_55_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["conversions"][0]["coefficients"][0]["value"] == \
               payload["tender"]["conversions"][0]["coefficients"][0]["value"]

    @pytestrail.case("27206")
    def test_27206_56_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["conversions"][0]["coefficients"][0]["coefficient"] == \
               payload["tender"]["conversions"][0]["coefficients"][0]["coefficient"]

    @pytestrail.case("27206")
    def test_27206_57_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["lots"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_58_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["lots"][0]["internalId"] == \
               payload["tender"]["lots"][0]["internalId"]

    @pytestrail.case("27206")
    def test_27206_59_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["lots"][0]["title"] == \
               payload["tender"]["lots"][0]["title"]

    @pytestrail.case("27206")
    def test_27206_60_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["lots"][0]["description"] == \
               payload["tender"]["lots"][0]["description"]

    @pytestrail.case("27206")
    def test_27206_61_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["lots"][0]["value"]["amount"] == \
               payload["tender"]["lots"][0]["value"]["amount"]

    @pytestrail.case("27206")
    def test_27206_62_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["lots"][0]["value"]["currency"] == \
               payload["tender"]["lots"][0]["value"]["currency"]

    @pytestrail.case("27206")
    def test_27206_63_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["lots"][0]["contractPeriod"]["startDate"] == \
               payload["tender"]["lots"][0]["contractPeriod"]["startDate"]

    @pytestrail.case("27206")
    def test_27206_64_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["lots"][0]["contractPeriod"]["endDate"] == \
               payload["tender"]["lots"][0]["contractPeriod"]["endDate"]

    @pytestrail.case("27206")
    def test_27206_65_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"] == \
               payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"]

    @pytestrail.case("27206")
    def test_27206_66_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["postalCode"] == \
               payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["postalCode"]

    @pytestrail.case("27206")
    def test_27206_67_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "country"][
                "id"] == payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"][
                "id"]

    @pytestrail.case("27206")
    def test_27206_68_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"][
                "id"] == payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"]

    @pytestrail.case("27206")
    def test_27206_69_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = "test_id"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
            "scheme"] = "test_scheme"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
            "description"] = "test_description"
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "locality"][
                "id"] == payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
                "id"]

    @pytestrail.case("27206")
    def test_27206_70_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = "test_id"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
            "scheme"] = "test_scheme"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
            "description"] = "test_description"
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "locality"]["scheme"] == \
            payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"]

    @pytestrail.case("27206")
    def test_27206_71_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = "test_id"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
            "scheme"] = "test_scheme"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
            "description"] = "test_description"
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                "locality"]["description"] == \
            payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["description"]

    @pytestrail.case("27206")
    def test_27206_72_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["description"] == \
            payload["tender"]["lots"][0]["placeOfPerformance"]["description"]

    @pytestrail.case("27206")
    def test_27206_73_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["hasOptions"] == \
            payload["tender"]["lots"][0]["hasOptions"]

    @pytestrail.case("27206")
    def test_27206_74_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["options"][0]["description"] == \
            payload["tender"]["lots"][0]["options"][0]["description"]

    @pytestrail.case("27206")
    def test_27206_75_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["options"][0]["period"]["durationInDays"] == \
            payload["tender"]["lots"][0]["options"][0]["period"]["durationInDays"]

    @pytestrail.case("27206")
    def test_27206_76_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["options"][0]["period"]["startDate"] == \
            payload["tender"]["lots"][0]["options"][0]["period"]["startDate"]

    @pytestrail.case("27206")
    def test_27206_77_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["options"][0]["period"]["endDate"] == \
            payload["tender"]["lots"][0]["options"][0]["period"]["endDate"]

    @pytestrail.case("27206")
    def test_27206_78_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["options"][0]["period"]["maxExtentDate"] == \
            payload["tender"]["lots"][0]["options"][0]["period"]["maxExtentDate"]

    @pytestrail.case("27206")
    def test_27206_79_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["hasRecurrence"] == \
            payload["tender"]["lots"][0]["hasRecurrence"]

    @pytestrail.case("27206")
    def test_27206_80_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["recurrence"]["dates"][0]["startDate"] == \
            payload["tender"]["lots"][0]["recurrence"]["dates"][0]["startDate"]

    @pytestrail.case("27206")
    def test_27206_81_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["recurrence"]["description"] == \
            payload["tender"]["lots"][0]["recurrence"]["description"]

    @pytestrail.case("27206")
    def test_27206_82_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["hasRenewal"] == \
            payload["tender"]["lots"][0]["hasRenewal"]

    @pytestrail.case("27206")
    def test_27206_83_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["renewal"]["description"] == \
            payload["tender"]["lots"][0]["renewal"]["description"]

    @pytestrail.case("27206")
    def test_27206_84_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["renewal"]["minimumRenewals"] == \
            payload["tender"]["lots"][0]["renewal"]["minimumRenewals"]

    @pytestrail.case("27206")
    def test_27206_85_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["renewal"]["maximumRenewals"] == \
            payload["tender"]["lots"][0]["renewal"]["maximumRenewals"]

    @pytestrail.case("27206")
    def test_27206_86_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["renewal"]["period"]["durationInDays"] == \
            payload["tender"]["lots"][0]["renewal"]["period"]["durationInDays"]

    @pytestrail.case("27206")
    def test_27206_87_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["renewal"]["period"]["startDate"] == \
            payload["tender"]["lots"][0]["renewal"]["period"]["startDate"]

    @pytestrail.case("27206")
    def test_27206_88_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["renewal"]["period"]["endDate"] == \
            payload["tender"]["lots"][0]["renewal"]["period"]["endDate"]

    @pytestrail.case("27206")
    def test_27206_89_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["lots"][0]["renewal"]["period"]["maxExtentDate"] == \
            payload["tender"]["lots"][0]["renewal"]["period"]["maxExtentDate"]

    @pytestrail.case("27206")
    def test_27206_90_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["items"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_91_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["internalId"] == \
            payload["tender"]["items"][0]["internalId"]

    @pytestrail.case("27206")
    def test_27206_92_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["classification"]["id"] == \
            payload["tender"]["items"][0]["classification"]["id"]

    @pytestrail.case("27206")
    def test_27206_93_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"] == \
            payload["tender"]["items"][0]["additionalClassifications"][0]["id"]

    @pytestrail.case("27206")
    def test_27206_94_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["quantity"] == payload["tender"]["items"][0]["quantity"]

    @pytestrail.case("27206")
    def test_27206_95_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["unit"]["id"] == \
            payload["tender"]["items"][0]["unit"]["id"]

    @pytestrail.case("27206")
    def test_27206_96_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["items"][0]["description"] == \
            payload["tender"]["items"][0]["description"]

    @pytestrail.case("27206")
    def test_27206_97_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["items"][0]["relatedLot"], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27206")
    def test_27206_98_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["documents"][0]["documentType"] == \
            payload["tender"]["documents"][0]["documentType"]

    @pytestrail.case("27206")
    def test_27206_99_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["documents"][0]["id"] == \
            payload["tender"]["documents"][0]["id"]

    @pytestrail.case("27206")
    def test_27206_100_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["documents"][0]["title"] == \
            payload["tender"]["documents"][0]["title"]

    @pytestrail.case("27206")
    def test_27206_101_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert \
            ev_release["releases"][0]["tender"]["documents"][0]["description"] == \
            payload["tender"]["documents"][0]["description"]

    @pytestrail.case("27206")
    def test_27206_102_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["documents"][0]["relatedLots"][0], 4)
        cn.delete_auction_from_database(cpid)
        assert checking_uuid == True

    @pytestrail.case("27197")
    def test_27197_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.00.00.00"
        assert message_from_kafka["errors"][0]["description"] == "Data processing exception."

    @pytestrail.case("27197")
    def test_27197_2_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["title"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlin" \
                                                                 "ParameterException: Instantiation of [simple " \
                                                                 "type, class com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest$Tender]" \
                                                                 " value failed for JSON property title due to " \
                                                                 "missing (therefore NULL) value for creator " \
                                                                 "parameter title which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column: " \
                                                                 "-1] (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"title\"])"

    @pytestrail.case("27197")
    def test_27197_3_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["description"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlin" \
                                                                 "ParameterException: Instantiation of [simple " \
                                                                 "type, class com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest$Tender]" \
                                                                 " value failed for JSON property description due " \
                                                                 "to missing (therefore NULL) value for creator " \
                                                                 "parameter description which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column: " \
                                                                 "-1] (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"description\"])"

    @pytestrail.case("27197")
    def test_27197_4_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["awardCriteria"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender] value failed for " \
                                                                 "JSON property awardCriteria due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "awardCriteria which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest" \
                                                                 "[\"tender\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"awardCriteria\"])"

    @pytestrail.case("27197")
    def test_27197_5_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["awardCriteriaDetails"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.84"
        assert message_from_kafka["errors"][0]["description"] == "Invalid award criteria. For awardCriteria in " \
                                                                 "[costOnly, qualityOnly, ratedCriteria] field " \
                                                                 "'awardCriteriaDetails' are required "

    @pytestrail.case("27197")
    def test_27197_6_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["tenderPeriod"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.04.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.submission." \
                                                                 "infrastructure.handler.v1.model.request.PeriodRq]" \
                                                                 " value failed for JSON property tenderPeriod due" \
                                                                 " to missing (therefore NULL) value for creator" \
                                                                 " parameter tenderPeriod which is a non-nullable" \
                                                                 " type\n at [Source: UNKNOWN; line: -1, column: -1]" \
                                                                 " (through reference chain: com.procurement." \
                                                                 "submission.infrastructure.handler.v1.model" \
                                                                 ".request.PeriodRq[\"tenderPeriod\"])"

    @pytestrail.case("27197")
    def test_27197_7_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["tenderPeriod"]["endDate"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.04.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.submission." \
                                                                 "model.dto.ocds.Period] value failed for JSON " \
                                                                 "property endDate due to missing (therefore NULL)" \
                                                                 " value for creator parameter endDate which is a " \
                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: com." \
                                                                 "procurement.submission.infrastructure.handler." \
                                                                 "v1.model.request.PeriodRq[\"tenderPeriod\"]->" \
                                                                 "com.procurement.submission.model.dto.ocds." \
                                                                 "Period[\"endDate\"])"

    @pytestrail.case("27197")
    def test_27197_8_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["enquiryPeriod"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.05.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement." \
                                                                 "clarification.infrastructure.handler.v1." \
                                                                 "model.request.PeriodRq] value failed for " \
                                                                 "JSON property enquiryPeriod due to missing" \
                                                                 " (therefore NULL) value for creator " \
                                                                 "parameter enquiryPeriod which is a non-" \
                                                                 "nullable type\n at [Source: UNKNOWN; line:" \
                                                                 " -1, column: -1] (through reference chain: " \
                                                                 "com.procurement.clarification.infrastructure." \
                                                                 "handler.v1.model.request.PeriodRq" \
                                                                 "[\"enquiryPeriod\"])"

    @pytestrail.case("27197")
    def test_27197_9_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["enquiryPeriod"]["endDate"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.05.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of" \
                                                                 " [simple type, class com.procurement." \
                                                                 "submission.model.dto.ocds.Period] value " \
                                                                 "failed for JSON property endDate due to " \
                                                                 "missing (therefore NULL) value for creator" \
                                                                 " parameter endDate which is a non-nullable" \
                                                                 " type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.submission.infrastructure." \
                                                                 "handler.v1.model.request.PeriodRq" \
                                                                 "[\"enquiryPeriod\"]->com.procurement." \
                                                                 "submission.model.dto.ocds.Period[\"endDate\"])"

    @pytestrail.case("27197")
    def test_27197_10_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procurementMethodModalities"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.67"
        assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value. Auction sign " \
                                                                 "must be passed"

    @pytestrail.case("27197")
    def test_27197_11_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["electronicAuctions"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.67"
        assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value. Auction sign " \
                                                                 "must be not passed"

    @pytestrail.case("27197")
    def test_27197_12_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["electronicAuctions"]["details"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions] " \
                                                                 "value failed for JSON property details due " \
                                                                 "to missing (therefore NULL) value for creator" \
                                                                 " parameter details which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column:" \
                                                                 " -1] (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"electronicAuctions\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "ElectronicAuctions[\"details\"])"

    @pytestrail.case("27197")
    def test_27197_13_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["electronicAuctions"]["details"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions" \
                                                                 "$Detail] value failed for JSON property id " \
                                                                 "due to missing (therefore NULL) value for " \
                                                                 "creator parameter id which is a non-nullable" \
                                                                 " type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"electronicAuctions\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model." \
                                                                 "request.OpenCnOnPnRequest$Tender$Electronic" \
                                                                 "Auctions[\"details\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest$" \
                                                                 "Tender$ElectronicAuctions$Detail[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_14_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["electronicAuctions"]["details"][0]["relatedLot"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of" \
                                                                 " [simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions$" \
                                                                 "Detail] value failed for JSON property " \
                                                                 "relatedLot due to missing (therefore NULL) " \
                                                                 "value for creator parameter relatedLot which" \
                                                                 " is a non-nullable type\n at [Source: UNKNOWN; " \
                                                                 "line: -1, column: -1] (through reference chain:" \
                                                                 " com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                                                 "->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest$" \
                                                                 "Tender[\"electronicAuctions\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions" \
                                                                 "[\"details\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Electronic" \
                                                                 "Auctions$Detail[\"relatedLot\"])"

    @pytestrail.case("27197")
    def test_27197_15_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender$ElectronicAuctions$Detail] value " \
                                                                 "failed for JSON property electronicAuction" \
                                                                 "Modalities due to missing (therefore NULL) value " \
                                                                 "for creator parameter electronicAuctionModalities " \
                                                                 "which is a non-nullable type\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"electronicAuctions\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "ElectronicAuctions[\"details\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender$ElectronicAuctions$Detail" \
                                                                 "[\"electronicAuctionModalities\"])"

    @pytestrail.case("27197")
    def test_27197_16_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
            "eligibleMinimumDifference"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions$" \
                                                                 "Detail$Modalities] value failed for JSON " \
                                                                 "property eligibleMinimumDifference due to " \
                                                                 "missing (therefore NULL) value for creator " \
                                                                 "parameter eligibleMinimumDifference which is " \
                                                                 "a non-nullable type\n at [Source: UNKNOWN; " \
                                                                 "line: -1, column: -1] (through reference " \
                                                                 "chain: com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest" \
                                                                 "[\"tender\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"electronicAuctions\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "ElectronicAuctions[\"details\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions$" \
                                                                 "Detail[\"electronicAuctionModalities\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model." \
                                                                 "request.OpenCnOnPnRequest$Tender$Electronic" \
                                                                 "Auctions$Detail$Modalities[\"eligibleMinimum" \
                                                                 "Difference\"])"

    @pytestrail.case("27197")
    def test_27197_17_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
            "eligibleMinimumDifference"]["amount"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of [simple" \
                                                                 " type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions$" \
                                                                 "Detail$Modalities$EligibleMinimumDifference] " \
                                                                 "value failed for JSON property amount due to " \
                                                                 "missing (therefore NULL) value for creator " \
                                                                 "parameter amount which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column: " \
                                                                 "-1] (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender" \
                                                                 "[\"electronicAuctions\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model." \
                                                                 "request.OpenCnOnPnRequest$Tender$Electronic" \
                                                                 "Auctions[\"details\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest$" \
                                                                 "Tender$ElectronicAuctions$Detail" \
                                                                 "[\"electronicAuctionModalities\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions$" \
                                                                 "Detail$Modalities[\"eligibleMinimumDifference\"]" \
                                                                 "->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest$" \
                                                                 "Tender$ElectronicAuctions$Detail$Modalities$" \
                                                                 "EligibleMinimumDifference[\"amount\"])"

    @pytestrail.case("27197")
    def test_27197_18_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
            "eligibleMinimumDifference"]["currency"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions$" \
                                                                 "Detail$Modalities$EligibleMinimumDifference] " \
                                                                 "value failed for JSON property currency due " \
                                                                 "to missing (therefore NULL) value for creator " \
                                                                 "parameter currency which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column: -1]" \
                                                                 " (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"electronicAuctions\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "ElectronicAuctions[\"details\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions$" \
                                                                 "Detail[\"electronicAuctionModalities\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions$" \
                                                                 "Detail$Modalities[\"eligibleMinimumDifference\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "ElectronicAuctions$Detail$Modalities$Eligible" \
                                                                 "MinimumDifference[\"currency\"])"

    @pytestrail.case("27197")
    def test_27197_19_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlin" \
                                                                 "ParameterException: Instantiation of [simple " \
                                                                 "type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ProcuringEntity] value " \
                                                                 "failed for JSON property id due to missing " \
                                                                 "(therefore NULL) value for creator parameter id " \
                                                                 "which is a non-nullable type\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"procuringEntity\"]->" \
                                                                 "com.procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "ProcuringEntity[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_20_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["title"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.Persone] value failed for JSON property" \
                                                                 " title due to missing (therefore NULL) value " \
                                                                 "for creator parameter title which is a non-" \
                                                                 "nullable type\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: " \
                                                                 "com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"title\"])"

    @pytestrail.case("27197")
    def test_27197_21_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["name"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.Persone] value failed for JSON " \
                                                                 "property name due to missing (therefore NULL) " \
                                                                 "value for creator parameter name which is a " \
                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: com." \
                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                 "model.dto.data.OrganizationReference" \
                                                                 "[\"persones\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"name\"])"

    @pytestrail.case("27197")
    def test_27197_22_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["identifier"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.Persone] value failed for JSON " \
                                                                 "property identifier due to missing (therefore " \
                                                                 "NULL) value for creator parameter identifier " \
                                                                 "which is a non-nullable type\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement." \
                                                                 "mdm.model.dto.data.TenderTD[\"procuringEntity\"]" \
                                                                 "->com.procurement.mdm.model.dto.data." \
                                                                 "OrganizationReference[\"persones\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                 "dto.data.Persone[\"identifier\"])"

    @pytestrail.case("27197")
    def test_27197_23_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["scheme"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm." \
                                                                 "model.dto.data.Identifier] value failed for " \
                                                                 "JSON property scheme due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "scheme which is a non-nullable type\n at " \
                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement.mdm." \
                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                 "mdm.model.dto.data.TenderTD[\"procuringEntity\"]" \
                                                                 "->com.procurement.mdm.model.dto.data." \
                                                                 "OrganizationReference[\"persones\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                 "dto.data.Persone[\"identifier\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Identifier" \
                                                                 "[\"scheme\"])"

    @pytestrail.case("27197")
    def test_27197_24_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.Identifier] value failed for JSON " \
                                                                 "property id due to missing (therefore NULL) " \
                                                                 "value for creator parameter id which is a " \
                                                                 "non-nullable type\n at [Source: UNKNOWN; " \
                                                                 "line: -1, column: -1] (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"identifier\"]->com.procurement." \
                                                                 "mdm.model.dto.data.Identifier[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_25_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlin" \
                                                                 "ParameterException: Instantiation of [simple " \
                                                                 "type, class com.procurement.mdm.model.dto.data." \
                                                                 "Persone] value failed for JSON property " \
                                                                 "businessFunctions due to missing (therefore " \
                                                                 "NULL) value for creator parameter " \
                                                                 "businessFunctions which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]" \
                                                                 "->com.procurement.mdm.model.dto.data." \
                                                                 "TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data.Persone" \
                                                                 "[\"businessFunctions\"])"

    @pytestrail.case("27197")
    def test_27197_26_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of" \
                                                                 " [simple type, class com.procurement.mdm." \
                                                                 "model.dto.data.BusinessFunction] value failed" \
                                                                 " for JSON property id due to missing (therefore" \
                                                                 " NULL) value for creator parameter id which is" \
                                                                 " a non-nullable type\n at [Source: UNKNOWN;" \
                                                                 " line: -1, column: -1] (through reference chain:" \
                                                                 " com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"businessFunctions\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.BusinessFunction[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_27_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["type"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.BusinessFunction] value failed for " \
                                                                 "JSON property type due to missing (therefore " \
                                                                 "NULL) value for creator parameter type which " \
                                                                 "is a non-nullable type\n at [Source: UNKNOWN; " \
                                                                 "line: -1, column: -1] (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data.Persone" \
                                                                 "[\"businessFunctions\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "BusinessFunction[\"type\"])"

    @pytestrail.case("27197")
    def test_27197_28_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["jobTitle"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.BusinessFunction] value failed for " \
                                                                 "JSON property jobTitle due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "jobTitle which is a non-nullable type\n at " \
                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement.mdm." \
                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                 "mdm.model.dto.data.TenderTD[\"procuringEntity\"]" \
                                                                 "->com.procurement.mdm.model.dto.data." \
                                                                 "OrganizationReference[\"persones\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                 "dto.data.Persone[\"businessFunctions\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                 "dto.data.BusinessFunction[\"jobTitle\"])"

    @pytestrail.case("27197")
    def test_27197_29_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["period"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.BusinessFunction] value failed for " \
                                                                 "JSON property period due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "period which is a non-nullable type\n " \
                                                                 "at [Source: UNKNOWN; line: -1, column: -1]" \
                                                                 " (through reference chain: com.procurement." \
                                                                 "mdm.model.dto.data.TD[\"tender\"]->com." \
                                                                 "procurement.mdm.model.dto.data.TenderTD" \
                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                 "model.dto.data.OrganizationReference" \
                                                                 "[\"persones\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.Persone" \
                                                                 "[\"businessFunctions\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "BusinessFunction[\"period\"])"

    @pytestrail.case("27197")
    def test_27197_30_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["period"]["startDate"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm." \
                                                                 "model.dto.data.Period] value failed for " \
                                                                 "JSON property startDate due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "startDate which is a non-nullable type\n at " \
                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement.mdm." \
                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                 "mdm.model.dto.data.TenderTD[\"procuringEntity\"]" \
                                                                 "->com.procurement.mdm.model.dto.data." \
                                                                 "OrganizationReference[\"persones\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.Persone[\"businessFunctions\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.BusinessFunction[\"period\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Period" \
                                                                 "[\"startDate\"])"

    @pytestrail.case("27197")
    def test_27197_31_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "500.14.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.storage." \
                                                                 "model.dto.registration.Document] value failed " \
                                                                 "for JSON property id due to missing (therefore " \
                                                                 "NULL) value for creator parameter id which is " \
                                                                 "a non-nullable type\n at [Source: UNKNOWN; " \
                                                                 "line: -1, column: -1] (through reference " \
                                                                 "chain: com.procurement.storage.model.dto." \
                                                                 "registration.DocumentsRq[\"documents\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement." \
                                                                 "storage.model.dto.registration.Document[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_32_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["documentType"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.Document] value failed for JSON " \
                                                                 "property documentType due to missing (therefore" \
                                                                 " NULL) value for creator parameter documentType" \
                                                                 " which is a non-nullable type\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement." \
                                                                 "mdm.model.dto.data.TenderTD[\"procuringEntity\"]" \
                                                                 "->com.procurement.mdm.model.dto.data." \
                                                                 "OrganizationReference[\"persones\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.Persone[\"businessFunctions\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                 "dto.data.BusinessFunction[\"documents\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement." \
                                                                 "mdm.model.dto.data.Document[\"documentType\"])"

    @pytestrail.case("27197")
    def test_27197_33_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["title"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.Document] value failed for JSON property " \
                                                                 "title due to missing (therefore NULL) value for " \
                                                                 "creator parameter title which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement.mdm." \
                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                 "mdm.model.dto.data.TenderTD[\"procuringEntity\"]" \
                                                                 "->com.procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.mdm.model.dto.data.Persone" \
                                                                 "[\"businessFunctions\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data.Business" \
                                                                 "Function[\"documents\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model." \
                                                                 "dto.data.Document[\"title\"])"

    @pytestrail.case("27197")
    def test_27197_34_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.80"
        assert message_from_kafka["errors"][0][
                   "description"] == "Invalid conversion value. Conversions cannot exists without criteria"

    @pytestrail.case("27197")
    def test_27197_35_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.criterion.CriterionRequest] value failed for JSON " \
                                     "property id due to missing (therefore NULL) value for creator parameter " \
                                     "id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: " \
                                     "-1] (through reference chain: com.procurement.access.infrastructure.handler." \
                                     "v1.model.request.OpenCnOnPnRequest[\"tender\"]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender" \
                                     "[\"criteria\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.criterion.CriterionRequest[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_36_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["title"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.criterion.CriterionRequest] value failed for JSON " \
                                     "property title due to missing (therefore NULL) value for creator parameter " \
                                     "title which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: " \
                                     "-1] (through reference chain: com.procurement.access.infrastructure.handler." \
                                     "v1.model.request.OpenCnOnPnRequest[\"tender\"]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender" \
                                     "[\"criteria\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.criterion.CriterionRequest[\"title\"])"

    @pytestrail.case("27197")
    def test_27197_37_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["relatesTo"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.criterion.CriterionRequest] value failed for JSON " \
                                     "property relatesTo due to missing (therefore NULL) value for creator " \
                                     "parameter relatesTo which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest" \
                                     "$Tender[\"criteria\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.criterion.Criterion" \
                                     "Request[\"relatesTo\"])"

    @pytestrail.case("27197")
    def test_27197_38_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["classification"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.criterion.CriterionRequest] value failed for JSON " \
                                     "property classification due to missing (therefore NULL) value for creator " \
                                     "parameter classification which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPn" \
                                     "Request$Tender[\"criteria\"]->java.util.ArrayList[0]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request." \
                                     "criterion.CriterionRequest[\"classification\"])"

    @pytestrail.case("27197")
    def test_27197_39_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["classification"]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.criterion.CriterionClassificationRequest] " \
                                     "value failed for JSON property id due to missing (therefore NULL) value " \
                                     "for creator parameter id which is a non-nullable type\n at [Source: " \
                                     "UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest" \
                                     "[\"tender\"]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.OpenCnOnPnRequest$Tender[\"criteria\"]->java.util.ArrayList[0]" \
                                     "->com.procurement.access.infrastructure.handler.v1.model.request.criterion." \
                                     "CriterionRequest[\"classification\"]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.criterion.Criterion" \
                                     "ClassificationRequest[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_40_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["classification"]["scheme"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.criterion.CriterionClassificationRequest] value " \
                                     "failed for JSON property scheme due to missing (therefore NULL) value for " \
                                     "creator parameter scheme which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPn" \
                                     "Request$Tender[\"criteria\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.criterion.CriterionRequest" \
                                     "[\"classification\"]->com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.criterion.CriterionClassificationRequest[\"scheme\"])"

    @pytestrail.case("27197")
    def test_27197_41_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["requirementGroups"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.criterion.CriterionRequest] value failed for " \
                                     "JSON property requirementGroups due to missing (therefore NULL) value " \
                                     "for creator parameter requirementGroups which is a non-nullable type\n " \
                                     "at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPn" \
                                     "Request[\"tender\"]->com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.OpenCnOnPnRequest$Tender[\"criteria\"]->java.util." \
                                     "ArrayList[0]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.criterion.CriterionRequest[\"requirementGroups\"])"

    @pytestrail.case("27197")
    def test_27197_42_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["requirementGroups"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.criterion.CriterionRequest$RequirementGroup] " \
                                     "value failed for JSON property id due to missing (therefore NULL) value " \
                                     "for creator parameter id which is a non-nullable type\n at [Source: " \
                                     "UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest" \
                                     "[\"tender\"]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.OpenCnOnPnRequest$Tender[\"criteria\"]->java.util.ArrayList[0]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.criterion." \
                                     "CriterionRequest[\"requirementGroups\"]->java.util.ArrayList[0]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.criterion." \
                                     "CriterionRequest$RequirementGroup[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_43_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.criterion.CriterionRequest$RequirementGroup] " \
                                     "value failed for JSON property requirements due to missing (therefore " \
                                     "NULL) value for creator parameter requirements which is a non-nullable " \
                                     "type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference " \
                                     "chain: com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest[\"tender\"]->com.procurement.access.infrastructure.handler." \
                                     "v1.model.request.OpenCnOnPnRequest$Tender[\"criteria\"]->java.util." \
                                     "ArrayList[0]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.criterion.CriterionRequest[\"requirementGroups\"]->java.util." \
                                     "ArrayList[0]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.criterion.CriterionRequest$RequirementGroup[\"requirements\"])"

    @pytestrail.case("27197")
    def test_27197_44_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: (was java.lang." \
                                     "NullPointerException) (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                     "->com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender[\"criteria\"]->java.util.ArrayList[0]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.criterion." \
                                     "CriterionRequest[\"requirementGroups\"]->java.util.ArrayList[0]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.criterion." \
                                     "CriterionRequest$RequirementGroup[\"requirements\"])"

    @pytestrail.case("27197")
    def test_27197_45_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["title"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: (was java.lang." \
                                     "NullPointerException) (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest$Tender[\"criteria\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.criterion.CriterionRequest" \
                                     "[\"requirementGroups\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.criterion.CriterionRequest$" \
                                     "RequirementGroup[\"requirements\"])"

    @pytestrail.case("27197")
    def test_27197_46_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["dataType"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: (was java.lang." \
                                     "NullPointerException) (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest$Tender[\"criteria\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.criterion.CriterionRequest" \
                                     "[\"requirementGroups\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.criterion." \
                                     "CriterionRequest$RequirementGroup[\"requirements\"])"

    @pytestrail.case("27197")
    def test_27197_47_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: (was java.lang." \
                                     "NullPointerException) (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                     "->com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender[\"criteria\"]->java.util.ArrayList[0]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.criterion." \
                                     "CriterionRequest[\"requirementGroups\"]->java.util.ArrayList[0]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "criterion.CriterionRequest$RequirementGroup[\"requirements\"])"

    @pytestrail.case("27197")
    def test_27197_48_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0]["title"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: (was java.lang." \
                                     "NullPointerException) (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                     "->com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest$Tender[\"criteria\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.criterion.CriterionRequest" \
                                     "[\"requirementGroups\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.criterion.CriterionRequest$" \
                                     "RequirementGroup[\"requirements\"])"

    @pytestrail.case("27197")
    def test_27197_49_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0]["type"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: (was java.lang." \
                                     "NullPointerException) (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest$Tender[\"criteria\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.criterion.CriterionRequest" \
                                     "[\"requirementGroups\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.criterion.CriterionRequest$" \
                                     "RequirementGroup[\"requirements\"])"

    @pytestrail.case("27197")
    def test_27197_50_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0][
            "relatedDocument"]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: (was java.lang." \
                                     "NullPointerException) (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest$Tender[\"criteria\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.criterion.CriterionRequest" \
                                     "[\"requirementGroups\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.criterion.CriterionRequest$" \
                                     "RequirementGroup[\"requirements\"])"

    @pytestrail.case("27197")
    def test_27197_51_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0]["period"]["startDate"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: (was java.lang." \
                                     "NullPointerException) (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                     "->com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender[\"criteria\"]->java.util.ArrayList[3]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.criterion." \
                                     "CriterionRequest[\"requirementGroups\"]->java.util.ArrayList[0]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "criterion.CriterionRequest$RequirementGroup[\"requirements\"])"

    @pytestrail.case("27197")
    def test_27197_52_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0]["period"]["endDate"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: (was java.lang." \
                                     "NullPointerException) (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest$Tender[\"criteria\"]->java.util.ArrayList[3]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.criterion.CriterionRequest" \
                                     "[\"requirementGroups\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.criterion." \
                                     "CriterionRequest$RequirementGroup[\"requirements\"])"

    @pytestrail.case("27197")
    def test_27197_53_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["conversions"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.84"
        assert message_from_kafka["errors"][0][
                   "description"] == "Invalid award criteria. For awardCriteria in [costOnly, qualityOnly, " \
                                     "ratedCriteria] && 'awardCriteriaDetails' in [automated] Criteria and " \
                                     "Conversion are required. "

    @pytestrail.case("27197")
    def test_27197_54_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["conversions"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.ConversionRequest] value failed for JSON property " \
                                     "id due to missing (therefore NULL) value for creator parameter id which is " \
                                     "a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through " \
                                     "reference chain: com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.OpenCnOnPnRequest[\"tender\"]->com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender[\"conversions\"]" \
                                     "->java.util.ArrayList[0]->com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.ConversionRequest[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_55_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["conversions"][0]["relatesTo"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.ConversionRequest] value failed for JSON property " \
                                     "relatesTo due to missing (therefore NULL) value for creator parameter " \
                                     "relatesTo which is a non-nullable type\n at [Source: UNKNOWN; line: -1, " \
                                     "column: -1] (through reference chain: com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender" \
                                     "[\"conversions\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.ConversionRequest[\"relatesTo\"])"

    @pytestrail.case("27197")
    def test_27197_56_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["conversions"][0]["relatedItem"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.ConversionRequest] value failed " \
                                     "for JSON property relatedItem due to missing (therefore NULL) value for " \
                                     "creator parameter relatedItem which is a non-nullable type\n at [Source: " \
                                     "UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                     "->com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender[\"conversions\"]->java.util.ArrayList[0]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request." \
                                     "ConversionRequest[\"relatedItem\"])"

    @pytestrail.case("27197")
    def test_27197_57_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["conversions"][0]["rationale"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.ConversionRequest] value failed for JSON property " \
                                     "rationale due to missing (therefore NULL) value for creator parameter " \
                                     "rationale which is a non-nullable type\n at [Source: UNKNOWN; line: -1, " \
                                     "column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                     "->com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender[\"conversions\"]->java.util.ArrayList[0]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "ConversionRequest[\"rationale\"])"

    @pytestrail.case("27197")
    def test_27197_58_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["conversions"][0]["coefficients"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.ConversionRequest] value failed for JSON property " \
                                     "coefficients due to missing (therefore NULL) value for creator parameter " \
                                     "coefficients which is a non-nullable type\n at [Source: UNKNOWN; line: -1, " \
                                     "column: -1] (through reference chain: com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender" \
                                     "[\"conversions\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.ConversionRequest[\"coefficients\"])"

    @pytestrail.case("27197")
    def test_27197_59_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["conversions"][0]["coefficients"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.ConversionRequest$Coefficient] value failed for " \
                                     "JSON property id due to missing (therefore NULL) value for creator parameter " \
                                     "id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] " \
                                     "(through reference chain: com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.OpenCnOnPnRequest[\"tender\"]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender" \
                                     "[\"conversions\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.ConversionRequest[\"coefficients\"]" \
                                     "->java.util.ArrayList[0]->com.procurement.access.infrastructure.handler." \
                                     "v1.model.request.ConversionRequest$Coefficient[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_60_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["conversions"][0]["coefficients"][0]["value"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.ConversionRequest$Coefficient] " \
                                     "value failed for JSON property value due to missing (therefore NULL) " \
                                     "value for creator parameter value which is a non-nullable type\n at " \
                                     "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest[\"tender\"]->com.procurement.access.infrastructure.handler." \
                                     "v1.model.request.OpenCnOnPnRequest$Tender[\"conversions\"]->java.util." \
                                     "ArrayList[0]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.ConversionRequest[\"coefficients\"]->java.util.ArrayList[0]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.Conversion" \
                                     "Request$Coefficient[\"value\"])"

    @pytestrail.case("27197")
    def test_27197_61_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["conversions"][0]["coefficients"][0]["coefficient"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.ConversionRequest$Coefficient] " \
                                     "value failed for JSON property coefficient due to missing (therefore NULL) " \
                                     "value for creator parameter coefficient which is a non-nullable type\n " \
                                     "at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: " \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest[\"tender\"]->com.procurement.access.infrastructure.handler." \
                                     "v1.model.request.OpenCnOnPnRequest$Tender[\"conversions\"]->java.util." \
                                     "ArrayList[0]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.ConversionRequest[\"coefficients\"]->java.util.ArrayList[0]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.Conversion" \
                                     "Request$Coefficient[\"coefficient\"])"

    @pytestrail.case("27197")
    def test_27197_62_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender] value " \
                                     "failed for JSON property lots due to missing (therefore NULL) value " \
                                     "for creator parameter lots which is a non-nullable type\n at [Source: " \
                                     "UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest" \
                                     "[\"tender\"]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.OpenCnOnPnRequest$Tender[\"lots\"])"

    @pytestrail.case("27197")
    def test_27197_63_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot] " \
                                     "value failed for JSON property id due to missing (therefore NULL) " \
                                     "value for creator parameter id which is a non-nullable type\n at " \
                                     "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     "procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest[\"tender\"]->com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender[\"lots\"]->java." \
                                     "util.ArrayList[0]->com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.OpenCnOnPnRequest$Tender$Lot[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_64_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["title"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot] value failed for " \
                                     "JSON property title due to missing (therefore NULL) value for creator " \
                                     "parameter title which is a non-nullable type\n at [Source: UNKNOWN; line: " \
                                     "-1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                     "->com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender[\"lots\"]->java.util.ArrayList[0]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender$Lot[\"title\"])"

    @pytestrail.case("27197")
    def test_27197_65_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["description"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot] value failed for " \
                                     "JSON property description due to missing (therefore NULL) value for creator " \
                                     "parameter description which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest$" \
                                     "Tender[\"lots\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender$" \
                                     "Lot[\"description\"])"

    @pytestrail.case("27197")
    def test_27197_66_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["value"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot] value failed for " \
                                     "JSON property value due to missing (therefore NULL) value for creator " \
                                     "parameter value which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest$Tender[\"lots\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot[\"value\"])"

    @pytestrail.case("27197")
    def test_27197_67_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["value"]["amount"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot$Value] value failed " \
                                     "for JSON property amount due to missing (therefore NULL) value for creator " \
                                     "parameter amount which is a non-nullable type\n at [Source: UNKNOWN; line: " \
                                     "-1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPn" \
                                     "Request$Tender[\"lots\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot" \
                                     "[\"value\"]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.OpenCnOnPnRequest$Tender$Lot$Value[\"amount\"])"

    @pytestrail.case("27197")
    def test_27197_68_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["value"]["currency"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot$Value] value failed for " \
                                     "JSON property currency due to missing (therefore NULL) value for creator " \
                                     "parameter currency which is a non-nullable type\n at [Source: UNKNOWN; line: " \
                                     "-1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPn" \
                                     "Request$Tender[\"lots\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot" \
                                     "[\"value\"]->com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender$Lot$Value[\"currency\"])"

    @pytestrail.case("27197")
    def test_27197_69_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["contractPeriod"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot] value failed for " \
                                     "JSON property contractPeriod due to missing (therefore NULL) value for " \
                                     "creator parameter contractPeriod which is a non-nullable type\n at " \
                                     "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPn" \
                                     "Request[\"tender\"]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.OpenCnOnPnRequest$Tender[\"lots\"]->java.util.ArrayList[0]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest$" \
                                     "Tender$Lot[\"contractPeriod\"])"

    @pytestrail.case("27197")
    def test_27197_70_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["contractPeriod"]["startDate"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot$ContractPeriod] value " \
                                     "failed for JSON property startDate due to missing (therefore NULL) value " \
                                     "for creator parameter startDate which is a non-nullable type\n at [Source: " \
                                     "UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest" \
                                     "[\"tender\"]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.OpenCnOnPnRequest$Tender[\"lots\"]->java.util.ArrayList[0]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest$" \
                                     "Tender$Lot[\"contractPeriod\"]->com.procurement.access.infrastructure.handler." \
                                     "v1.model.request.OpenCnOnPnRequest$Tender$Lot$ContractPeriod[\"startDate\"])"

    @pytestrail.case("27197")
    def test_27197_71_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["contractPeriod"]["endDate"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender$" \
                                     "Lot$ContractPeriod] value failed for JSON property endDate due to missing " \
                                     "(therefore NULL) value for creator parameter endDate which is a non-nullable " \
                                     "type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: " \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPn" \
                                     "Request[\"tender\"]->com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.OpenCnOnPnRequest$Tender[\"lots\"]->java.util.ArrayList[0]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOnPn" \
                                     "Request$Tender$Lot[\"contractPeriod\"]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                     "ContractPeriod[\"endDate\"])"

    @pytestrail.case("27197")
    def test_27197_72_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender$Lot] " \
                                     "value failed for JSON property placeOfPerformance due to missing " \
                                     "(therefore NULL) value for creator parameter placeOfPerformance " \
                                     "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, " \
                                     "column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                     "->com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender[\"lots\"]->java.util.ArrayList[0]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender$Lot[\"placeOfPerformance\"])"

    @pytestrail.case("27197")
    def test_27197_73_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "PlaceOfPerformance] value failed for JSON property address due to " \
                                     "missing (therefore NULL) value for creator parameter address which " \
                                     "is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] " \
                                     "(through reference chain: com.procurement.mdm.model.dto.data.TD" \
                                     "[\"tender\"]->com.procurement.mdm.model.dto.data.TenderTD[\"lots\"]" \
                                     "->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data." \
                                     "LotTD[\"placeOfPerformance\"]->com.procurement.mdm.model.dto." \
                                     "data.PlaceOfPerformance[\"address\"])"

    @pytestrail.case("27197")
    def test_27197_74_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "Address] value failed for JSON property streetAddress due to missing " \
                                     "(therefore NULL) value for creator parameter streetAddress which is a non-" \
                                     "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through " \
                                     "reference chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                     "com.procurement.mdm.model.dto.data.TenderTD[\"lots\"]->java.util." \
                                     "ArrayList[0]->com.procurement.mdm.model.dto.data.LotTD[\"placeOf" \
                                     "Performance\"]->com.procurement.mdm.model.dto.data.PlaceOfPerformance" \
                                     "[\"address\"]->com.procurement.mdm.model.dto.data.Address[\"streetAddress\"])"

    @pytestrail.case("27197")
    def test_27197_75_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "Address] value failed for JSON property addressDetails due to missing " \
                                     "(therefore NULL) value for creator parameter addressDetails which is a " \
                                     "non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through " \
                                     "reference chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]->com." \
                                     "procurement.mdm.model.dto.data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                     "[0]->com.procurement.mdm.model.dto.data.LotTD[\"placeOfPerformance\"]->" \
                                     "com.procurement.mdm.model.dto.data.PlaceOfPerformance[\"address\"]->com." \
                                     "procurement.mdm.model.dto.data.Address[\"addressDetails\"])"

    @pytestrail.case("27197")
    def test_27197_76_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "AddressDetails] value failed for JSON property country due to missing " \
                                     "(therefore NULL) value for creator parameter country which is a " \
                                     "non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] " \
                                     "(through reference chain: com.procurement.mdm.model.dto.data.TD" \
                                     "[\"tender\"]->com.procurement.mdm.model.dto.data.TenderTD[\"lots\"]" \
                                     "->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.LotTD" \
                                     "[\"placeOfPerformance\"]->com.procurement.mdm.model.dto.data." \
                                     "PlaceOfPerformance[\"address\"]->com.procurement.mdm.model.dto." \
                                     "data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto." \
                                     "data.AddressDetails[\"country\"])"

    @pytestrail.case("27197")
    def test_27197_77_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "CountryDetails] value failed for JSON property id due to missing " \
                                     "(therefore NULL) value for creator parameter id which is a " \
                                     "non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] " \
                                     "(through reference chain: com.procurement.mdm.model.dto.data.TD" \
                                     "[\"tender\"]->com.procurement.mdm.model.dto.data.TenderTD[\"lots\"]" \
                                     "->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.LotTD" \
                                     "[\"placeOfPerformance\"]->com.procurement.mdm.model.dto.data." \
                                     "PlaceOfPerformance[\"address\"]->com.procurement.mdm.model.dto." \
                                     "data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto." \
                                     "data.AddressDetails[\"country\"]->com.procurement.mdm.model.dto." \
                                     "data.CountryDetails[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_78_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "AddressDetails] value failed for JSON property region due to missing " \
                                     "(therefore NULL) value for creator parameter region which is a " \
                                     "non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through " \
                                     "reference chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]->com." \
                                     "procurement.mdm.model.dto.data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                     "[0]->com.procurement.mdm.model.dto.data.LotTD[\"placeOfPerformance\"]->" \
                                     "com.procurement.mdm.model.dto.data.PlaceOfPerformance[\"address\"]->com." \
                                     "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->com.procurement." \
                                     "mdm.model.dto.data.AddressDetails[\"region\"])"

    @pytestrail.case("27197")
    def test_27197_79_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "RegionDetails] value failed for JSON property id due to missing (therefore " \
                                     "NULL) value for creator parameter id which is a non-nullable type\n at " \
                                     "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     "procurement.mdm.model.dto.data.TD[\"tender\"]->com.procurement.mdm.model." \
                                     "dto.data.TenderTD[\"lots\"]->java.util.ArrayList[0]->com.procurement.mdm." \
                                     "model.dto.data.LotTD[\"placeOfPerformance\"]->com.procurement.mdm.model." \
                                     "dto.data.PlaceOfPerformance[\"address\"]->com.procurement.mdm.model.dto." \
                                     "data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto.data." \
                                     "AddressDetails[\"region\"]->com.procurement.mdm.model.dto.data." \
                                     "RegionDetails[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_80_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "AddressDetails] value failed for JSON property locality due to missing " \
                                     "(therefore NULL) value for creator parameter locality which is a " \
                                     "non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] " \
                                     "(through reference chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]" \
                                     "->com.procurement.mdm.model.dto.data.TenderTD[\"lots\"]->java.util." \
                                     "ArrayList[0]->com.procurement.mdm.model.dto.data.LotTD" \
                                     "[\"placeOfPerformance\"]->com.procurement.mdm.model.dto.data.PlaceOf" \
                                     "Performance[\"address\"]->com.procurement.mdm.model.dto.data.Address" \
                                     "[\"addressDetails\"]->com.procurement.mdm.model.dto.data." \
                                     "AddressDetails[\"locality\"])"

    @pytestrail.case("27197")
    def test_27197_81_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "LocalityDetails] value failed for JSON property id due to missing " \
                                     "(therefore NULL) value for creator parameter id which is a non-nullable " \
                                     "type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: " \
                                     "com.procurement.mdm.model.dto.data.TD[\"tender\"]->com.procurement.mdm.model." \
                                     "dto.data.TenderTD[\"lots\"]->java.util.ArrayList[0]->com.procurement.mdm." \
                                     "model.dto.data.LotTD[\"placeOfPerformance\"]->com.procurement.mdm.model." \
                                     "dto.data.PlaceOfPerformance[\"address\"]->com.procurement.mdm.model.dto." \
                                     "data.Address[\"addressDetails\"]->com.procurement.mdm.model.dto.data." \
                                     "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto.data." \
                                     "LocalityDetails[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_82_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "LocalityDetails] value failed for JSON property scheme due to missing " \
                                     "(therefore NULL) value for creator parameter scheme which is a non-nullable " \
                                     "type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference " \
                                     "chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]->com.procurement." \
                                     "mdm.model.dto.data.TenderTD[\"lots\"]->java.util.ArrayList[0]->com." \
                                     "procurement.mdm.model.dto.data.LotTD[\"placeOfPerformance\"]->com." \
                                     "procurement.mdm.model.dto.data.PlaceOfPerformance[\"address\"]->com." \
                                     "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->com." \
                                     "procurement.mdm.model.dto.data.AddressDetails[\"locality\"]->com." \
                                     "procurement.mdm.model.dto.data.LocalityDetails[\"scheme\"])"

    @pytestrail.case("27197")
    def test_27197_83_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["description"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "LocalityDetails] value failed for JSON property description due to " \
                                     "missing (therefore NULL) value for creator parameter description which " \
                                     "is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] " \
                                     "(through reference chain: com.procurement.mdm.model.dto.data.TD" \
                                     "[\"tender\"]->com.procurement.mdm.model.dto.data.TenderTD[\"lots\"]" \
                                     "->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.LotTD" \
                                     "[\"placeOfPerformance\"]->com.procurement.mdm.model.dto.data." \
                                     "PlaceOfPerformance[\"address\"]->com.procurement.mdm.model.dto.data." \
                                     "Address[\"addressDetails\"]->com.procurement.mdm.model.dto.data.Address" \
                                     "Details[\"locality\"]->com.procurement.mdm.model.dto.data.Locality" \
                                     "Details[\"description\"])"

    @pytestrail.case("27197")
    def test_27197_84_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["items"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender] value failed for JSON " \
                                     "property items due to missing (therefore NULL) value for creator parameter " \
                                     "items which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: " \
                                     "-1] (through reference chain: com.procurement.access.infrastructure.handler." \
                                     "v1.model.request.OpenCnOnPnRequest[\"tender\"]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender[\"items\"])"

    @pytestrail.case("27197")
    def test_27197_85_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["items"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.CheckItemsRequest$Item] value failed for JSON " \
                                     "property id due to missing (therefore NULL) value for creator parameter " \
                                     "id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: " \
                                     "-1] (through reference chain: com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.CheckItemsRequest[\"items\"]->java.util." \
                                     "ArrayList[0]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.CheckItemsRequest$Item[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_86_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["items"][0]["classification"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.CheckItemsRequest$Item] value failed for JSON " \
                                     "property classification due to missing (therefore NULL) value for creator " \
                                     "parameter classification which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.CheckItemsRequest[\"items\"]->java." \
                                     "util.ArrayList[0]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.CheckItemsRequest$Item[\"classification\"])"

    @pytestrail.case("27197")
    def test_27197_87_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["items"][0]["classification"]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.CheckItemsRequest$Item$Classification] value " \
                                     "failed for JSON property id due to missing (therefore NULL) value for " \
                                     "creator parameter id which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.CheckItemsRequest[\"items\"]->java." \
                                     "util.ArrayList[0]->com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.CheckItemsRequest$Item[\"classification\"]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.CheckItemsRequest$Item$" \
                                     "Classification[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_88_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "ClassificationTD] value failed for JSON property id due to missing " \
                                     "(therefore NULL) value for creator parameter id which is a non-nullable " \
                                     "type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference " \
                                     "chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]->com." \
                                     "procurement.mdm.model.dto.data.TenderTD[\"items\"]->java.util.ArrayList[0]" \
                                     "->com.procurement.mdm.model.dto.data.ItemTD[\"additional" \
                                     "Classifications\"]->java.util.ArrayList[0]->com.procurement." \
                                     "mdm.model.dto.data.ClassificationTD[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_89_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["items"][0]["quantity"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto." \
                                     "data.ItemTD] value failed for JSON property quantity due to missing " \
                                     "(therefore NULL) value for creator parameter quantity which is a non-" \
                                     "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through " \
                                     "reference chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                     "com.procurement.mdm.model.dto.data.TenderTD[\"items\"]->java.util." \
                                     "ArrayList[0]->com.procurement.mdm.model.dto.data.ItemTD[\"quantity\"])"

    @pytestrail.case("27197")
    def test_27197_90_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["items"][0]["unit"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "ItemTD] value failed for JSON property unit due to missing (therefore NULL) " \
                                     "value for creator parameter unit which is a non-nullable type\n at " \
                                     "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     "procurement.mdm.model.dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                     "model.dto.data.TenderTD[\"items\"]->java.util.ArrayList[0]->com." \
                                     "procurement.mdm.model.dto.data.ItemTD[\"unit\"])"

    @pytestrail.case("27197")
    def test_27197_91_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["items"][0]["unit"]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "ItemUnitTD] value failed for JSON property id due to missing (therefore " \
                                     "NULL) value for creator parameter id which is a non-nullable type\n at " \
                                     "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     "procurement.mdm.model.dto.data.TD[\"tender\"]->com.procurement.mdm.model." \
                                     "dto.data.TenderTD[\"items\"]->java.util.ArrayList[0]->com.procurement." \
                                     "mdm.model.dto.data.ItemTD[\"unit\"]->com.procurement.mdm.model.dto." \
                                     "data.ItemUnitTD[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_92_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["items"][0]["description"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender$Item] value failed " \
                                     "for JSON property description due to missing (therefore NULL) value for " \
                                     "creator parameter description which is a non-nullable type\n at [Source: " \
                                     "UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                     "->com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest$Tender[\"items\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender$Item" \
                                     "[\"description\"])"

    @pytestrail.case("27197")
    def test_27197_93_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["items"][0]["relatedLot"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.CheckItemsRequest$Item] value failed for JSON " \
                                     "property relatedLot due to missing (therefore NULL) value for creator " \
                                     "parameter relatedLot which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.CheckItemsRequest[\"items\"]->" \
                                     "java.util.ArrayList[0]->com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.CheckItemsRequest$Item[\"relatedLot\"])"

    @pytestrail.case("27197")
    def test_27197_94_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["documents"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.OpenCnOnPnRequest$Tender] value failed for JSON " \
                                     "property documents due to missing (therefore NULL) value for creator " \
                                     "parameter documents which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "OpenCnOnPnRequest$Tender[\"documents\"])"

    @pytestrail.case("27197")
    def test_27197_95_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["documents"][0]["documentType"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.document.DocumentRequest] value failed for JSON " \
                                     "property documentType due to missing (therefore NULL) value for creator " \
                                     "parameter documentType which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest$Tender[\"documents\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.document.Document" \
                                     "Request[\"documentType\"])"

    @pytestrail.case("27197")
    def test_27197_96_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["documents"][0]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "500.14.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.storage.model.dto." \
                                     "registration.Document] value failed for JSON property id due to missing " \
                                     "(therefore NULL) value for creator parameter id which is a non-nullable " \
                                     "type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference " \
                                     "chain: com.procurement.storage.model.dto.registration.DocumentsRq" \
                                     "[\"documents\"]->java.util.ArrayList[0]->com.procurement.storage.model." \
                                     "dto.registration.Document[\"id\"])"

    @pytestrail.case("27197")
    def test_27197_97_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        del payload["tender"]["documents"][0]["title"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.document.DocumentRequest] " \
                                     "value failed for JSON property title due to missing (therefore NULL) " \
                                     "value for creator parameter title which is a non-nullable type\n at " \
                                     "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.OpenCnOn" \
                                     "PnRequest[\"tender\"]->com.procurement.access.infrastructure.handler." \
                                     "v1.model.request.OpenCnOnPnRequest$Tender[\"documents\"]->java.util." \
                                     "ArrayList[0]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.document.DocumentRequest[\"title\"])"

    @pytestrail.case("27198")
    def test_27198_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        previous_ms_release = cn.get_previous_ms_release(pn)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["planning"]["rationale"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka
        assert ms_release["releases"][0]["planning"]["rationale"] == previous_ms_release["releases"][0]["planning"][
            "rationale"]

    @pytestrail.case("27198")
    def test_27198_2_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        previous_ms_release = cn.get_previous_ms_release(pn)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["planning"]["budget"]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka
        assert ms_release["releases"][0]["planning"]["budget"]["description"] == \
               previous_ms_release["releases"][0]["planning"]["budget"]["description"]

    @pytestrail.case("27198")
    def test_27198_3_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["title"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka
        assert ev_release["releases"][0]["tender"]["title"] == "Evaluation"

    @pytestrail.case("27198")
    def test_27198_4_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka
        assert ev_release["releases"][0]["tender"]["description"] == "Evaluation stage of contracting process"

    @pytestrail.case("27198")
    def test_27198_5_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procurementMethodRationale"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka
        assert ev_release["releases"][0]["tender"]["procurementMethodRationale"] == str(
            payload["tender"]["procurementMethodRationale"]).lower()

    @pytestrail.case("27198")
    def test_27198_6_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procurementMethodAdditionalInfo"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ms_release["releases"][0]["tender"]["procurementMethodAdditionalInfo"] == \
               str(payload["tender"]["procurementMethodAdditionalInfo"]).lower()

    @pytestrail.case("27198")
    def test_27198_7_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["awardCriteria"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "InvalidDefinitionException: Cannot construct " \
                                                                 "instance of `com.procurement.access.domain." \
                                                                 "model.enums.AwardCriteria`, problem: Unknown " \
                                                                 "value for enumType com.procurement.access." \
                                                                 "domain.model.enums.AwardCriteria: false, " \
                                                                 "Allowed values are priceOnly, costOnly, " \
                                                                 "qualityOnly, ratedCriteria\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com." \
                                                                 "procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"awardCriteria\"])"

    @pytestrail.case("27198")
    def test_27198_8_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["awardCriteriaDetails"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "InvalidDefinitionException: Cannot construct " \
                                                                 "instance of `com.procurement.access.domain." \
                                                                 "model.enums.AwardCriteriaDetails`, problem: " \
                                                                 "Unknown value for enumType com.procurement." \
                                                                 "access.domain.model.enums.AwardCriteriaDetails:" \
                                                                 " false, Allowed values are manual, " \
                                                                 "automated\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]" \
                                                                 "->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest$" \
                                                                 "Tender[\"awardCriteriaDetails\"])"

    @pytestrail.case("27198")
    def test_27198_9_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["tenderPeriod"]["endDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.04.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text 'false' could not be parsed at " \
                                                                 "index 0 (through reference chain: com." \
                                                                 "procurement.submission.infrastructure.handler." \
                                                                 "v1.model.request.PeriodRq[\"tenderPeriod\"]->" \
                                                                 "com.procurement.submission.model.dto.ocds." \
                                                                 "Period[\"endDate\"])"

    @pytestrail.case("27198")
    def test_27198_10_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["enquiryPeriod"]["endDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.05.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: Text 'false' could not " \
                                                                 "be parsed at index 0 (through reference chain: " \
                                                                 "com.procurement.clarification.infrastructure." \
                                                                 "handler.v1.model.request.PeriodRq" \
                                                                 "[\"enquiryPeriod\"]->com.procurement." \
                                                                 "clarification.model.dto.ocds.Period[\"endDate\"])"

    @pytestrail.case("27198")
    def test_27198_11_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procurementMethodModalities"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "MismatchedInputException: Cannot " \
                                                                 "deserialize instance of `java.util.HashSet` " \
                                                                 "out of VALUE_FALSE token\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model." \
                                                                 "request.OpenCnOnPnRequest[\"tender\"]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"procurementMethodModalities\"])"

    @pytestrail.case("27198")
    def test_27198_12_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["electronicAuctions"]["details"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert checking_uuid == True

    @pytestrail.case("27198")
    def test_27198_13_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["relatedLot"] = False
        value_of_key = str(payload["tender"]["electronicAuctions"]["details"][0]["relatedLot"]).lower()
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.15.10.01"
        assert message_from_kafka["errors"][0]["description"] == f"Electronic auctions contain an invalid related " \
                                                                 f"lot: '{value_of_key}'."

    @pytestrail.case("27198")
    def test_27198_14_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
            "eligibleMinimumDifference"]["amount"] = False
        value_of_key = str(
            payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
                "eligibleMinimumDifference"]["amount"]).lower()
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind." \
                                                                 f"JsonMappingException: Incorrect value of the " \
                                                                 f"amount: '\"{value_of_key}\"'. The value must " \
                                                                 f"be a real number. (through reference chain: " \
                                                                 f"com.procurement.access.infrastructure.handler." \
                                                                 f"v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                                                 f"->com.procurement.access.infrastructure.handler." \
                                                                 f"v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 f"[\"electronicAuctions\"]->com.procurement." \
                                                                 f"access.infrastructure.handler.v1.model.request." \
                                                                 f"OpenCnOnPnRequest$Tender$ElectronicAuctions" \
                                                                 f"[\"details\"]->java.util.ArrayList[0]->com." \
                                                                 f"procurement.access.infrastructure.handler." \
                                                                 f"v1.model.request.OpenCnOnPnRequest$Tender$" \
                                                                 f"ElectronicAuctions$Detail[\"electronicAuction" \
                                                                 f"Modalities\"]->java.util.ArrayList[0]->com." \
                                                                 f"procurement.access.infrastructure.handler.v1." \
                                                                 f"model.request.OpenCnOnPnRequest$Tender$" \
                                                                 f"ElectronicAuctions$Detail$Modalities" \
                                                                 f"[\"eligibleMinimumDifference\"]->com." \
                                                                 f"procurement.access.infrastructure.handler." \
                                                                 f"v1.model.request.OpenCnOnPnRequest$Tender$" \
                                                                 f"ElectronicAuctions$Detail$Modalities$" \
                                                                 f"EligibleMinimumDifference[\"amount\"])"

    @pytestrail.case("27198")
    def test_27198_15_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
            "eligibleMinimumDifference"]["currency"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.15.10.01"
        assert message_from_kafka["errors"][0]["description"] == "Electronic auction with id: '1' contain invalid " \
                                                                 "currency in 'EligibleMinimumDifference' attribute."

    @pytestrail.case("27198")
    def test_27198_16_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data." \
                                                                 "OrganizationReference[\"id\"])"

    @pytestrail.case("27198")
    def test_27198_17_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["title"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto.data." \
                                                                 "TenderTD[\"procuringEntity\"]->com.procurement." \
                                                                 "mdm.model.dto.data.OrganizationReference" \
                                                                 "[\"persones\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"title\"])"

    @pytestrail.case("27198")
    def test_27198_18_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["name"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"name\"])"

    @pytestrail.case("27198")
    def test_27198_19_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["scheme"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"identifier\"]->com.procurement.mdm." \
                                                                 "model.dto.data.Identifier[\"scheme\"])"

    @pytestrail.case("27198")
    def test_27198_20_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"procuringEntity\"]->" \
                                                                 "com.procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data.Persone" \
                                                                 "[\"identifier\"]->com.procurement.mdm.model." \
                                                                 "dto.data.Identifier[\"id\"])"

    @pytestrail.case("27198")
    def test_27198_21_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["uri"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"identifier\"]->com.procurement.mdm." \
                                                                 "model.dto.data.Identifier[\"uri\"])"

    @pytestrail.case("27198")
    def test_27198_22_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"businessFunctions\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.BusinessFunction[\"id\"])"

    @pytestrail.case("27198")
    def test_27198_23_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["type"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"businessFunctions\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.BusinessFunction[\"type\"])"

    @pytestrail.case("27198")
    def test_27198_24_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["jobTitle"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"procuringEntity\"]" \
                                                                 "->com.procurement.mdm.model.dto.data." \
                                                                 "OrganizationReference[\"persones\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                 "dto.data.Persone[\"businessFunctions\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement.mdm." \
                                                                 "model.dto.data.BusinessFunction[\"jobTitle\"])"

    @pytestrail.case("27198")
    def test_27198_25_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["period"][
            "startDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: Text 'false' could not " \
                                                                 "be parsed at index 0 (through reference chain: " \
                                                                 "com.procurement.mdm.model.dto.data.TD[\"tender\"]" \
                                                                 "->com.procurement.mdm.model.dto.data.TenderTD" \
                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                 "model.dto.data.OrganizationReference" \
                                                                 "[\"persones\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.Persone" \
                                                                 "[\"businessFunctions\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data." \
                                                                 "BusinessFunction[\"period\"]->com.procurement." \
                                                                 "mdm.model.dto.data.Period[\"startDate\"])"

    @pytestrail.case("27198")
    def test_27198_26_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0][
            "id"] = False
        value_of_key = str(
            payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0][
                "id"]).lower()
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.14.00.14"
        assert message_from_kafka["errors"][0]["description"] == f"Files not found: [{value_of_key}]"

    @pytestrail.case("27198")
    def test_27198_27_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0][
            "documentType"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"procuringEntity\"]->" \
                                                                 "com.procurement.mdm.model.dto.data." \
                                                                 "OrganizationReference[\"persones\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                 "dto.data.Persone[\"businessFunctions\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement.mdm." \
                                                                 "model.dto.data.BusinessFunction[\"documents\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.mdm." \
                                                                 "model.dto.data.Document[\"documentType\"])"

    @pytestrail.case("27198")
    def test_27198_28_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0][
            "title"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"businessFunctions\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.BusinessFunction[\"documents\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.Document[\"title\"])"

    @pytestrail.case("27198")
    def test_27198_29_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0][
            "description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"procuringEntity\"]" \
                                                                 "->com.procurement.mdm.model.dto.data." \
                                                                 "OrganizationReference[\"persones\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                 "dto.data.Persone[\"businessFunctions\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement.mdm." \
                                                                 "model.dto.data.BusinessFunction[\"documents\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.mdm." \
                                                                 "model.dto.data.Document[\"description\"])"

    @pytestrail.case("27198")
    def test_27198_30_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["criteria"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert checking_uuid == True

    @pytestrail.case("27198")
    def test_27198_31_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["title"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ev_release["releases"][0]["tender"]["criteria"][0]["title"] == str(
            payload["tender"]["criteria"][0]["title"]).lower()

    @pytestrail.case("27198")
    def test_27198_32_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["relatesTo"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "InvalidDefinitionException: Cannot construct " \
                                                                 "instance of `com.procurement.access.domain.model." \
                                                                 "enums.CriteriaRelatesTo`, problem: Unknown value " \
                                                                 "for enumType com.procurement.access.domain.model." \
                                                                 "enums.CriteriaRelatesTo: false, Allowed values " \
                                                                 "are award, item, lot, qualification, tender, " \
                                                                 "tenderer\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"criteria\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.criterion.CriterionRequest" \
                                                                 "[\"relatesTo\"])"

    @pytestrail.case("27198")
    def test_27198_33_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["classification"]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.79"
        assert message_from_kafka["errors"][0]["description"] == "Invalid criteria value. FReq-1.1.1.31"

    @pytestrail.case("27198")
    def test_27198_34_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["classification"]["scheme"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.79"
        assert message_from_kafka["errors"][0]["description"] == "Invalid criteria value. FReq-1.1.1.34 "

    @pytestrail.case("27198")
    def test_27198_35_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ev_release["releases"][0]["tender"]["criteria"][0]["description"] == str(
            payload["tender"]["criteria"][0]["description"]).lower()

    @pytestrail.case("27198")
    def test_27198_36_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert checking_uuid == True

    @pytestrail.case("27198")
    def test_27198_37_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(
            ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert checking_uuid == True

    @pytestrail.case("27198")
    def test_27198_38_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["title"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                   "title"] == str(
            payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["title"]).lower()

    @pytestrail.case("27198")
    def test_27198_39_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["dataType"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Unknown value for enumType com." \
                                                                 "procurement.access.domain.model.enums." \
                                                                 "RequirementDataType: false, Allowed values are " \
                                                                 "boolean, string, number, integer (through " \
                                                                 "reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"criteria\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest[\"requirementGroups\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest$RequirementGroup" \
                                                                 "[\"requirements\"])"

    @pytestrail.case("27198")
    def test_27198_40_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["dataType"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: Unknown value for " \
                                                                 "enumType com.procurement.access.domain.model." \
                                                                 "enums.RequirementDataType: false, Allowed " \
                                                                 "values are boolean, string, number, integer " \
                                                                 "(through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"criteria\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest[\"requirementGroups\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest$RequirementGroup" \
                                                                 "[\"requirements\"])"

    @pytestrail.case("27198")
    def test_27198_41_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][
            0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                   "eligibleEvidences"][0]["id"] == str(
            payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                "eligibleEvidences"][0]["id"]).lower()

    @pytestrail.case("27198")
    def test_27198_42_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][
            0]["title"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                   "eligibleEvidences"][0]["title"] == str(
            payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                "eligibleEvidences"][0]["title"]).lower()

    @pytestrail.case("27198")
    def test_27198_43_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][
            0]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ev_release["releases"][0]["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                   "eligibleEvidences"][0]["description"] == str(
            payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                "eligibleEvidences"][0]["description"]).lower()

    @pytestrail.case("27198")
    def test_27198_44_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][
            0]["type"] = False
        value_of_key = str(payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0][
                               "eligibleEvidences"][0]["type"]).lower()
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0][
                   "description"] == f"com.fasterxml.jackson.databind.JsonMappingException: Error of parsing " \
                                     f"element of 'EligibleEvidenceType' enum. Invalid value '{value_of_key}'. " \
                                     f"(through reference chain: com.procurement.access.infrastructure.handler.v1." \
                                     f"model.request.OpenCnOnPnRequest[\"tender\"]->com.procurement.access." \
                                     f"infrastructure.handler.v1.model.request.OpenCnOnPnRequest$Tender" \
                                     f"[\"criteria\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     f"infrastructure.handler.v1.model.request.criterion.CriterionRequest" \
                                     f"[\"requirementGroups\"]->java.util.ArrayList[0]->com.procurement." \
                                     f"access.infrastructure.handler.v1.model.request.criterion.Criterion" \
                                     f"Request$RequirementGroup[\"requirements\"])"

    @pytestrail.case("27198")
    def test_27198_45_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][
            0]["relatedDocument"]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.79"
        assert message_from_kafka["errors"][0]["description"] == "Invalid criteria value. FReq-1.1.1.38"

    @pytestrail.case("27198")
    def test_27198_46_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0]["maxValue"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: Invalid requirement " \
                                                                 "value. Requirement.dataType mismatch with " \
                                                                 "datatype in expectedValue || minValue || " \
                                                                 "maxValue. (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"criteria\"]->java.util.ArrayList[3]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.criterion.CriterionRequest" \
                                                                 "[\"requirementGroups\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.criterion.Criterion" \
                                                                 "Request$RequirementGroup[\"requirements\"])"

    @pytestrail.case("27198")
    def test_27198_47_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0]["maxValue"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: Invalid requirement " \
                                                                 "value. Requirement.dataType mismatch with " \
                                                                 "datatype in expectedValue || minValue || " \
                                                                 "maxValue. (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]" \
                                                                 "->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest$" \
                                                                 "Tender[\"criteria\"]->java.util.ArrayList[3]" \
                                                                 "->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.criterion.Criterion" \
                                                                 "Request[\"requirementGroups\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest$RequirementGroup" \
                                                                 "[\"requirements\"])"

    @pytestrail.case("27198")
    def test_27198_48_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0]["period"][
            "startDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text 'false' could not be parsed at " \
                                                                 "index 0 (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"criteria\"]->java.util.ArrayList[3]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.criterion.CriterionRequest" \
                                                                 "[\"requirementGroups\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.criterion.CriterionRequest$" \
                                                                 "RequirementGroup[\"requirements\"])"

    @pytestrail.case("27198")
    def test_27198_49_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0]["period"][
            "endDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text 'false' could not be parsed at " \
                                                                 "index 0 (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"criteria\"]->java.util.ArrayList[3]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.criterion.CriterionRequest" \
                                                                 "[\"requirementGroups\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.criterion.CriterionRequest$" \
                                                                 "RequirementGroup[\"requirements\"])"

    @pytestrail.case("27198")
    def test_27198_50_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["conversions"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert checking_uuid == True

    @pytestrail.case("27198")
    def test_27198_51_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["relatesTo"] = False
        value_of_key = str(payload["tender"]["conversions"][0]["relatesTo"]).lower()
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.exc." \
                                                                 f"InvalidDefinitionException: Cannot construct " \
                                                                 f"instance of `com.procurement.access.domain." \
                                                                 f"model.enums.ConversionsRelatesTo`, problem: " \
                                                                 f"Unknown value for enumType com.procurement." \
                                                                 f"access.domain.model.enums.ConversionsRelatesTo: " \
                                                                 f"{value_of_key}, Allowed values are requirement, " \
                                                                 f"observation, option\n at [Source: UNKNOWN; line: " \
                                                                 f"-1, column: -1] (through reference chain: com." \
                                                                 f"procurement.access.infrastructure.handler." \
                                                                 f"v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                                                 f"->com.procurement.access.infrastructure.handler." \
                                                                 f"v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 f"[\"conversions\"]->java.util.ArrayList[0]->" \
                                                                 f"com.procurement.access.infrastructure.handler." \
                                                                 f"v1.model.request.ConversionRequest[\"relatesTo\"])"

    @pytestrail.case("27198")
    def test_27198_52_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["relatedItem"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.80"
        assert message_from_kafka["errors"][0]["description"] == f"Invalid conversion value. Conversion relates " \
                                                                 f"to requirement that does not exists"

    @pytestrail.case("27198")
    def test_27198_53_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["rationale"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert \
            ev_release["releases"][0]["tender"]["conversions"][0]["rationale"] == \
            str(payload["tender"]["conversions"][0]["rationale"]).lower()

    @pytestrail.case("27198")
    def test_27198_54_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert \
            ev_release["releases"][0]["tender"]["conversions"][0]["description"] == \
            str(payload["tender"]["conversions"][0]["description"]).lower()

    @pytestrail.case("27198")
    def test_27198_55_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        checking_uuid = is_it_uuid(ev_release["releases"][0]["tender"]["conversions"][0]["id"], 4)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert checking_uuid == True

    @pytestrail.case("27198")
    def test_27198_56_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["coefficients"][0]["coefficient"] = False
        value_of_key = str(payload["tender"]["conversions"][0]["coefficients"][0]["coefficient"]).lower()
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind." \
                                                                 f"JsonMappingException: Incorrect coefficient: " \
                                                                 f"'{value_of_key}'. Invalid type. Number or " \
                                                                 f"Integer required (through reference chain: " \
                                                                 f"com.procurement.access.infrastructure.handler." \
                                                                 f"v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                                                 f"->com.procurement.access.infrastructure." \
                                                                 f"handler.v1.model.request.OpenCnOnPnRequest$" \
                                                                 f"Tender[\"conversions\"]->java.util.ArrayList" \
                                                                 f"[0]->com.procurement.access.infrastructure." \
                                                                 f"handler.v1.model.request.ConversionRequest" \
                                                                 f"[\"coefficients\"]->java.util.ArrayList[0]->" \
                                                                 f"com.procurement.access.infrastructure.handler." \
                                                                 f"v1.model.request.ConversionRequest$Coefficient" \
                                                                 f"[\"coefficient\"])"

    @pytestrail.case("27198")
    def test_27198_57_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"id\"])"

    @pytestrail.case("27198")
    def test_27198_58_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["internalId"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"internalId\"])"

    @pytestrail.case("27198")
    def test_27198_59_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["title"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"title\"])"

    @pytestrail.case("27198")
    def test_27198_60_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"description\"])"

    @pytestrail.case("27198")
    def test_27198_61_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["value"]["amount"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "MismatchedInputException: Cannot deserialize " \
                                                                 "instance of `java.math.BigDecimal` out of " \
                                                                 "VALUE_FALSE token\n at [Source: UNKNOWN; " \
                                                                 "line: -1, column: -1] (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model." \
                                                                 "dto.data.LotTD[\"value\"]->com.procurement." \
                                                                 "mdm.model.dto.data.Value[\"amount\"])"

    @pytestrail.case("27198")
    def test_27198_62_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["value"]["currency"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"value\"]->com.procurement.mdm." \
                                                                 "model.dto.data.Value[\"currency\"])"

    @pytestrail.case("27198")
    def test_27198_63_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"contractPeriod\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Contract" \
                                                                 "Period[\"startDate\"])"

    @pytestrail.case("27198")
    def test_27198_64_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"contractPeriod\"]->com.procurement.mdm.model." \
                                                                 "dto.data.ContractPeriod[\"endDate\"])"

    @pytestrail.case("27198")
    def test_27198_65_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"placeOfPerformance\"]->com." \
                                                                 "procurement.mdm.model.dto.data.PlaceOf" \
                                                                 "Performance[\"address\"]->com.procurement." \
                                                                 "mdm.model.dto.data.Address[\"streetAddress\"])"

    @pytestrail.case("27198")
    def test_27198_66_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["postalCode"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: (was com.procurement.mdm.exception." \
                                                                 "InErrorException) (through reference chain: " \
                                                                 "com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"placeOfPerformance\"]->com.procurement.mdm." \
                                                                 "model.dto.data.PlaceOfPerformance[\"address\"]" \
                                                                 "->com.procurement.mdm.model.dto.data." \
                                                                 "Address[\"postalCode\"])"

    @pytestrail.case("27198")
    def test_27198_67_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"placeOfPerformance\"]->com." \
                                                                 "procurement.mdm.model.dto.data.PlaceOf" \
                                                                 "Performance[\"address\"]->com.procurement.mdm." \
                                                                 "model.dto.data.Address[\"addressDetails\"]->" \
                                                                 "com.procurement.mdm.model.dto.data.Address" \
                                                                 "Details[\"country\"]->com.procurement.mdm." \
                                                                 "model.dto.data.CountryDetails[\"id\"])"

    @pytestrail.case("27198")
    def test_27198_68_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"placeOfPerformance\"]->com." \
                                                                 "procurement.mdm.model.dto.data.PlaceOf" \
                                                                 "Performance[\"address\"]->com.procurement.mdm." \
                                                                 "model.dto.data.Address[\"addressDetails\"]->" \
                                                                 "com.procurement.mdm.model.dto.data.Address" \
                                                                 "Details[\"region\"]->com.procurement.mdm." \
                                                                 "model.dto.data.RegionDetails[\"id\"])"

    @pytestrail.case("27198")
    def test_27198_69_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"placeOfPerformance\"]->com.procurement.mdm." \
                                                                 "model.dto.data.PlaceOfPerformance[\"address\"]->" \
                                                                 "com.procurement.mdm.model.dto.data.Address" \
                                                                 "[\"addressDetails\"]->com.procurement.mdm." \
                                                                 "model.dto.data.AddressDetails[\"locality\"]->" \
                                                                 "com.procurement.mdm.model.dto.data." \
                                                                 "LocalityDetails[\"id\"])"

    @pytestrail.case("27198")
    def test_27198_70_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"lots\"]->java.util.Array" \
                                                                 "List[0]->com.procurement.mdm.model.dto.data." \
                                                                 "LotTD[\"placeOfPerformance\"]->com." \
                                                                 "procurement.mdm.model.dto.data.PlaceOf" \
                                                                 "Performance[\"address\"]->com.procurement." \
                                                                 "mdm.model.dto.data.Address[\"addressDetails\"]" \
                                                                 "->com.procurement.mdm.model.dto.data.Address" \
                                                                 "Details[\"locality\"]->com.procurement.mdm." \
                                                                 "model.dto.data.LocalityDetails[\"scheme\"])"

    @pytestrail.case("27198")
    def test_27198_71_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
            "description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "LotTD[\"placeOfPerformance\"]->com.procurement." \
                                                                 "mdm.model.dto.data.PlaceOfPerformance" \
                                                                 "[\"address\"]->com.procurement.mdm.model.dto." \
                                                                 "data.Address[\"addressDetails\"]->com." \
                                                                 "procurement.mdm.model.dto.data.AddressDetails" \
                                                                 "[\"locality\"]->com.procurement.mdm.model.dto." \
                                                                 "data.LocalityDetails[\"description\"])"

    @pytestrail.case("27198")
    def test_27198_72_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"placeOfPerformance\"]->com.procurement.mdm." \
                                                                 "model.dto.data.PlaceOfPerformance" \
                                                                 "[\"description\"])"

    @pytestrail.case("27198")
    def test_27198_73_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"options\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "LotTD$Option[\"description\"])"

    @pytestrail.case("27198")
    def test_27198_74_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0]["period"]["durationInDays"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "MismatchedInputException: Cannot deserialize " \
                                                                 "instance of `java.lang.Integer` out of VALUE_" \
                                                                 "FALSE token\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]" \
                                                                 "->com.procurement.mdm.model.dto.data.TenderTD" \
                                                                 "[\"lots\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"options\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD$Option" \
                                                                 "[\"period\"]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD$Period[\"durationInDays\"])"

    @pytestrail.case("27198")
    def test_27198_75_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0]["period"]["startDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"options\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD$Option" \
                                                                 "[\"period\"]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD$Period[\"startDate\"])"

    @pytestrail.case("27198")
    def test_27198_76_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0]["period"]["endDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"options\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD$Option" \
                                                                 "[\"period\"]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD$Period[\"endDate\"])"

    @pytestrail.case("27198")
    def test_27198_77_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0]["period"]["maxExtentDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"options\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD$Option" \
                                                                 "[\"period\"]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD$Period[\"maxExtentDate\"])"

    @pytestrail.case("27198")
    def test_27198_78_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["recurrence"]["dates"][0]["startDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"recurrence\"]->com.procurement." \
                                                                 "mdm.model.dto.data.LotTD$Recurrence[\"dates\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.mdm." \
                                                                 "model.dto.data.LotTD$Recurrence$Date[\"startDate\"])"

    @pytestrail.case("27198")
    def test_27198_79_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["recurrence"]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "LotTD[\"recurrence\"]->com.procurement.mdm." \
                                                                 "model.dto.data.LotTD$Recurrence[\"description\"])"

    @pytestrail.case("27198")
    def test_27198_80_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"renewal\"]->com.procurement.mdm.model." \
                                                                 "dto.data.LotTD$Renewal[\"description\"])"

    @pytestrail.case("27198")
    def test_27198_81_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["minimumRenewals"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "MismatchedInputException: Cannot deserialize " \
                                                                 "instance of `java.lang.Integer` out of VALUE_" \
                                                                 "FALSE token\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]" \
                                                                 "->com.procurement.mdm.model.dto.data.TenderTD" \
                                                                 "[\"lots\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD[\"renewal\"]" \
                                                                 "->com.procurement.mdm.model.dto.data.LotTD$" \
                                                                 "Renewal[\"minimumRenewals\"])"

    @pytestrail.case("27198")
    def test_27198_82_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["maximumRenewals"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "MismatchedInputException: Cannot deserialize " \
                                                                 "instance of `java.lang.Integer` out of VALUE_" \
                                                                 "FALSE token\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]" \
                                                                 "->com.procurement.mdm.model.dto.data.TenderTD" \
                                                                 "[\"lots\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"renewal\"]->com.procurement.mdm.model." \
                                                                 "dto.data.LotTD$Renewal[\"maximumRenewals\"])"

    @pytestrail.case("27198")
    def test_27198_83_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["period"]["durationInDays"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "MismatchedInputException: Cannot deserialize " \
                                                                 "instance of `java.lang.Integer` out of VALUE_" \
                                                                 "FALSE token\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                 "[\"lots\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"renewal\"]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD$Renewal[\"period\"]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD$Period" \
                                                                 "[\"durationInDays\"])"

    @pytestrail.case("27198")
    def test_27198_84_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["period"]["startDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data.LotTD" \
                                                                 "[\"renewal\"]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD$Renewal[\"period\"]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD$" \
                                                                 "Period[\"startDate\"])"

    @pytestrail.case("27198")
    def test_27198_85_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["period"]["endDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"renewal\"]->com.procurement.mdm." \
                                                                 "model.dto.data.LotTD$Renewal[\"period\"]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD$Period" \
                                                                 "[\"endDate\"])"

    @pytestrail.case("27198")
    def test_27198_86_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["period"]["maxExtentDate"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.LotTD[\"renewal\"]->com.procurement.mdm." \
                                                                 "model.dto.data.LotTD$Renewal[\"period\"]->com." \
                                                                 "procurement.mdm.model.dto.data.LotTD$Period" \
                                                                 "[\"maxExtentDate\"])"

    @pytestrail.case("27198")
    def test_27198_87_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"items\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data.ItemTD" \
                                                                 "[\"id\"])"

    @pytestrail.case("27198")
    def test_27198_88_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["internalId"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"items\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.ItemTD[\"internalId\"])"

    @pytestrail.case("27198")
    def test_27198_89_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.54"
        assert message_from_kafka["errors"][0]["description"] == "The calculated CPV code does not match the " \
                                                                 "CPV code in the tender."

    @pytestrail.case("27198")
    def test_27198_90_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model." \
                                                                 "dto.data.TD[\"tender\"]->com.procurement.mdm." \
                                                                 "model.dto.data.TenderTD[\"items\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.ItemTD[\"additionalClassifications\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement.mdm." \
                                                                 "model.dto.data.ClassificationTD[\"id\"])"

    @pytestrail.case("27198")
    def test_27198_91_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["quantity"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "MismatchedInputException: Cannot deserialize " \
                                                                 "instance of `java.math.BigDecimal` out of " \
                                                                 "VALUE_FALSE token\n at [Source: UNKNOWN; " \
                                                                 "line: -1, column: -1] (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"items\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "ItemTD[\"quantity\"])"

    @pytestrail.case("27198")
    def test_27198_92_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"items\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.ItemTD[\"unit\"]->com.procurement.mdm." \
                                                                 "model.dto.data.ItemUnitTD[\"id\"])"

    @pytestrail.case("27198")
    def test_27198_93_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement." \
                                                                 "mdm.exception.InErrorException) (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"items\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.ItemTD[\"description\"])"

    @pytestrail.case("27198")
    def test_27198_94_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["relatedLot"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: (was com.procurement.mdm." \
                                                                 "exception.InErrorException) (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"items\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "ItemTD[\"relatedLot\"])"

    @pytestrail.case("27198")
    def test_27198_95_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["documentType"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc." \
                                                                 "InvalidDefinitionException: Cannot construct " \
                                                                 "instance of `com.procurement.access.domain." \
                                                                 "model.enums.DocumentType`, problem: Unknown " \
                                                                 "value for enumType com.procurement.access." \
                                                                 "domain.model.enums.DocumentType: false, Allowed " \
                                                                 "values are evaluationCriteria, " \
                                                                 "eligibilityCriteria, billOfQuantity, " \
                                                                 "illustration, marketStudies, tenderNotice, " \
                                                                 "biddingDocuments, procurementPlan, " \
                                                                 "technicalSpecifications, contractDraft, " \
                                                                 "hearingNotice, clarifications, " \
                                                                 "environmentalImpact, " \
                                                                 "assetAndLiabilityAssessment, riskProvisions, " \
                                                                 "complaints, needsAssessment, " \
                                                                 "feasibilityStudy, projectPlan, " \
                                                                 "conflictOfInterest, cancellationDetails, " \
                                                                 "shortlistedFirms, evaluationReports, " \
                                                                 "contractArrangements, contractGuarantees\n at " \
                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"documents\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.document." \
                                                                 "DocumentRequest[\"documentType\"])"

    @pytestrail.case("27198")
    def test_27198_96_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["id"] = False
        value_of_key = str(payload["tender"]["documents"][0]["id"]).lower()
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.14.00.14"
        assert message_from_kafka["errors"][0]["description"] == f"Files not found: [{value_of_key}]"

    @pytestrail.case("27198")
    def test_27198_97_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["title"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ev_release["releases"][0]["tender"]["documents"][0]["title"] == str(
            payload["tender"]["documents"][0]["title"]).lower()

    @pytestrail.case("27198")
    def test_27198_98_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["description"] = False
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ev_release["releases"][0]["tender"]["documents"][0]["description"] == str(
            payload["tender"]["documents"][0]["description"]).lower()

    @pytestrail.case("27198")
    def test_27198_99_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["relatedLots"] = [False]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.06"
        assert message_from_kafka["errors"][0]["description"] == "Invalid documents related lots."

    @pytestrail.case("27196")
    def test_27196_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202

    @pytestrail.case("27196")
    def test_27196_2_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert message_from_kafka["data"]["ocid"] == cpid
        assert message_from_kafka["data"]["url"] == f"http://dev.public.eprocurement.systems/tenders/{cpid}"

    @pytestrail.case("27196")
    def test_27196_3_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        execute_cql_from_orchestrator_operation_step_by_oper_id(
            message_from_kafka["X-OPERATION-ID"], "NoticeCreateReleaseTask")
        cn.delete_auction_from_database(cpid)

    @pytestrail.case("27196")
    def test_27196_4_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        context_start_date_from_database = execute_cql_from_orchestrator_operation_step_by_oper_id(
            message_from_kafka["X-OPERATION-ID"], "NoticeCreateReleaseTask")[3]["startDate"]
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert ev_release["releases"][0]["date"] == context_start_date_from_database

    @pytestrail.case("27200")
    def test_27200_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        access_token = get_access_token_for_platform_two()
        x_operation_id = get_x_operation_id(access_token)
        host = set_instance_for_request()
        create_cnonpn_response = requests.post(
            url=host + create_cn + cpid + '/' + pn[3],
            headers={
                'Authorization': 'zzz',
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': pn[4],
                'Content-Type': 'application/json'},
            json=payload)
        dict = json.loads(create_cnonpn_response.text)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.status_code == 401
        assert dict["errors"][0]["code"] == "401.81.02.02"
        assert dict["errors"][0][
                   "description"] == "Invalid type of the authentication token. Expected type is 'Bearer'."

    @pytestrail.case("27201")
    def test_27201_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        access_token = get_access_token_for_platform_two()
        x_operation_id = get_x_operation_id(access_token)
        time.sleep(2)
        host = set_instance_for_request()
        create_cnonpn_response = requests.post(
            url=host + create_cn + cpid + '/' + pn[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': pn[4],
                'Content-Type': 'application/json'},
            json=payload)
        time.sleep(2)
        error_from_DB = execute_cql_from_orchestrator_operation_step(cpid, 'AccessCheckOwnerTokenTask')
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert error_from_DB['errors'][0]['code'] == '400.03.00.02'
        assert error_from_DB['errors'][0]['description'] == 'Invalid owner.'

    @pytestrail.case("27202")
    def test_27202_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        time.sleep(2)
        host = set_instance_for_request()
        create_cnonpn_response = requests.post(
            url=host + create_cn + cpid + '/' + pn[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=payload)
        time.sleep(2)
        dict = json.loads(create_cnonpn_response.text)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.status_code == 400
        assert dict["errors"][0]["code"] == "400.00.00.00"
        assert dict["errors"][0]["description"] == \
               "Missing request header 'X-TOKEN' for method parameter of type String"

    @pytestrail.case("27203")
    def test_27203_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        time.sleep(2)
        host = set_instance_for_request()
        create_cnonpn_response = requests.post(
            url=host + create_cn + cpid + '/' + pn[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': str(uuid4()),
                'Content-Type': 'application/json'},
            json=payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.04"
        assert message_from_kafka["errors"][0]["description"] == "Invalid token."

    @pytestrail.case("27204")
    def test_27204_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        document = Document("/home/roman/Documents/git/es_system_tests/API.pdf", "API.pdf")
        document_was_uploaded = document.uploading_document()
        payload["tender"]["documents"][1]["id"] = document_was_uploaded[0]["data"]["id"]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202

    @pytestrail.case("27204")
    def test_27204_2_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        document = Document("/home/roman/Documents/git/es_system_tests/API.pdf", "API.pdf")
        document_was_uploaded = document.uploading_document()
        payload["tender"]["documents"][1]["id"] = document_was_uploaded[0]["data"]["id"]
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert message_from_kafka["data"]["ocid"] == cpid
        assert message_from_kafka["data"]["url"] == f"http://dev.public.eprocurement.systems/tenders/{cpid}"

    @pytestrail.case("27204")
    def test_27204_3_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        document = Document("/home/roman/Documents/git/es_system_tests/API.pdf", "API.pdf")
        document_was_uploaded = document.uploading_document()
        hash_of_document = document_was_uploaded[2]
        weight_of_document = document_was_uploaded[3]
        payload["tender"]["documents"][1]["id"] = document_was_uploaded[0]["data"]["id"]
        cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()

        f = open(f"/home/roman/Documents/git/es_system_tests/download/{document_was_uploaded[1]}",
                 "wb")
        open_document = requests.get(
            url=ev_release["releases"][0]["tender"]["documents"][1]["url"]).content
        f.write(open_document)
        f.close()
        hash_of_downloaded_file = get_hash_md5(
            f"/home/roman/Documents/git/es_system_tests/download/{payload['tender']['documents'][1]['id']}")
        weight_of_downloaded_file = get_weught(
            f"/home/roman/Documents/git/es_system_tests/download/{payload['tender']['documents'][1]['id']}")
        cn.delete_auction_from_database(cpid)
        assert hash_of_document == hash_of_downloaded_file
        assert weight_of_document == weight_of_downloaded_file

    @pytestrail.case("27199")
    def test_27199_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        previous_ms_release = cn.get_previous_ms_release(pn)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["planning"]["rationale"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka
        assert ms_release["releases"][0]["planning"]["rationale"] == previous_ms_release["releases"][0]["planning"][
            "rationale"]

    @pytestrail.case("27199")
    def test_27199_2_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        previous_ms_release = cn.get_previous_ms_release(pn)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["planning"]["budget"]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka
        assert ms_release["releases"][0]["planning"]["budget"]["description"] == \
               previous_ms_release["releases"][0]["planning"]["budget"]["description"]

    @pytestrail.case("27199")
    def test_27199_3_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["title"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka
        assert ev_release["releases"][0]["tender"]["title"] == "Evaluation"

    @pytestrail.case("27199")
    def test_27199_4_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka
        assert ev_release["releases"][0]["tender"]["description"] == "Evaluation stage of contracting process"

    @pytestrail.case("27199")
    def test_27199_5_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procurementMethodRationale"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procurementMethod" \
                                                                 "Rationale' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_6_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procurementMethodAdditionalInfo"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procurementMethodAdditionalInfo' is empty " \
                                                                 "or blank."

    @pytestrail.case("27199")
    def test_27199_7_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["awardCriteria"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.exc." \
                                                                 "InvalidDefinitionException: Cannot construct " \
                                                                 "instance of `com.procurement.access.domain.model." \
                                                                 "enums.AwardCriteria`, problem: Unknown value for " \
                                                                 "enumType com.procurement.access.domain.model." \
                                                                 "enums.AwardCriteria: , Allowed values are " \
                                                                 "priceOnly, costOnly, qualityOnly, ratedCriteria\n " \
                                                                 "at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"awardCriteria\"])"

    @pytestrail.case("27199")
    def test_27199_8_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["awardCriteriaDetails"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.exc.Invalid" \
                                                                 "DefinitionException: Cannot construct instance " \
                                                                 "of `com.procurement.access.domain.model.enums." \
                                                                 "AwardCriteriaDetails`, problem: Unknown value " \
                                                                 "for enumType com.procurement.access.domain.model." \
                                                                 "enums.AwardCriteriaDetails: , Allowed values are " \
                                                                 "manual, automated\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"awardCriteriaDetails\"])"

    @pytestrail.case("27199")
    def test_27199_9_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["tenderPeriod"]["endDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.04.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at " \
                                                                 "index 0 (through reference chain: com." \
                                                                 "procurement.submission.infrastructure.handler." \
                                                                 "v1.model.request.PeriodRq[\"tenderPeriod\"]" \
                                                                 "->com.procurement.submission.model.dto.ocds." \
                                                                 "Period[\"endDate\"])"

    @pytestrail.case("27199")
    def test_27199_10_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["enquiryPeriod"]["endDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.05.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at " \
                                                                 "index 0 (through reference chain: com." \
                                                                 "procurement.clarification.infrastructure." \
                                                                 "handler.v1.model.request.PeriodRq" \
                                                                 "[\"enquiryPeriod\"]->com.procurement." \
                                                                 "clarification.model.dto.ocds.Period[\"endDate\"])"

    @pytestrail.case("27199")
    def test_27199_11_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procurementMethodModalities"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.exc.Mismatched" \
                                                                 "InputException: Cannot construct instance of " \
                                                                 "`java.util.HashSet` (although at least one " \
                                                                 "Creator exists): no String-argument constructor" \
                                                                 "/factory method to deserialize from String value " \
                                                                 "('')\n at [Source: UNKNOWN; line: -1, column: " \
                                                                 "-1] (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"procurementMethod" \
                                                                 "Modalities\"])"

    @pytestrail.case("27199")
    def test_27199_12_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.electronicAuctions.details[0].id' " \
                                                                 "is empty or blank."

    @pytestrail.case("27199")
    def test_27199_13_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["relatedLot"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.15.10.01'
        assert message_from_kafka['errors'][0]['description'] == "Electronic auctions contain an invalid " \
                                                                 "related lot: ''."

    @pytestrail.case("27199")
    def test_27199_14_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
            "eligibleMinimumDifference"]["currency"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.15.10.01'
        assert message_from_kafka['errors'][0]['description'] == "Electronic auction with id: '1' contain invalid " \
                                                                 "currency in 'EligibleMinimumDifference' attribute."

    @pytestrail.case("27199")
    def test_27199_15_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procuringEntity.id' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_16_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["title"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procuringEntity.persones.title' is " \
                                                                 "empty or blank."

    @pytestrail.case("27199")
    def test_27199_17_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["name"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procuringEntity.persones.name' is " \
                                                                 "empty or blank."

    @pytestrail.case("27199")
    def test_27199_18_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procuringEntity.persones.identifier.id' " \
                                                                 "is empty or blank."

    @pytestrail.case("27199")
    def test_27199_19_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["scheme"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procuringEntity.persones.identifier." \
                                                                 "scheme' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_20_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["identifier"]["uri"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procuringEntity.persones.identifier.uri' " \
                                                                 "is empty or blank."

    @pytestrail.case("27199")
    def test_27199_21_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procuringEntity.persones." \
                                                                 "businessFunctions.id' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_22_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["type"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.exc." \
                                                                 "InvalidDefinitionException: Cannot construct " \
                                                                 "instance of `com.procurement.access.domain." \
                                                                 "model.enums.BusinessFunctionType`, problem: " \
                                                                 "Unknown value for enumType com.procurement." \
                                                                 "access.domain.model.enums.BusinessFunctionType:" \
                                                                 " , Allowed values are chairman, procurement" \
                                                                 "Officer, contactPoint, technicalEvaluator, " \
                                                                 "technicalOpener, priceOpener, priceEvaluator\n " \
                                                                 "at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model." \
                                                                 "request.OpenCnOnPnRequest[\"tender\"]->com." \
                                                                 "procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"procuringEntity\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ProcuringEntity" \
                                                                 "[\"persones\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "ProcuringEntity$Persone[\"businessFunctions\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ProcuringEntity$" \
                                                                 "Persone$BusinessFunction[\"type\"])"

    @pytestrail.case("27199")
    def test_27199_23_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["jobTitle"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procuringEntity.persones.businessFunctions." \
                                                                 "jobTitle' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_24_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["period"]["startDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: Text '' could not " \
                                                                 "be parsed at index 0 (through reference " \
                                                                 "chain: com.procurement.mdm.model.dto.data." \
                                                                 "TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"businessFunctions\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.BusinessFunction[\"period\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Period" \
                                                                 "[\"startDate\"])"

    @pytestrail.case("27199")
    def test_27199_25_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.14.00.02'
        assert message_from_kafka['errors'][0]['description'] == "Invalid documents ids: The id of the document " \
                                                                 "is empty or blank."

    @pytestrail.case("27199")
    def test_27199_26_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["documentType"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.exc.Invalid" \
                                                                 "DefinitionException: Cannot construct instance " \
                                                                 "of `com.procurement.access.domain.model.enums." \
                                                                 "BusinessFunctionDocumentType`, problem: Unknown " \
                                                                 "value for enumType com.procurement.access.domain." \
                                                                 "model.enums.BusinessFunctionDocumentType: , " \
                                                                 "Allowed values are regulatoryDocument\n at " \
                                                                 "[Source: UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest[\"tender\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest$Tender[\"procuringEntity\"]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Procuring" \
                                                                 "Entity[\"persones\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Procuring" \
                                                                 "Entity$Persone[\"businessFunctions\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest$Tender$ProcuringEntity$Persone$" \
                                                                 "BusinessFunction[\"documents\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ProcuringEntity$" \
                                                                 "Persone$BusinessFunction$Document[\"documentType\"])"

    @pytestrail.case("27199")
    def test_27199_27_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["title"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procuringEntity.persones.business" \
                                                                 "Functions.documents.title' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_28_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.procuringEntity.persones.business" \
                                                                 "Functions.documents.description' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_29_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].id' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_30_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["title"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].title' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_31_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["relatesTo"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.exc.Invalid" \
                                                                 "DefinitionException: Cannot construct instance " \
                                                                 "of `com.procurement.access.domain.model.enums." \
                                                                 "CriteriaRelatesTo`, problem: Unknown value for " \
                                                                 "enumType com.procurement.access.domain.model." \
                                                                 "enums.CriteriaRelatesTo: , Allowed values are " \
                                                                 "award, item, lot, qualification, tender, " \
                                                                 "tenderer\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"criteria\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.criterion.CriterionRequest" \
                                                                 "[\"relatesTo\"])"

    @pytestrail.case("27199")
    def test_27199_32_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["classification"]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.79'
        assert message_from_kafka['errors'][0]['description'] == "Invalid criteria value. FReq-1.1.1.31"

    @pytestrail.case("27199")
    def test_27199_33_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["classification"]["scheme"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.79'
        assert message_from_kafka['errors'][0]['description'] == "Invalid criteria value. FReq-1.1.1.34 "

    @pytestrail.case("27199")
    def test_27199_34_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].description' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_35_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].requirementGroups[0].id' " \
                                                                 "is empty or blank."

    @pytestrail.case("27199")
    def test_27199_36_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].requirementGroups[0]." \
                                                                 "requirements[0].id' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_37_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["title"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].requirementGroups[0]." \
                                                                 "requirements[0].title' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_38_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["dataType"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: Unknown value for enumType " \
                                                                 "com.procurement.access.domain.model.enums." \
                                                                 "RequirementDataType: , Allowed values are boolean, " \
                                                                 "string, number, integer (through reference " \
                                                                 "chain: com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest" \
                                                                 "[\"tender\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"criteria\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model." \
                                                                 "request.criterion.CriterionRequest" \
                                                                 "[\"requirementGroups\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest$Requirement" \
                                                                 "Group[\"requirements\"])"

    @pytestrail.case("27199")
    def test_27199_39_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["expectedValue"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].requirementGroups[0]." \
                                                                 "requirements[0].expectedValue' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_40_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0]["period"]["startDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at index " \
                                                                 "0 (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"criteria\"]->java." \
                                                                 "util.ArrayList[3]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest[\"requirementGroups\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.criterion." \
                                                                 "CriterionRequest$RequirementGroup[\"requirements\"])"

    @pytestrail.case("27199")
    def test_27199_41_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][3]["requirementGroups"][0]["requirements"][0]["period"]["endDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at index " \
                                                                 "0 (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"criteria\"]->java." \
                                                                 "util.ArrayList[3]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest[\"requirementGroups\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.criterion." \
                                                                 "CriterionRequest$RequirementGroup[\"requirements\"])"

    @pytestrail.case("27199")
    def test_27199_42_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].requirementGroups[0]." \
                                                                 "requirements[0].eligibleEvidences[0].id' " \
                                                                 "is empty or blank."

    @pytestrail.case("27199")
    def test_27199_43_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0][
            "title"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].requirementGroups[0]." \
                                                                 "requirements[0].eligibleEvidences[0].title' " \
                                                                 "is empty or blank."

    @pytestrail.case("27199")
    def test_27199_44_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0][
            "description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].requirementGroups[0]." \
                                                                 "requirements[0].eligibleEvidences[0]." \
                                                                 "description' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_45_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0][
            "type"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Error of parsing element of " \
                                                                 "'EligibleEvidenceType' enum. Invalid value ''. " \
                                                                 "(through reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"criteria\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest[\"requirementGroups\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest$RequirementGroup" \
                                                                 "[\"requirements\"])"

    @pytestrail.case("27199")
    def test_27199_46_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0][
            "relatedDocument"]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.criteria[0].requirementGroups[0]." \
                                                                 "requirements[0].eligibleEvidences[0]." \
                                                                 "relatedDocument.id' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_47_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.conversions[0].id' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_48_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["relatesTo"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.exc.Invalid" \
                                                                 "DefinitionException: Cannot construct instance " \
                                                                 "of `com.procurement.access.domain.model.enums." \
                                                                 "ConversionsRelatesTo`, problem: Unknown value " \
                                                                 "for enumType com.procurement.access.domain.model." \
                                                                 "enums.ConversionsRelatesTo: , Allowed values are " \
                                                                 "requirement, observation, option\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"conversions\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "ConversionRequest[\"relatesTo\"])"

    @pytestrail.case("27199")
    def test_27199_49_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["relatedItem"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.conversions[0].relatedItem' " \
                                                                 "is empty or blank."

    @pytestrail.case("27199")
    def test_27199_50_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["rationale"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.conversions[0].rationale' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_51_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.conversions[0].description' is empty " \
                                                                 "or blank."

    @pytestrail.case("27199")
    def test_27199_52_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["coefficients"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.conversions[0].coefficients[0]." \
                                                                 "id' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_53_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["coefficients"][0]["value"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.conversions[0].coefficients[0].value' " \
                                                                 "is empty or blank."

    @pytestrail.case("27199")
    def test_27199_54_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].id' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_55_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["internalId"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].internalId' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_56_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["title"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].title' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_57_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].description' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_58_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["value"]["currency"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.15'
        assert message_from_kafka['errors'][0]['description'] == "Invalid lot currency. Lot with id: '1' contains " \
                                                                 "invalid currency (lot currency: '', budget " \
                                                                 "amount currency: 'EUR')"

    @pytestrail.case("27199")
    def test_27199_59_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at index " \
                                                                 "0 (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot[\"contractPeriod\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                                                 "ContractPeriod[\"startDate\"])"

    @pytestrail.case("27199")
    def test_27199_60_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at index " \
                                                                 "0 (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot[\"contractPeriod\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                                                 "ContractPeriod[\"endDate\"])"

    @pytestrail.case("27199")
    def test_27199_61_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].placeOfPerformance.address." \
                                                                 "streetAddress' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_62_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["postalCode"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].placeOfPerformance.address." \
                                                                 "postalCode' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_63_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.00.11'
        assert message_from_kafka['errors'][0]['description'] == "Country not found. "

    @pytestrail.case("27199")
    def test_27199_64_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.00.13'
        assert message_from_kafka['errors'][0]['description'] == "Region not found. "

    @pytestrail.case("27199")
    def test_27199_65_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.00.14'
        assert message_from_kafka['errors'][0]['description'] == "Locality not found. "

    @pytestrail.case("27199")
    def test_27199_66_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].placeOfPerformance.address." \
                                                                 "addressDetails.locality.scheme' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_67_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = "5700000"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = "5711001"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ev_release["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                   "locality"]["description"] == "s.Piteşti"

    @pytestrail.case("27199")
    def test_27199_68_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].placeOfPerformance.description' " \
                                                                 "is empty or blank."

    @pytestrail.case("27199")
    def test_27199_69_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].options[0].description' is " \
                                                                 "empty or blank."

    @pytestrail.case("27199")
    def test_27199_70_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0]["period"]["startDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at index " \
                                                                 "0 (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot[\"options\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender$Lot$Option[\"period\"]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                                                 "Period[\"startDate\"])"

    @pytestrail.case("27199")
    def test_27199_71_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0]["period"]["endDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at index " \
                                                                 "0 (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot[\"options\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender$Lot$Option[\"period\"]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                                                 "Period[\"endDate\"])"

    @pytestrail.case("27199")
    def test_27199_72_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0]["period"]["maxExtentDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at index " \
                                                                 "0 (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest$Tender$Lot[\"options\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest$Tender$Lot$Option[\"period\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                                                 "Period[\"maxExtentDate\"])"

    @pytestrail.case("27199")
    def test_27199_73_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["recurrence"]["dates"][0]["startDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at index " \
                                                                 "0 (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot[\"recurrence\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                                                 "Recurrence[\"dates\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                                                 "Recurrence$Date[\"startDate\"])"

    @pytestrail.case("27199")
    def test_27199_74_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["recurrence"]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].recurrence.description' is " \
                                                                 "empty or blank."

    @pytestrail.case("27199")
    def test_27199_75_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.lots[0].renewal.description' is " \
                                                                 "empty or blank."

    @pytestrail.case("27199")
    def test_27199_76_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["period"]["startDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at index" \
                                                                 " 0 (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot[\"renewal\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                                                 "Renewal[\"period\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest$Tender$Lot$Period[\"startDate\"])"

    @pytestrail.case("27199")
    def test_27199_77_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["period"]["endDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: Text '' could not be parsed at index" \
                                                                 " 0 (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot[\"renewal\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                                                 "Renewal[\"period\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest$Tender$Lot$Period[\"endDate\"])"

    @pytestrail.case("27199")
    def test_27199_78_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["period"]["maxExtentDate"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind." \
                                                                 "JsonMappingException: Text '' could not be " \
                                                                 "parsed at index 0 (through reference chain: " \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"lots\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Lot" \
                                                                 "[\"renewal\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot$Renewal[\"period\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "Lot$Period[\"maxExtentDate\"])"

    @pytestrail.case("27199")
    def test_27199_79_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.items[0].id' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_80_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["internalId"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.items[0].internalId' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_81_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.54'
        assert message_from_kafka['errors'][0]['description'] == "The calculated CPV code does not match the CPV " \
                                                                 "code in the tender."

    @pytestrail.case("27199")
    def test_27199_82_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.01.05'
        assert message_from_kafka['errors'][0]['description'] == "Invalid cpvs code. "

    @pytestrail.case("27199")
    def test_27199_83_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.01.06'
        assert message_from_kafka['errors'][0]['description'] == "Invalid unit code. "

    @pytestrail.case("27199")
    def test_27199_84_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.items[0].description' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_85_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["relatedLot"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.items[0].relatedLot' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_86_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["id"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.14.00.02'
        assert message_from_kafka['errors'][0]['description'] == "Invalid documents ids: The id of the " \
                                                                 "document is empty or blank."

    @pytestrail.case("27199")
    def test_27199_87_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["documentType"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.exc.Invalid" \
                                                                 "DefinitionException: Cannot construct instance " \
                                                                 "of `com.procurement.access.domain.model.enums." \
                                                                 "DocumentType`, problem: Unknown value for " \
                                                                 "enumType com.procurement.access.domain.model." \
                                                                 "enums.DocumentType: , Allowed values are " \
                                                                 "evaluationCriteria, eligibilityCriteria, " \
                                                                 "billOfQuantity, illustration, marketStudies, " \
                                                                 "tenderNotice, biddingDocuments, procurementPlan, " \
                                                                 "technicalSpecifications, contractDraft, " \
                                                                 "hearingNotice, clarifications, environmental" \
                                                                 "Impact, assetAndLiabilityAssessment, risk" \
                                                                 "Provisions, complaints, needsAssessment, " \
                                                                 "feasibilityStudy, projectPlan, conflict" \
                                                                 "OfInterest, cancellationDetails, shortlisted" \
                                                                 "Firms, evaluationReports, contractArrangements, " \
                                                                 "contractGuarantees\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"documents\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.document.DocumentRequest" \
                                                                 "[\"documentType\"])"

    @pytestrail.case("27199")
    def test_27199_88_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["title"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.documents[0].title' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_89_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["description"] = ""
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.documents[0].description' is empty or blank."

    @pytestrail.case("27199")
    def test_27199_90_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["relatedLots"] = [""]
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        time.sleep(3)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. The attribute " \
                                                                 "'tender.documents[0].relatedLots[0]' is " \
                                                                 "empty or blank."

    @pytestrail.case("27205")
    def test_27205_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        previous_ms_release = cn.get_previous_ms_release(pn)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["planning"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ms_release["releases"][0]["planning"] == previous_ms_release["releases"][0]["planning"]

    @pytestrail.case("27205")
    def test_27205_2_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        previous_ms_release = cn.get_previous_ms_release(pn)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["planning"]["budget"]["description"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert ms_release["releases"][0]["planning"]["budget"] == \
               previous_ms_release["releases"][0]["planning"]["budget"]

    @pytestrail.case("27205")
    def test_27205_3_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.05.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin." \
                                                                 "MissingKotlinParameterException: " \
                                                                 "Instantiation of [simple type, " \
                                                                 "class com.procurement.clarification." \
                                                                 "infrastructure.handler.v1.model." \
                                                                 "request.PeriodRq] value failed for " \
                                                                 "JSON property enquiryPeriod due to " \
                                                                 "missing (therefore NULL) value for " \
                                                                 "creator parameter enquiryPeriod " \
                                                                 "which is a non-nullable type\n at " \
                                                                 "[Source: UNKNOWN; line: -1, column: " \
                                                                 "-1] (through reference chain: com." \
                                                                 "procurement.clarification." \
                                                                 "infrastructure.handler.v1.model." \
                                                                 "request.PeriodRq[\"enquiryPeriod\"])"

    @pytestrail.case("27205")
    def test_27205_4_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["tenderPeriod"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.04.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin." \
                                                                 "MissingKotlinParameterException: " \
                                                                 "Instantiation of [simple type, " \
                                                                 "class com.procurement.submission." \
                                                                 "model.dto.ocds.Period] value failed " \
                                                                 "for JSON property endDate due to " \
                                                                 "missing (therefore NULL) value for " \
                                                                 "creator parameter endDate which is " \
                                                                 "a non-nullable type\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com." \
                                                                 "procurement.submission." \
                                                                 "infrastructure.handler.v1.model." \
                                                                 "request.PeriodRq[\"tenderPeriod\"]" \
                                                                 "->com.procurement.submission.model." \
                                                                 "dto.ocds.Period[\"endDate\"])"

    @pytestrail.case("27205")
    def test_27205_5_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["enquiryPeriod"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.05.01.02'
        assert message_from_kafka['errors'][0]['description'] == "Invalid period."

    @pytestrail.case("27205")
    def test_27205_6_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procurementMethodModalities"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.67'
        assert message_from_kafka['errors'][0]['description'] == "Incorrect an attribute value. Auction sign must " \
                                                                 "be passed"

    @pytestrail.case("27205")
    def test_27205_7_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation " \
                                                                 "of [simple type, class com.procurement." \
                                                                 "access.infrastructure.handler.v1.model." \
                                                                 "request.OpenCnOnPnRequest$Tender$" \
                                                                 "ElectronicAuctions] value failed for " \
                                                                 "JSON property details due to missing " \
                                                                 "(therefore NULL) value for creator " \
                                                                 "parameter details which is a non-" \
                                                                 "nullable type\n at [Source: UNKNOWN; " \
                                                                 "line: -1, column: -1] (through reference chain: " \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"electronicAuctions\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender$ElectronicAuctions[\"details\"])"

    @pytestrail.case("27205")
    def test_27205_8_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.15.10.01'
        assert message_from_kafka['errors'][0]['description'] == "Electronic auctions are empty."

    @pytestrail.case("27205")
    def test_27205_9_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module." \
                                                                 "kotlin.MissingKotlinParameterException: " \
                                                                 "Instantiation of [simple type, class com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Electronic" \
                                                                 "Auctions$Detail] value failed for JSON property " \
                                                                 "id due to missing (therefore NULL) value for " \
                                                                 "creator parameter id which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column: " \
                                                                 "-1] (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"electronicAuctions\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "ElectronicAuctions[\"details\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest$Tender$ElectronicAuctions$Detail[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_10_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.15.10.01'
        assert message_from_kafka['errors'][0]['description'] == "Electronic auctions modalities are empty."

    @pytestrail.case("27205")
    def test_27205_11_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin." \
                                                                 "MissingKotlinParameterException: Instantiation " \
                                                                 "of [simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions$" \
                                                                 "Detail$Modalities] value failed for JSON " \
                                                                 "property eligibleMinimumDifference due to " \
                                                                 "missing (therefore NULL) value for creator " \
                                                                 "parameter eligibleMinimumDifference which is a " \
                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"electronicAuctions\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions" \
                                                                 "[\"details\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Electronic" \
                                                                 "Auctions$Detail[\"electronicAuctionModalities\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender$ElectronicAuctions$Detail$" \
                                                                 "Modalities[\"eligibleMinimumDifference\"])"

    @pytestrail.case("27205")
    def test_27205_12_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
            "eligibleMinimumDifference"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation " \
                                                                 "of [simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender$ElectronicAuctions$Detail$" \
                                                                 "Modalities] value failed for JSON property " \
                                                                 "eligibleMinimumDifference due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "eligibleMinimumDifference which is a non-" \
                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"electronicAuctions\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$ElectronicAuctions" \
                                                                 "[\"details\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Electronic" \
                                                                 "Auctions$Detail[\"electronicAuctionModalities\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender$ElectronicAuctions$Detail$" \
                                                                 "Modalities[\"eligibleMinimumDifference\"])"

    @pytestrail.case("27205")
    def test_27205_12_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["electronicAuctions"]["details"][0]["electronicAuctionModalities"][0][
            "eligibleMinimumDifference"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest$Tender$ElectronicAuctions$Detail$" \
                                                                 "Modalities$EligibleMinimumDifference] value " \
                                                                 "failed for JSON property amount due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "amount which is a non-nullable type\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through reference " \
                                                                 "chain: com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest" \
                                                                 "[\"tender\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest$Tender[\"electronicAuctions\"]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "ElectronicAuctions[\"details\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest$Tender$ElectronicAuctions$Detail" \
                                                                 "[\"electronicAuctionModalities\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest$Tender$ElectronicAuctions$Detail$" \
                                                                 "Modalities[\"eligibleMinimumDifference\"]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Electronic" \
                                                                 "Auctions$Detail$Modalities$EligibleMinimum" \
                                                                 "Difference[\"amount\"])"

    @pytestrail.case("27205")
    def test_27205_13_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlin" \
                                                                 "ParameterException: Instantiation of [simple " \
                                                                 "type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest$Tender$ProcuringEntity] value " \
                                                                 "failed for JSON property id due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "id which is a non-nullable type\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through reference " \
                                                                 "chain: com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest" \
                                                                 "[\"tender\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest$Tender[\"procuringEntity\"]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$" \
                                                                 "ProcuringEntity[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_14_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.01.12'
        assert message_from_kafka['errors'][0]['description'] == "Persones array must not be empty. "

    @pytestrail.case("27205")
    def test_27205_15_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.Persone] value failed for JSON property " \
                                                                 "title due to missing (therefore NULL) value for " \
                                                                 "creator parameter title which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column: " \
                                                                 "-1] (through reference chain: com.procurement." \
                                                                 "mdm.model.dto.data.TD[\"tender\"]->com." \
                                                                 "procurement.mdm.model.dto.data.TenderTD" \
                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                 "model.dto.data.OrganizationReference" \
                                                                 "[\"persones\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"title\"])"

    @pytestrail.case("27205")
    def test_27205_16_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["identifier"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.Identifier] value failed for JSON " \
                                                                 "property id due to missing (therefore NULL) " \
                                                                 "value for creator parameter id which is a non" \
                                                                 "-nullable type\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: " \
                                                                 "com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
                                                                 "procurement.mdm.model.dto.data.Organization" \
                                                                 "Reference[\"persones\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data." \
                                                                 "Persone[\"identifier\"]->com.procurement." \
                                                                 "mdm.model.dto.data.Identifier[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_17_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.66'
        assert message_from_kafka['errors'][0]['description'] == "Invalid procuring entity. At least one " \
                                                                 "businessFunctions detalization should be added. "

    @pytestrail.case("27205")
    def test_27205_18_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.BusinessFunction] value failed for " \
                                                                 "JSON property id due to missing (therefore NULL) " \
                                                                 "value for creator parameter id which is a non-" \
                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                 "[\"procuringEntity\"]->com.procurement.mdm.model." \
                                                                 "dto.data.OrganizationReference[\"persones\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement.mdm." \
                                                                 "model.dto.data.Persone[\"businessFunctions\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement.mdm." \
                                                                 "model.dto.data.BusinessFunction[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_19_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["period"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.20.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.Period] value failed for JSON property " \
                                                                 "startDate due to missing (therefore NULL) value " \
                                                                 "for creator parameter startDate which is a non-" \
                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                 "model.dto.data.OrganizationReference" \
                                                                 "[\"persones\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.mdm.model.dto.data.Persone" \
                                                                 "[\"businessFunctions\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.mdm.model.dto.data.Business" \
                                                                 "Function[\"period\"]->com.procurement.mdm.model." \
                                                                 "dto.data.Period[\"startDate\"])"

    @pytestrail.case("27205")
    def test_27205_20_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        cn.delete_auction_from_database(cpid)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        ms_url = list()
        for d in ev_release["releases"][0]["relatedProcesses"]:
            if d["relationship"] == ["parent"]:
                ms_url.append(d["uri"])
        ms_release = requests.get(url=ms_url[0]).json()
        procuring_entity_obj = list()
        for p in ms_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                procuring_entity_obj.append(p)
        check_documents_array_into_ms_releaase = "documents" in \
                                                 procuring_entity_obj[0]["persones"][0]["businessFunctions"][0].keys()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert check_documents_array_into_ms_releaase == False

    @pytestrail.case("27205")
    def test_27205_21_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["procuringEntity"]["persones"][0]["businessFunctions"][0]["documents"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '500.14.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.storage." \
                                                                 "model.dto.registration.Document] value failed " \
                                                                 "for JSON property id due to missing (therefore " \
                                                                 "NULL) value for creator parameter id which is a " \
                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: com." \
                                                                 "procurement.storage.model.dto.registration." \
                                                                 "DocumentsRq[\"documents\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.storage.model.dto." \
                                                                 "registration.Document[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_22_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.82'
        assert message_from_kafka['errors'][0]['description'] == "Collection is empty. All arrays of " \
                                                                 "'CriterionRequest' in json must have at least " \
                                                                 "one object have to be added "

    @pytestrail.case("27205")
    def test_27205_23_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest] value failed for " \
                                                                 "JSON property id due to missing (therefore NULL) " \
                                                                 "value for creator parameter id which is a non-" \
                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"criteria\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.criterion.CriterionRequest[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_24_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["classification"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionClassificationRequest] value " \
                                                                 "failed for JSON property id due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "id which is a non-nullable type\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"criteria\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest[\"classification\"]" \
                                                                 "->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.criterion." \
                                                                 "CriterionClassificationRequest[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_25_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.82'
        assert message_from_kafka['errors'][0]['description'] == "Collection is empty. All arrays of 'Requirement" \
                                                                 "Group' in json must have at least one object " \
                                                                 "have to be added "

    @pytestrail.case("27205")
    def test_27205_26_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.00'
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest$RequirementGroup] " \
                                                                 "value failed for JSON property id due to missing " \
                                                                 "(therefore NULL) value for creator parameter id " \
                                                                 "which is a non-nullable type\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"criteria\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest" \
                                                                 "[\"requirementGroups\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.criterion.Criterion" \
                                                                 "Request$RequirementGroup[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_27_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == '400.03.10.82'
        assert message_from_kafka['errors'][0]['description'] == "Collection is empty. All arrays of " \
                                                                 "'Requirement' in json must have at least one " \
                                                                 "object have to be added "

    @pytestrail.case("27205")
    def test_27205_28_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: (was java.lang.NullPointerException) " \
                                                                 "(through reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"criteria\"]->java." \
                                                                 "util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest[\"requirementGroups\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model." \
                                                                 "request.criterion.CriterionRequest$Requirement" \
                                                                 "Group[\"requirements\"])"

    @pytestrail.case("27205")
    def test_27205_29_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        check_eligibleEvidences_into_criteria_array = "eligibleEvidences" in \
                                                      ev_release["releases"][0]["tender"]["criteria"][0][
                                                          "requirementGroups"][0]["requirements"][0].keys()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert check_eligibleEvidences_into_criteria_array == False

    @pytestrail.case("27205")
    def test_27205_30_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: (was java.lang.NullPointerException) " \
                                                                 "(through reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model." \
                                                                 "request.OpenCnOnPnRequest$Tender[\"criteria\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model." \
                                                                 "request.criterion.CriterionRequest" \
                                                                 "[\"requirementGroups\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest$Requirement" \
                                                                 "Group[\"requirements\"])"

    @pytestrail.case("27205")
    def test_27205_31_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["eligibleEvidences"][0][
            "relatedDocument"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: (was java.lang.NullPointer" \
                                                                 "Exception) (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest[\"tender\"]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"criteria\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.criterion.CriterionRequest" \
                                                                 "[\"requirementGroups\"]->java.util.ArrayList[0]" \
                                                                 "->com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.criterion.CriterionRequest$" \
                                                                 "RequirementGroup[\"requirements\"])"

    @pytestrail.case("27205")
    def test_27205_32_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["criteria"][0]["requirementGroups"][0]["requirements"][0]["period"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                 "Exception: (was java.lang.NullPointerException) " \
                                                                 "(through reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest[\"tender\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender[\"criteria\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest[\"requirementGroups\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "criterion.CriterionRequest$Requirement" \
                                                                 "Group[\"requirements\"])"

    @pytestrail.case("27205")
    def test_27205_33_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.10.82"
        assert message_from_kafka['errors'][0]['description'] == "Collection is empty. All arrays of " \
                                                                 "'ConversionRequest' in json must have at least " \
                                                                 "one object have to be added "

    @pytestrail.case("27205")
    def test_27205_34_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "ConversionRequest] value failed for JSON " \
                                                                 "property id due to missing (therefore NULL) " \
                                                                 "value for creator parameter id which is a non-" \
                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"conversions\"]->java.util.ArrayList[0]->" \
                                                                 "com.procurement.access.infrastructure.handler." \
                                                                 "v1.model.request.ConversionRequest[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_35_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["coefficients"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.10.82"
        assert message_from_kafka['errors'][0]['description'] == "Collection is empty. All arrays of 'Coefficient' " \
                                                                 "in json must have at least one object have to " \
                                                                 "be added "

    @pytestrail.case("27205")
    def test_27205_36_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["conversions"][0]["coefficients"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "ConversionRequest$Coefficient] value failed " \
                                                                 "for JSON property id due to missing (therefore " \
                                                                 "NULL) value for creator parameter id which is a " \
                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender" \
                                                                 "[\"conversions\"]->java.util.ArrayList[0]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.ConversionRequest[\"coefficients\"]->" \
                                                                 "java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "ConversionRequest$Coefficient[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_37_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.10.29"
        assert message_from_kafka['errors'][0]['description'] == "Lots must not be empty."

    @pytestrail.case("27205")
    def test_27205_38_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest$Tender$Lot] value failed for JSON " \
                                                                 "property id due to missing (therefore NULL) value " \
                                                                 "for creator parameter id which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column: " \
                                                                 "-1] (through reference chain: com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest[\"tender\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest$Tender$Lot[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_39_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["value"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest$Tender$Lot$Value] value failed for " \
                                                                 "JSON property amount due to missing (therefore " \
                                                                 "NULL) value for creator parameter amount which is " \
                                                                 "a non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest[\"tender\"]->" \
                                                                 "com.procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender[\"lots\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender$Lot[\"value\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot$Value[\"amount\"])"

    @pytestrail.case("27205")
    def test_27205_40_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["contractPeriod"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest$Tender$Lot$ContractPeriod] value " \
                                                                 "failed for JSON property startDate due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "startDate which is a non-nullable type\n at " \
                                                                 "[Source: UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest[\"tender\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCnOn" \
                                                                 "PnRequest$Tender[\"lots\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.access.infrastructure." \
                                                                 "handler.v1.model.request.OpenCnOnPnRequest$" \
                                                                 "Tender$Lot[\"contractPeriod\"]->com.procurement." \
                                                                 "access.infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot$ContractPeriod" \
                                                                 "[\"startDate\"])"

    @pytestrail.case("27205")
    def test_27205_41_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["value"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlin" \
                                                                 "ParameterException: Instantiation of [simple " \
                                                                 "type, class com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request." \
                                                                 "OpenCnOnPnRequest$Tender$Lot$Value] value failed " \
                                                                 "for JSON property amount due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "amount which is a non-nullable type\n at [Source: " \
                                                                 "UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.OpenCn" \
                                                                 "OnPnRequest[\"tender\"]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest$Tender[\"lots\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.access." \
                                                                 "infrastructure.handler.v1.model.request.Open" \
                                                                 "CnOnPnRequest$Tender$Lot[\"value\"]->com." \
                                                                 "procurement.access.infrastructure.handler.v1." \
                                                                 "model.request.OpenCnOnPnRequest$Tender$Lot$" \
                                                                 "Value[\"amount\"])"

    @pytestrail.case("27205")
    def test_27205_42_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.00"
        assert message_from_kafka['errors'][0][
                   'description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "PlaceOfPerformance] value failed for JSON property address due to missing " \
                                     "(therefore NULL) value for creator parameter address which is a non-nullable " \
                                     "type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: " \
                                     "com.procurement.mdm.model.dto.data.TD[\"tender\"]->com.procurement.mdm.model." \
                                     "dto.data.TenderTD[\"lots\"]->java.util.ArrayList[0]->com.procurement.mdm." \
                                     "model.dto.data.LotTD[\"placeOfPerformance\"]->com.procurement.mdm.model." \
                                     "dto.data.PlaceOfPerformance[\"address\"])"

    @pytestrail.case("27205")
    def test_27205_43_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.00"
        assert message_from_kafka['errors'][0][
                   'description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "Address] value failed for JSON property streetAddress due to missing " \
                                     "(therefore NULL) value for creator parameter streetAddress which is a non-" \
                                     "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through " \
                                     "reference chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]->com." \
                                     "procurement.mdm.model.dto.data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
                                     "->com.procurement.mdm.model.dto.data.LotTD[\"placeOfPerformance\"]->com." \
                                     "procurement.mdm.model.dto.data.PlaceOfPerformance[\"address\"]->com." \
                                     "procurement.mdm.model.dto.data.Address[\"streetAddress\"])"

    @pytestrail.case("27205")
    def test_27205_44_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.00"
        assert message_from_kafka['errors'][0][
                   'description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto." \
                                     "data.AddressDetails] value failed for JSON property country due to " \
                                     "missing (therefore NULL) value for creator parameter country which is a " \
                                     "non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through " \
                                     "reference chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]->com." \
                                     "procurement.mdm.model.dto.data.TenderTD[\"lots\"]->java.util.ArrayList[0]->" \
                                     "com.procurement.mdm.model.dto.data.LotTD[\"placeOfPerformance\"]->com." \
                                     "procurement.mdm.model.dto.data.PlaceOfPerformance[\"address\"]->com." \
                                     "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->com.procurement." \
                                     "mdm.model.dto.data.AddressDetails[\"country\"])"

    @pytestrail.case("27205")
    def test_27205_45_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.00"
        assert message_from_kafka['errors'][0][
                   'description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "CountryDetails] value failed for JSON property id due to missing " \
                                     "(therefore NULL) value for creator parameter id which is a non-nullable " \
                                     "type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: " \
                                     "com.procurement.mdm.model.dto.data.TD[\"tender\"]->com.procurement.mdm.model." \
                                     "dto.data.TenderTD[\"lots\"]->java.util.ArrayList[0]->com.procurement.mdm." \
                                     "model.dto.data.LotTD[\"placeOfPerformance\"]->com.procurement.mdm.model.dto." \
                                     "data.PlaceOfPerformance[\"address\"]->com.procurement.mdm.model.dto.data." \
                                     "Address[\"addressDetails\"]->com.procurement.mdm.model.dto.data.Address" \
                                     "Details[\"country\"]->com.procurement.mdm.model.dto.data.CountryDetails[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_46_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.00"
        assert message_from_kafka['errors'][0][
                   'description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "RegionDetails] value failed for JSON property id due to missing (therefore " \
                                     "NULL) value for creator parameter id which is a non-nullable type\n at " \
                                     "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     "procurement.mdm.model.dto.data.TD[\"tender\"]->com.procurement.mdm.model.dto." \
                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]->com.procurement.mdm.model." \
                                     "dto.data.LotTD[\"placeOfPerformance\"]->com.procurement.mdm.model.dto.data." \
                                     "PlaceOfPerformance[\"address\"]->com.procurement.mdm.model.dto.data.Address" \
                                     "[\"addressDetails\"]->com.procurement.mdm.model.dto.data.AddressDetails" \
                                     "[\"region\"]->com.procurement.mdm.model.dto.data.RegionDetails[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_47_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.00"
        assert message_from_kafka['errors'][0][
                   'description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.mdm.model.dto.data." \
                                     "LocalityDetails] value failed for JSON property scheme due to missing " \
                                     "(therefore NULL) value for creator parameter scheme which is a non-" \
                                     "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through " \
                                     "reference chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]->com." \
                                     "procurement.mdm.model.dto.data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                     "[0]->com.procurement.mdm.model.dto.data.LotTD[\"placeOfPerformance\"]->" \
                                     "com.procurement.mdm.model.dto.data.PlaceOfPerformance[\"address\"]->com." \
                                     "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->com." \
                                     "procurement.mdm.model.dto.data.AddressDetails[\"locality\"]->com." \
                                     "procurement.mdm.model.dto.data.LocalityDetails[\"scheme\"])"

    @pytestrail.case("27205")
    def test_27205_48_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        check_options_into_lots_array = "options" in ev_release["releases"][0]["tender"]["lots"][0].keys()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert check_options_into_lots_array == False

    @pytestrail.case("27205")
    def test_27205_49_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.01.12"
        assert message_from_kafka['errors'][0][
                   'description'] == "tender.lots.options object must not be empty. "

    @pytestrail.case("27205")
    def test_27205_50_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["options"][0]["period"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.01.12"
        assert message_from_kafka['errors'][0][
                   'description'] == "tender.lots.options.period object must not be empty. "

    @pytestrail.case("27205")
    def test_27205_51_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["recurrence"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.01.12"
        assert message_from_kafka['errors'][0][
                   'description'] == "tender.lots.recurrence object must not be empty. "

    @pytestrail.case("27205")
    def test_27205_52_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["recurrence"]["dates"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        check_dates_into_recurrence_array = "dates" in ev_release["releases"][0]["tender"]["lots"][0][
            "recurrence"].keys()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert check_dates_into_recurrence_array == False

    @pytestrail.case("27205")
    def test_27205_53_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["recurrence"]["dates"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.01.12"
        assert message_from_kafka['errors'][0][
                   'description'] == "tender.lots.recurrence.dates object must not be empty. "

    @pytestrail.case("27205")
    def test_27205_54_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.01.12"
        assert message_from_kafka['errors'][0][
                   'description'] == "tender.lots.renewal object must not be empty. "

    @pytestrail.case("27205")
    def test_27205_55_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["lots"][0]["renewal"]["period"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.01.12"
        assert message_from_kafka['errors'][0][
                   'description'] == "tender.lots.renewal.period object must not be empty. "

    @pytestrail.case("27205")
    def test_27205_56_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.10.28"
        assert message_from_kafka['errors'][0][
                   'description'] == "Items must not be empty. Items must not be empty."

    @pytestrail.case("27205")
    def test_27205_57_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0][
                   'description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.CheckItemsRequest$Item] value failed for JSON " \
                                     "property classification due to missing (therefore NULL) value for creator " \
                                     "parameter classification which is a non-nullable type\n at [Source: " \
                                     "UNKNOWN; line: -1, column: -1] (through reference chain: com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.CheckItemsRequest[\"items\"]" \
                                     "->java.util.ArrayList[0]->com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.CheckItemsRequest$Item[\"classification\"])"

    @pytestrail.case("27205")
    def test_27205_58_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["classification"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.00"
        assert message_from_kafka['errors'][0][
                   'description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.CheckItemsRequest$Item$Classification] value " \
                                     "failed for JSON property id due to missing (therefore NULL) value for " \
                                     "creator parameter id which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.CheckItemsRequest[\"items\"]->" \
                                     "java.util.ArrayList[0]->com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.CheckItemsRequest$Item[\"classification\"]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.CheckItemsRequest$Item$" \
                                     "Classification[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_59_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        check_additional_classification_into_items_array = "additionalClassifications" in \
                                                           ev_release["releases"][0]["tender"]["items"][0].keys()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert check_additional_classification_into_items_array == False

    @pytestrail.case("27205")
    def test_27205_60_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.ClassificationTD] value failed for " \
                                                                 "JSON property id due to missing (therefore " \
                                                                 "NULL) value for creator parameter id which is " \
                                                                 "a non-nullable type\n at [Source: UNKNOWN; " \
                                                                 "line: -1, column: -1] (through reference chain: " \
                                                                 "com.procurement.mdm.model.dto.data.TD" \
                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                 "data.TenderTD[\"items\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data.ItemTD" \
                                                                 "[\"additionalClassifications\"]->java.util." \
                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                 "data.ClassificationTD[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_61_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["items"][0]["unit"] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.20.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlin" \
                                                                 "ParameterException: Instantiation of [simple " \
                                                                 "type, class com.procurement.mdm.model.dto.data." \
                                                                 "ItemUnitTD] value failed for JSON property id " \
                                                                 "due to missing (therefore NULL) value for creator " \
                                                                 "parameter id which is a non-nullable type\n at " \
                                                                 "[Source: UNKNOWN; line: -1, column: -1] (through " \
                                                                 "reference chain: com.procurement.mdm.model.dto." \
                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                 "dto.data.TenderTD[\"items\"]->java.util.ArrayList" \
                                                                 "[0]->com.procurement.mdm.model.dto.data.ItemTD" \
                                                                 "[\"unit\"]->com.procurement.mdm.model.dto." \
                                                                 "data.ItemUnitTD[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_62_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "400.03.10.30"
        assert message_from_kafka['errors'][0]['description'] == "Documents must not be empty. At least one " \
                                                                 "document should be added to tenders documents. "

    @pytestrail.case("27205")
    def test_27205_63_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0] = {}
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert message_from_kafka['errors'][0]['code'] == "500.14.00"
        assert message_from_kafka['errors'][0]['description'] == "com.fasterxml.jackson.module.kotlin.MissingKotlin" \
                                                                 "ParameterException: Instantiation of [simple " \
                                                                 "type, class com.procurement.storage.model.dto." \
                                                                 "registration.Document] value failed for JSON " \
                                                                 "property id due to missing (therefore NULL) value " \
                                                                 "for creator parameter id which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement.storage." \
                                                                 "model.dto.registration.DocumentsRq[\"documents\"]" \
                                                                 "->java.util.ArrayList[0]->com.procurement.storage." \
                                                                 "model.dto.registration.Document[\"id\"])"

    @pytestrail.case("27205")
    def test_27205_64_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        payload["tender"]["documents"][0]["relatedLots"] = []
        create_cnonpn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
        message_from_kafka = cn.get_message_from_kafka()
        ev_url = requests.get(url=message_from_kafka["data"]["url"]).json()["actualReleases"][0]["uri"]
        ev_release = requests.get(url=ev_url).json()
        check_related_lots_into_documents_array = "relatedLots" in \
                                                  ev_release["releases"][0]["tender"]["documents"][0].keys()
        cn.delete_auction_from_database(cpid)
        assert create_cnonpn_response.text == "ok"
        assert create_cnonpn_response.status_code == 202
        assert check_related_lots_into_documents_array == False