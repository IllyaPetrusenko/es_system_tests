import copy
import fnmatch
import time

import requests
from pytest_testrail.plugin import pytestrail
from tests.bpe_update_fs.payloads import fs_update_full_own_money
from tests.bpe_update_fs.update_fs import bpe_update_fs
from tests.cassandra_inserts_into_Database import insert_into_db_create_fs
from useful_functions import prepared_cpid, get_period


class TestBpeCreateEI(object):

    @pytestrail.case("25518")
    def test_25518_1(self):
        cpid = prepared_cpid()
        create_fs_response = insert_into_db_create_fs(cpid)
        payload = fs_update_full_own_money
        payload["planning"]["budget"]["amount"]["amount"] = 6000.66
        payload["planning"]["rationale"] = "for FS updating"
        update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
        assert update_fs_response[0].text == "ok"
        assert update_fs_response[0].status_code == 202
        assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]

    @pytestrail.case("25518")
    def test_25518_2(self):
        cpid = prepared_cpid()
        create_fs_response = insert_into_db_create_fs(cpid)
        payload = fs_update_full_own_money
        payload["planning"]["budget"]["amount"]["amount"] = 6000.66
        payload["planning"]["rationale"] = "for FS updating"
        update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
        ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
        assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
        assert ocid == True

    @pytestrail.case("25518")
    def test_25518_3(self):
        cpid = prepared_cpid()
        create_fs_response = insert_into_db_create_fs(cpid)
        payload = fs_update_full_own_money
        payload["planning"]["budget"]["amount"]["amount"] = 6000.66
        payload["planning"]["rationale"] = "for FS updating"
        update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
        time.sleep(2)
        url_update = update_fs_response[1]["data"]["url"]
        publicPoint_update = requests.get(url=url_update).json()
        assert publicPoint_update["releases"][0]["planning"]["budget"]["amount"]["amount"] == \
               payload["planning"]["budget"]["amount"]["amount"]
        assert publicPoint_update["releases"][0]["planning"]["rationale"] == payload["planning"]["rationale"]

    @pytestrail.case("25519")
    def test_25519_1(self):
        cpid = prepared_cpid()
        create_fs_response = insert_into_db_create_fs(cpid)
        payload = fs_update_full_own_money
        payload["planning"]["budget"]["description"] = "for FS updating"
        update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
        assert update_fs_response[0].text == "ok"
        assert update_fs_response[0].status_code == 202
        assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]

    @pytestrail.case('25519')
    def test_25519_2(self):
        cpid = prepared_cpid()
        create_fs_response = insert_into_db_create_fs(cpid)
        payload = fs_update_full_own_money
        payload['planning']['budget']['description'] = "for FS updating"
        update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
        ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
        assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
        assert ocid == True

    @pytestrail.case("25519")
    def test_25519_3(self):
        cpid = prepared_cpid()
        create_fs_response = insert_into_db_create_fs(cpid)
        payload = fs_update_full_own_money
        payload["planning"]["budget"]["description"] = "for FS updating"
        update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
        time.sleep(2)
        url_update = update_fs_response[1]["data"]["url"]
        publicPoint_update = requests.get(url=url_update).json()
        assert publicPoint_update["releases"][0]["planning"]["budget"]["description"] == payload["planning"]["budget"][
            "description"]

    @pytestrail.case("25520")
    def test_25520_1(self):
        cpid = prepared_cpid()
        create_fs_response = insert_into_db_create_fs(cpid)
        payload = fs_update_full_own_money
        period = get_period()
        payload["planning"]["budget"]["period"]["startDate"] = period[0]
        payload["planning"]["budget"]["period"]["endDate"] = period[1]
        update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
        assert update_fs_response[0].text == "ok"
        assert update_fs_response[0].status_code == 202
        assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]

    @pytestrail.case('25520')
    def test_25520_2(self):
        cpid = prepared_cpid()
        create_fs_response = insert_into_db_create_fs(cpid)
        payload = fs_update_full_own_money
        period = get_period()
        payload["planning"]["budget"]["period"]["startDate"] = period[0]
        payload["planning"]["budget"]["period"]["endDate"] = period[1]
        update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
        ocid = fnmatch.fnmatch(update_fs_response[1]["data"]["ocid"], update_fs_response[3])
        assert update_fs_response[1]["X-OPERATION-ID"] == update_fs_response[2]
        assert ocid == True

    @pytestrail.case("25520")
    def test_25520_3(self):
        cpid = prepared_cpid()
        create_fs_response = insert_into_db_create_fs(cpid)
        payload = fs_update_full_own_money
        period = get_period()
        payload["planning"]["budget"]["period"]["startDate"] = period[0]
        payload["planning"]["budget"]["period"]["endDate"] = period[1]
        update_fs_response = bpe_update_fs(cpid, create_fs_response[2], payload, f"{create_fs_response[1]}")
        time.sleep(2)
        url_update = update_fs_response[1]["data"]["url"]
        publicPoint_update = requests.get(url=url_update).json()
        assert publicPoint_update["releases"][0]["planning"]["budget"]["period"]["startDate"] == \
               payload["planning"]["budget"]["period"]["startDate"]
        assert publicPoint_update["releases"][0]["planning"]["budget"]["period"]["endDate"] == \
               payload["planning"]["budget"]["period"]["endDate"]
