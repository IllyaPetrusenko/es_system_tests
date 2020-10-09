import copy
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

    # @pytestrail.case('23891')
    # def test_23891_1(self):
    #     def update(payload):
    #         access_token = get_access_token_for_platform_one()
    #         x_operation_id = get_x_operation_id(access_token)
    #         ei = copy.deepcopy(ei_full)
    #         create_ei_response = bpe_create_ei(ei)
    #         request_to_create_ei = requests.post(
    #             url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
    #             headers={
    #                 'Authorization': 'Bearer ' + access_token,
    #                 'X-OPERATION-ID': x_operation_id,
    #                 'X-TOKEN': str(uuid4()),
    #                 'Content-Type': 'application/json'},
    #             json=payload)
    #         time.sleep(1)
    #         message_from_kafka = get_message_from_kafka(x_operation_id)
    #         return request_to_create_ei, message_from_kafka, x_operation_id
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     update_ei_response = update(ei_update)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('23891')
    # def test_23891_2(self):
    #     def update(payload):
    #         access_token = get_access_token_for_platform_one()
    #         x_operation_id = get_x_operation_id(access_token)
    #         ei = copy.deepcopy(ei_full)
    #         create_ei_response = bpe_create_ei(ei)
    #         request_to_create_ei = requests.post(
    #             url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
    #             headers={
    #                 'Authorization': 'Bearer ' + access_token,
    #                 'X-OPERATION-ID': x_operation_id,
    #                 'X-TOKEN': str(uuid4()),
    #                 'Content-Type': 'application/json'},
    #             json=payload)
    #         time.sleep(1)
    #         message_from_kafka = get_message_from_kafka(x_operation_id)
    #         return request_to_create_ei, message_from_kafka, x_operation_id
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     update_ei_response = update(ei_update)
    #
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.10.00.04'
    #     assert update_ei_response[1]['errors'][0]['description'] == 'Invalid token.'

    # @pytestrail.case('23892')
    # def test_23892_1(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['id'] = '99900000-8'
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     print(update_ei_response)
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]

    @pytestrail.case('23892')
    def test_23892_2(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['tender']['title'] = 'HALLO moe '
        ei_update = copy.deepcopy(ei_update_full)

        ei_update['tender']['title'] = 'MOI DANNIE'
        # ei_update['tender']['classification']['id'] = '99900000-8'

        update_ei_response = bpe_update_ei(ei_update, ei_create)

        print(ei_update['tender']['classification']['id'])
        print(update_ei_response)
        # assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
        # assert update_ei_response[1]['errors'][0]['code'] == '400.20.00.06'
        # assert update_ei_response[1]['errors'][0]['description'] == 'Cpv code not found. '

    # @pytestrail.case('23893')
    # def test_23893_1(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_full)
    #     ei_update['tender']['classification']['id'] = random.choice(copy.deepcopy(cpv_services))
    #     update_ei_response = bpe_update_ei(ei_update)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('23893')
    # def test_23893_2(self):
    #     ei = copy.deepcopy(ei_full)
    #     ei['tender']['classification']['id'] = random.choice(copy.deepcopy(cpv_services))
    #     update_ei_response = bpe_update_ei(ei)
    #
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('23893')
    # def test_23893_3(self):
    #     ei = copy.deepcopy(ei_full)
    #     ei['tender']['classification']['id'] = random.choice(copy.deepcopy(cpv_services))
    #     update_ei_response = bpe_update_ei(ei)
    #
    #     url = update_ei_response[1]['data']['url']
    #     publicPoint = requests.get(url=url).json()
    #     print(ei['tender']['classification']['id'])
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert publicPoint['releases'][0]['tender']['mainProcurementCategory'] == 'services'
