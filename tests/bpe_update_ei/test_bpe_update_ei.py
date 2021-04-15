import copy
import json
import time
from uuid import uuid4

import allure
import requests
from pytest_testrail.plugin import pytestrail

from tests.Cassandra_session import execute_cql_from_orchestrator_operation_step
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.essences.ei import EI
from tests.kafka_messages import get_message_from_kafka
from tests.payloads.ei_payload import payload_ei_full_data_model, payload_ei_obligatory_data_model
from tests.presets import set_instance_for_request, update_ei
from useful_functions import compare_actual_result_and_expected_result, request_update_ei, \
    get_access_token_for_platform_two


class TestCheckOnPossibilityUpdateEiWithObligatoryFieldsInPayloadWithoutTenderItems(object):
    @pytestrail.case("23890")
    def test_send_the_request_23890_1(self, country, language):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        del payload["tender"]["items"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.insert_ei_full_data_model()
        update_ei_response = ei.update_ei()
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23890")
    def test_see_the_result_in_feed_point_23890_2(self, country, language):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        del payload["tender"]["items"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.insert_ei_full_data_model()
        ei.update_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull_update_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckOnPossibilityUpdateEiWithObligatoryFieldsInPayloadWithTenderItems(object):
    @pytestrail.case("24441")
    def test_send_the_request_24441_1(self, country, language):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.insert_ei_full_data_model()
        update_ei_response = ei.update_ei()
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24441")
    def test_see_the_result_in_feed_point_24441_2(self, country, language):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.insert_ei_full_data_model()
        ei.update_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull_update_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckOnPossibilityUpdateEiWithFullDataInPayload(object):
    @pytestrail.case("24442")
    def test_send_the_request_24442_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.insert_ei_obligatory_data_model()
        update_ei_response = ei.update_ei()
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24442")
    def test_see_the_result_in_feed_point_24442_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.insert_ei_obligatory_data_model()
        ei.update_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull_update_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckOnImpossibilityUpdateEiIfTokenFromRequestNotEqualTokenFromDB(object):
    @pytestrail.case("24443")
    def test_send_the_request_24443_1(self, country, language):
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        insert_ei = ei.insert_ei_full_data_model()
        update_ei_response = request_update_ei(access_token=access_token, x_operation_id=x_operation_id,
                                               cpid=insert_ei[2], ei_token=f"{uuid4()}", payload=payload)
        expected_result = str(202)
        actual_result = str(update_ei_response.status_code)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24443")
    def test_see_the_result_in_feed_point_24443_2(self, country, language):
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        insert_ei = ei.insert_ei_full_data_model()
        request_update_ei(access_token=access_token, x_operation_id=x_operation_id,
                                               cpid=insert_ei[2], ei_token=f"{uuid4()}", payload=payload)
        time.sleep(1.8)
        message_from_kafka = get_message_from_kafka(x_operation_id)
        expected_result = str([{"code": "400.10.00.04", "description": "Invalid token."}])
        actual_result = str(message_from_kafka["errors"])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    class TestCheckOnImpossibilityUpdateEiIfOwnerFromRequestNotEqualOwnerFromDB(object):
        @pytestrail.case("24444")
        def test_send_the_request_24444_1(self, country, language):
            access_token = get_access_token_for_platform_two()
            x_operation_id = get_x_operation_id(access_token)
            payload = copy.deepcopy(payload_ei_obligatory_data_model)
            ei = EI(payload=payload, lang=language, country=country)
            insert_ei = ei.insert_ei_full_data_model()
            update_ei_response = request_update_ei(access_token=access_token, x_operation_id=x_operation_id,
                                                   cpid=insert_ei[2], ei_token=f"{insert_ei[1]}", payload=payload)
            expected_result = str(202)
            actual_result = str(update_ei_response.status_code)
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24444")
        def test_see_the_result_in_feed_point_24444_2(self, country, language):
            access_token = get_access_token_for_platform_two()
            x_operation_id = get_x_operation_id(access_token)
            payload = copy.deepcopy(payload_ei_obligatory_data_model)
            ei = EI(payload=payload, lang=language, country=country)
            insert_ei = ei.insert_ei_full_data_model()
            request_update_ei(access_token=access_token, x_operation_id=x_operation_id,
                              cpid=insert_ei[2], ei_token=f"{insert_ei[1]}", payload=payload)
            print(insert_ei[2])

            error_from_DB = execute_cql_from_orchestrator_operation_step(insert_ei[2], 'BudgetUpdateEiTask')
            expected_result = str([{"code": "400.10.00.03", "description": "Invalid owner."}])
            actual_result = str(error_from_DB)
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)
    #
    # @pytestrail.case('24445')
    # def test_24445_1(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['classification']['id'] = '50100000-6'
    #     ei_create['tender']['items'][0]['classification']['id'] = '50100000-6'
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['id'] = '90900000-6'
    #
    #     ei_update['tender']['items'] = [{
    #         "id": "1",
    #         "description": "item 1",
    #         "classification": {
    #             "id": "19700000-3"
    #         },
    #         "additionalClassifications": [
    #             {
    #                 "id": "AA12-4"
    #             }
    #         ],
    #         "deliveryAddress": {
    #             "streetAddress": "хрещатик",
    #             "postalCode": "02235",
    #             "addressDetails": {
    #                 "country": {
    #                     "id": "MD",
    #                     "description": "ОПИСАНИЕ",
    #                     "scheme": "other"
    #                 },
    #                 "region": {
    #                     "id": "1700000",
    #                     "description": "ОПИСАНИЕ",
    #                     "scheme": "CUATM"
    #                 },
    #                 "locality": {
    #                     "id": "1701000",
    #                     "description": "ОПИСАНИЕ2",
    #                     "scheme": "other"
    #                 }
    #
    #             }
    #         },
    #         "quantity": 1,
    #         "unit": {
    #             "id": "10",
    #             "name": "name"
    #         }
    #     },
    #         {
    #             "id": "2",
    #             "description": "item 2",
    #             "classification": {
    #                 "id": "50100000-6"
    #             },
    #             "additionalClassifications": [
    #                 {
    #                     "id": "AA12-4"
    #                 }
    #             ],
    #             "deliveryAddress": {
    #                 "streetAddress": "хрещатик",
    #                 "postalCode": "02235",
    #                 "addressDetails": {
    #                     "country": {
    #                         "id": "MD",
    #                         "description": "ОПИСАНИЕ",
    #                         "scheme": "other"
    #                     },
    #                     "region": {
    #                         "id": "1700000",
    #                         "description": "ОПИСАНИЕ",
    #                         "scheme": "CUATM"
    #                     },
    #                     "locality": {
    #                         "id": "1701000",
    #                         "description": "ОПИСАНИЕ2",
    #                         "scheme": "other"
    #                     }
    #
    #                 }
    #             },
    #             "quantity": 1,
    #             "unit": {
    #                 "id": "10",
    #                 "name": "name"
    #             }
    #         }
    #     ]
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('24445')
    # def test_24445_2(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['classification']['id'] = '50100000-6'
    #     ei_create['tender']['items'][0]['classification']['id'] = '50100000-6'
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['id'] = '90900000-6'
    #
    #     ei_update['tender']['items'] = [{
    #         "id": "1",
    #         "description": "item 1",
    #         "classification": {
    #             "id": "19700000-3"
    #         },
    #         "additionalClassifications": [
    #             {
    #                 "id": "AA12-4"
    #             }
    #         ],
    #         "deliveryAddress": {
    #             "streetAddress": "хрещатик",
    #             "postalCode": "02235",
    #             "addressDetails": {
    #                 "country": {
    #                     "id": "MD",
    #                     "description": "ОПИСАНИЕ",
    #                     "scheme": "other"
    #                 },
    #                 "region": {
    #                     "id": "1700000",
    #                     "description": "ОПИСАНИЕ",
    #                     "scheme": "CUATM"
    #                 },
    #                 "locality": {
    #                     "id": "1701000",
    #                     "description": "ОПИСАНИЕ2",
    #                     "scheme": "other"
    #                 }
    #
    #             }
    #         },
    #         "quantity": 1,
    #         "unit": {
    #             "id": "10",
    #             "name": "name"
    #         }
    #     },
    #         {
    #             "id": "2",
    #             "description": "item 2",
    #             "classification": {
    #                 "id": "50100000-6"
    #             },
    #             "additionalClassifications": [
    #                 {
    #                     "id": "AA12-4"
    #                 }
    #             ],
    #             "deliveryAddress": {
    #                 "streetAddress": "хрещатик",
    #                 "postalCode": "02235",
    #                 "addressDetails": {
    #                     "country": {
    #                         "id": "MD",
    #                         "description": "ОПИСАНИЕ",
    #                         "scheme": "other"
    #                     },
    #                     "region": {
    #                         "id": "1700000",
    #                         "description": "ОПИСАНИЕ",
    #                         "scheme": "CUATM"
    #                     },
    #                     "locality": {
    #                         "id": "1701000",
    #                         "description": "ОПИСАНИЕ2",
    #                         "scheme": "other"
    #                     }
    #
    #                 }
    #             },
    #             "quantity": 1,
    #             "unit": {
    #                 "id": "10",
    #                 "name": "name"
    #             }
    #         }
    #     ]
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.10.20.12'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == f"Invalid CPV.Invalid CPV code in classification(s) " \
    #                                  f"'{ei_update['tender']['items'][0]['classification']['id']}'"
    #
    # @pytestrail.case('24446')
    # def test_24446_1(self):
    #     ei_create = copy.deepcopy(ei_obligatory)
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['items'][0]['quantity'] = 0
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('24446')
    # def test_24446_2(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_full)
    #     del ei_update['tender']['items'][0]['additionalClassifications']
    #     ei_update['tender']['items'][0]['quantity'] = 0
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.10.20.09'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == "Invalid item quantity.Quantity of item '1' must be greater than zero"
    #
    # @pytestrail.case('24447')
    # def test_24447_1(self):
    #     ei_create = copy.deepcopy(ei_obligatory)
    #     ei_create['tender']['classification']['id'] = '45100000-8'
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['id'] = '45100000-8'
    #     ei_update['tender']['items'] = [{
    #         "id": "1",
    #         "description": "item 1",
    #         "classification": {
    #             "id": "45112350-3"
    #         },
    #         "deliveryAddress": {
    #             "streetAddress": "хрещатик",
    #             "postalCode": "02235",
    #             "addressDetails": {
    #                 "country": {
    #                     "id": "MD",
    #                     "description": "ОПИСАНИЕ",
    #                     "scheme": "other"
    #                 },
    #                 "region": {
    #                     "id": "1700000",
    #                     "description": "ОПИСАНИЕ",
    #                     "scheme": "CUATM"
    #                 },
    #                 "locality": {
    #                     "id": "1701000",
    #                     "description": "ОПИСАНИЕ2",
    #                     "scheme": "other"
    #                 }
    #
    #             }
    #         },
    #         "quantity": 1,
    #         "unit": {
    #             "id": "10",
    #             "name": "name"
    #         }
    #     },
    #         {
    #             "id": "1",
    #             "description": "item 2",
    #             "classification": {
    #                 "id": "45112360-6"
    #             },
    #
    #             "deliveryAddress": {
    #                 "streetAddress": "хрещатик",
    #                 "postalCode": "02235",
    #                 "addressDetails": {
    #                     "country": {
    #                         "id": "MD",
    #                         "description": "ОПИСАНИЕ",
    #                         "scheme": "other"
    #                     },
    #                     "region": {
    #                         "id": "1700000",
    #                         "description": "ОПИСАНИЕ",
    #                         "scheme": "CUATM"
    #                     },
    #                     "locality": {
    #                         "id": "1701000",
    #                         "description": "ОПИСАНИЕ2",
    #                         "scheme": "other"
    #                     }
    #
    #                 }
    #             },
    #             "quantity": 1,
    #             "unit": {
    #                 "id": "10",
    #                 "name": "name"
    #             }
    #         }
    #     ]
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('24447')
    # def test_24447_2(self):
    #     ei_create = copy.deepcopy(ei_obligatory)
    #     ei_create['tender']['classification']['id'] = '45100000-8'
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['id'] = '45100000-8'
    #     ei_update['tender']['items'] = [{
    #         "id": "1",
    #         "description": "item 1",
    #         "classification": {
    #             "id": "45112350-3"
    #         },
    #         "deliveryAddress": {
    #             "streetAddress": "хрещатик",
    #             "postalCode": "02235",
    #             "addressDetails": {
    #                 "country": {
    #                     "id": "MD",
    #                     "description": "ОПИСАНИЕ",
    #                     "scheme": "other"
    #                 },
    #                 "region": {
    #                     "id": "1700000",
    #                     "description": "ОПИСАНИЕ",
    #                     "scheme": "CUATM"
    #                 },
    #                 "locality": {
    #                     "id": "1701000",
    #                     "description": "ОПИСАНИЕ2",
    #                     "scheme": "other"
    #                 }
    #
    #             }
    #         },
    #         "quantity": 1,
    #         "unit": {
    #             "id": "10",
    #             "name": "name"
    #         }
    #     },
    #         {
    #             "id": "1",
    #             "description": "item 2",
    #             "classification": {
    #                 "id": "45112360-6"
    #             },
    #
    #             "deliveryAddress": {
    #                 "streetAddress": "хрещатик",
    #                 "postalCode": "02235",
    #                 "addressDetails": {
    #                     "country": {
    #                         "id": "MD",
    #                         "description": "ОПИСАНИЕ",
    #                         "scheme": "other"
    #                     },
    #                     "region": {
    #                         "id": "1700000",
    #                         "description": "ОПИСАНИЕ",
    #                         "scheme": "CUATM"
    #                     },
    #                     "locality": {
    #                         "id": "1701000",
    #                         "description": "ОПИСАНИЕ2",
    #                         "scheme": "other"
    #                     }
    #
    #                 }
    #             },
    #             "quantity": 1,
    #             "unit": {
    #                 "id": "10",
    #                 "name": "name"
    #             }
    #         }
    #     ]
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.10.20.10'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == "Duplicated items found.Item '1' has a duplicate"
    #
    # @pytestrail.case('24449')
    # def test_24449_1(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['classification']['scheme'] = 'CPV'
    #     ei_create['tender']['classification']['id'] = '50100000-6'
    #     ei_create['tender']['classification']['description'] = 'Timbre'
    #     ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
    #     ei_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
    #     ei_create['buyer']['name'] = 'Directia Cultura a Primariei mun.Chisinau'
    #     ei_create['buyer']['identifier']['id'] = '1007601010585'
    #     ei_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
    #     ei_create['buyer']['identifier']['legalName'] = 'Directia Cultura'
    #     ei_create['buyer']['identifier']['uri'] = 'www'
    #     ei_create['buyer']['address']['streetAddress'] = 'str.Bucuresti 68'
    #     ei_create['buyer']['address']['addressDetails']['country']['id'] = 'MD'
    #     ei_create['buyer']['address']['addressDetails']['region']['id'] = '0101000'
    #     ei_create['buyer']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
    #     ei_create['buyer']['address']['addressDetails']['locality']['id'] = '0101000'
    #     ei_create['buyer']['address']['addressDetails']['locality']['description'] = 'mun.Chişinău'
    #     ei_create['buyer']['contactPoint']['name'] = 'Dumitru Popa'
    #     ei_create['buyer']['contactPoint']['email'] = 'directiacultшra@yahoo.com'
    #     ei_create['buyer']['contactPoint']['telephone'] = '022242290'
    #     ei_create['buyer']['contactPoint']['faxNumber'] = '123'
    #     ei_create['buyer']['contactPoint']['url'] = 'www url'
    #     ei_create['buyer']['address']['postalCode'] = '147'
    #     del ei_create['tender']['items']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['scheme'] = 'ZVS'
    #     ei_update['tender']['classification']['id'] = '45100000-8'
    #     ei_update['tender']['classification']['description'] = 'Dada'
    #     ei_update['planning']['budget']['period']['startDate'] = '2021-01-01T00:00:00Z '
    #     ei_update['planning']['budget']['period']['endDate'] = '2021-12-31T00:00:00Z'
    #     ei_update['buyer']['name'] = ' zama'
    #     ei_update['buyer']['identifier']['id'] = '380632074071 '
    #     ei_update['buyer']['identifier']['scheme'] = 'MD-IDNO'
    #     ei_update['buyer']['identifier']['legalName'] = 'zao'
    #     ei_update['buyer']['identifier']['uri'] = 'fop'
    #     ei_update['buyer']['address']['streetAddress'] = 'Romashkova'
    #     ei_update['buyer']['address']['addressDetails']['country']['id'] = 'MD'
    #     ei_update['buyer']['address']['addressDetails']['region']['id'] = '1700000'
    #     ei_update['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
    #     ei_update['buyer']['address']['addressDetails']['locality']['id'] = '1701000'
    #     ei_update['buyer']['address']['addressDetails']['locality']['description'] = 'mun.Chişinău789'
    #     ei_update['buyer']['contactPoint']['name'] = 'Petro'
    #     ei_update['buyer']['contactPoint']['email'] = 'petro@lpo '
    #     ei_update['buyer']['contactPoint']['telephone'] = '0574256'
    #     ei_update['buyer']['contactPoint']['faxNumber'] = '456'
    #     ei_update['buyer']['contactPoint']['url'] = 'www url4444 '
    #     ei_update['buyer']['address']['postalCode'] = '87'
    #     del ei_update['tender']['items']
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('24449')
    # def test_24449_2(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['classification']['scheme'] = 'CPV'
    #     ei_create['tender']['classification']['id'] = '50100000-6'
    #     ei_create['tender']['classification']['description'] = 'Timbre'
    #     ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
    #     ei_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
    #     ei_create['buyer']['name'] = 'Directia Cultura a Primariei mun.Chisinau'
    #     ei_create['buyer']['identifier']['id'] = '1007601010585'
    #     ei_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
    #     ei_create['buyer']['identifier']['legalName'] = 'Directia Cultura'
    #     ei_create['buyer']['identifier']['uri'] = 'www'
    #     ei_create['buyer']['address']['streetAddress'] = 'str.Bucuresti 68'
    #     ei_create['buyer']['address']['addressDetails']['country']['id'] = 'MD'
    #     ei_create['buyer']['address']['addressDetails']['region']['id'] = '0101000'
    #     ei_create['buyer']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
    #     ei_create['buyer']['address']['addressDetails']['locality']['id'] = '0101000'
    #     ei_create['buyer']['address']['addressDetails']['locality']['description'] = 'mun.Chişinău'
    #     ei_create['buyer']['contactPoint']['name'] = 'Dumitru Popa'
    #     ei_create['buyer']['contactPoint']['email'] = 'directiacultшra@yahoo.com'
    #     ei_create['buyer']['contactPoint']['telephone'] = '022242290'
    #     ei_create['buyer']['contactPoint']['faxNumber'] = '123'
    #     ei_create['buyer']['contactPoint']['url'] = 'www url'
    #     ei_create['buyer']['address']['postalCode'] = '147'
    #     del ei_create['tender']['items']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['scheme'] = 'ZVS'
    #     ei_update['tender']['classification']['id'] = '45100000-8'
    #     ei_update['tender']['classification']['description'] = 'Dada'
    #     ei_update['planning']['budget']['period']['startDate'] = '2021-01-01T00:00:00Z '
    #     ei_update['planning']['budget']['period']['endDate'] = '2021-12-31T00:00:00Z'
    #     ei_update['buyer']['name'] = ' zama'
    #     ei_update['buyer']['identifier']['id'] = '380632074071 '
    #     ei_update['buyer']['identifier']['scheme'] = 'MD-IDNO'
    #     ei_update['buyer']['identifier']['legalName'] = 'zao'
    #     ei_update['buyer']['identifier']['uri'] = 'fop'
    #     ei_update['buyer']['address']['streetAddress'] = 'Romashkova'
    #     ei_update['buyer']['address']['addressDetails']['country']['id'] = 'MD'
    #     ei_update['buyer']['address']['addressDetails']['region']['id'] = '1700000'
    #     ei_update['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
    #     ei_update['buyer']['address']['addressDetails']['locality']['id'] = '1701000'
    #     ei_update['buyer']['address']['addressDetails']['locality']['description'] = 'mun.Chişinău789'
    #     ei_update['buyer']['contactPoint']['name'] = 'Petro'
    #     ei_update['buyer']['contactPoint']['email'] = 'petro@lpo '
    #     ei_update['buyer']['contactPoint']['telephone'] = '0574256'
    #     ei_update['buyer']['contactPoint']['faxNumber'] = '456'
    #     ei_update['buyer']['contactPoint']['url'] = 'www url4444 '
    #     ei_update['buyer']['address']['postalCode'] = '87'
    #     del ei_update['tender']['items']
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     ocid = fnmatch.fnmatch(update_ei_response[1]['data']['ocid'], '*')
    #
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert ocid == True
    #
    # @pytestrail.case('24449')
    # def test_24449_3(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['classification']['scheme'] = 'CPV'
    #     ei_create['tender']['classification']['id'] = '50100000-6'
    #     ei_create['tender']['classification']['description'] = 'Timbre'
    #     ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
    #     ei_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
    #     ei_create['buyer']['name'] = 'Directia Cultura a Primariei mun.Chisinau'
    #     ei_create['buyer']['identifier']['id'] = '1007601010585'
    #     ei_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
    #     ei_create['buyer']['identifier']['legalName'] = 'Directia Cultura'
    #     ei_create['buyer']['identifier']['uri'] = 'www'
    #     ei_create['buyer']['address']['streetAddress'] = 'str.Bucuresti 68'
    #     ei_create['buyer']['address']['addressDetails']['country']['id'] = 'MD'
    #     ei_create['buyer']['address']['addressDetails']['region']['id'] = '0101000'
    #     ei_create['buyer']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
    #     ei_create['buyer']['address']['addressDetails']['locality']['id'] = '0101000'
    #     ei_create['buyer']['address']['addressDetails']['locality']['description'] = 'mun.Chişinău'
    #     ei_create['buyer']['contactPoint']['name'] = 'Dumitru Popa'
    #     ei_create['buyer']['contactPoint']['email'] = 'directiacultшra@yahoo.com'
    #     ei_create['buyer']['contactPoint']['telephone'] = '022242290'
    #     ei_create['buyer']['contactPoint']['faxNumber'] = '123'
    #     ei_create['buyer']['contactPoint']['url'] = 'www url'
    #     ei_create['buyer']['address']['postalCode'] = '147'
    #     del ei_create['tender']['items']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['scheme'] = 'ZVS'
    #     ei_update['tender']['classification']['id'] = '45100000-8'
    #     ei_update['tender']['classification']['description'] = 'Dada'
    #     ei_update['planning']['budget']['period']['startDate'] = '2021-01-01T00:00:00Z '
    #     ei_update['planning']['budget']['period']['endDate'] = '2021-12-31T00:00:00Z'
    #     ei_update['buyer']['name'] = ' zama'
    #     ei_update['buyer']['identifier']['id'] = '380632074071 '
    #     ei_update['buyer']['identifier']['scheme'] = 'MD-IDNO'
    #     ei_update['buyer']['identifier']['legalName'] = 'zao'
    #     ei_update['buyer']['identifier']['uri'] = 'fop'
    #     ei_update['buyer']['address']['streetAddress'] = 'Romashkova'
    #     ei_update['buyer']['address']['addressDetails']['country']['id'] = 'MD'
    #     ei_update['buyer']['address']['addressDetails']['region']['id'] = '1700000'
    #     ei_update['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
    #     ei_update['buyer']['address']['addressDetails']['locality']['id'] = '1701000'
    #     ei_update['buyer']['address']['addressDetails']['locality']['description'] = 'mun.Chişinău789'
    #     ei_update['buyer']['contactPoint']['name'] = 'Petro'
    #     ei_update['buyer']['contactPoint']['email'] = 'petro@lpo '
    #     ei_update['buyer']['contactPoint']['telephone'] = '0574256'
    #     ei_update['buyer']['contactPoint']['faxNumber'] = '456'
    #     ei_update['buyer']['contactPoint']['url'] = 'www url4444 '
    #     ei_update['buyer']['address']['postalCode'] = '87'
    #     del ei_update['tender']['items']
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     time.sleep(2)
    #
    #     url_update = update_ei_response[1]['data']['url']
    #
    #     publicPoint_update = requests.get(url=url_update).json()
    #     assert update_ei_response[3]['releases'][0]['tender']['id'] == publicPoint_update['releases'][0]['tender']['id']
    #     assert update_ei_response[3]['releases'][0]['tender']['status'] == publicPoint_update['releases'][0]['tender'][
    #         'status']
    #     assert update_ei_response[3]['releases'][0]['tender']['statusDetails'] == \
    #            publicPoint_update['releases'][0]['tender'][
    #                'statusDetails']
    #     assert update_ei_response[3]['releases'][0]['tender']['classification']['id'] == \
    #            publicPoint_update['releases'][0]['tender']['classification']['id']
    #     assert update_ei_response[3]['releases'][0]['tender']['classification']['scheme'] == \
    #            publicPoint_update['releases'][0]['tender']['classification']['scheme']
    #     assert update_ei_response[3]['releases'][0]['tender']['classification']['description'] == \
    #            publicPoint_update['releases'][0]['tender']['classification']['description']
    #     assert update_ei_response[3]['releases'][0]['tender']['mainProcurementCategory'] == \
    #            publicPoint_update['releases'][0]['tender']['mainProcurementCategory']
    #     assert update_ei_response[3]['releases'][0]['planning']['budget']['id'] == \
    #            publicPoint_update['releases'][0]['planning']['budget']['id']
    #     assert update_ei_response[3]['releases'][0]['planning']['budget']['period']['startDate'] == \
    #            publicPoint_update['releases'][0]['planning']['budget']['period']['startDate']
    #     assert update_ei_response[3]['releases'][0]['planning']['budget']['period']['endDate'] == \
    #            publicPoint_update['releases'][0]['planning']['budget']['period']['endDate']
    #     assert update_ei_response[3]['releases'][0]['buyer']['id'] == publicPoint_update['releases'][0]['buyer']['id']
    #     assert update_ei_response[3]['releases'][0]['buyer']['name'] == publicPoint_update['releases'][0]['buyer'][
    #         'name']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['id'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['id']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['name'] == \
    #            publicPoint_update['releases'][0]['parties'][0][
    #                'name']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['identifier']['scheme'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['identifier']['scheme']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['identifier']['id'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['identifier']['id']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['identifier']['legalName'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['identifier']['legalName']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['identifier']['uri'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['identifier']['uri']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['streetAddress'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['streetAddress']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['country']['scheme'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['country']['scheme']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['country']['id']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['country'][
    #                'description'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['country']['description']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['country']['uri'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['country']['uri']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['region']['scheme'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['region']['scheme']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['region']['id']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['region'][
    #                'description'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['region']['description']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['region']['uri'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['region']['uri']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
    #                'description'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['locality']['description']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['address']['addressDetails']['locality']['uri'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['address']['addressDetails']['locality']['uri']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['contactPoint']['name'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['contactPoint']['name']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['contactPoint']['email'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['contactPoint']['email']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['contactPoint']['telephone'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['contactPoint']['telephone']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['contactPoint']['faxNumber'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['contactPoint']['faxNumber']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['contactPoint']['url'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['contactPoint']['url']
    #     assert update_ei_response[3]['releases'][0]['parties'][0]['roles'] == \
    #            publicPoint_update['releases'][0]['parties'][0]['roles']
    #
    # @pytestrail.case('24450')
    # def test_24450_1(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['description'] = 'kola'
    #     ei_create['tender']['title'] = 'volk'
    #     del ei_create['tender']['items']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['description'] = 'fada'
    #     ei_update['tender']['title'] = 'zayac'
    #     del ei_update['tender']['items']
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('24450')
    # def test_24450_2(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['description'] = 'kola'
    #     ei_create['tender']['title'] = 'volk'
    #     del ei_create['tender']['items']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['description'] = 'fada'
    #     ei_update['tender']['title'] = 'zayac'
    #     del ei_update['tender']['items']
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     ocid = fnmatch.fnmatch(update_ei_response[1]['data']['ocid'], '*')
    #
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert ocid == True
    #
    # @pytestrail.case('24450')
    # def test_24450_3(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['description'] = 'kola'
    #     ei_create['tender']['title'] = 'volk'
    #     del ei_create['tender']['items']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['description'] = 'fada'
    #     ei_update['tender']['title'] = 'zayac'
    #     del ei_update['tender']['items']
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     time.sleep(2)
    #
    #     url_update = update_ei_response[1]['data']['url']
    #
    #     publicPoint_update = requests.get(url=url_update).json()
    #
    #     assert update_ei_response[3]['releases'][0]['tender']['description'] == ei_create['tender']['description']
    #     assert publicPoint_update['releases'][0]['tender']['description'] == ei_update['tender']['description']
    #     description_false = update_ei_response[3]['releases'][0]['tender']['description'] is \
    #                         publicPoint_update['releases'][0]['tender']['description']
    #     assert description_false == False
    #
    #     assert update_ei_response[3]['releases'][0]['tender']['title'] == ei_create['tender']['title']
    #     assert publicPoint_update['releases'][0]['tender']['title'] == ei_update['tender']['title']
    #     title_false = update_ei_response[3]['releases'][0]['tender']['title'] is \
    #                   publicPoint_update['releases'][0]['tender']['title']
    #     assert title_false == False
    #
    # @pytestrail.case('24451')
    # def test_24451_1(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['planning']['rationale'] = 'gf'
    #     del ei_create['tender']['items']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['planning']['rationale'] = 'fada'
    #     del ei_update['tender']['items']
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('24451')
    # def test_24451_2(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['planning']['rationale'] = 'gf'
    #     del ei_create['tender']['items']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['planning']['rationale'] = 'fada'
    #     del ei_update['tender']['items']
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     ocid = fnmatch.fnmatch(update_ei_response[1]['data']['ocid'], '*')
    #
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert ocid == True
    #
    # @pytestrail.case('24451')
    # def test_24451_3(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['planning']['rationale'] = 'gf'
    #     del ei_create['tender']['items']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['planning']['rationale'] = 'fada'
    #     del ei_update['tender']['items']
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     time.sleep(2)
    #
    #     url_update = update_ei_response[1]['data']['url']
    #
    #     publicPoint_update = requests.get(url=url_update).json()
    #
    #     assert update_ei_response[3]['releases'][0]['planning']['rationale'] == ei_create['planning']['rationale']
    #     assert publicPoint_update['releases'][0]['planning']['rationale'] == ei_update['planning']['rationale']
    #     title_false = update_ei_response[3]['releases'][0]['planning']['rationale'] is \
    #                   publicPoint_update['releases'][0]['planning']['rationale']
    #     assert title_false == False
    #
    # @pytestrail.case('24452')
    # def test_24452_1(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['items'][0]['description'] = 'gaga'
    #     ei_create['tender']['items'][0]['classification']['id'] = '45100000-8'
    #     ei_create['tender']['items'][0]['additionalClassifications'][0]['id'] = 'AA12-4'
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['items'][0]['description'] = 'popo'
    #     ei_update['tender']['items'][0]['classification']['id'] = '45112350-3'
    #     ei_update['tender']['items'][0]['additionalClassifications'][0]['id'] = 'AA04-0'
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('24452')
    # def test_24452_2(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['items'][0]['description'] = 'gaga'
    #     ei_create['tender']['items'][0]['classification']['id'] = '45100000-8'
    #     ei_create['tender']['items'][0]['additionalClassifications'][0]['id'] = 'AA12-4'
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['items'][0]['description'] = 'popo'
    #     ei_update['tender']['items'][0]['classification']['id'] = '45112350-3'
    #     ei_update['tender']['items'][0]['additionalClassifications'][0]['id'] = 'AA04-0'
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     ocid = fnmatch.fnmatch(update_ei_response[1]['data']['ocid'], '*')
    #
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert ocid == True
    #
    # @pytestrail.case('24452')
    # def test_24452_3(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['items'][0]['description'] = 'gaga'
    #     ei_create['tender']['items'][0]['classification']['id'] = '45100000-8'
    #     ei_create['tender']['items'][0]['additionalClassifications'][0]['id'] = 'AA12-4'
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['items'][0]['description'] = 'popo'
    #     ei_update['tender']['items'][0]['classification']['id'] = '45112350-3'
    #     ei_update['tender']['items'][0]['additionalClassifications'][0]['id'] = 'AA04-0'
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     time.sleep(2)
    #
    #     url_update = update_ei_response[1]['data']['url']
    #
    #     publicPoint_update = requests.get(url=url_update).json()
    #
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['description'] == \
    #            ei_create['tender']['items'][0]['description']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['description'] == \
    #            ei_update['tender']['items'][0]['description']
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['description'] != \
    #            publicPoint_update['releases'][0]['tender']['items'][0]['description']
    #
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['classification']['id'] == \
    #            ei_create['tender']['items'][0]['classification']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['classification']['id'] == \
    #            ei_update['tender']['items'][0]['classification']['id']
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['classification']['id'] != \
    #            publicPoint_update['releases'][0]['tender']['items'][0]['classification']['id']
    #
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['additionalClassifications'][0]['id'] == \
    #            ei_create['tender']['items'][0]['additionalClassifications'][0]['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['additionalClassifications'][0]['id'] == \
    #            ei_update['tender']['items'][0]['additionalClassifications'][0]['id']
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['additionalClassifications'][0]['id'] != \
    #            publicPoint_update['releases'][0]['tender']['items'][0]['additionalClassifications'][0]['id']
    #
    # @pytestrail.case('24453')
    # def test_24453_1(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['items'][0]['deliveryAddress']['streetAddress'] = 'Khreshchatyk'
    #     ei_create['tender']['items'][0]['deliveryAddress']['postalCode'] = '01124'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = 'description_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = 'scheme_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = 'www.deutch'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['description'] = 'description_2'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = 'scheme'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = 'CUATM'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = 'ww.io.io '
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #         'description'] = 'description_test'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = 'www,regi_16'
    #     ei_create['tender']['items'][0]['quantity'] = 10
    #     ei_create['tender']['items'][0]['unit']['id'] = '10'
    #     ei_create['tender']['items'][0]['unit']['name'] = 'name'
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['items'][0]['deliveryAddress']['streetAddress'] = 'Vladimirskaya'
    #     ei_update['tender']['items'][0]['deliveryAddress']['postalCode'] = '33344'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = 'Re_44'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = 'scheme_1_1'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = 'www.poland'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = '1700000'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #         'description'] = 'description_44_2'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = 'sheme_region_78'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = 'other'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = 'locality_1'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = 'www.vbn.ko'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #         'description'] = 'description_test_22'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = 'www,regi_12'
    #     ei_update['tender']['items'][0]['quantity'] = 256
    #     ei_update['tender']['items'][0]['unit']['id'] = '120'
    #     ei_update['tender']['items'][0]['unit']['name'] = 'name_2'
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('24453')
    # def test_24453_2(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['items'][0]['deliveryAddress']['streetAddress'] = 'Khreshchatyk'
    #     ei_create['tender']['items'][0]['deliveryAddress']['postalCode'] = '01124'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = 'description_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = 'scheme_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = 'www.deutch'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['description'] = 'description_2'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = 'scheme'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = 'CUATM'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = 'ww.io.io '
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #         'description'] = 'description_test'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = 'www,regi_16'
    #     ei_create['tender']['items'][0]['quantity'] = 10
    #     ei_create['tender']['items'][0]['unit']['id'] = '10'
    #     ei_create['tender']['items'][0]['unit']['name'] = 'name'
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['items'][0]['deliveryAddress']['streetAddress'] = 'Vladimirskaya'
    #     ei_update['tender']['items'][0]['deliveryAddress']['postalCode'] = '33344'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = 'Re_44'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = 'scheme_1_1'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = 'www.poland'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = '1700000'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #         'description'] = 'description_44_2'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = 'sheme_region_78'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = 'other'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = 'locality_1'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = 'www.vbn.ko'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #         'description'] = 'description_test_22'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = 'www,regi_12'
    #     ei_update['tender']['items'][0]['quantity'] = 256
    #     ei_update['tender']['items'][0]['unit']['id'] = '120'
    #     ei_update['tender']['items'][0]['unit']['name'] = 'name_2'
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     ocid = fnmatch.fnmatch(update_ei_response[1]['data']['ocid'], '*')
    #
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert ocid == True
    #
    # @pytestrail.case('24453')
    # def test_24453_3(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['items'][0]['deliveryAddress']['streetAddress'] = 'Khreshchatyk'
    #     ei_create['tender']['items'][0]['deliveryAddress']['postalCode'] = '01124'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = 'description_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = 'scheme_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = 'www.deutch'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['description'] = 'description_2'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = 'scheme'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = 'CUATM'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = 'ww.io.io '
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #         'description'] = 'description_test'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = 'www,regi_16'
    #     ei_create['tender']['items'][0]['quantity'] = 10
    #     ei_create['tender']['items'][0]['unit']['id'] = '10'
    #     ei_create['tender']['items'][0]['unit']['name'] = 'name'
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['items'][0]['deliveryAddress']['streetAddress'] = 'Vladimirskaya'
    #     ei_update['tender']['items'][0]['deliveryAddress']['postalCode'] = '33344'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = 'Re_44'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = 'scheme_1_1'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = 'www.poland'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = '1700000'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #         'description'] = 'description_44_2'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = 'sheme_region_78'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = 'other'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = 'locality_1'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = 'www.vbn.ko'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #         'description'] = 'description_test_22'
    #     ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = 'www,regi_12'
    #     ei_update['tender']['items'][0]['quantity'] = 256
    #     ei_update['tender']['items'][0]['unit']['id'] = '120'
    #     ei_update['tender']['items'][0]['unit']['name'] = 'name_2'
    #
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     time.sleep(2)
    #
    #     url_update = update_ei_response[1]['data']['url']
    #
    #     publicPoint_update = requests.get(url=url_update).json()
    #
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['streetAddress'] == \
    #            ei_create['tender']['items'][0]['deliveryAddress']['streetAddress']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['streetAddress'] == \
    #            ei_update['tender']['items'][0]['deliveryAddress']['streetAddress']
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['streetAddress'] != \
    #            publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['streetAddress']
    #
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['postalCode'] == \
    #            ei_create['tender']['items'][0]['deliveryAddress']['postalCode']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['postalCode'] == \
    #            ei_update['tender']['items'][0]['deliveryAddress']['postalCode']
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress'][
    #                'postalCode'] != publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress'][
    #                'postalCode']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'id'] == ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                'id'] == ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id']
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'id'] == \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'id']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'description'] == 'Moldova, Republica'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                'description'] == 'Moldova, Republica'
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'description'] == \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'description']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'scheme'] == 'iso-alpha2'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                'scheme'] == 'iso-alpha2'
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'scheme'] == \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'scheme']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'uri'] == 'https://www.iso.org'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                'uri'] == 'https://www.iso.org'
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'uri'] == \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'uri']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'id'] == ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                'id'] == ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id']
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'id'] != \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'description'] == 'mun.Chişinău'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                'description'] == 'Cahul'
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'description'] != \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'description']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'scheme'] == 'CUATM'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                'scheme'] == 'CUATM'
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'scheme'] == \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'scheme']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'uri'] == 'http://statistica.md'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                'uri'] == 'http://statistica.md'
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'uri'] == \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'uri']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #             'scheme'] == ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #                'scheme'] == ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #                'scheme']
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #             'scheme'] != \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #             'scheme']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #             'id'] == ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #                'id'] == ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id']
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #             'id'] != \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #             'id']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #             'uri'] == 'http://statistica.md'
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #             'description'] == 'mun.Chişinău'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #                'description'] == ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #                'description']
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #             'description'] != \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #             'description']
    #
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'uri'] == 'http://statistica.md'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                'uri'] == 'http://statistica.md'
    #     assert \
    #         update_ei_response[3]['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'uri'] == \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #             'uri']
    #
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['quantity'] == \
    #            ei_create['tender']['items'][0]['quantity']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['quantity'] == ei_update['tender']['items'][0][
    #         'quantity']
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['quantity'] != \
    #            publicPoint_update['releases'][0]['tender']['items'][0]['quantity']
    #
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['unit']['id'] == \
    #            ei_create['tender']['items'][0]['unit']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['unit']['id'] == \
    #            ei_update['tender']['items'][0]['unit']['id']
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['unit']['id'] != \
    #            publicPoint_update['releases'][0]['tender']['items'][0]['unit']['id']
    #
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['unit']['name'] == \
    #            'Parsec'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['unit']['name'] == 'Milion decalitri'
    #     assert update_ei_response[3]['releases'][0]['tender']['items'][0]['unit']['id'] != \
    #            publicPoint_update['releases'][0]['tender']['items'][0]['unit']['id']
    #
    # @pytestrail.case('24454')
    # def test_24454_1(self):
    #
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['classification']['id'] = '45100000-8'
    #     ei_create['tender']['items'][0]['id'] = '1'
    #     ei_create['tender']['items'][0]['description'] = 'item_1'
    #     ei_create['tender']['items'][0]['classification']['id'] = '45112350-3'
    #     ei_create['tender']['items'][0]['additionalClassifications'][0]['id'] = 'AA12-4'
    #     ei_create['tender']['items'][0]['quantity'] = 10
    #     ei_create['tender']['items'][0]['unit']['id'] = '10'
    #     ei_create['tender']['items'][0]['unit']['name'] = 'name'
    #     ei_create['tender']['items'][0]['deliveryAddress']['streetAddress'] = 'Khreshchatyk'
    #     ei_create['tender']['items'][0]['deliveryAddress']['postalCode'] = '01124'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #         'description'] = 'description_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = 'scheme_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = 'www.deutch'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #         'description'] = 'description_2'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = 'scheme_2'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = 'www,regi_16'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = 'CUATM'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = 'ww.io.io '
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #         'description'] = 'description_test'
    #
    #     create_ei_response = bpe_create_ei(ei_create)
    #     url = create_ei_response[1]['data']['url'] + '/' + str(
    #         create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
    #     publicPoint = requests.get(url=url).json()
    #     saved_item_id = publicPoint['releases'][00]['tender']['items'][0]['id']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['id'] = '45100000-8'
    #     ei_update['tender']['items'] = [{
    #         "id": saved_item_id,
    #         "description": ei_create['tender']['items'][0]['description'],
    #         "classification": {
    #             "id": ei_create['tender']['items'][0]['classification']['id']
    #         },
    #         "additionalClassifications": [
    #             {
    #                 "id": ei_create['tender']['items'][0]['additionalClassifications'][0]['id']
    #             }
    #         ],
    #         "deliveryAddress": {
    #             "streetAddress": ei_create['tender']['items'][0]['deliveryAddress']['streetAddress'],
    #             "postalCode": ei_create['tender']['items'][0]['deliveryAddress']['postalCode'],
    #             "addressDetails": {
    #                 "country": {
    #                     "id": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'],
    #                     "description": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                         'description'],
    #                     "scheme": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                         'scheme'],
    #                     "uri": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri']
    #                 },
    #                 "region": {
    #                     "id": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'],
    #                     "description": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                         'description'],
    #                     "scheme": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                         'scheme'],
    #                     "uri": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri']
    #                 },
    #                 "locality": {
    #                     "id": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'],
    #                     "description": "description_test",
    #                     "scheme": 'CUATM',
    #                     "uri": "ww.io.io"
    #                 }
    #
    #             }
    #         },
    #         "quantity": 10,
    #         "unit": {
    #             "id": "10",
    #             "name": "name"
    #         }
    #     },
    #         {"id": "2",
    #          "description": "item 2",
    #          "classification": {
    #              "id": '45112360-6'
    #          },
    #          "additionalClassifications": [
    #              {
    #                  "id": "AA04-0"
    #              }
    #          ],
    #          "deliveryAddress": {
    #              "streetAddress": "Voloshkina",
    #              "postalCode": "55555",
    #              "addressDetails": {
    #                  "country": {
    #                      "id": "MD",
    #                      "description": "description_55",
    #                      "scheme": "scheme_55",
    #                      "uri": "www.55"
    #                  },
    #                  "region": {
    #                      "id": "0101000",
    #                      "description": "description_55",
    #                      "scheme": "scheme_55",
    #                      "uri": "www.regi_55"
    #                  },
    #                  "locality": {
    #                      "id": "555555",
    #                      "description": "description_test_55",
    #                      "scheme": 'other',
    #                      "uri": "ww.io.55"
    #                  }
    #
    #              }
    #          },
    #          "quantity": 20,
    #          "unit": {
    #              "id": "120",
    #              "name": "name_2"
    #          }
    #          }
    #     ]
    #
    #     access_token = get_access_token_for_platform_one()
    #     x_operation_id = get_x_operation_id(access_token)
    #     host = set_instance_for_request()
    #     update_ei_response = requests.post(
    #         url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
    #         headers={
    #             'Authorization': 'Bearer ' + access_token,
    #             'X-OPERATION-ID': x_operation_id,
    #             'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
    #             'Content-Type': 'application/json'},
    #         json=ei_update)
    #     time.sleep(1)
    #     message_from_kafka = get_message_from_kafka(x_operation_id)
    #
    #     assert update_ei_response.text == 'ok'
    #     assert update_ei_response.status_code == 202
    #     assert message_from_kafka['X-OPERATION-ID'] == x_operation_id
    #
    # @pytestrail.case('24454')
    # def test_24454_2(self):
    #
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['classification']['id'] = '45100000-8'
    #     ei_create['tender']['items'][0]['id'] = '1'
    #     ei_create['tender']['items'][0]['description'] = 'item_1'
    #     ei_create['tender']['items'][0]['classification']['id'] = '45112350-3'
    #     ei_create['tender']['items'][0]['additionalClassifications'][0]['id'] = 'AA12-4'
    #     ei_create['tender']['items'][0]['quantity'] = 10
    #     ei_create['tender']['items'][0]['unit']['id'] = '10'
    #     ei_create['tender']['items'][0]['unit']['name'] = 'name'
    #     ei_create['tender']['items'][0]['deliveryAddress']['streetAddress'] = 'Khreshchatyk'
    #     ei_create['tender']['items'][0]['deliveryAddress']['postalCode'] = '01124'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #         'description'] = 'description_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = 'scheme_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = 'www.deutch'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #         'description'] = 'description_2'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = 'scheme_2'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = 'www,regi_16'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = 'CUATM'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = 'ww.io.io '
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #         'description'] = 'description_test'
    #
    #     create_ei_response = bpe_create_ei(ei_create)
    #     url = create_ei_response[1]['data']['url'] + '/' + str(
    #         create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
    #     publicPoint = requests.get(url=url).json()
    #     saved_item_id = publicPoint['releases'][00]['tender']['items'][0]['id']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['id'] = '45100000-8'
    #     ei_update['tender']['items'] = [{
    #         "id": saved_item_id,
    #         "description": ei_create['tender']['items'][0]['description'],
    #         "classification": {
    #             "id": ei_create['tender']['items'][0]['classification']['id']
    #         },
    #         "additionalClassifications": [
    #             {
    #                 "id": ei_create['tender']['items'][0]['additionalClassifications'][0]['id']
    #             }
    #         ],
    #         "deliveryAddress": {
    #             "streetAddress": ei_create['tender']['items'][0]['deliveryAddress']['streetAddress'],
    #             "postalCode": ei_create['tender']['items'][0]['deliveryAddress']['postalCode'],
    #             "addressDetails": {
    #                 "country": {
    #                     "id": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'],
    #                     "description": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                         'description'],
    #                     "scheme": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                         'scheme'],
    #                     "uri": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri']
    #                 },
    #                 "region": {
    #                     "id": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'],
    #                     "description": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                         'description'],
    #                     "scheme": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                         'scheme'],
    #                     "uri": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri']
    #                 },
    #                 "locality": {
    #                     "id": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'],
    #                     "description": "description_test",
    #                     "scheme": 'CUATM',
    #                     "uri": "ww.io.io"
    #                 }
    #
    #             }
    #         },
    #         "quantity": 10,
    #         "unit": {
    #             "id": "10",
    #             "name": "name"
    #         }
    #     },
    #         {"id": "2",
    #          "description": "item 2",
    #          "classification": {
    #              "id": '45112360-6'
    #          },
    #          "additionalClassifications": [
    #              {
    #                  "id": "AA04-0"
    #              }
    #          ],
    #          "deliveryAddress": {
    #              "streetAddress": "Voloshkina",
    #              "postalCode": "55555",
    #              "addressDetails": {
    #                  "country": {
    #                      "id": "MD",
    #                      "description": "description_55",
    #                      "scheme": "scheme_55",
    #                      "uri": "www.55"
    #                  },
    #                  "region": {
    #                      "id": "0101000",
    #                      "description": "description_55",
    #                      "scheme": "scheme_55",
    #                      "uri": "www.regi_55"
    #                  },
    #                  "locality": {
    #                      "id": "555555",
    #                      "description": "description_test_55",
    #                      "scheme": 'other',
    #                      "uri": "ww.io.55"
    #                  }
    #
    #              }
    #          },
    #          "quantity": 20,
    #          "unit": {
    #              "id": "120",
    #              "name": "name_2"
    #          }
    #          }
    #     ]
    #
    #     access_token = get_access_token_for_platform_one()
    #     x_operation_id = get_x_operation_id(access_token)
    #     host = set_instance_for_request()
    #     requests.post(
    #         url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
    #         headers={
    #             'Authorization': 'Bearer ' + access_token,
    #             'X-OPERATION-ID': x_operation_id,
    #             'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
    #             'Content-Type': 'application/json'},
    #         json=ei_update)
    #     time.sleep(1)
    #     message_from_kafka = get_message_from_kafka(x_operation_id)
    #
    #     ocid = fnmatch.fnmatch(message_from_kafka['data']['ocid'], '*')
    #
    #     assert message_from_kafka['X-OPERATION-ID'] == x_operation_id
    #     assert ocid == True
    #
    # @pytestrail.case('24454')
    # def test_24454_3(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_create['tender']['classification']['id'] = '45100000-8'
    #     ei_create['tender']['items'][0]['id'] = '1'
    #     ei_create['tender']['items'][0]['description'] = 'item_1'
    #     ei_create['tender']['items'][0]['classification']['id'] = '45112350-3'
    #     ei_create['tender']['items'][0]['additionalClassifications'][0]['id'] = 'AA12-4'
    #     ei_create['tender']['items'][0]['quantity'] = 10
    #     ei_create['tender']['items'][0]['unit']['id'] = '10'
    #     ei_create['tender']['items'][0]['unit']['name'] = 'name'
    #     ei_create['tender']['items'][0]['deliveryAddress']['streetAddress'] = 'Khreshchatyk'
    #     ei_create['tender']['items'][0]['deliveryAddress']['postalCode'] = '01124'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #         'description'] = 'description_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = 'scheme_1'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = 'www.deutch'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #         'description'] = 'description_2'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = 'scheme_2'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = 'www,regi_16'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = 'CUATM'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = '0101000'
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = 'ww.io.io '
    #     ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
    #         'description'] = 'description_test'
    #
    #     create_ei_response = bpe_create_ei(ei_create)
    #     url = create_ei_response[1]['data']['url'] + '/' + str(
    #         create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
    #     publicPoint = requests.get(url=url).json()
    #     saved_item_id = publicPoint['releases'][00]['tender']['items'][0]['id']
    #
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['classification']['id'] = '45100000-8'
    #     ei_update['tender']['items'] = [{
    #         "id": saved_item_id,
    #         "description": ei_create['tender']['items'][0]['description'],
    #         "classification": {
    #             "id": ei_create['tender']['items'][0]['classification']['id']
    #         },
    #         "additionalClassifications": [
    #             {
    #                 "id": ei_create['tender']['items'][0]['additionalClassifications'][0]['id']
    #             }
    #         ],
    #         "deliveryAddress": {
    #             "streetAddress": ei_create['tender']['items'][0]['deliveryAddress']['streetAddress'],
    #             "postalCode": ei_create['tender']['items'][0]['deliveryAddress']['postalCode'],
    #             "addressDetails": {
    #                 "country": {
    #                     "id": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'],
    #                     "description": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                         'description'],
    #                     "scheme": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                         'scheme'],
    #                     "uri": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri']
    #                 },
    #                 "region": {
    #                     "id": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'],
    #                     "description": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                         'description'],
    #                     "scheme": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                         'scheme'],
    #                     "uri": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri']
    #                 },
    #                 "locality": {
    #                     "id": ei_create['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'],
    #                     "description": "description_test",
    #                     "scheme": 'CUATM',
    #                     "uri": "ww.io.io"
    #                 }
    #
    #             }
    #         },
    #         "quantity": 10,
    #         "unit": {
    #             "id": "10",
    #             "name": "name"
    #         }
    #     },
    #         {"id": "2",
    #          "description": "item 2",
    #          "classification": {
    #              "id": '45112360-6'
    #          },
    #          "additionalClassifications": [
    #              {
    #                  "id": "AA04-0"
    #              }
    #          ],
    #          "deliveryAddress": {
    #              "streetAddress": "Voloshkina",
    #              "postalCode": "55555",
    #              "addressDetails": {
    #                  "country": {
    #                      "id": "MD",
    #                      "description": "description_55",
    #                      "scheme": "scheme_55",
    #                      "uri": "www.55"
    #                  },
    #                  "region": {
    #                      "id": "0101000",
    #                      "description": "description_55",
    #                      "scheme": "scheme_55",
    #                      "uri": "www.regi_55"
    #                  },
    #                  "locality": {
    #                      "id": "555555",
    #                      "description": "description_test_55",
    #                      "scheme": 'other',
    #                      "uri": "ww.io.55"
    #                  }
    #
    #              }
    #          },
    #          "quantity": 20,
    #          "unit": {
    #              "id": "120",
    #              "name": "name_2"
    #          }
    #          }
    #     ]
    #
    #     access_token = get_access_token_for_platform_one()
    #     x_operation_id = get_x_operation_id(access_token)
    #     host = set_instance_for_request()
    #     requests.post(
    #         url=host + update_ei + create_ei_response[1]['data']['outcomes']['ei'][0]['id'],
    #         headers={
    #             'Authorization': 'Bearer ' + access_token,
    #             'X-OPERATION-ID': x_operation_id,
    #             'X-TOKEN': create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'],
    #             'Content-Type': 'application/json'},
    #         json=ei_update)
    #     time.sleep(1)
    #     message_from_kafka = get_message_from_kafka(x_operation_id)
    #
    #     url_update = message_from_kafka['data']['url']
    #
    #     publicPoint_update = requests.get(url=url_update).json()
    #
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['id'] == saved_item_id
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['description'] == \
    #            ei_update['tender']['items'][0]['description']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['classification']['scheme'] == 'CPV'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['classification']['id'] == \
    #            ei_update['tender']['items'][0]['classification']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['classification']['description'] == \
    #            'Lucrări de valorificare a terenurilor virane'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['additionalClassifications'][0][
    #                'scheme'] == 'CPVS'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['additionalClassifications'][0]['id'] == \
    #            ei_update['tender']['items'][0]['additionalClassifications'][0]['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['additionalClassifications'][0][
    #                'description'] == 'Oţel carbon'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['quantity'] == 10
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['unit']['name'] == 'Parsec'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['unit']['id'] == \
    #            ei_update['tender']['items'][0]['unit']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['streetAddress'] == \
    #            ei_update['tender']['items'][0]['deliveryAddress']['streetAddress']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['postalCode'] == \
    #            ei_update['tender']['items'][0]['deliveryAddress']['postalCode']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #                'scheme'] == 'iso-alpha2'
    #     assert \
    #         publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #             'id'] == 'MD'
    #     # assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails']['country'][
    #     #            'description'] == 'Moldova, Republica'
    #     # assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails'][
    #     #            'country']['uri'] == 'https://www.iso.org'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails'][
    #                'region']['scheme'] == 'CUATM'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails'][
    #                'region']['id'] == ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region'][
    #                'id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails'][
    #                'region']['description'] == 'mun.Chişinău'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails'][
    #                'region']['uri'] == 'http://statistica.md'
    #
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails'][
    #                'locality']['scheme'] == \
    #            ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails'][
    #                'locality']['id'] == \
    #            ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails'][
    #                'locality']['description'] == 'mun.Chişinău'
    #     assert publicPoint_update['releases'][0]['tender']['items'][0]['deliveryAddress']['addressDetails'][
    #                'locality']['uri'] == 'http://statistica.md'
    #
    #     is_uuid_item_id = is_valid_uuid(publicPoint_update['releases'][0]['tender']['items'][1]['id'])
    #     assert is_uuid_item_id == True
    #
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['description'] == \
    #            ei_update['tender']['items'][1]['description']
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['classification']['scheme'] == 'CPV'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['classification']['id'] == \
    #            ei_update['tender']['items'][1]['classification']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['classification']['description'] == \
    #            'Lucrări de reabilitare a terenului'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['additionalClassifications'][0][
    #                'scheme'] == 'CPVS'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['additionalClassifications'][0]['id'] == \
    #            ei_update['tender']['items'][1]['additionalClassifications'][0]['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['additionalClassifications'][0][
    #                'description'] == 'Cupru'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['quantity'] == 20
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['unit']['name'] == 'Milion decalitri'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['unit']['id'] == \
    #            ei_update['tender']['items'][1]['unit']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['streetAddress'] == \
    #            ei_update['tender']['items'][1]['deliveryAddress']['streetAddress']
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['postalCode'] == \
    #            ei_update['tender']['items'][1]['deliveryAddress']['postalCode']
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails']['country'][
    #                'scheme'] == 'iso-alpha2'
    #     assert \
    #         publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails']['country'][
    #             'id'] == 'MD'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails']['country'][
    #                'description'] == 'Moldova, Republica'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails'][
    #                'country']['uri'] == 'https://www.iso.org'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails'][
    #                'region']['scheme'] == 'CUATM'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails'][
    #                'region']['id'] == ei_update['tender']['items'][1]['deliveryAddress']['addressDetails']['region'][
    #                'id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails'][
    #                'region']['description'] == 'mun.Chişinău'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails'][
    #                'region']['uri'] == 'http://statistica.md'
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails'][
    #                'locality']['scheme'] == \
    #            ei_update['tender']['items'][1]['deliveryAddress']['addressDetails']['locality']['scheme']
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails'][
    #                'locality']['id'] == \
    #            ei_update['tender']['items'][1]['deliveryAddress']['addressDetails']['locality']['id']
    #     assert publicPoint_update['releases'][0]['tender']['items'][1]['deliveryAddress']['addressDetails'][
    #                'locality']['description'] == \
    #            ei_update['tender']['items'][1]['deliveryAddress']['addressDetails']['locality']['description']
    #
    # @pytestrail.case('24455')
    # def test_24455_1(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['items'][0]['id'] = '656'
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #
    # @pytestrail.case('24455')
    # def test_24455_2(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['items'][0]['id'] = '656'
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     ocid = fnmatch.fnmatch(update_ei_response[1]['data']['ocid'], '*')
    #
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert ocid == True
    #
    # @pytestrail.case('24455')
    # def test_24455_3(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_full)
    #     ei_update['tender']['items'][0]['id'] = '656'
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #     time.sleep(2)
    #
    #     url_update = update_ei_response[1]['data']['url']
    #
    #     publicPoint_update = requests.get(url=url_update).json()
    #
    #     def is_valid_uuid(uuid_to_test, version=4):
    #         try:
    #             uuid_obj = UUID(uuid_to_test, version=version)
    #         except:
    #             return False
    #         return str(uuid_obj) == uuid_to_test
    #
    #     is_uuid_item_id = is_valid_uuid(publicPoint_update['releases'][0]['tender']['items'][0]['id'])
    #     assert is_uuid_item_id == True
    #
    # @pytestrail.case('24456')
    # def test_24456_2(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.00.00.00'
    #     assert update_ei_response[1]['errors'][0]['description'] == 'Data processing exception.'
    #
    # @pytestrail.case('24456')
    # def test_24456_3(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['title']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.10.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.budget.model.dto.ei.' \
    #                                  'request.EiUpdate$TenderEiUpdate] value failed for JSON property title due to ' \
    #                                  'missing (therefore NULL) value for creator parameter title which is a ' \
    #                                  'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
    #                                  'reference chain: com.procurement.budget.model.dto.ei.request.' \
    #                                  'EiUpdate[\"tender\"]->com.procurement.budget.model.dto.ei.request.' \
    #                                  'EiUpdate$TenderEiUpdate[\"title\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_4(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['id']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item] value failed for JSON property id due to missing ' \
    #                                  '(therefore NULL) value for creator parameter id which is a non-nullable type\n ' \
    #                                  'at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.procurement.mdm.' \
    #                                  'model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item[\"id\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_5(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['description']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item] value failed for JSON property description due to ' \
    #                                  'missing (therefore NULL) value for creator parameter description which is a ' \
    #                                  'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
    #                                  'reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->' \
    #                                  'com.procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util.' \
    #                                  'ArrayList[0]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$' \
    #                                  'Item[\"description\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_6(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['classification']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item] value failed for JSON property classification due to ' \
    #                                  'missing (therefore NULL) value for creator parameter classification which is a ' \
    #                                  'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
    #                                  'reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->' \
    #                                  'com.procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util.' \
    #                                  'ArrayList[0]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$' \
    #                                  'Item[\"classification\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_7(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['classification']['id']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$Classification] value failed for JSON property id due to ' \
    #                                  'missing (therefore NULL) value for creator parameter id which is a non-' \
    #                                  'nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference ' \
    #                                  'chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util.' \
    #                                  'ArrayList[0]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item' \
    #                                  '[\"classification\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender' \
    #                                  '$Item$Classification[\"id\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_8(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['additionalClassifications'][0]['id']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$AdditionalClassification] value failed for JSON property ' \
    #                                  'id due to missing (therefore NULL) value for creator parameter id which is a ' \
    #                                  'non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
    #                                  'reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->' \
    #                                  'com.procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util.' \
    #                                  'ArrayList[0]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item' \
    #                                  '[\"additionalClassifications\"]->java.util.ArrayList[0]->com.procurement.mdm.' \
    #                                  'model.dto.data.ei.EIRequest$Tender$Item$AdditionalClassification[\"id\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_9(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['deliveryAddress']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item] value failed for JSON property deliveryAddress due to ' \
    #                                  'missing (therefore NULL) value for creator parameter deliveryAddress which is ' \
    #                                  'a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through ' \
    #                                  'reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->' \
    #                                  'com.procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util.' \
    #                                  'ArrayList[0]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item' \
    #                                  '[\"deliveryAddress\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_10(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$DeliveryAddress] value failed for JSON property ' \
    #                                  'addressDetails due to missing (therefore NULL) value for creator parameter ' \
    #                                  'addressDetails which is a non-nullable type\n at [Source: UNKNOWN; line: -1, ' \
    #                                  'column: -1] (through reference chain: com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender' \
    #                                  '[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.' \
    #                                  'ei.EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_11(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$DeliveryAddress$AddressDetails] value failed for JSON ' \
    #                                  'property country due to missing (therefore NULL) value for creator parameter ' \
    #                                  'country which is a non-nullable type\n at [Source: UNKNOWN; line: -1, ' \
    #                                  'column: -1] (through reference chain: com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender' \
    #                                  '[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.' \
    #                                  'ei.EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->com.procurement.' \
    #                                  'mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$AddressDetails' \
    #                                  '[\"country\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_12(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$DeliveryAddress$AddressDetails$Country] value failed for ' \
    #                                  'JSON property id due to missing (therefore NULL) value for creator parameter ' \
    #                                  'id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] ' \
    #                                  '(through reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest' \
    #                                  '[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender' \
    #                                  '[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item[\"deliveryAddress\"]->com.procurement.mdm.model.dto.' \
    #                                  'data.ei.EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$' \
    #                                  'AddressDetails[\"country\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$' \
    #                                  'Tender$Item$DeliveryAddress$AddressDetails$Country[\"id\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_13(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$DeliveryAddress$AddressDetails] value failed for JSON ' \
    #                                  'property region due to missing (therefore NULL) value for creator parameter ' \
    #                                  'region which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: ' \
    #                                  '-1] (through reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest' \
    #                                  '[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender' \
    #                                  '[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item[\"deliveryAddress\"]->com.procurement.mdm.model.dto.' \
    #                                  'data.ei.EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$' \
    #                                  'AddressDetails[\"region\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_14(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$DeliveryAddress$AddressDetails$Region] value failed for ' \
    #                                  'JSON property id due to missing (therefore NULL) value for creator parameter ' \
    #                                  'id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] ' \
    #                                  '(through reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest' \
    #                                  '[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender' \
    #                                  '[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item[\"deliveryAddress\"]->com.procurement.mdm.model.dto.' \
    #                                  'data.ei.EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$' \
    #                                  'AddressDetails[\"region\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$' \
    #                                  'Tender$Item$DeliveryAddress$AddressDetails$Region[\"id\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_15(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$DeliveryAddress$AddressDetails$Locality] value failed ' \
    #                                  'for JSON property id due to missing (therefore NULL) value for creator ' \
    #                                  'parameter id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, ' \
    #                                  'column: -1] (through reference chain: com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender' \
    #                                  '[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.' \
    #                                  'ei.EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->com.procurement.' \
    #                                  'mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$AddressDetails' \
    #                                  '[\"locality\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$' \
    #                                  'DeliveryAddress$AddressDetails$Locality[\"id\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_16(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$DeliveryAddress$AddressDetails$Locality] value failed ' \
    #                                  'for JSON property scheme due to missing (therefore NULL) value for creator ' \
    #                                  'parameter scheme which is a non-nullable type\n at [Source: UNKNOWN; line: -1, ' \
    #                                  'column: -1] (through reference chain: com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender' \
    #                                  '[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item[\"deliveryAddress\"]->com.procurement.mdm.model.dto.' \
    #                                  'data.ei.EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$' \
    #                                  'AddressDetails[\"locality\"]->com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$DeliveryAddress$AddressDetails$Locality[\"scheme\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_17(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['quantity']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item] value failed for JSON property quantity due to missing ' \
    #                                  '(therefore NULL) value for creator parameter quantity which is a non-nullable ' \
    #                                  'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
    #                                  'com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.procurement.' \
    #                                  'mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->' \
    #                                  'com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item[\"quantity\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_18(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['unit']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item] value failed for JSON property unit due to missing ' \
    #                                  '(therefore NULL) value for creator parameter unit which is a non-nullable ' \
    #                                  'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
    #                                  'com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.procurement.' \
    #                                  'mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->' \
    #                                  'com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item[\"unit\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_19(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['items'][0]['unit']['id']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Item$Unit] value failed for JSON property id due to missing ' \
    #                                  '(therefore NULL) value for creator parameter id which is a non-nullable ' \
    #                                  'type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: ' \
    #                                  'com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.procurement.' \
    #                                  'mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->' \
    #                                  'com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item[\"unit\"]->com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$Unit[\"id\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_20(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['classification']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender] value failed for JSON property classification due to missing ' \
    #                                  '(therefore NULL) value for creator parameter classification which is a non-' \
    #                                  'nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference ' \
    #                                  'chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"classification\"])'
    #
    # @pytestrail.case('24456')
    # def test_24456_21(self):
    #     ei_create = copy.deepcopy(ei_full)
    #     ei_update = copy.deepcopy(ei_update_obligatory_fields_with_obligatory_fields_in_tender_items)
    #     del ei_update['tender']['classification']['id']
    #     update_ei_response = bpe_update_ei(ei_update, ei_create)
    #
    #     assert update_ei_response[0].text == 'ok'
    #     assert update_ei_response[0].status_code == 202
    #     assert update_ei_response[1]['X-OPERATION-ID'] == update_ei_response[2]
    #     assert update_ei_response[1]['errors'][0]['code'] == '400.20.00'
    #     assert update_ei_response[1]['errors'][0][
    #                'description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: ' \
    #                                  'Instantiation of [simple type, class com.procurement.mdm.model.dto.data.ei.' \
    #                                  'EIRequest$Tender$Classification] value failed for JSON property id due to ' \
    #                                  'missing (therefore NULL) value for creator parameter id which is a non-' \
    #                                  'nullable type\n at [Source: UNKNOWN; line: -1, column: -1] (through reference ' \
    #                                  'chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"classification\"]->com.' \
    #                                  'procurement.mdm.model.dto.data.ei.EIRequest$Tender$Classification[\"id\"])'
