import copy
import fnmatch
import json
import random
from pytest_testrail.plugin import pytestrail
from tests.bpe_update_ei.update_ei import bpe_update_ei
from tests.bpe_update_ei.payloads import ei_update_full
import requests, time
from config import host, create_ei, update_ei
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.kafka_messages import get_message_from_kafka
from tests.bpe_create_ei.payloads import ei_full
from tests.bpe_create_ei.create_ei import bpe_create_ei
from uuid import uuid4
from tests.bpe_update_ei.payloads import cpv_goods, cpv_works, cpv_services


class TestBpeCreateEI(object):

    @pytestrail.case('23890')
    def test_23890_1(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['tender']['title'] = 'HALLO moe '
        ei_update = copy.deepcopy(ei_update_full)
        ei_update['tender']['title'] = 'MOI DANNIE'
        update_ei_response = bpe_update_ei(ei_update, ei_create)

        assert update_ei_response[0].text == 'ok'
        assert update_ei_response[0].status_code == 202
        assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]


    @pytestrail.case('23890')
    def test_23890_2(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['tender']['title'] = 'HALLO moe '
        ei_update = copy.deepcopy(ei_update_full)
        ei_update['tender']['title'] = 'MOI DANNIE'
        update_ei_response = bpe_update_ei(ei_update, ei_create)
        ocid = fnmatch.fnmatch(update_ei_response[1]['data']['ocid'], '*')

        assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
        assert ocid == True

    @pytestrail.case('23890')
    def test_23890_3(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['tender']['title'] = 'HALLO moe '
        ei_update = copy.deepcopy(ei_update_full)
        ei_update['tender']['title'] = 'MOI DANNIE'
        update_ei_response = bpe_update_ei(ei_update, ei_create)
        publicPoint = requests.get(url=update_ei_response[1]['data']['url']).json()
        print(update_ei_response[1]['data']['operationDate'])
        assert publicPoint['releases'][0]['date'] == update_ei_response[1]['data']['operationDate']

    @pytestrail.case('23891')
    def test_23891_1(self):
        ei_create = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei_create)
        ei_update = copy.deepcopy(ei_update_full)
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        time.sleep(2)
        request_to_update_ei = requests.post(
            url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': str(uuid4()),
                'Content-Type': 'application/json'},
            json=ei_update)

        assert request_to_update_ei.text == 'ok'
        assert request_to_update_ei.status_code == 202

    @pytestrail.case('23891')
    def test_23891_2(self):
        ei_create = copy.deepcopy(ei_full)
        create_ei_response = bpe_create_ei(ei_create)
        ei_update = copy.deepcopy(ei_update_full)
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        time.sleep(2)
        requests.post(
            url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': str(uuid4()),
                'Content-Type': 'application/json'},
            json=ei_update)
        time.sleep(1)
        message_from_kafka = get_message_from_kafka(x_operation_id)

        assert message_from_kafka['errors'][0]['code'] == '400.10.00.04'
        assert message_from_kafka['errors'][0]['description'] == 'Invalid token.'

    @pytestrail.case('23892')
    def test_23892_1(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['tender']['classification']['id'] = '45200000-9'
        create_ei_response = bpe_create_ei(ei_create)

        ei_update = copy.deepcopy(ei_update_full)
        ei_update['tender']['classification']['id'] = '03100000-2'
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        time.sleep(2)
        update_ei_response=requests.post(
            url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                'Content-Type': 'application/json'},
            json=ei_update)

        assert update_ei_response.text == 'ok'
        assert update_ei_response.status_code == 202

    @pytestrail.case('23892')
    def test_23892_2(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['tender']['classification']['id'] = '45200000-9'
        create_ei_response = bpe_create_ei(ei_create)

        ei_update = copy.deepcopy(ei_update_full)
        ei_update['tender']['classification']['id'] = '03100000-2'
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        time.sleep(2)
        requests.post(
            url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                'Content-Type': 'application/json'},
            json=ei_update)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
        ocid = fnmatch.fnmatch(message_from_kafka['data']['ocid'], '*')

        assert message_from_kafka['X-OPERATION-ID'] == x_operation_id
        assert ocid == True

    @pytestrail.case('23892')
    def test_23892_3(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['tender']['classification']['id'] = '45200000-9'
        create_ei_response = bpe_create_ei(ei_create)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint_create_ei = requests.get(url=url).json()

        ei_update = copy.deepcopy(ei_update_full)
        ei_update['tender']['classification']['id'] = '03100000-2'
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        time.sleep(2)
        requests.post(
            url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                'Content-Type': 'application/json'},
            json=ei_update)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
        publicPoint_update_ei = requests.get(url=message_from_kafka['data']['url']).json()

        assert publicPoint_create_ei['releases'][0]['tender']['classification']['id'] == \
               publicPoint_update_ei['releases'][0]['tender']['classification']['id']

    @pytestrail.case('23893')
    def test_23893_1(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['tender']['classification']['id'] = '45200000-9'
        create_ei_response = bpe_create_ei(ei_create)

        ei_update = copy.deepcopy(ei_update_full)
        ei_update['tender']['classification']['id'] = '03100000-2'
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        time.sleep(2)
        update_ei_response = requests.post(
            url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                'Content-Type': 'application/json'},
            json=ei_update)

        assert update_ei_response.text == 'ok'
        assert update_ei_response.status_code == 202

    @pytestrail.case('23893')
    def test_23893_2(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['tender']['classification']['id'] = '45200000-9'
        create_ei_response = bpe_create_ei(ei_create)

        ei_update = copy.deepcopy(ei_update_full)
        ei_update['tender']['classification']['id'] = '03100000-2'
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        time.sleep(2)
        requests.post(
            url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                'Content-Type': 'application/json'},
            json=ei_update)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
        ocid = fnmatch.fnmatch(message_from_kafka['data']['ocid'], '*')

        assert message_from_kafka['X-OPERATION-ID'] == x_operation_id
        assert ocid == True

    @pytestrail.case('23893')
    def test_23893_3(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['tender']['classification']['id'] = '45200000-9'
        create_ei_response = bpe_create_ei(ei_create)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint_create_ei = requests.get(url=url).json()

        ei_update = copy.deepcopy(ei_update_full)
        ei_update['tender']['classification']['id'] = '03100000-2'
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        time.sleep(2)
        requests.post(
            url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                'Content-Type': 'application/json'},
            json=ei_update)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
        publicPoint_update_ei = requests.get(url=message_from_kafka['data']['url']).json()

        assert publicPoint_create_ei['releases'][0]['tender']['mainProcurementCategory'] == \
               publicPoint_update_ei['releases'][0]['tender']['mainProcurementCategory']

    # In progress:

    @pytestrail.case('23897')
    def test_23897_1(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['buyer'] = {
            "name": "name for create EI",
            "identifier": {
                "id": "1",
                "scheme": "MD-IDNO",
                "legalName": "legalName for create EI"
            },
            "address": {
                "streetAddress": "fake_address",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "1700000"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "1701000",
                        "description": "mun.Chişinău"
                    }
                }

            },
            "contactPoint": {
                "name": "Petro Petrovich",
                "email": "petrovich_test@petro.md",
                "telephone": "0994445566"
            }
        }
        create_ei_response = bpe_create_ei(ei_create)

        ei_update = copy.deepcopy(ei_update_full)
        ei_update['buyer'] = {
            "name": "name for update EI",
            "identifier": {
                "id": "2",
                "scheme": "MD-IDNO",
                "legalName": "legalName for update EI"
            },
            "address": {
                "streetAddress": "update",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "0101000"
                    },
                    "locality": {
                        "scheme": "other",
                        "id": "0101000",
                        "description": "KOZYATIN2"
                    }
                }

            },
            "contactPoint": {
                "name": "Mykola Mykolaevich",
                "email": "Mykolaevich_test@mykola.md",
                "telephone": "088111111"
            }
        }
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        time.sleep(2)
        update_ei_response = requests.post(
            url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                'Content-Type': 'application/json'},
            json=ei_update)

        assert update_ei_response.text == 'ok'
        assert update_ei_response.status_code == 202

    @pytestrail.case('23897')
    def test_23897_2(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['buyer'] = {
            "name": "name for create EI",
            "identifier": {
                "id": "1",
                "scheme": "MD-IDNO",
                "legalName": "legalName for create EI"
            },
            "address": {
                "streetAddress": "fake_address",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "1700000"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "1701000",
                        "description": "mun.Chişinău"
                    }
                }

            },
            "contactPoint": {
                "name": "Petro Petrovich",
                "email": "petrovich_test@petro.md",
                "telephone": "0994445566"
            }
        }
        create_ei_response = bpe_create_ei(ei_create)

        ei_update = copy.deepcopy(ei_update_full)
        ei_update['buyer'] = {
            "name": "name for update EI",
            "identifier": {
                "id": "2",
                "scheme": "MD-IDNO",
                "legalName": "legalName for update EI"
            },
            "address": {
                "streetAddress": "update",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "0101000"
                    },
                    "locality": {
                        "scheme": "other",
                        "id": "0101000",
                        "description": "KOZYATIN2"
                    }
                }

            },
            "contactPoint": {
                "name": "Mykola Mykolaevich",
                "email": "Mykolaevich_test@mykola.md",
                "telephone": "088111111"
            }
        }
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)


        requests.post(
            url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
                'Content-Type': 'application/json'},
            json=ei_update)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
        print(type(ei_update))

        # ocid = fnmatch.fnmatch(message_from_kafka['data']['ocid'], '*')
        # print(json.dumps(message_from_kafka))
        # assert message_from_kafka['X-OPERATION-ID'] == x_operation_id
        # assert ocid == True
