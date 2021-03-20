import copy
import time

import requests
from pytest_testrail.plugin import pytestrail

from tests.bpe_create_cnonpn.create_cnonpn import CNonPN
from tests.bpe_create_cnonpn.payloads import payload_cnonpn_auction_full_data_model, \
    payload_cnonpn_obligatory_data_model
from useful_functions import prepared_cpid, get_human_date_in_utc_format, is_it_uuid


class TestBpeCreateCN(object):
    @pytestrail.case("27194")
    def test_27194_1_smoke_regression(self, additional_value):
        cn = CNonPN()
        cpid = prepared_cpid()
        pn = cn.create_pn_obligatory_data_model(cpid=cpid, additional_value=additional_value)
        payload = copy.deepcopy(payload_cnonpn_auction_full_data_model)
        create_cn_response = cn.create_request_cnonpn(cpid=cpid, pn=pn, payload=payload)
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
        assert checking_uuid == True
