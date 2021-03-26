import copy
import datetime
import fnmatch
import time
import requests
from pytest_testrail.plugin import pytestrail
from useful_functions import is_valid_uuid, is_it_uuid, get_human_date_in_utc_format, get_period
from tests.bpe_create_ei.create_ei import EI
from tests.bpe_create_ei.payloads import payload_ei_full_data_model


class TestBpeCreateEI(object):

    @pytestrail.case("22132")
    def test_22132_1_smoke(self, country, language):
        ei = EI()
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]
        create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
        message_from_kafka = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.00.00.00"
        assert message_from_kafka["errors"][0]["description"] == "Data processing exception."

    @pytestrail.case("22132")
    def test_22132_2_smoke(self, country, language):
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
                                                                 "[\"title2\"])"

    @pytestrail.case("22132")
    def test_22132_3_smoke(self, country, language):
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

    @pytestrail.case("22132")
    def test_22132_4_smoke(self, country, language):
        ei = EI()
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["classification"]["id"]
        create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
        message_from_kafka = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.20.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.mdm.model." \
                                                                 "dto.data.ei.EIRequest$Tender$Classification] " \
                                                                 "value failed for JSON property id due to " \
                                                                 "missing (therefore NULL) value for creator " \
                                                                 "parameter id which is a non-nullable type\n " \
                                                                 "at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement.mdm." \
                                                                 "model.dto.data.ei.EIRequest[\"tender\"]->com." \
                                                                 "procurement.mdm.model.dto.data.ei.EIRequest$" \
                                                                 "Tender[\"classification\"]->com.procurement." \
                                                                 "mdm.model.dto.data.ei.EIRequest$Tender$" \
                                                                 "Classification[\"id\"])"

    @pytestrail.case("22132")
    def test_22132_5_smoke(self, country, language):
        ei = EI()
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]
        create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
        message_from_kafka = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.10.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.budget." \
                                                                 "model.dto.ei.request.EiCreate] value failed " \
                                                                 "for JSON property planning due to missing " \
                                                                 "(therefore NULL) value for creator parameter " \
                                                                 "planning which is a non-nullable type\n at " \
                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                 "(through reference chain: com.procurement." \
                                                                 "budget.model.dto.ei.request.EiCreate[\"planning\"])"

    @pytestrail.case("22132")
    def test_22132_6_smoke(self, country, language):
        ei = EI()
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]
        create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
        message_from_kafka = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.10.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlin" \
                                                                 "ParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.budget." \
                                                                 "model.dto.ei.request.EiCreate$PlanningEiCreate] " \
                                                                 "value failed for JSON property budget due to " \
                                                                 "missing (therefore NULL) value for creator " \
                                                                 "parameter budget which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, " \
                                                                 "column: -1] (through reference chain: com." \
                                                                 "procurement.budget.model.dto.ei.request." \
                                                                 "EiCreate[\"planning\"]->com.procurement.budget." \
                                                                 "model.dto.ei.request.EiCreate$PlanningEiCreate" \
                                                                 "[\"budget\"])"

    @pytestrail.case("22132")
    def test_22132_7_smoke(self, country, language):
        ei = EI()
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]["period"]
        create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
        message_from_kafka = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.10.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                 "KotlinParameterException: Instantiation of " \
                                                                 "[simple type, class com.procurement.budget." \
                                                                 "model.dto.ei.request.EiCreate$PlanningEiCreate$" \
                                                                 "BudgetEiCreate] value failed for JSON property " \
                                                                 "period due to missing (therefore NULL) value for " \
                                                                 "creator parameter period which is a non-nullable " \
                                                                 "type\n at [Source: UNKNOWN; line: -1, column: " \
                                                                 "-1] (through reference chain: com.procurement." \
                                                                 "budget.model.dto.ei.request.EiCreate" \
                                                                 "[\"planning\"]->com.procurement.budget.model." \
                                                                 "dto.ei.request.EiCreate$PlanningEiCreate" \
                                                                 "[\"budget\"]->com.procurement.budget.model.dto." \
                                                                 "ei.request.EiCreate$PlanningEiCreate$BudgetEi" \
                                                                 "Create[\"period\"])"

    @pytestrail.case("22132")
    def test_22132_8_smoke(self, country, language):
        ei = EI()
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]["period"]["startDate"]
        create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
        message_from_kafka = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.10.00"
        assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlin" \
                                                                 "ParameterException: Instantiation of [simple " \
                                                                 "type, class com.procurement.budget.model.dto." \
                                                                 "ocds.Period] value failed for JSON property " \
                                                                 "startDate due to missing (therefore NULL) value " \
                                                                 "for creator parameter startDate which is a " \
                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                 "-1, column: -1] (through reference chain: " \
                                                                 "com.procurement.budget.model.dto.ei.request." \
                                                                 "EiCreate[\"planning\"]->com.procurement.budget." \
                                                                 "model.dto.ei.request.EiCreate$PlanningEiCreate" \
                                                                 "[\"budget\"]->com.procurement.budget.model.dto." \
                                                                 "ei.request.EiCreate$PlanningEiCreate$Budget" \
                                                                 "EiCreate[\"period\"]->com.procurement.budget." \
                                                                 "model.dto.ocds.Period[\"startDate\"])"