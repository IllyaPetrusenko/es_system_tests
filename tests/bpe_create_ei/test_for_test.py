import copy, datetime, fnmatch, time, requests, pytest, allure

from pytest_testrail.plugin import pytestrail
from useful_functions import is_valid_uuid, is_it_uuid, get_human_date_in_utc_format, get_period
from tests.bpe_create_ei.create_ei import EI
from tests.bpe_create_ei.payloads import payload_ei_full_data_model


class TestCheckTheImpossibilityToCreateEIWithoutObligatoryData(object):

    @allure.step('Delete tender object from request')
    @pytestrail.case("22132")
    def test_22132_1(self, country, language, tag):

        ei = EI()
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]
        create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
        actual_result = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        expected_result = '{"code":"400.00.00.00","description":"Data processing exception."}'
        allure.attach(str(expected_result), 'Expected result')
        assert actual_result['errors'] == expected_result

    @allure.step('Delete tender title from request')
    @pytestrail.case("22132")
    def test_22132_2(self, country, language):
        ei = EI()
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["title"]
        create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
        message_from_kafka = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.10.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.budget." \
                                                                 "model.dto.ei.request.EiCreate$TenderEiCreate] " \
                                                                 "value failed for JSON property title due to " \
                                                                 "missing (therefore NULL) value for creator " \
                                                                 "parameter title which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.budget.model.dto.ei.request." \
                                                                 "EiCreate[\"tender\"]->com.procurement.budget." \
                                                                 "model.dto.ei.request.EiCreate$TenderEiCreate" \
                                                                 "[\"title\"])"

    @allure.step('Delete tender classification from request')
    @pytestrail.case("22132")
    def test_22132_3(self, country, language):
        ei = EI()
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["classification"]
        create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
        message_from_kafka = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.ei.EIRequest$Tender] value failed for " \
                                                                 "JSON property classification due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "classification which is a non-nullable type\n " \
                                                                 "at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement.mdm." \
                                                                 "model.dto.data.ei.EIRequest[\"tender\"]->com." \
                                                                 "procurement.mdm.model.dto.data.ei.EIRequest$" \
                                                                 "Tender[\"classification\"])"

