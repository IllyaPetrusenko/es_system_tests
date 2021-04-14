import copy
import datetime
import json

import requests
from pytest_testrail.plugin import pytestrail
from tests.essences.ei import EI
from tests.payloads.ei_payload import payload_ei_full_data_model
from tests.presets import choose_instance
from useful_functions import compare_actual_result_and_expected_result, get_human_date_in_utc_format, is_it_uuid, \
    get_period


class TestCheckTheImpossibilityToCreateEIWithoutObligatoryData(object):
    @pytestrail.case("22132")
    def test_delete_tender_object_from_the_payload_22132_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{'code': '400.00.00.00', 'description': 'Data processing exception.'}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_title_field_from_the_payload_22132_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["title"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ei.request.EiCreate$TenderEiCreate] value "
                                               "failed for JSON property title due to missing (therefore NULL) "
                                               "value for creator parameter title which is a non-nullable type\n "
                                               "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.budget.model.dto.ei.request.EiCreate"
                                               "[\"tender\"]->com.procurement.budget.model.dto.ei.request."
                                               "EiCreate$TenderEiCreate[\"title\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_classification_object_from_the_payload_22132_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["classification"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender] value failed for JSON "
                                               "property classification due to missing (therefore NULL) value "
                                               "for creator parameter classification which is a non-nullable "
                                               "type\n at [Source: UNKNOWN; line: -1, column: -1] (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender[\"classification\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_classification_id_field_from_the_payload_22132_4(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Classification] value "
                                               "failed for JSON property id due to missing (therefore NULL) "
                                               "value for creator parameter id which is a non-nullable type\n "
                                               "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]"
                                               "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender"
                                               "[\"classification\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Classification[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_planning_object_from_the_payload_22132_5(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ei.request.EiCreate] value failed for JSON "
                                               "property planning due to missing (therefore NULL) value for "
                                               "creator parameter planning which is a non-nullable type\n at "
                                               "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: "
                                               "com.procurement.budget.model.dto.ei.request.EiCreate[\"planning\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_planning_budget_object_from_the_payload_22132_6(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ei.request.EiCreate$PlanningEiCreate] value "
                                               "failed for JSON property budget due to missing (therefore NULL) "
                                               "value for creator parameter budget which is a non-nullable type\n "
                                               "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.budget.model.dto.ei.request.EiCreate"
                                               "[\"planning\"]->com.procurement.budget.model.dto.ei.request."
                                               "EiCreate$PlanningEiCreate[\"budget\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_planning_budget_period_object_from_the_payload_22132_7(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]["period"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ei.request.EiCreate$PlanningEiCreate$Budget"
                                               "EiCreate] value failed for JSON property period due to missing "
                                               "(therefore NULL) value for creator parameter period which is a "
                                               "non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                               "(through reference chain: com.procurement.budget.model.dto.ei."
                                               "request.EiCreate[\"planning\"]->com.procurement.budget.model."
                                               "dto.ei.request.EiCreate$PlanningEiCreate[\"budget\"]->com."
                                               "procurement.budget.model.dto.ei.request.EiCreate$PlanningEi"
                                               "Create$BudgetEiCreate[\"period\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_planning_budget_period_startDate_field_from_the_payload_22132_8(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]["period"]["startDate"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ocds.Period] value failed for JSON property "
                                               "startDate due to missing (therefore NULL) value for creator "
                                               "parameter startDate which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.budget.model.dto.ei.request.EiCreate[\"planning\"]->"
                                               "com.procurement.budget.model.dto.ei.request.EiCreate$Planning"
                                               "EiCreate[\"budget\"]->com.procurement.budget.model.dto.ei.request."
                                               "EiCreate$PlanningEiCreate$BudgetEiCreate[\"period\"]->"
                                               "com.procurement.budget.model.dto.ocds.Period[\"startDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_planning_budget_period_endDate_field_from_the_payload_22132_9(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]["period"]["endDate"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ocds.Period] value failed for JSON property "
                                               "endDate due to missing (therefore NULL) value for creator "
                                               "parameter endDate which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: "
                                               "com.procurement.budget.model.dto.ei.request.EiCreate"
                                               "[\"planning\"]->com.procurement.budget.model.dto.ei.request."
                                               "EiCreate$PlanningEiCreate[\"budget\"]->com.procurement.budget."
                                               "model.dto.ei.request.EiCreate$PlanningEiCreate$BudgetEiCreate"
                                               "[\"period\"]->com.procurement.budget.model.dto.ocds.Period"
                                               "[\"endDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_object_from_the_payload_22132_10(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest] value failed for JSON property "
                                               "buyer due to missing (therefore NULL) value for creator parameter "
                                               "buyer which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                               "-1, column: -1] (through reference chain: com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest[\"buyer\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_name_field_from_the_payload_22132_11(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["name"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ei.OrganizationReferenceEi] value failed for JSON "
                                               "property name due to missing (therefore NULL) value for creator "
                                               "parameter name which is a non-nullable type\n at [Source: UNKNOWN; "
                                               "line: -1, column: -1] (through reference chain: com.procurement."
                                               "budget.model.dto.ei.request.EiCreate[\"buyer\"]->com.procurement."
                                               "budget.model.dto.ei.OrganizationReferenceEi[\"name\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_identifier_field_from_the_payload_22132_12(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["identifier"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ei.OrganizationReferenceEi] value failed for "
                                               "JSON property identifier due to missing (therefore NULL) value "
                                               "for creator parameter identifier which is a non-nullable type\n "
                                               "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.budget.model.dto.ei.request.EiCreate"
                                               "[\"buyer\"]->com.procurement.budget.model.dto.ei."
                                               "OrganizationReferenceEi[\"identifier\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_identifier_scheme_field_from_the_payload_22132_13(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["identifier"]["scheme"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.Identifier] value failed for JSON property "
                                               "scheme due to missing (therefore NULL) value for creator "
                                               "parameter scheme which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com."
                                               "procurement.mdm.model.dto.data.OrganizationReference"
                                               "[\"identifier\"]->com.procurement.mdm.model.dto.data."
                                               "Identifier[\"scheme\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_identifier_id_field_from_the_payload_22132_14(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["identifier"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00", "description": "com.fasterxml.jackson.module.kotlin."
                                                                    "MissingKotlinParameterException: Instantiation "
                                                                    "of [simple type, class com.procurement.mdm."
                                                                    "model.dto.data.Identifier] value failed for "
                                                                    "JSON property id due to missing (therefore "
                                                                    "NULL) value for creator parameter id which is "
                                                                    "a non-nullable type\n at [Source: UNKNOWN; line: "
                                                                    "-1, column: -1] (through reference chain: com."
                                                                    "procurement.mdm.model.dto.data.ei.EIRequest"
                                                                    "[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                                                    "OrganizationReference[\"identifier\"]->com."
                                                                    "procurement.mdm.model.dto.data.Identifier"
                                                                    "[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_identifier_legalName_field_from_the_payload_22132_15(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["identifier"]["legalName"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ocds.Identifier] value failed for JSON property "
                                               "legalName due to missing (therefore NULL) value for creator "
                                               "parameter legalName which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.budget.model.dto.ei.request.EiCreate[\"buyer\"]->com."
                                               "procurement.budget.model.dto.ei.OrganizationReferenceEi"
                                               "[\"identifier\"]->com.procurement.budget.model.dto.ocds."
                                               "Identifier[\"legalName\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_object_from_the_payload_22132_16(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ei.OrganizationReferenceEi] value failed for "
                                               "JSON property address due to missing (therefore NULL) value for "
                                               "creator parameter address which is a non-nullable type\n at "
                                               "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.budget.model.dto.ei.request.EiCreate"
                                               "[\"buyer\"]->com.procurement.budget.model.dto.ei.Organization"
                                               "ReferenceEi[\"address\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_Delete_buyer_address_streetAddress_object_from_the_payload_22132_17(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["streetAddress"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement.mdm."
                                               "model.dto.data.Address] value failed for JSON property "
                                               "streetAddress due to missing (therefore NULL) value for creator "
                                               "parameter streetAddress which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com."
                                               "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]->"
                                               "com.procurement.mdm.model.dto.data.Address[\"streetAddress\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_addressDetails_object_from_the_payload_22132_18(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.Address] value failed for JSON property "
                                               "addressDetails due to missing (therefore NULL) value for creator "
                                               "parameter addressDetails which is a non-nullable type\n at "
                                               "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: "
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com."
                                               "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                               "->com.procurement.mdm.model.dto.data.Address[\"addressDetails\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_Delete_buyer_address_addressDetails_country_object_from_the_payload_22132_19(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["country"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.AddressDetails] value failed for JSON property "
                                               "country due to missing (therefore NULL) value for creator "
                                               "parameter country which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com."
                                               "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                               "->com.procurement.mdm.model.dto.data.Address[\"addressDetails\"]"
                                               "->com.procurement.mdm.model.dto.data.AddressDetails[\"country\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_Delete_buyer_address_addressDetails_country_id_field_from_the_payload_22132_20(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["country"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.CountryDetails] value failed for JSON property "
                                               "id due to missing (therefore NULL) value for creator parameter "
                                               "id which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                               "column: -1] (through reference chain: com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest[\"buyer\"]->com.procurement.mdm.model.dto."
                                               "data.OrganizationReference[\"address\"]->com.procurement.mdm.model."
                                               "dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model."
                                               "dto.data.AddressDetails[\"country\"]->com.procurement.mdm.model."
                                               "dto.data.CountryDetails[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_addressDetails_region_field_from_the_payload_22132_21(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["region"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.AddressDetails] value failed for JSON property "
                                               "region due to missing (therefore NULL) value for creator parameter "
                                               "region which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                               "-1, column: -1] (through reference chain: com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.mdm.model."
                                               "dto.data.OrganizationReference[\"address\"]->com.procurement.mdm."
                                               "model.dto.data.Address[\"addressDetails\"]->com.procurement."
                                               "mdm.model.dto.data.AddressDetails[\"region\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_addressDetails_region_id_field_from_the_payload_22132_22(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["region"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.RegionDetails] value failed for JSON property "
                                               "id due to missing (therefore NULL) value for creator parameter "
                                               "id which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                               "-1, column: -1] (through reference chain: com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.mdm."
                                               "model.dto.data.OrganizationReference[\"address\"]->com."
                                               "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->"
                                               "com.procurement.mdm.model.dto.data.AddressDetails[\"region\"]->"
                                               "com.procurement.mdm.model.dto.data.RegionDetails[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_addressDetails_locality_field_from_the_payload_22132_23(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["locality"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.AddressDetails] value failed for JSON property "
                                               "locality due to missing (therefore NULL) value for creator "
                                               "parameter locality which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com."
                                               "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                               "->com.procurement.mdm.model.dto.data.Address[\"addressDetails\"]"
                                               "->com.procurement.mdm.model.dto.data.AddressDetails[\"locality\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_addressDetails_locality_scheme_field_from_the_payload_22132_24(self, country,
                                                                                                 language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                               "property scheme due to missing (therefore NULL) value for "
                                               "creator parameter scheme which is a non-nullable type\n at "
                                               "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"buyer\"]->com.procurement.mdm.model.dto.data.Organization"
                                               "Reference[\"address\"]->com.procurement.mdm.model.dto.data."
                                               "Address[\"addressDetails\"]->com.procurement.mdm.model.dto."
                                               "data.AddressDetails[\"locality\"]->com.procurement.mdm.model."
                                               "dto.data.LocalityDetails[\"scheme\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_addressDetails_locality_id_field_from_the_payload_22132_25(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["locality"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                               "property id due to missing (therefore NULL) value for creator "
                                               "parameter id which is a non-nullable type\n at [Source: UNKNOWN; "
                                               "line: -1, column: -1] (through reference chain: com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.mdm."
                                               "model.dto.data.OrganizationReference[\"address\"]->com."
                                               "procurement.mdm.model.dto.data.Address[\"addressDetails\"]->"
                                               "com.procurement.mdm.model.dto.data.AddressDetails[\"locality\"]"
                                               "->com.procurement.mdm.model.dto.data.LocalityDetails[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_addressDetails_locality_description_field_from_the_payload_22132_26(self, country,
                                                                                                      language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["locality"]["description"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.LocalityDetails] value failed for JSON property "
                                               "description due to missing (therefore NULL) value for creator "
                                               "parameter description which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com."
                                               "procurement.mdm.model.dto.data.OrganizationReference[\"address\"]"
                                               "->com.procurement.mdm.model.dto.data.Address[\"addressDetails\"]"
                                               "->com.procurement.mdm.model.dto.data.AddressDetails[\"locality\"]"
                                               "->com.procurement.mdm.model.dto.data.LocalityDetails"
                                               "[\"description\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_contactPoint_field_from_the_payload_22132_27(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["contactPoint"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "budget.model.dto.ei.OrganizationReferenceEi] value failed for "
                                               "JSON property contactPoint due to missing (therefore NULL) value "
                                               "for creator parameter contactPoint which is a non-nullable type\n "
                                               "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.budget.model.dto.ei.request.EiCreate"
                                               "[\"buyer\"]->com.procurement.budget.model.dto.ei.Organization"
                                               "ReferenceEi[\"contactPoint\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_contactPoint_name_field_from_the_payload_22132_28(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["contactPoint"]["name"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                               "name due to missing (therefore NULL) value for creator parameter "
                                               "name which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                               "-1, column: -1] (through reference chain: com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.mdm.model."
                                               "dto.data.OrganizationReference[\"contactPoint\"]->com.procurement."
                                               "mdm.model.dto.data.ContactPoint[\"name\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_contactPoint_email_field_from_the_payload_22132_29(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["contactPoint"]["email"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                               "email due to missing (therefore NULL) value for creator parameter "
                                               "email which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                               "-1, column: -1] (through reference chain: com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.mdm.model."
                                               "dto.data.OrganizationReference[\"contactPoint\"]->com.procurement."
                                               "mdm.model.dto.data.ContactPoint[\"email\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_buyer_address_contactPoint_telephone_field_from_the_payload_22132_30(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["contactPoint"]["telephone"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ContactPoint] value failed for JSON property "
                                               "telephone due to missing (therefore NULL) value for creator "
                                               "parameter telephone which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com."
                                               "procurement.mdm.model.dto.data.OrganizationReference"
                                               "[\"contactPoint\"]->com.procurement.mdm.model.dto."
                                               "data.ContactPoint[\"telephone\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_id_field_from_the_payload_22132_31(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                               "JSON property id due to missing (therefore NULL) value for creator "
                                               "parameter id which is a non-nullable type\n at [Source: UNKNOWN; "
                                               "line: -1, column: -1] (through reference chain: com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util."
                                               "ArrayList[0]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender$Item[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_description_field_from_the_payload_22132_32(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["description"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest$Tender$Item] value failed for JSON "
                                               "property description due to missing (therefore NULL) value for "
                                               "creator parameter description which is a non-nullable type\n at "
                                               "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: "
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->"
                                               "java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Item[\"description\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_classification_field_from_the_payload_22132_33(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["classification"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                               "JSON property classification due to missing (therefore NULL) value "
                                               "for creator parameter classification which is a non-nullable "
                                               "type\n at [Source: UNKNOWN; line: -1, column: -1] (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest$Tender$Item[\"classification\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_classification_id_field_from_the_payload_22132_34(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$Classification] value "
                                               "failed for JSON property id due to missing (therefore NULL) value "
                                               "for creator parameter id which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->"
                                               "java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Item[\"classification\"]->com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest$Tender$Item$Classification[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_additionalClassifications_id_field_from_the_payload_22132_35(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$Additional"
                                               "Classification] value failed for JSON property id due to missing"
                                               " (therefore NULL) value for creator parameter id which is a "
                                               "non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1]"
                                               " (through reference chain: com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"additionalClassifications\"]->java.util.ArrayList[0]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$"
                                               "Item$AdditionalClassification[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_deliveryAddress_field_from_the_payload_22132_36(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                               "JSON property deliveryAddress due to missing (therefore NULL) "
                                               "value for creator parameter deliveryAddress which is a non-"
                                               "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                               "(through reference chain: com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"deliveryAddress\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_deliveryAddress_addressDetails_field_from_the_payload_22132_37(self, country,
                                                                                                language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress] value "
                                               "failed for JSON property addressDetails due to missing (therefore "
                                               "NULL) value for creator parameter addressDetails which is a non-"
                                               "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                               "(through reference chain: com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_deliveryAddress_addressDetails_country_field_from_the_payload_22132_38(self, country,
                                                                                                        language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails] value failed for JSON property country due to "
                                               "missing (therefore NULL) value for creator parameter country "
                                               "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                               "column: -1] (through reference chain: com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest[\"tender\"]->com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util."
                                               "ArrayList[0]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender$Item[\"deliveryAddress\"]->com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest$Tender$Item$DeliveryAddress[\"address"
                                               "Details\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender$Item$DeliveryAddress$AddressDetails[\"country\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_deliveryAddress_addressDetails_country_id_field_from_the_payload_22132_39(self,
                                                                                                           country,
                                                                                                           language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails$Country] value failed for JSON property id due "
                                               "to missing (therefore NULL) value for creator parameter id "
                                               "which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                               "-1, column: -1] (through reference chain: com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util."
                                               "ArrayList[0]->com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "$Tender$Item[\"deliveryAddress\"]->com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest$Tender$Item$DeliveryAddress[\"address"
                                               "Details\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender$Item$DeliveryAddress$AddressDetails[\"country\"]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                               "DeliveryAddress$AddressDetails$Country[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_deliveryAddress_addressDetails_region_field_from_the_payload_22132_40(self, country,
                                                                                                       language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails] value failed for JSON property region due to "
                                               "missing (therefore NULL) value for creator parameter region "
                                               "which is a non-nullable type\n at [Source: UNKNOWN; line: "
                                               "-1, column: -1] (through reference chain: com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util."
                                               "ArrayList[0]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender$Item[\"deliveryAddress\"]->com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest$Tender$Item$DeliveryAddress[\"address"
                                               "Details\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender$Item$DeliveryAddress$AddressDetails[\"region\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_deliveryAddress_addressDetails_locality_scheme_from_the_payload_22132_41(self,
                                                                                                          country,
                                                                                                          language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails$Locality] value failed for JSON property scheme "
                                               "due to missing (therefore NULL) value for creator parameter scheme"
                                               " which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                               "column: -1] (through reference chain: com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest[\"tender\"]->com.procurement.mdm.model.dto."
                                               "data.ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                               "DeliveryAddress$AddressDetails[\"locality\"]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails$Locality[\"scheme\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_deliveryAddress_addressDetails_region_id_from_the_payload_22132_42(self, country,
                                                                                                    language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails$Region] value failed for JSON property id due "
                                               "to missing (therefore NULL) value for creator parameter id "
                                               "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                               "column: -1] (through reference chain: com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest[\"tender\"]->com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]"
                                               "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                               "DeliveryAddress$AddressDetails[\"region\"]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails$Region[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_deliveryAddress_addressDetails_locality_id_from_the_payload_22132_43(self, country,
                                                                                                      language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$Address"
                                               "Details$Locality] value failed for JSON property id due to "
                                               "missing (therefore NULL) value for creator parameter id which "
                                               "is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: "
                                               "-1] (through reference chain: com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                               "DeliveryAddress$AddressDetails[\"locality\"]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails$Locality[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_deliveryAddress_addressDetails_locality_description_from_payload_22132_44(self,
                                                                                                           country,
                                                                                                           language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["description"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails$Locality] value failed for JSON property "
                                               "description due to missing (therefore NULL) value for creator "
                                               "parameter description which is a non-nullable type\n at "
                                               "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender[\"items\"]->java.util.ArrayList[0]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item[\"deliveryAddress\"]"
                                               "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$"
                                               "Item$DeliveryAddress[\"addressDetails\"]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                               "data.ei.EIRequest$Tender$Item$DeliveryAddress$AddressDetails$"
                                               "Locality[\"description\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_quantity_field_from_the_payload_22132_45(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["quantity"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                               "JSON property quantity due to missing (therefore NULL) value "
                                               "for creator parameter quantity which is a non-nullable type\n "
                                               "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender[\"items\"]->java.util.ArrayList[0]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item[\"quantity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_unit_field_from_the_payload_22132_46(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["unit"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                               "JSON property unit due to missing (therefore NULL) value for "
                                               "creator parameter unit which is a non-nullable type\n at "
                                               "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender[\"items\"]->java.util.ArrayList[0]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item[\"unit\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_items_unit_id_field_from_the_payload_22132_47(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["unit"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$Unit] value failed "
                                               "for JSON property id due to missing (therefore NULL) value for "
                                               "creator parameter id which is a non-nullable type\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->"
                                               "java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Item[\"unit\"]->com.procurement.mdm.model.dto."
                                               "data.ei.EIRequest$Tender$Item$Unit[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheCountryAddressIsFormedCorrectly(object):
    @pytestrail.case("22135")
    def test_send_the_request_22135_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22135")
    def test_see_the_result_in_feed_point_22135_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22135")
    def test_check_the_attribute_country_in_the_EI_record_22135_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_country_id = payload["buyer"]["address"]["addressDetails"]["country"]["id"]
        expected_result_country_id = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
                "id"]
        actual_result_country_scheme = "iso-alpha2"
        expected_result_country_scheme = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
                "scheme"]
        actual_result_country_description = "Moldova, Republica"
        expected_result_country_description = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["description"]
        actual_result_country_uri = "https://www.iso.org"
        expected_result_country_uri = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["uri"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result_country_id,
                                                         actual_result=actual_result_country_id)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_country_scheme,
                                                         actual_result=actual_result_country_scheme)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_country_description,
                                                         actual_result=actual_result_country_description)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_country_uri,
                                                         actual_result=actual_result_country_uri)


class TestCheckOnCorrectnessOfEnrichingTheSchemeOfCountry(object):
    @pytestrail.case("22136")
    def test_send_the_request_22136_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["buyer"]["address"]["addressDetails"]["country"]["scheme"] = "sheme for test"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22136")
    def test_see_the_result_in_feed_point_22136_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["buyer"]["address"]["addressDetails"]["country"]["scheme"] = "sheme for test"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22136")
    def test_check_the_attribute_country_in_the_EI_record_22136_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["buyer"]["address"]["addressDetails"]["country"]["scheme"] = "sheme for test"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_country_scheme = ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
            "scheme"]
        expected_result_country_scheme = "iso-alpha2"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_country_scheme,
                                                         actual_result=actual_result_country_scheme)


class TestCheckOnCorrectnessOfEnrichingTheUriOfCountry(object):
    @pytestrail.case("22137")
    def test_send_the_request_22137_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["buyer"]["address"]["addressDetails"]["country"]["uri"] = "uri for test"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22137")
    def test_see_the_result_in_feed_point_22137_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["buyer"]["address"]["addressDetails"]["country"]["uri"] = "uri for test"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22137")
    def test_check_the_attribute_country_in_the_EI_record_22137_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["buyer"]["address"]["addressDetails"]["country"]["uri"] = "uri for test"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_country_uri = ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
            "uri"]
        expected_result_country_uri = "https://www.iso.org"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_country_uri,
                                                         actual_result=actual_result_country_uri)


class TestCheckOnCorrectnessOfEnrichingTheDescriptionOfCountry(object):
    @pytestrail.case("22138")
    def test_send_the_request_22138_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["buyer"]["address"]["addressDetails"]["country"]["description"] = "description for test"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22138")
    def test_see_the_result_in_feed_point_22138_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["buyer"]["address"]["addressDetails"]["country"]["description"] = "description for test"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22138")
    def test_check_the_attribute_country_in_the_EI_record_22138_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["buyer"]["address"]["addressDetails"]["country"]["description"] = "description for test"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_country_description = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["description"]
        expected_result_country_description = "Moldova, Republica"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_country_description,
                                                         actual_result=actual_result_country_description)


class TestValidateTheInvalidCountryIdCantBeUsed(object):
    @pytestrail.case("22139")
    def test_send_the_request_22139_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "UK"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22139")
    def test_see_the_result_in_feed_point_22139_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "UK"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.10",
                                "description": "Invalid country. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheRegionAddressIsFormedCorrectly(object):
    @pytestrail.case("22140")
    def test_send_the_request_22140_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22140")
    def test_see_the_result_in_feed_point_22140_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22140")
    def test_check_the_attribute_region_in_the_EI_record_22140_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_region_id = payload["buyer"]["address"]["addressDetails"]["region"]["id"]
        expected_result_region_id = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
                "id"]
        actual_result_region_scheme = "CUATM"
        expected_result_region_scheme = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
                "scheme"]
        actual_result_region_description = "Donduşeni"
        expected_result_region_description = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["description"]
        actual_result_region_uri = "http://statistica.md"
        expected_result_region_uri = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result_region_id,
                                                         actual_result=actual_result_region_id)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_region_scheme,
                                                         actual_result=actual_result_region_scheme)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_region_description,
                                                         actual_result=actual_result_region_description)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_region_uri,
                                                         actual_result=actual_result_region_uri)


class TestCheckOnCorrectnessOfEnrichingTheSchemeOfRegion(object):
    @pytestrail.case("22141")
    def test_send_the_request_22141_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "1700000"
        payload["buyer"]["address"]["addressDetails"]["region"]["scheme"] = "other"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22141")
    def test_see_the_result_in_feed_point_22141_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "1700000"
        payload["buyer"]["address"]["addressDetails"]["region"]["scheme"] = "other"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22141")
    def test_check_the_attribute_region_in_the_EI_record_22141_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "1700000"
        payload["buyer"]["address"]["addressDetails"]["region"]["scheme"] = "other"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_region_scheme = ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
            "scheme"]
        expected_result_region_scheme = "CUATM"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_region_scheme,
                                                         actual_result=actual_result_region_scheme)


class TestCheckOnCorrectnessOfEnrichingTheUriOfRegion(object):
    @pytestrail.case("22142")
    def test_send_the_request_22142_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["uri"] = "test fro uri"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22142")
    def test_see_the_result_in_feed_point_22142_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["uri"] = "test fro uri"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22142")
    def test_check_the_attribute_region_in_the_EI_record_22142_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["uri"] = "test fro uri"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_region_uri = ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
            "uri"]
        expected_result_region_uri = "http://statistica.md"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_region_uri,
                                                         actual_result=actual_result_region_uri)


class TestCheckOnCorrectnessOfEnrichingTheDescriptionOfRegion(object):
    @pytestrail.case("22143")
    def test_send_the_request_22143_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["description"] = "test fro description"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22143")
    def test_see_the_result_in_feed_point_22143_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["description"] = "test fro description"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22143")
    def test_check_the_attribute_region_in_the_EI_record_22143_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["description"] = "test fro description"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_region_description = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["description"]
        expected_result_region_description = "Cahul"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_region_description,
                                                         actual_result=actual_result_region_description)


class TestValidateTheInvalidRegionIdCantBeUsed(object):
    @pytestrail.case("22144")
    def test_send_the_request_22144_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "UK"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22144")
    def test_see_the_result_in_feed_point_22144_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "UK"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.13",
                                "description": "Region not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheUnsuitableLocalityAddressIdCantBeUsed(object):
    @pytestrail.case("22145")
    def test_send_the_request_22145_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "1701000"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22145")
    def test_see_the_result_in_feed_point_22145_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "1701000"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.14",
                                "description": "Locality not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheSuitableLocalityAddressIdCanBeUsed(object):
    @pytestrail.case("22146")
    def test_send_the_request_22146_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22146")
    def test_see_the_result_in_feed_point_22146_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22146")
    def test_check_the_attribute_locality_in_the_EI_record_22146_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_locality_id = payload["buyer"]["address"]["addressDetails"]["locality"]["id"]
        expected_result_locality_id = ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
            "id"]
        actual_result_locality_scheme = "CUATM"
        expected_result_locality_scheme = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "scheme"]
        actual_result_locality_description = "or.Donduşeni (r-l Donduşeni)"
        expected_result_locality_description = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["description"]
        actual_result_locality_uri = "http://statistica.md"
        expected_result_locality_uri = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result_locality_id,
                                                         actual_result=actual_result_locality_id)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_locality_scheme,
                                                         actual_result=actual_result_locality_scheme)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_locality_description,
                                                         actual_result=actual_result_locality_description)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_locality_uri,
                                                         actual_result=actual_result_locality_uri)


class TestCheckWhenTheOtherSchemeForLocalityAddressUsedDescriptionIsObligatory(object):
    @pytestrail.case("22147")
    def test_send_the_request_22147_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
        del payload["buyer"]["address"]["addressDetails"]["locality"]["description"]
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22147")
    def test_see_the_result_in_feed_point_22147_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
        del payload["buyer"]["address"]["addressDetails"]["locality"]["description"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                               "Exception: Instantiation of [simple type, class com.procurement."
                                               "mdm.model.dto.data.LocalityDetails] value failed for JSON "
                                               "property description due to missing (therefore NULL) value for "
                                               "creator parameter description which is a non-nullable type\n "
                                               "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]"
                                               "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                               "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                               "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                               "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                               "data.LocalityDetails[\"description\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheOtherSchemeForLocalityAddressCanBeUsed(object):
    @pytestrail.case("22148")
    def test_send_the_request_22148_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "desc"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22148")
    def test_see_the_result_in_feed_point_22148_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "desc"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22148")
    def test_check_the_locality_object_has_values_from_the_request_22148_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "desc"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_locality_id = ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
            "id"]
        expected_result_locality_id = payload["buyer"]["address"]["addressDetails"]["locality"]["id"]
        actual_result_locality_scheme = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "scheme"]
        expected_result_locality_scheme = payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"]
        actual_result_locality_description = \
            ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["description"]
        expected_result_locality_description = "or.Donduşeni (r-l Donduşeni)"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_locality_id,
                                                         actual_result=actual_result_locality_id)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_locality_scheme,
                                                         actual_result=actual_result_locality_scheme)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_locality_description,
                                                         actual_result=actual_result_locality_description)


class TestCheckTheValidSchemeForBuyerIdentifier(object):
    @pytestrail.case("22149")
    def test_send_the_request_22149_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22149")
    def test_see_the_result_in_feed_point_22149_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22149")
    def test_check_the_identifier_object_in_the_EI_record_22149_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_identifier_scheme = ei_release["releases"][0]["parties"][0]["identifier"]["scheme"]
        expected_result_identifier_scheme = "MD-IDNO"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_identifier_scheme,
                                                         actual_result=actual_result_identifier_scheme)


class TestCheckTheInvalidSchemeForBuyerIdentifierCantBeUsed(object):
    @pytestrail.case("22150")
    def test_send_the_request_22150_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["scheme"] = "MD-NE-DNO"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22150")
    def test_see_the_result_in_feed_point_22150_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["scheme"] = "MD-NE-DNO"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.12",
                                "description": "Registration scheme not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheValidValueForTypeOfBuyerField(object):
    @pytestrail.case("22151")
    def test_send_the_request_22151_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["typeOfBuyer"] = "MINISTRY"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22151")
    def test_see_the_result_in_feed_point_22151_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["typeOfBuyer"] = "MINISTRY"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22151")
    def test_check_the_buyer_details_typeOfBuyer_field_in_the_EI_record_22151_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["typeOfBuyer"] = "MINISTRY"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result_type_of_buyer = ei_release["releases"][0]["parties"][0]["details"]["typeOfBuyer"]
        expected_result_type_of_buyer = payload["buyer"]["details"]["typeOfBuyer"] = "MINISTRY"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_type_of_buyer,
                                                         actual_result=actual_result_type_of_buyer)


class TestCheckTheInvalidValueForTypeOfBuyerFieldCantBeUsed(object):
    @pytestrail.case("22152")
    def test_send_the_request_22152_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["typeOfBuyer"] = "SCHOOL IS NOT HOME"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22152")
    def test_see_the_result_in_feed_point_22152_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["typeOfBuyer"] = "SCHOOL IS NOT HOME"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.exc.InvalidFormatException: "
                                               "Cannot deserialize value of type `com.procurement.mdm.model.dto."
                                               "data.TypeOfBuyer` from String \"SCHOOL IS NOT HOME\": value not "
                                               "one of declared Enum instance names: [NATIONAL_AGENCY, "
                                               "REGIONAL_AUTHORITY, REGIONAL_AGENCY, BODY_PUBLIC, EU_INSTITUTION, "
                                               "MINISTRY]\n at [Source: UNKNOWN; line: -1, column: -1] (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"buyer\"]->com.procurement.mdm.model.dto.data.Organizat"
                                               "ionReference[\"details\"]->com.procurement.mdm.model.dto."
                                               "data.Details[\"typeOfBuyer\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheValidValueForMainGeneralActivityField(object):
    @pytestrail.case("22153")
    def test_send_the_request_22153_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = "SOCIAL_PROTECTION"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22153")
    def test_see_the_result_in_feed_point_22153_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = "SOCIAL_PROTECTION"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22153")
    def test_check_the_buyer_details_mainGeneralActivity_field_in_the_EI_record_22153_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = "SOCIAL_PROTECTION"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result = ei_release["releases"][0]["parties"][0]["details"]["mainGeneralActivity"]
        expected_result = payload["buyer"]["details"]["mainGeneralActivity"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheInvalidValueForMainGeneralActivityFieldCantBeUsed(object):
    @pytestrail.case("22154")
    def test_send_the_request_22154_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = "SOC"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22154")
    def test_see_the_result_in_feed_point_22154_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = "SOC"
        value_of_key = payload["buyer"]["details"]["mainGeneralActivity"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": f"com.fasterxml.jackson.databind.exc.InvalidFormatException: "
                                               f"Cannot deserialize value of type `com.procurement.mdm.model.dto."
                                               f"data.MainGeneralActivity` from String \"{value_of_key}\": value "
                                               f"not one of declared Enum instance names: [DEFENCE, "
                                               f"PUBLIC_ORDER_AND_SAFETY, ECONOMIC_AND_FINANCIAL_AFFAIRS, "
                                               f"ENVIRONMENT, RECREATION_CULTURE_AND_RELIGION, EDUCATION, "
                                               f"SOCIAL_PROTECTION, HEALTH, GENERAL_PUBLIC_SERVICES, "
                                               f"HOUSING_AND_COMMUNITY_AMENITIES]\n at [Source: UNKNOWN; "
                                               f"line: -1, column: -1] (through reference chain: "
                                               f"com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]"
                                               f"->com.procurement.mdm.model.dto.data.OrganizationReference"
                                               f"[\"details\"]->com.procurement.mdm.model.dto.data.Details"
                                               f"[\"mainGeneralActivity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheValidValueForMainSectoralActivityField(object):
    @pytestrail.case("22155")
    def test_send_the_request_22155_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainSectoralActivity"] = "WATER"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22155")
    def test_see_the_result_in_feed_point_22155_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainSectoralActivity"] = "WATER"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22155")
    def test_check_the_buyer_details_mainSectoralActivity_in_the_EI_record_22155_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainSectoralActivity"] = "WATER"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        actual_result = payload["buyer"]["details"]["mainSectoralActivity"]
        expected_result = ei_release["releases"][0]["parties"][0]["details"]["mainSectoralActivity"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheInvalidValueForMainSectoralActivityFieldCantBeUsed(object):
    @pytestrail.case("22156")
    def test_send_the_request_22156_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainSectoralActivity"] = "WAT"
        value_of_key = payload["buyer"]["details"]["mainSectoralActivity"]
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22156")
    def test_see_the_result_in_feed_point_22156_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainSectoralActivity"] = "WAT"
        value_of_key = payload["buyer"]["details"]["mainSectoralActivity"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": f"com.fasterxml.jackson.databind.exc.InvalidFormatException: "
                                               f"Cannot deserialize value of type `com.procurement.mdm.model."
                                               f"dto.data.MainSectoralActivity` from String \"{value_of_key}\": "
                                               f"value not one of declared Enum instance names: "
                                               f"[EXPLORATION_EXTRACTION_GAS_OIL, ELECTRICITY, "
                                               f"POSTAL_SERVICES, PRODUCTION_TRANSPORT_DISTRIBUTION_GAS_HEAT, "
                                               f"WATER, URBAN_RAILWAY_TRAMWAY_TROLLEYBUS_BUS_SERVICES, "
                                               f"PORT_RELATED_ACTIVITIES, RAILWAY_SERVICES, "
                                               f"EXPLORATION_EXTRACTION_COAL_OTHER_SOLID_FUEL, "
                                               f"AIRPORT_RELATED_ACTIVITIES]\n at [Source: UNKNOWN; line: -1, "
                                               f"column: -1] (through reference chain: com.procurement.mdm."
                                               f"model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement."
                                               f"mdm.model.dto.data.OrganizationReference[\"details\"]->"
                                               f"com.procurement.mdm.model.dto.data.Details"
                                               f"[\"mainSectoralActivity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheCpIdOfEIisFormedCorrectly(object):
    @pytestrail.case("22157")
    def test_send_the_request_22157_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22157")
    def test_see_the_result_in_feed_point_22157_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22157")
    def test_check_the_EI_cpid_is_formed_according_to_the_pattern_22157_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        actual_result_date = get_human_date_in_utc_format(int(cpid[15:28]))[0]
        expected_result_date = message_from_kafka["data"]["operationDate"]
        actual_result_cpid_first_part = cpid[0:15]
        expected_result_cpid_first_part = "ocds-t1s2t3-MD-"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_date,
                                                         actual_result=actual_result_date)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_cpid_first_part,
                                                         actual_result=actual_result_cpid_first_part)


class TestCheckTheTimestampOfEIocidOfCoincidesWithRequestSentDate(object):
    @pytestrail.case("22158")
    def test_send_the_request_22158_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22158")
    def test_see_the_result_in_feed_point_22158_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22158")
    def test_check_the_timestamp_of_the_EI_coincides_with_the_release_date_22158_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        release_id = ei_release["releases"][0]["id"]
        timestamp = int(release_id[29:39])
        convert_timestamp_to_date = datetime.datetime.utcfromtimestamp(timestamp)
        convert_date_to_human_date = convert_timestamp_to_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        actual_result = convert_date_to_human_date
        expected_result = message_from_kafka["data"]["operationDate"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheReleaseDateCoincidesWithRequestSentDate(object):
    @pytestrail.case("22159")
    def test_send_the_request_22159_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22159")
    def test_see_the_result_in_feed_point_22159_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22159")
    def test_check_the_release_date_in_EI_record_coincides_with_the_date_of_request_22159_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        expected_result = message_from_kafka["data"]["operationDate"]
        actual_result = ei_release["releases"][0]["date"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheIdentificationOfTenderEqualsTheOCIDofTheEI(object):
    @pytestrail.case("22160")
    def test_send_the_request_22160_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22160")
    def test_see_the_result_in_feed_point_22160_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22160")
    def test_check_the_tender_id_has_the_same_value_as_cpid_of_the_EI_22160_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result = str(is_it_uuid(ei_release['releases'][0]['tender']['id'], 4))
        expected_result = "True"
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheStatusOfTTender(object):
    @pytestrail.case("22161")
    def test_send_the_request_22161_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22161")
    def test_see_the_result_in_feed_point_22161_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22161")
    def test_check_the_tender_status_value_22161_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result = ei_release["releases"][0]["tender"]["status"]
        expected_result = "planning"
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheStatusDetailsOfTheTender(object):
    @pytestrail.case("22162")
    def test_send_the_request_22162_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22162")
    def test_see_the_result_in_feed_point_22162_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22162")
    def test_checkthetender_statusDetails_value_22162_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result = ei_release["releases"][0]["tender"]["statusDetails"]
        expected_result = "empty"
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TesCheckTheBuyerIdentifierIsFormedCorrectly(object):
    @pytestrail.case("22163")
    def test_send_the_request_22163_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22163")
    def test_see_the_result_in_feed_point_22163_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22163")
    def test_checkthetender_statusDetails_value_22163_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result = ei_release["releases"][0]["buyer"]["id"]
        expected_result = payload["buyer"]["identifier"]["scheme"] + "-" + \
                          payload["buyer"]["identifier"]["id"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheBudgetIDisTenderClassificationID(object):
    @pytestrail.case("22164")
    def test_send_the_request_22164_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "24200000-6"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["classification"]["scheme"] = "CPV"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22164")
    def test_see_the_result_in_feed_point_22164_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "24200000-6"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["classification"]["scheme"] = "CPV"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22164")
    def test_check_the_budget_id_value_22164_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "24200000-6"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["classification"]["scheme"] = "CPV"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result = ei_release["releases"][0]["planning"]["budget"]["id"]
        expected_result = ei_release["releases"][0]["tender"]["classification"]["id"]
        assert compare_actual_result_and_expected_result(expected_result=payload["planning"]["budget"]["id"],
                                                         actual_result=ei_release["releases"][0]["planning"]["budget"][
                                                             "id"])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheValidValueForTheEiPlanningDates(object):
    @pytestrail.case("22165")
    def test_send_the_request_22165_1(self, country, language):
        budget_period = get_period()
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
        payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22165")
    def test_see_the_result_in_feed_point_22165_2(self, country, language):
        budget_period = get_period()
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
        payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22165")
    def test_check_the_planning_budget_startDate_and_planning_budget_endDate_in_the_EI_record_22165_3(self, country,
                                                                                                      language):
        budget_period = get_period()
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
        payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result = ei_release["releases"][0]["planning"]["budget"]["period"]["endDate"] > \
                        ei_release["releases"][0]["planning"]["budget"]["period"]["startDate"]

        actual_result_start_date = ei_release["releases"][0]["planning"]["budget"]["period"]["startDate"]
        expected_result_start_date = payload["planning"]["budget"]["period"]["startDate"]

        actual_result_end_date = ei_release["releases"][0]["planning"]["budget"]["period"]["endDate"]
        expected_result_end_date = payload["planning"]["budget"]["period"]["endDate"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result_start_date,
                                                         actual_result=actual_result_start_date)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_end_date,
                                                         actual_result=actual_result_end_date)
        assert compare_actual_result_and_expected_result(expected_result=str(True), actual_result=str(actual_result))


class TestCheckTheInvalidTypeOfPatternForValueForTheEiPlanningDates(object):
    @pytestrail.case("22166")
    def test_send_the_request_22166_1(self, country, language):
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y/%m/%dT%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(minutes=10)
        end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22166")
    def test_see_the_result_in_feed_point_22166_2(self, country, language):
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y/%m/%dT%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(minutes=10)
        end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": f"com.fasterxml.jackson.databind.JsonMappingException: "
                                               f"Text '{start_date}' could not be parsed at index 4 "
                                               f"(through reference chain: com.procurement.budget.model."
                                               f"dto.ei.request.EiCreate[\"planning\"]->com.procurement."
                                               f"budget.model.dto.ei.request.EiCreate$PlanningEiCreate"
                                               f"[\"budget\"]->com.procurement.budget.model.dto.ei.request."
                                               f"EiCreate$PlanningEiCreate$BudgetEiCreate[\"period\"]->com."
                                               f"procurement.budget.model.dto.ocds.Period[\"startDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheStartDateForPlanningBudgetDoesntExistInTheCurrentYear(object):
    @pytestrail.case("22168")
    def test_send_the_request_22168_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y-%m-34T%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(days=90)
        end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22168")
    def test_see_the_result_in_feed_point_22168_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y-%m-34T%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(days=90)
        end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": f"com.fasterxml.jackson.databind.JsonMappingException: "
                                               f"Text '{start_date}' could not be parsed: Invalid value for "
                                               f"DayOfMonth (valid values 1 - 28/31): 34 (through reference "
                                               f"chain: com.procurement.budget.model.dto.ei.request.EiCreate"
                                               f"[\"planning\"]->com.procurement.budget.model.dto.ei.request."
                                               f"EiCreate$PlanningEiCreate[\"budget\"]->com.procurement.budget."
                                               f"model.dto.ei.request.EiCreate$PlanningEiCreate$BudgetEiCreate"
                                               f"[\"period\"]->com.procurement.budget.model.dto.ocds."
                                               f"Period[\"startDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheStartDateForPlanningBudgetDoesntExist(object):
    @pytestrail.case("22169")
    def test_send_the_request_22169_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y-13-%dT%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(days=365)
        end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22169")
    def test_see_the_result_in_feed_point_22169_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y-13-%dT%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(days=365)
        end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": f"com.fasterxml.jackson.databind.JsonMappingException: "
                                               f"Text '{start_date}' could not be parsed: Invalid value for "
                                               f"MonthOfYear (valid values 1 - 12): 13 (through reference chain: "
                                               f"com.procurement.budget.model.dto.ei.request.EiCreate"
                                               f"[\"planning\"]->com.procurement.budget.model.dto.ei.request."
                                               f"EiCreate$PlanningEiCreate[\"budget\"]->com.procurement.budget."
                                               f"model.dto.ei.request.EiCreate$PlanningEiCreate$BudgetEiCreate"
                                               f"[\"period\"]->com.procurement.budget.model.dto.ocds."
                                               f"Period[\"startDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheInvalidTypeOfPatternForValueForTheEiPlanningDate(object):
    @pytestrail.case("22170")
    def test_send_the_request_22170_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(minutes=10)
        end_date = duration_date.strftime("%Y/%m/%dT%H:%M:%SZ")
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22170")
    def test_see_the_result_in_feed_point_22170_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(minutes=10)
        end_date = duration_date.strftime("%Y/%m/%dT%H:%M:%SZ")
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": f"com.fasterxml.jackson.databind.JsonMappingException: "
                                               f"Text '{end_date}' could not be parsed at index 4 (through "
                                               f"reference chain: com.procurement.budget.model.dto.ei.request."
                                               f"EiCreate[\"planning\"]->com.procurement.budget.model.dto.ei."
                                               f"request.EiCreate$PlanningEiCreate[\"budget\"]->com.procurement."
                                               f"budget.model.dto.ei.request.EiCreate$PlanningEiCreate$Budget"
                                               f"EiCreate[\"period\"]->com.procurement.budget.model.dto.ocds."
                                               f"Period[\"endDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheEndDateForPlanningBudgetThatDoesntExistInTheCurrentYear(object):
    @pytestrail.case("22171")
    def test_send_the_request_22171_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(days=90)
        end_date = duration_date.strftime("%Y-%m-34T%H:%M:%SZ")
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22171")
    def test_see_the_result_in_feed_point_22171_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(days=90)
        end_date = duration_date.strftime("%Y-%m-34T%H:%M:%SZ")
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": f"com.fasterxml.jackson.databind.JsonMappingException: "
                                               f"Text '{end_date}' could not be parsed: Invalid value for "
                                               f"DayOfMonth (valid values 1 - 28/31): 34 (through reference chain: "
                                               f"com.procurement.budget.model.dto.ei.request.EiCreate"
                                               f"[\"planning\"]->com.procurement.budget.model.dto.ei.request."
                                               f"EiCreate$PlanningEiCreate[\"budget\"]->com.procurement.budget."
                                               f"model.dto.ei.request.EiCreate$PlanningEiCreate$BudgetEiCreate"
                                               f"[\"period\"]->com.procurement.budget.model.dto.ocds.Period"
                                               f"[\"endDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheEndDateForPlanningBudgetThatDoesntExist(object):
    @pytestrail.case("22172")
    def test_send_the_request_22172_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(days=365)
        end_date = duration_date.strftime("%Y-13-%dT%H:%M:%SZ")
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22172")
    def test_see_the_result_in_feed_point_22172_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        date_now = datetime.datetime.now()
        start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
        duration_date = date_now + datetime.timedelta(days=365)
        end_date = duration_date.strftime("%Y-13-%dT%H:%M:%SZ")
        payload["planning"]["budget"]["period"]["startDate"] = start_date
        payload["planning"]["budget"]["period"]["endDate"] = end_date
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": f"com.fasterxml.jackson.databind.JsonMappingException: "
                                               f"Text '{end_date}' could not be parsed: Invalid value for "
                                               f"MonthOfYear (valid values 1 - 12): 13 (through reference chain: "
                                               f"com.procurement.budget.model.dto.ei.request.EiCreate[\"planning\"]"
                                               f"->com.procurement.budget.model.dto.ei.request.EiCreate$"
                                               f"PlanningEiCreate[\"budget\"]->com.procurement.budget.model."
                                               f"dto.ei.request.EiCreate$PlanningEiCreate$BudgetEiCreate"
                                               f"[\"period\"]->com.procurement.budget.model.dto.ocds."
                                               f"Period[\"endDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckClassificationIdIsSentCorrectly(object):
    @pytestrail.case("22173")
    def test_send_the_request_22173_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "45100000-8"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22173")
    def test_see_the_result_in_feed_point_22173_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "45100000-8"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22173")
    def test_check_the_tender_classification_id_has_the_value_sent_in_the_request_22173_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "45100000-8"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result = ei_release["releases"][0]["tender"]["classification"]["id"]
        expected_result = payload["tender"]["classification"]["id"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckClassificationIdUsesZeroesAfterFourthDigit(object):
    @pytestrail.case("22174")
    def test_send_the_request_22174_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "03110000-5"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22174")
    def test_see_the_result_in_feed_point_22174_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "03110000-5"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00.05",
                                "description": "Invalid CPV."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheTagHasAppropriateValueInTheEiRecord(object):
    @pytestrail.case("22175")
    def test_send_the_request_22175_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22175")
    def test_see_the_result_in_feed_point_22175_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22175")
    def test_CheckTheTagAttributeInTheEirecord_22175_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result = ei_release["releases"][0]["tag"][0]
        expected_result = "compiled"
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheDateHasAppropriateValueInTheEiRecord(object):
    @pytestrail.case("22176")
    def test_send_the_request_22176_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22176")
    def test_see_the_result_in_feed_point_22176_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22176")
    def test_check_the_release_date_field_in_theEirecord_22176_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result = ei_release["releases"][0]["date"]
        expected_result = message_from_kafka["data"]["operationDate"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheInitiationTypeHasAnAppropriateValueInTheEiRecord(object):
    @pytestrail.case("22178")
    def test_send_the_request_22178_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22178")
    def test_see_the_result_in_feed_point_22178_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22178")
    def test_Check_the_initiationType_field_in_the_Ei_record_22178_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result = ei_release["releases"][0]["initiationType"]
        expected_result = "tender"
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckThePlanningSectionInTheEiRecord(object):
    @pytestrail.case("22181")
    def test_send_the_request_22181_1(self, country, language):
        budget_period = get_period()
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
        payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
        payload["tender"]["classification"]["id"] = "45100000-8"
        payload['planning']['budget']['id'] = payload['tender']['classification']['id']
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22181")
    def test_see_the_result_in_feed_point_22181_2(self, country, language):
        budget_period = get_period()
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
        payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
        payload["tender"]["classification"]["id"] = "45100000-8"
        payload['planning']['budget']['id'] = payload['tender']['classification']['id']
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22181")
    def test_check_the_planning_section_in_the_EI_record_22181_3(self, country, language):
        budget_period = get_period()
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
        payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
        payload["tender"]["classification"]["id"] = "45100000-8"
        payload['planning']['budget']['id'] = payload['tender']['classification']['id']
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result_budget_id = ei_release["releases"][0]["planning"]["budget"]["id"]
        expected_result_budget_id = payload["tender"]["classification"]["id"]
        actual_result_period_start_date = ei_release["releases"][0]["planning"]["budget"]["period"]["startDate"]
        expected_result_period_start_date = payload["planning"]["budget"]["period"]["startDate"]
        actual_result_period_end_date = ei_release["releases"][0]["planning"]["budget"]["period"]["endDate"]
        expected_result_period_end_date = payload["planning"]["budget"]["period"]["endDate"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result_budget_id,
                                                         actual_result=actual_result_budget_id)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_period_start_date,
                                                         actual_result=actual_result_period_start_date)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_period_end_date,
                                                         actual_result=actual_result_period_end_date)


class TestCheckTheTenderSectionInTheEiRecord(object):
    @pytestrail.case("22182")
    def test_send_the_request_22182_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["title"] = "This is some text for field"
        payload["tender"]["description"] = "This is some text for field 22 orange"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22182")
    def test_see_the_result_in_feed_point_22182_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["title"] = "This is some text for field"
        payload["tender"]["description"] = "This is some text for field 22 orange"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22182")
    def test_check_the_tender_section_and_compare_with_sent_data_in_the_request_22182_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["title"] = "This is some text for field"
        payload["tender"]["description"] = "This is some text for field 22 orange"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result_tender_title = ei_release["releases"][0]["tender"]["title"]
        expected_result_tender_title = payload["tender"]["title"]
        actual_result_tender_classification_id = ei_release["releases"][0]["tender"]["classification"]["id"]
        expected_result_tender_classification_id = payload["tender"]["classification"]["id"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result_tender_title,
                                                         actual_result=actual_result_tender_title)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_tender_classification_id,
                                                         actual_result=actual_result_tender_classification_id)


class TestCheckTheBuyerSectionInTheEiRecord(object):
    @pytestrail.case("22183")
    def test_send_the_request_22183_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload['buyer']['name'] = 'Peter Alekseevich'
        payload['buyer']['identifier']['id'] = '5_channel'
        payload['buyer']['identifier']['scheme'] = 'MD-IDNO'
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22183")
    def test_see_the_result_in_feed_point_22183_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload['buyer']['name'] = 'Peter Alekseevich'
        payload['buyer']['identifier']['id'] = '5_channel'
        payload['buyer']['identifier']['scheme'] = 'MD-IDNO'
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22183")
    def test_check_the_release_parties_section_22183_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload['buyer']['name'] = 'Peter Alekseevich'
        payload['buyer']['identifier']['id'] = '5_channel'
        payload['buyer']['identifier']['scheme'] = 'MD-IDNO'
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        actual_result_parties_id = ei_release["releases"][0]["parties"][0]["id"]
        expected_result_parties_id = payload["buyer"]["identifier"]["scheme"] + "-" + \
                                     payload["buyer"]["identifier"]["id"]
        actual_result_parties_role = ei_release["releases"][0]["parties"][0]["roles"][0]
        expected_result_parties_role = "buyer"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_parties_id,
                                                         actual_result=actual_result_parties_id)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_parties_role,
                                                         actual_result=actual_result_parties_role)


class TestCheckTheOtherRolesAreIgnoredInTheEiCreationRequest(object):
    @pytestrail.case("22184")
    def test_send_the_request_22184_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        procuring_entity = {
            "name": "Procuring Entity Name",
            "identifier": {
                "id": "444444444444",
                "scheme": "MD-IDNO",
                "legalName": "Legal Name",
                "uri": "http://454.to"
            },
            "address": {
                "streetAddress": "street",
                "postalCode": "785412",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "3400000"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": ""
                    }
                }
            },
            "additionalIdentifiers": [
                {
                    "id": "additional identifier",
                    "scheme": "MD-K",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }
            ],
            "contactPoint": {
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87",
                "faxNumber": "78-56-55",
                "url": "http://url.com"
            }
        }
        payload.update({"procuringEntity": procuring_entity})
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22184")
    def test_see_the_result_in_feed_point_22184_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        procuring_entity = {
            "name": "Procuring Entity Name",
            "identifier": {
                "id": "444444444444",
                "scheme": "MD-IDNO",
                "legalName": "Legal Name",
                "uri": "http://454.to"
            },
            "address": {
                "streetAddress": "street",
                "postalCode": "785412",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "3400000"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": ""
                    }
                }
            },
            "additionalIdentifiers": [
                {
                    "id": "additional identifier",
                    "scheme": "MD-K",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }
            ],
            "contactPoint": {
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87",
                "faxNumber": "78-56-55",
                "url": "http://url.com"
            }
        }
        payload.update({"procuringEntity": procuring_entity})
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22184")
    def test_check_the_release_parties_section_22184_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        procuring_entity = {
            "name": "Procuring Entity Name",
            "identifier": {
                "id": "444444444444",
                "scheme": "MD-IDNO",
                "legalName": "Legal Name",
                "uri": "http://454.to"
            },
            "address": {
                "streetAddress": "street",
                "postalCode": "785412",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": "3400000"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "3401000",
                        "description": ""
                    }
                }
            },
            "additionalIdentifiers": [
                {
                    "id": "additional identifier",
                    "scheme": "MD-K",
                    "legalName": "legalname",
                    "uri": "http://k.to"
                }
            ],
            "contactPoint": {
                "name": "contact person",
                "email": "string@mail.ccc",
                "telephone": "98-79-87",
                "faxNumber": "78-56-55",
                "url": "http://url.com"
            }
        }
        payload.update({"procuringEntity": procuring_entity})
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        parties_obj_list = list()
        for p in ei_release["releases"][0]["parties"]:
            if p["roles"] == ["procuringEntity"]:
                parties_obj_list.append(p)
        for p in ei_release["releases"][0]["parties"]:
            if p["roles"] == ["buyer"]:
                parties_obj_list.append(p)

        parties_obj_dict = dict(parties_obj_list[0])
        actual_result_procuring_entity_role = ["procuringEntity"] in parties_obj_dict.values()
        actual_result_buyer_role = ["buyer"] in parties_obj_dict.values()
        assert compare_actual_result_and_expected_result(expected_result=str(False),
                                                         actual_result=str(actual_result_procuring_entity_role))
        assert compare_actual_result_and_expected_result(expected_result=str(True),
                                                         actual_result=str(actual_result_buyer_role))


class TestCheckTheBuyerSectionInTheEiRecord(object):
    @pytestrail.case("22185")
    def test_send_the_request_22185_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22185")
    def test_see_the_result_in_feed_point_22185_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22185")
    def test_check_the_release_buyer_section_22185_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()

        actual_result_buyer_id = ei_release["releases"][0]["buyer"]["id"]
        expected_result_buyer_id = payload["buyer"]["identifier"]["scheme"] + "-" + \
                                   payload["buyer"]["identifier"]["id"]
        actual_result_buyer_name = ei_release["releases"][0]["buyer"]["name"]
        expected_result_buyer_name = payload["buyer"]["name"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result_buyer_id,
                                                         actual_result=actual_result_buyer_id)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_buyer_name,
                                                         actual_result=actual_result_buyer_name)


class TestCheckTheFieldsWithEmptyStringsAreNotPublishedInThePublicPoint(object):
    @pytestrail.case("22186")
    def test_tender_title_as_empty_string_22186_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["title"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'tender.title' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_description_as_empty_string_22186_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'tender.description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_planningrationaleasemptystring_22186_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["rationale"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'planning.rationale' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_name_as_emptystring_22186_4(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["name"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.name' is "
                                               "empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_identifier_id_as_empty_string_22186_5(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'buyer.identifier.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_identifier_legalName_as_empty_string_22186_6(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["legalName"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute "
                                               "'buyer.identifier.legalName' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_identifier_uri_as_empty_string_22186_7(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["uri"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.identifier.uri' "
                                               "is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_streetAddress_as_empty_string_22186_8(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["streetAddress"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "streetAddress' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_postalCode_as_empty_string_22186_9(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["postalCode"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "postalCode' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_addressDetails_locality_scheme_as_empty_string_22186_10(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "addressDetails.locality.scheme' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_addressDetails_locality_id_as_empty_string_22186_11(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "addressDetails.locality.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_addressDetails_locality_description_as_empty_string_22186_12(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "addressDetails.locality.description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_additionalIdentifiers_id_as_empty_string_22186_13(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer."
                                               "additionalIdentifiers.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_additionalIdentifiers_scheme_as_empty_string_22186_14(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["scheme"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer."
                                               "additionalIdentifiers.scheme' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_additionalIdentifiers_legalName_as_empty_string_22186_15(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["legalName"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.additional"
                                               "Identifiers.legalName' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_additionalIdentifiers_uri_as_empty_string_22186_16(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["uri"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute "
                                               "'buyer.additionalIdentifiers.uri' is empty "
                                               "or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_contactPoint_name_as_empty_string_22186_17(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["name"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "name' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_contactPoint_email_as_empty_string_22186_18(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["email"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "email' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_contactPoint_telephone_as_empty_string_22186_19(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["telephone"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "telephone' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_contactPoint_faxNumber_as_empty_string_22186_20(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["faxNumber"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "faxNumber' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_contactPoint_url_as_empty_string_22186_21(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["faxNumber"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "faxNumber' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_deliveryAddress_streetAddress_as_empty_string_22186_22(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "deliveryAddress.streetAddress' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_deliveryAddress_postalCode_as_empty_string_22186_23(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "deliveryAddress.postalCode' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_deliveryAddress_addressDetails_locality_scheme_as_empty_string_22186_24(self, country,
                                                                                                  language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                               "addressDetails.locality.scheme' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_deliveryAddress_addressDetails_locality_id_as_empty_string_22186_25(self, country,
                                                                                              language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                               "addressDetails.locality.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_deliveryAddress_addressDetails_locality_description_as_empty_string_22186_26(self, country,
                                                                                                       language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                               "addressDetails.locality.description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_description_as_empty_string_22186_27(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_classification_id_as_empty_string_22186_28(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_classification_id_as_empty_string_22186_29(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.03", "description": "Invalid cpv code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_additionalClassifications_id_as_empty_string_22186_30(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.05", "description": "Invalid cpvs code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_deliveryAddress_addressDetails_country_id_as_empty_string_22186_31(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.10", "description": "Invalid country. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_deliveryAddress_addressDetails_region_id_as_empty_string_22186_32(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.13", "description": "Region not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_quantity_as_empty_string_22186_33(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["quantity"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                               "procurement.mdm.exception.InErrorException) (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]"
                                               "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]"
                                               "->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Item[\"quantity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_ender_items_unit_id_as_empty_string_22186_34(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.06", "description": "Invalid unit code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_planning_budget_period_startDate_as_empty_string_22186_35(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.06", "description": "Invalid unit code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_planning_budget_period_endDate_as_empty_string_22186_36(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["endDate"] = ""
        value_of_key = payload["planning"]["budget"]["period"]["endDate"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": f"com.fasterxml.jackson.databind.JsonMappingException: "
                                               f"Text '{value_of_key}' could not be parsed at index 0 "
                                               f"(through reference chain: com.procurement.budget.model."
                                               f"dto.ei.request.EiCreate[\"planning\"]->com.procurement."
                                               f"budget.model.dto.ei.request.EiCreate$PlanningEiCreate"
                                               f"[\"budget\"]->com.procurement.budget.model.dto.ei.request."
                                               f"EiCreate$PlanningEiCreate$BudgetEiCreate[\"period\"]->com."
                                               f"procurement.budget.model.dto.ocds.Period[\"endDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_identifier_scheme_as_empty_string_22186_37(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["scheme"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.12", "description": "Registration scheme not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_addressDetails_country_id_as_empty_string_22186_38(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.11", "description": "Country not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_addressDetails_region_id_as_empty_string_22186_39(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.13", "description": "Region not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_details_typeOfBuyer_as_empty_string_22186_40(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["typeOfBuyer"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.exc.InvalidFormatException: "
                                               "Cannot deserialize value of type `com.procurement.mdm.model."
                                               "dto.data.TypeOfBuyer` from String \"\": value not one of "
                                               "declared Enum instance names: [NATIONAL_AGENCY, "
                                               "REGIONAL_AUTHORITY, REGIONAL_AGENCY, BODY_PUBLIC, EU_INSTITUTION, "
                                               "MINISTRY]\n at [Source: UNKNOWN; line: -1, column: -1] (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"details\"]->com.procurement.mdm.model."
                                               "dto.data.Details[\"typeOfBuyer\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_details_mainGeneralActivity_as_empty_string_22186_41(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.exc.InvalidFormatException: "
                                               "Cannot deserialize value of type `com.procurement.mdm.model."
                                               "dto.data.MainGeneralActivity` from String \"\": value not one "
                                               "of declared Enum instance names: [DEFENCE, PUBLIC_ORDER_AND_"
                                               "SAFETY, ECONOMIC_AND_FINANCIAL_AFFAIRS, ENVIRONMENT, RECREATION_"
                                               "CULTURE_AND_RELIGION, EDUCATION, SOCIAL_PROTECTION, HEALTH, "
                                               "GENERAL_PUBLIC_SERVICES, HOUSING_AND_COMMUNITY_AMENITIES]\n "
                                               "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"buyer\"]->com.procurement.mdm.model.dto.data.Organization"
                                               "Reference[\"details\"]->com.procurement.mdm.model.dto.data."
                                               "Details[\"mainGeneralActivity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_details_mainSectoralActivity_as_empty_string_22186_42(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainSectoralActivity"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.exc.InvalidFormatException: "
                                               "Cannot deserialize value of type `com.procurement.mdm.model."
                                               "dto.data.MainSectoralActivity` from String \"\": value not one "
                                               "of declared Enum instance names: [EXPLORATION_EXTRACTION_GAS_OIL, "
                                               "ELECTRICITY, POSTAL_SERVICES, PRODUCTION_TRANSPORT_DISTRIBUTION_"
                                               "GAS_HEAT, WATER, URBAN_RAILWAY_TRAMWAY_TROLLEYBUS_BUS_SERVICES, "
                                               "PORT_RELATED_ACTIVITIES, RAILWAY_SERVICES, EXPLORATION_EXTRACTION_"
                                               "COAL_OTHER_SOLID_FUEL, AIRPORT_RELATED_ACTIVITIES]\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com."
                                               "procurement.mdm.model.dto.data.OrganizationReference[\"details\"]"
                                               "->com.procurement.mdm.model.dto.data.Details"
                                               "[\"mainSectoralActivity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckThePossibilityToFetXtokenAndCpidAfterEiCreation(object):
    @pytestrail.case("22830")
    def test_send_the_request_22830_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22830")
    def test_see_the_result_in_feed_point_22830_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheImpossibilityToCreateEiWithBooleanValueAsTheCpvCode(object):
    @pytestrail.case("22833")
    def test_send_the_request_22833_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22833")
    def test_see_the_result_in_feed_point_22833_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                               "procurement.mdm.exception.InErrorException) (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]"
                                               "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender"
                                               "[\"classification\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Classification[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheImpossibilityToCreateEiWithEmptyValueInaCpvCode(object):
    @pytestrail.case("22834")
    def test_send_the_request_22834_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22834")
    def test_see_the_result_in_feed_point_22834_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.06", "description": "Cpv code not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheImpossibilityToCreateEiWithBooleanTypeAsTheCpv(object):
    @pytestrail.case("22835")
    def test_send_the_request_22835_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22835")
    def test_see_the_result_in_feed_point_22835_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender[\"classification\"]->com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest$Tender$Classification[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheImpossibilityToCreateEiWithTheIncorrectCpv(object):
    @pytestrail.case("22836")
    def test_send_the_request_22836_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "86655566"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22836")
    def test_see_the_result_in_feed_point_22836_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "86655566"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.06", "description": "Cpv code not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheMainProcurementCategoryIsSetCorrectlyGoods(object):
    @pytestrail.case("22837")
    def test_send_the_request_22837_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "24200000-6"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22837")
    def test_see_the_result_in_feed_point_22837_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "24200000-6"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22837")
    def test_Check_the_attribute_records_compiledRelease_tender_mainProcurementCategory_22837_3(self, country,
                                                                                                language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "24200000-6"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        ei_url = message_from_kafka["data"]["url"]
        ei_record = requests.get(url=ei_url).json()
        actual_result = ei_record["records"][0]["compiledRelease"]["tender"]["mainProcurementCategory"]
        expected_result = "goods"
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheMainProcurementCategoryIsSetCorrectlyWorks(object):
    @pytestrail.case("22838")
    def test_send_the_request_22838_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "45100000-8"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22838")
    def test_see_the_result_in_feed_point_22838_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "45100000-8"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22838")
    def test_Check_the_attribute_records_compiledRelease_tender_mainProcurementCategory_22838_3(self, country,
                                                                                                language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "45100000-8"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        ei_url = message_from_kafka["data"]["url"]
        ei_record = requests.get(url=ei_url).json()
        actual_result = ei_record["records"][0]["compiledRelease"]["tender"]["mainProcurementCategory"]
        expected_result = "works"
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheMainProcurementCategoryIsSetCorrectlyServices(object):
    @pytestrail.case("22839")
    def test_send_the_request_22839_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "76100000-4"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22839")
    def test_see_the_result_in_feed_point_22839_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "76100000-4"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22839")
    def test_Check_the_attribute_records_compiledRelease_tender_mainProcurementCategory_22839_3(self, country,
                                                                                                language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "76100000-4"
        payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
        payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        ei_url = message_from_kafka["data"]["url"]
        ei_record = requests.get(url=ei_url).json()
        actual_result = ei_record["records"][0]["compiledRelease"]["tender"]["mainProcurementCategory"]
        expected_result = "services"
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckTheCountryIdIsSetsCorrectly(object):
    @pytestrail.case("22840")
    def test_send_the_request_22840_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22840")
    def test_see_the_result_in_feed_point_22840_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22840")
    def test_check_the_attribute_in_parties_address_addressDetails_country_id_22840_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        ei_url = message_from_kafka["data"]["url"]
        ei_record = requests.get(url=ei_url).json()
        actual_result = ei_record["records"][0]["compiledRelease"]["parties"][0]["address"]["addressDetails"][
            "country"]["id"]
        assert compare_actual_result_and_expected_result(expected_result="MD", actual_result=actual_result)


class TestCheckTheCountrySchemeIsSetsCorrectly(object):
    @pytestrail.case("22841")
    def test_send_the_request_22841_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22841")
    def test_see_the_result_in_feed_point_22841_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22841")
    def test_check_the_attribute_in_parties_address_addressDetails_country_scheme_22841_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        ei_url = message_from_kafka["data"]["url"]
        ei_record = requests.get(url=ei_url).json()
        actual_result = ei_record["records"][0]["compiledRelease"]["parties"][0]["address"]["addressDetails"][
            "country"]["scheme"]
        assert compare_actual_result_and_expected_result(expected_result="iso-alpha2", actual_result=actual_result)


class TestCheckTheCountryDescriptionIsSetsCorrectly(object):
    @pytestrail.case("22842")
    def test_send_the_request_22842_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22842")
    def test_see_the_result_in_feed_point_22842_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22842")
    def test_check_the_attribute_in_parties_address_addressDetails_country_description_22842_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        ei_url = message_from_kafka["data"]["url"]
        ei_record = requests.get(url=ei_url).json()
        actual_result = ei_record["records"][0]["compiledRelease"]["parties"][0]["address"]["addressDetails"][
            "country"]["description"]
        assert compare_actual_result_and_expected_result(expected_result="Moldova, Republica",
                                                         actual_result=actual_result)


class TestCheckTheCountryUriIsSetsCorrectly(object):
    @pytestrail.case("22843")
    def test_send_the_request_22843_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22843")
    def test_see_the_result_in_feed_point_22843_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22843")
    def test_check_the_attribute_in_parties_address_addressDetails_country_uri_22843_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        ei_url = message_from_kafka["data"]["url"]
        ei_record = requests.get(url=ei_url).json()
        actual_result = ei_record["records"][0]["compiledRelease"]["parties"][0]["address"]["addressDetails"][
            "country"]["uri"]
        assert compare_actual_result_and_expected_result(expected_result="https://www.iso.org",
                                                         actual_result=actual_result)


class TestCheckOnPossibilityToCreateEiWithFullDataModel(object):
    @pytestrail.case("22908")
    def test_send_the_request_22908_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22908")
    def test_see_the_result_in_feed_point_22908_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22908")
    def test_check_the_attributes_of_the_expenditure_item_on_PublicPoint_22908_3(self, country, language):
        instance = choose_instance()
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["uri"] = "test fro uri"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei_release_timestamp = int(ei_release["releases"][0]["id"][29:42])
        convert_timestamp_to_date = get_human_date_in_utc_format(ei_release_timestamp)
        keys_list = list()
        for i in ei_release.keys():
            if i == "uri":
                keys_list.append(i)
            if i == "version":
                keys_list.append(i)
            if i == "extensions":
                keys_list.append(i)
            if i == "publisher":
                keys_list.append(i)
            if i == "license":
                keys_list.append(i)
            if i == "publicationPolicy":
                keys_list.append(i)
            if i == "publishedDate":
                keys_list.append(i)
            if i == "releases":
                keys_list.append(i)
        for i in ei_release["publisher"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0].keys():
            if i == "ocid":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "date":
                keys_list.append(i)
            if i == "tag":
                keys_list.append(i)
            if i == "language":
                keys_list.append(i)
            if i == "initiationType":
                keys_list.append(i)
            if i == "tender":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "title":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "status":
                keys_list.append(i)
            if i == "statusDetails":
                keys_list.append(i)
            if i == "items":
                keys_list.append(i)
            if i == "mainProcurementCategory":
                keys_list.append(i)
            if i == "classification":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0].keys():
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "classification":
                keys_list.append(i)
            if i == "additionalClassifications":
                keys_list.append(i)
            if i == "quantity":
                keys_list.append(i)
            if i == "unit":
                keys_list.append(i)
            if i == "deliveryAddress":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["classification"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["unit"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"].keys():
            if i == "streetAddress":
                keys_list.append(i)
            if i == "postalCode":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"].keys():
            if i == "country":
                keys_list.append(i)
            if i == "region":
                keys_list.append(i)
            if i == "locality":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
            "locality"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["classification"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
        for i in ei_release["releases"][0]["buyer"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
        for i in ei_release["releases"][0]["parties"][0].keys():
            if i == "id":
                keys_list.append(i)
            if i == "name":
                keys_list.append(i)
            if i == "identifier":
                keys_list.append(i)
            if i == "address":
                keys_list.append(i)
            if i == "additionalIdentifiers":
                keys_list.append(i)
            if i == "contactPoint":
                keys_list.append(i)
            if i == "details":
                keys_list.append(i)
            if i == "roles":
                keys_list.append(i)
        for i in ei_release["releases"][0]["parties"][0]["identifier"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0]["parties"][0]["address"].keys():
            if i == "streetAddress":
                keys_list.append(i)
            if i == "postalCode":
                keys_list.append(i)
            if i == "addressDetails":
                keys_list.append(i)
        for i in ei_release["releases"][0]["parties"][0]["address"]["addressDetails"].keys():
            if i == "country":
                keys_list.append(i)
            if i == "region":
                keys_list.append(i)
            if i == "locality":
                keys_list.append(i)
        for i in ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0]["parties"][0]["additionalIdentifiers"][0].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "legalName":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0]["parties"][0]["contactPoint"].keys():
            if i == "name":
                keys_list.append(i)
            if i == "email":
                keys_list.append(i)
            if i == "telephone":
                keys_list.append(i)
            if i == "faxNumber":
                keys_list.append(i)
            if i == "url":
                keys_list.append(i)
        for i in ei_release["releases"][0]["parties"][0]["details"].keys():
            if i == "typeOfBuyer":
                keys_list.append(i)
            if i == "mainGeneralActivity":
                keys_list.append(i)
            if i == "mainSectoralActivity":
                keys_list.append(i)
        for i in ei_release["releases"][0]["planning"].keys():
            if i == "budget":
                keys_list.append(i)
            if i == "rationale":
                keys_list.append(i)
        for i in ei_release["releases"][0]["planning"]["budget"].keys():
            if i == "id":
                keys_list.append(i)
            if i == "period":
                keys_list.append(i)
        for i in ei_release["releases"][0]["planning"]["budget"]["period"].keys():
            if i == "startDate":
                keys_list.append(i)
            if i == "endDate":
                keys_list.append(i)
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[0])
        assert compare_actual_result_and_expected_result(expected_result="version", actual_result=keys_list[1])
        assert compare_actual_result_and_expected_result(expected_result="extensions", actual_result=keys_list[2])
        assert compare_actual_result_and_expected_result(expected_result="publisher", actual_result=keys_list[3])
        assert compare_actual_result_and_expected_result(expected_result="license", actual_result=keys_list[4])
        assert compare_actual_result_and_expected_result(expected_result="publicationPolicy",
                                                         actual_result=keys_list[5])
        assert compare_actual_result_and_expected_result(expected_result="publishedDate", actual_result=keys_list[6])
        assert compare_actual_result_and_expected_result(expected_result="releases", actual_result=keys_list[7])
        assert compare_actual_result_and_expected_result(expected_result="name", actual_result=keys_list[8])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[9])
        assert compare_actual_result_and_expected_result(expected_result="ocid", actual_result=keys_list[10])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[11])
        assert compare_actual_result_and_expected_result(expected_result="date", actual_result=keys_list[12])
        assert compare_actual_result_and_expected_result(expected_result="tag", actual_result=keys_list[13])
        assert compare_actual_result_and_expected_result(expected_result="language", actual_result=keys_list[14])
        assert compare_actual_result_and_expected_result(expected_result="initiationType", actual_result=keys_list[15])
        assert compare_actual_result_and_expected_result(expected_result="tender", actual_result=keys_list[16])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[17])
        assert compare_actual_result_and_expected_result(expected_result="title", actual_result=keys_list[18])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[19])
        assert compare_actual_result_and_expected_result(expected_result="status", actual_result=keys_list[20])
        assert compare_actual_result_and_expected_result(expected_result="statusDetails", actual_result=keys_list[21])
        assert compare_actual_result_and_expected_result(expected_result="items", actual_result=keys_list[22])
        assert compare_actual_result_and_expected_result(expected_result="mainProcurementCategory",
                                                         actual_result=keys_list[23])
        assert compare_actual_result_and_expected_result(expected_result="classification", actual_result=keys_list[24])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[25])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[26])
        assert compare_actual_result_and_expected_result(expected_result="classification", actual_result=keys_list[27])
        assert compare_actual_result_and_expected_result(expected_result="additionalClassifications",
                                                         actual_result=keys_list[28])
        assert compare_actual_result_and_expected_result(expected_result="quantity", actual_result=keys_list[29])
        assert compare_actual_result_and_expected_result(expected_result="unit", actual_result=keys_list[30])
        assert compare_actual_result_and_expected_result(expected_result="deliveryAddress", actual_result=keys_list[31])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[32])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[33])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[34])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[35])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[36])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[37])
        assert compare_actual_result_and_expected_result(expected_result="name", actual_result=keys_list[38])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[39])
        assert compare_actual_result_and_expected_result(expected_result="streetAddress", actual_result=keys_list[40])
        assert compare_actual_result_and_expected_result(expected_result="postalCode", actual_result=keys_list[41])
        assert compare_actual_result_and_expected_result(expected_result="country", actual_result=keys_list[42])
        assert compare_actual_result_and_expected_result(expected_result="region", actual_result=keys_list[43])
        assert compare_actual_result_and_expected_result(expected_result="locality", actual_result=keys_list[44])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[45])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[46])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[47])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[48])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[49])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[50])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[51])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[52])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[53])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[54])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[55])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[56])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[57])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[58])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[59])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[60])
        assert compare_actual_result_and_expected_result(expected_result="name", actual_result=keys_list[61])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[62])
        assert compare_actual_result_and_expected_result(expected_result="name", actual_result=keys_list[63])
        assert compare_actual_result_and_expected_result(expected_result="identifier", actual_result=keys_list[64])
        assert compare_actual_result_and_expected_result(expected_result="address", actual_result=keys_list[65])
        assert compare_actual_result_and_expected_result(expected_result="additionalIdentifiers",
                                                         actual_result=keys_list[66])
        assert compare_actual_result_and_expected_result(expected_result="contactPoint", actual_result=keys_list[67])
        assert compare_actual_result_and_expected_result(expected_result="details", actual_result=keys_list[68])
        assert compare_actual_result_and_expected_result(expected_result="roles", actual_result=keys_list[69])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[70])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[71])
        assert compare_actual_result_and_expected_result(expected_result="legalName", actual_result=keys_list[72])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[73])
        assert compare_actual_result_and_expected_result(expected_result="streetAddress", actual_result=keys_list[74])
        assert compare_actual_result_and_expected_result(expected_result="postalCode", actual_result=keys_list[75])
        assert compare_actual_result_and_expected_result(expected_result="addressDetails", actual_result=keys_list[76])
        assert compare_actual_result_and_expected_result(expected_result="country", actual_result=keys_list[77])
        assert compare_actual_result_and_expected_result(expected_result="region", actual_result=keys_list[78])
        assert compare_actual_result_and_expected_result(expected_result="locality", actual_result=keys_list[79])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[80])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[81])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[82])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[83])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[84])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[85])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[86])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[87])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[88])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[89])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[90])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[91])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[92])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[93])
        assert compare_actual_result_and_expected_result(expected_result="legalName", actual_result=keys_list[94])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[95])
        assert compare_actual_result_and_expected_result(expected_result="name", actual_result=keys_list[96])
        assert compare_actual_result_and_expected_result(expected_result="email", actual_result=keys_list[97])
        assert compare_actual_result_and_expected_result(expected_result="telephone", actual_result=keys_list[98])
        assert compare_actual_result_and_expected_result(expected_result="faxNumber", actual_result=keys_list[99])
        assert compare_actual_result_and_expected_result(expected_result="url", actual_result=keys_list[100])
        assert compare_actual_result_and_expected_result(expected_result="typeOfBuyer", actual_result=keys_list[101])
        assert compare_actual_result_and_expected_result(expected_result="mainGeneralActivity",
                                                         actual_result=keys_list[102])
        assert compare_actual_result_and_expected_result(expected_result="mainSectoralActivity",
                                                         actual_result=keys_list[103])
        assert compare_actual_result_and_expected_result(expected_result="budget", actual_result=keys_list[104])
        assert compare_actual_result_and_expected_result(expected_result="rationale", actual_result=keys_list[105])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[106])
        assert compare_actual_result_and_expected_result(expected_result="period", actual_result=keys_list[107])
        assert compare_actual_result_and_expected_result(expected_result="startDate", actual_result=keys_list[108])
        assert compare_actual_result_and_expected_result(expected_result="endDate", actual_result=keys_list[109])

        assert compare_actual_result_and_expected_result(
            expected_result=f"http://dev.public.eprocurement.systems/budgets/{cpid}/{cpid}",
            actual_result=ei_release["uri"])
        assert compare_actual_result_and_expected_result(expected_result="666", actual_result=ei_release["version"])
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/"
                            "extension.json", actual_result=ei_release["extensions"][0])
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/"
                            "extension.js222", actual_result=ei_release["extensions"][1])
        assert compare_actual_result_and_expected_result(
            expected_result=instance.upper() + "-ENV", actual_result=ei_release["publisher"]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.ustudio.com", actual_result=ei_release["publisher"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/222", actual_result=ei_release["license"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/222", actual_result=ei_release["publicationPolicy"])
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"], actual_result=ei_release["publishedDate"])
        assert compare_actual_result_and_expected_result(
            expected_result=cpid, actual_result=ei_release["releases"][0]["ocid"])
        assert compare_actual_result_and_expected_result(
            expected_result=cpid, actual_result=ei_release["releases"][0]["id"][0:28])
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"], actual_result=convert_timestamp_to_date[0])
        assert compare_actual_result_and_expected_result(expected_result=message_from_kafka["data"]["operationDate"],
                                                         actual_result=ei_release["releases"][0]["date"])
        assert compare_actual_result_and_expected_result(expected_result="compiled",
                                                         actual_result=ei_release["releases"][0]["tag"][0])
        assert compare_actual_result_and_expected_result(expected_result=language,
                                                         actual_result=ei_release["releases"][0]["language"])
        assert compare_actual_result_and_expected_result(expected_result="tender",
                                                         actual_result=ei_release["releases"][0]["initiationType"])
        assert compare_actual_result_and_expected_result(expected_result=str(True), actual_result=str(is_it_uuid(
            ei_release["releases"][0]["tender"]["id"], 4)))
        assert compare_actual_result_and_expected_result(expected_result=payload["tender"]["title"],
                                                         actual_result=ei_release["releases"][0]["tender"]["title"])
        assert compare_actual_result_and_expected_result(expected_result=payload["tender"]["description"],
                                                         actual_result=ei_release["releases"][0]["tender"][
                                                             "description"])
        assert compare_actual_result_and_expected_result(expected_result="planning",
                                                         actual_result=ei_release["releases"][0]["tender"]["status"])
        assert compare_actual_result_and_expected_result(expected_result="empty",
                                                         actual_result=ei_release["releases"][0]["tender"][
                                                             "statusDetails"])
        assert compare_actual_result_and_expected_result(expected_result=str(True), actual_result=str(is_it_uuid(
            ei_release["releases"][0]["tender"]["items"][0]["id"], 4)))
        assert compare_actual_result_and_expected_result(expected_result=payload["tender"]["items"][0]["description"],
                                                         actual_result=ei_release["releases"][0]["tender"]["items"][0][
                                                             "description"])
        assert compare_actual_result_and_expected_result(expected_result="CPV", actual_result=ei_release[
            "releases"][0]["tender"]["items"][0]["classification"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["classification"]["id"], actual_result=ei_release[
                "releases"][0]["tender"]["items"][0]["classification"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Lucrări de pregătire a şantierului", actual_result=ei_release[
                "releases"][0]["tender"]["items"][0]["classification"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="CPVS",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["additionalClassifications"][0]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Oţel carbon",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
                "description"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["quantity"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["quantity"])
        assert compare_actual_result_and_expected_result(
            expected_result="Parsec", actual_result=ei_release["releases"][0]["tender"]["items"][0]["unit"]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["unit"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["unit"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["streetAddress"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["postalCode"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["postalCode"])
        assert compare_actual_result_and_expected_result(
            expected_result="iso-alpha2", actual_result=
            ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "country"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Moldova, Republica", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["country"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.iso.org", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["country"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result="CUATM", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["region"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "region"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Cahul", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["region"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["region"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "locality"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "locality"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="mun.Cahul", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["locality"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["locality"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result="works", actual_result=ei_release["releases"][0]["tender"]["mainProcurementCategory"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["classification"]["scheme"],
            actual_result=ei_release["releases"][0]["tender"]["classification"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["classification"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["classification"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Lucrări de pregătire a şantierului",
            actual_result=ei_release["releases"][0]["tender"]["classification"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["scheme"] + "-" + payload["buyer"]["identifier"]["id"],
            actual_result=ei_release["releases"][0]["buyer"]["id"])
        assert compare_actual_result_and_expected_result(expected_result=payload["buyer"]["identifier"]["legalName"],
                                                         actual_result=ei_release["releases"][0]["buyer"]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["scheme"] + "-" + payload["buyer"]["identifier"]["id"],
            actual_result=ei_release["releases"][0]["parties"][0]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["legalName"],
            actual_result=ei_release["releases"][0]["parties"][0]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["scheme"],
            actual_result=ei_release["releases"][0]["parties"][0]["identifier"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["id"],
            actual_result=ei_release["releases"][0]["parties"][0]["identifier"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["legalName"],
            actual_result=ei_release["releases"][0]["parties"][0]["identifier"]["legalName"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["uri"],
            actual_result=ei_release["releases"][0]["parties"][0]["identifier"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["streetAddress"],
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["streetAddress"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["postalCode"],
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["postalCode"])
        assert compare_actual_result_and_expected_result(
            expected_result="iso-alpha2",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["country"]["id"],
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Moldova, Republica", actual_result=ei_release["releases"][0]["parties"][0]["address"][
                "addressDetails"]["country"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.iso.org", actual_result=ei_release["releases"][0]["parties"][0]["address"][
                "addressDetails"]["country"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result="CUATM",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["region"]["id"],
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Cahul", actual_result=ei_release["releases"][0]["parties"][0]["address"][
                "addressDetails"]["region"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md", actual_result=ei_release["releases"][0]["parties"][0]["address"][
                "addressDetails"]["region"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result="CUATM",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["locality"]["id"],
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="mun.Cahul", actual_result=ei_release["releases"][0]["parties"][0]["address"][
                "addressDetails"]["locality"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md", actual_result=ei_release["releases"][0]["parties"][0]["address"][
                "addressDetails"]["locality"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["additionalIdentifiers"][0]["scheme"],
            actual_result=ei_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["additionalIdentifiers"][0]["id"],
            actual_result=ei_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["additionalIdentifiers"][0]["legalName"],
            actual_result=ei_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]["legalName"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["additionalIdentifiers"][0]["uri"],
            actual_result=ei_release["releases"][0]["parties"][0]["additionalIdentifiers"][0]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["name"],
            actual_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["email"],
            actual_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["email"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["telephone"],
            actual_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["telephone"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["faxNumber"],
            actual_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["faxNumber"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["contactPoint"]["url"],
            actual_result=ei_release["releases"][0]["parties"][0]["contactPoint"]["url"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["details"]["typeOfBuyer"],
            actual_result=ei_release["releases"][0]["parties"][0]["details"]["typeOfBuyer"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["details"]["mainGeneralActivity"],
            actual_result=ei_release["releases"][0]["parties"][0]["details"]["mainGeneralActivity"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["details"]["mainSectoralActivity"],
            actual_result=ei_release["releases"][0]["parties"][0]["details"]["mainSectoralActivity"])
        assert compare_actual_result_and_expected_result(
            expected_result="buyer", actual_result=ei_release["releases"][0]["parties"][0]["roles"][0])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["classification"]["id"],
            actual_result=ei_release["releases"][0]["planning"]["budget"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["startDate"],
            actual_result=ei_release["releases"][0]["planning"]["budget"]["period"]["startDate"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["endDate"],
            actual_result=ei_release["releases"][0]["planning"]["budget"]["period"]["endDate"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["rationale"],
            actual_result=ei_release["releases"][0]["planning"]["rationale"])

class TestCheckOnImpossibilityToCreateEiWithCpvsCodeIdWhichIsNotPresentInTheDictionary(object):
    @pytestrail.case("23993")
    def test_send_the_request_23993_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "866zx"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23993")
    def test_see_the_result_in_feed_point_23993_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "866zx"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.05", "description": "Invalid cpvs code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

class TestCheckOnImpossibilityToCreateEiWithCpvCodeIdWhichIsNotPresentInTheDictionary(object):
    @pytestrail.case("23995")
    def test_send_the_request_23995_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = "86655566"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23995")
    def test_see_the_result_in_feed_point_23995_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = "86655566"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.03", "description": "Invalid cpv code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckOnItemsAdditionalClassificationsIsSupplementedWithSchemeAndDescription(object):
    @pytestrail.case("23994")
    def test_send_the_request_23994_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23994")
    def test_see_the_result_in_feed_point_23994_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23994")
    def test_check_items_additionalClassifications_object_23994_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result="CPVS", actual_result=
        ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["additionalClassifications"][0]["id"], actual_result=
            ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"])
        assert compare_actual_result_and_expected_result(expected_result="Oţel carbon", actual_result=ei_release[
            "releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["description"])

class TestCheckOnItemClassificationIsSupplementedWithSchemeAndDescription(object):
    @pytestrail.case("23996")
    def test_send_the_request_23996_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = "45100000-8"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23996")
    def test_see_the_result_in_feed_point_23996_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = "45100000-8"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23996")
    def test_check_items_classifications_object_23996_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = "45100000-8"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result="CPV", actual_result=ei_release[
            "releases"][0]["tender"]["items"][0]["classification"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["classification"]["id"], actual_result=ei_release[
                "releases"][0]["tender"]["items"][0]["classification"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Lucrări de pregătire a şantierului", actual_result=ei_release[
                "releases"][0]["tender"]["items"][0]["classification"]["description"])

class TestCheckOnImpossibiltyToCreateEiWithItemsUnitIdWhichIsNotPresentInTheDictionary(object):
    @pytestrail.case("23997")
    def test_send_the_request_23997_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = "zx10"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23997")
    def test_see_the_result_in_feed_point_23997_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = "zx10"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.06", "description": "Invalid unit code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

class TestCheckOnItemsUnitIsSupplementedWithNameById(object):
    @pytestrail.case("23998")
    def test_send_the_request_23998_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = "120"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23998")
    def test_see_the_result_in_feed_point_23998_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = "120"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23998")
    def test_check_the_items_unit_object_in_the_EI_release_23998_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = "120"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result="Milion decalitri",
                                                         actual_result=ei_release["releases"][0]["tender"][
                                                             "items"][0]["unit"]["name"])
        assert compare_actual_result_and_expected_result(expected_result=payload["tender"]["items"][0]["unit"]["id"],
                                                         actual_result=ei_release["releases"][0]["tender"][
                                                             "items"][0]["unit"]["id"])

class TestCheckOnImpossibiltyToCreateEiIfDeliveryAddressAddressDetailsCountryIdIsNotPresentInDictionary(object):
    @pytestrail.case("23999")
    def test_send_the_request_23999_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "DE"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23999")
    def test_see_the_result_in_feed_point_23999_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "DE"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.10", "description": "Invalid country. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

class TestCheckOnDeliveryAddressAddressDetailsCountryObjectIsSupplementedWithSchemeDescriptionUri(object):
    @pytestrail.case("24000")
    def test_send_the_request_24000_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24000")
    def test_see_the_result_in_feed_point_24000_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24000")
    def test_check_the_deliveryAddress_addressDetails_country_24000_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "country"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="iso-alpha2",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "country"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result="Moldova, Republica",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
                   "description"])
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.iso.org",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "country"]["uri"])

class TestCheckThePossibilityToCreateEiOnObligatoryDataModelAddItems(object):
    @pytestrail.case("22133")
    def test_send_the_request_22133_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22133")
    def test_see_the_result_in_feed_point_22133_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22133")
    def test_check_sent_fields_are_published_in_the_EI_release_22133_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["title"], actual_result=ei_release["releases"][0]["tender"]["title"])
        assert compare_actual_result_and_expected_result(
            expected_result="CPV", actual_result=ei_release["releases"][0]["tender"]["classification"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["classification"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["classification"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Lucrări de pregătire a şantierului",
            actual_result=ei_release["releases"][0]["tender"]["classification"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["classification"]["id"],
            actual_result=ei_release["releases"][0]["planning"]["budget"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["startDate"],
            actual_result=ei_release["releases"][0]["planning"]["budget"]["period"]["startDate"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["planning"]["budget"]["period"]["endDate"],
            actual_result=ei_release["releases"][0]["planning"]["budget"]["period"]["endDate"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["scheme"] + "-" + payload["buyer"]["identifier"]["id"],
            actual_result=ei_release["releases"][0]["buyer"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["name"], actual_result=ei_release["releases"][0]["buyer"]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["scheme"] + "-" + payload["buyer"]["identifier"]["id"],
            actual_result=ei_release["releases"][0]["parties"][0]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["name"], actual_result=ei_release["releases"][0]["parties"][0]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"][
                "scheme"], actual_result=ei_release["releases"][0]["parties"][0]["identifier"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["id"],
            actual_result=ei_release["releases"][0]["parties"][0]["identifier"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"][
                "legalName"], actual_result=ei_release["releases"][0]["parties"][0]["identifier"]["legalName"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["streetAddress"], actual_result=ei_release["releases"][0][
                "parties"][0]["address"]["streetAddress"])
        assert compare_actual_result_and_expected_result(
            expected_result="iso-alpha2",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
                "scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["country"]["id"],
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Moldova, Republica",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
                "description"])
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.iso.org",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
                "uri"])
        assert compare_actual_result_and_expected_result(
            expected_result="CUATM",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result="1700000",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Cahul",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
                "description"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result="CUATM", actual_result=ei_release["releases"][0]["parties"][0]["address"][
                "addressDetails"]["locality"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result="1701000",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result=str(payload["buyer"]["contactPoint"]),
            actual_result=str(ei_release["releases"][0]["parties"][0]["contactPoint"]))

class TestCheckTheStartDateIsLaterThanEndDateForPlanningBudget(object):
    @pytestrail.case("22167")
    def test_send_the_request_22167_1(self, country, language):
        budget_period = get_period()
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload['planning']['budget']['period']['startDate'] = budget_period[1]
        payload["planning"]["budget"]["period"]["endDate"] = budget_period[0]
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22167")
    def test_see_the_result_in_feed_point_22167_2(self, country, language):
        budget_period = get_period()
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload['planning']['budget']['period']['startDate'] = budget_period[1]
        payload["planning"]["budget"]["period"]["endDate"] = budget_period[0]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.01.01", "description": "Invalid period."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

class TestCheckOnImpossibiltyToCreateEiIfDeliveryAddressAddressDetailsRegionIdIsNotPresentInDictionary(object):
    @pytestrail.case("24001")
    def test_send_the_request_24001_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "ABCD1234"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24001")
    def test_see_the_result_in_feed_point_24001_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "ABCD1234"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.13", "description": "Region not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckOnDeliveryAddressAddressDetailsRegionObjectIsSupplementedWithSchemeDescriptionUri(object):
    @pytestrail.case("24002")
    def test_send_the_request_24002_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24002")
    def test_see_the_result_in_feed_point_24002_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24002")
    def test_check_deliveryAddress_addressDetails_regionobject_24002_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "region"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="CUATM",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "region"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result="Cahul",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "region"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "region"]["uri"])

class TestCheckOnImpossibiltyToCreateEiIfDeliveryAddressAddressDetailsLocalityIdIsNotPresentInDictionary(object):
    @pytestrail.case("24003")
    def test_send_the_request_24003_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "ABCD1234"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24003")
    def test_see_the_result_in_feed_point_24003_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "ABCD1234"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.14", "description": "Locality not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

class TestCheckOnImpossibiltyToCreateEiIfDeliveryAddressAddressDetailsLocalityIdIsNotRelatedToValueOfRegionId(object):
    @pytestrail.case("24004")
    def test_send_the_request_24004_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "0101000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24004")
    def test_see_the_result_in_feed_point_24004_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "0101000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.14", "description": "Locality not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

class TestCheckOnDeliveryAddressAddressDetailsLocalityObjectIsSupplementedWithDescriptionUri(object):
    @pytestrail.case("24005")
    def test_send_the_request_24005_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24005")
    def test_see_the_result_in_feed_point_24005_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24005")
    def test_checkdeliveryAddress_addressDetails_locality_object_24005_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"],
            actual_result=
            ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
                "id"])
        assert compare_actual_result_and_expected_result(
            expected_result="CUATM", actual_result=
            ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
                "scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result="mun.Cahul", actual_result=
            ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
                "description"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md", actual_result=
            ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
                "uri"])

class TestCheckOnPossibiltyToCreateEiIfDeliveryAddressAddressDetailsLocalitySchemeIsNotCuatm(object):
    @pytestrail.case("24006")
    def test_send_the_request_24006_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "OTHER"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24006")
    def test_see_the_result_in_feed_point_24006_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "OTHER"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24006")
    def test_Check_tender_items_deliveryAddress_addressDetails_locality_object_24006_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "OTHER"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"],
            actual_result=
            ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
                "id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"],
            actual_result=
            ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
                "scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
                "description"], actual_result=
            ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
                "description"])

class TestCheckOnIfTemporalItemsIdHaveChangedToPermanent(object):
    @pytestrail.case("24011")
    def test_send_the_request_24011_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24011")
    def test_see_the_result_in_feed_point_24011_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24011")
    def test_check_tender_items_id_have_changed_to_permanent_24011_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=str(True), actual_result=str(is_it_uuid(
            ei_release["releases"][0]["tender"]["items"][0]["id"], 4)))

class TestCheckOnTenderItemsInRelease(object):
    @pytestrail.case("24012")
    def test_send_the_request_24012_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "45100000-8"
        payload["tender"]["items"][0]["id"] = "1"
        payload["tender"]["items"][0]["description"] = "item_1"
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
        payload["tender"]["items"][0]["quantity"] = 10.0
        payload["tender"]["items"][0]["unit"]["id"] = "10"
        payload["tender"]["items"][0]["unit"]["name"] = "name"
        payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = "Khreshchatyk"
        payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = "01124"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
            "description"] = "description_1"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["scheme"] = "scheme_1"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["uri"] = "www.deutch"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "0101000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
            "description"] = "description_2"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["scheme"] = "scheme_2"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["uri"] = "www,regi_16"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "0101000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["uri"] = "ww.io.io"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
            "description"] = "description_test"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24012")
    def test_see_the_result_in_feed_point_24012_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "45100000-8"
        payload["tender"]["items"][0]["id"] = "1"
        payload["tender"]["items"][0]["description"] = "item_1"
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
        payload["tender"]["items"][0]["quantity"] = 10
        payload["tender"]["items"][0]["unit"]["id"] = "10"
        payload["tender"]["items"][0]["unit"]["name"] = "name"
        payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = "Khreshchatyk"
        payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = "01124"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
            "description"] = "description_1"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["scheme"] = "scheme_1"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["uri"] = "www.deutch"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "0101000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
            "description"] = "description_2"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["scheme"] = "scheme_2"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["uri"] = "www,regi_16"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "0101000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["uri"] = "ww.io.io"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
            "description"] = "description_test"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfull())
        expected_result = str(True)
        ei.delete_data_from_database()
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24012")
    def test_check_tender_items_object_24012_3(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "45100000-8"
        payload["tender"]["items"][0]["id"] = "1"
        payload["tender"]["items"][0]["description"] = "item_1"
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
        payload["tender"]["items"][0]["quantity"] = 10
        payload["tender"]["items"][0]["unit"]["id"] = "10"
        payload["tender"]["items"][0]["unit"]["name"] = "name"
        payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = "Khreshchatyk"
        payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = "01124"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
            "description"] = "description_1"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["scheme"] = "scheme_1"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["uri"] = "www.deutch"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "0101000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
            "description"] = "description_2"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["scheme"] = "scheme_2"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["uri"] = "www,regi_16"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "0101000"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["uri"] = "ww.io.io"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
            "description"] = "description_test"
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        assert compare_actual_result_and_expected_result(expected_result=str(True), actual_result=str(is_it_uuid(
            ei_release["releases"][0]["tender"]["items"][0]["id"], 4)))
        assert compare_actual_result_and_expected_result(expected_result=payload["tender"]["items"][0]["description"],
                                                         actual_result=ei_release["releases"][0]["tender"]["items"][0][
                                                             "description"])
        assert compare_actual_result_and_expected_result(expected_result="CPV", actual_result=ei_release[
            "releases"][0]["tender"]["items"][0]["classification"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["classification"]["id"], actual_result=ei_release[
                "releases"][0]["tender"]["items"][0]["classification"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Lucrări de valorificare a terenurilor virane", actual_result=ei_release[
                "releases"][0]["tender"]["items"][0]["classification"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="CPVS",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["additionalClassifications"][0]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Oţel carbon",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
                "description"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["quantity"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["quantity"])
        assert compare_actual_result_and_expected_result(
            expected_result="Parsec", actual_result=ei_release["releases"][0]["tender"]["items"][0]["unit"]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["unit"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["unit"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["streetAddress"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["postalCode"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["postalCode"])
        assert compare_actual_result_and_expected_result(
            expected_result="iso-alpha2", actual_result=
            ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "country"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="Moldova, Republica", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["country"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.iso.org", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["country"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result="CUATM", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["region"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "region"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="mun.Chişinău", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["region"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["region"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "locality"]["scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"],
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "locality"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="mun.Chişinău", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["locality"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md", actual_result=ei_release["releases"][0]["tender"]["items"][0][
                "deliveryAddress"]["addressDetails"]["locality"]["uri"])

class TestTenderClassificationIdDoesNotMatchToTenderItemsClassificationIdBy3FirstSymbols(object):
    @pytestrail.case("24013")
    def test_send_the_request_24013_1(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "90900000-6"
        payload["tender"]["items"][0]["classification"]["id"] = "50100000-6"
        ei = EI(payload=payload, lang=language, country=country)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("24013")
    def test_see_the_result_in_feed_point_24013_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = "90900000-6"
        payload["tender"]["items"][0]["classification"]["id"] = "50100000-6"
        value_of_key = payload["tender"]["items"][0]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00.05", "description": f"Invalid CPV.Invalid CPV code in "
                                                                       f"classification(s) '{value_of_key}'"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)
#
#
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["title"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'tender.title' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["description"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'tender.description' is empty or " \
#                                  "blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["rationale"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'planning.rationale' is empty or " \
#                                  "blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_4(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["name"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.name' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_5(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.identifier.id' is empty or " \
#                                  "blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_6(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["legalName"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.identifier.legalName' " \
#                                  "is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_7(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["uri"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.identifier.uri' " \
#                                  "is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_8(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["streetAddress"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.address.streetAddress' " \
#                                  "is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_9(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["postalCode"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.address.postalCode' " \
#                                  "is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_10(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.address.addressDetails." \
#                                  "locality.scheme' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_11(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.address.addressDetails." \
#                                  "locality.id' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_12(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.address.addressDetails." \
#                                  "locality.description' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_13(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["additionalIdentifiers"][0]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.additionalIdentifiers.id' " \
#                                  "is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_14(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["additionalIdentifiers"][0]["scheme"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.additionalIdentifiers." \
#                                  "scheme' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_15(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["additionalIdentifiers"][0]["legalName"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.additionalIdentifiers." \
#                                  "legalName' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_16(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["additionalIdentifiers"][0]["uri"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.additionalIdentifiers.uri' " \
#                                  "is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_17(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["contactPoint"]["name"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.contactPoint.name' is " \
#                                  "empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_18(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["contactPoint"]["email"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.contactPoint.email' is " \
#                                  "empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_19(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["contactPoint"]["telephone"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.contactPoint.telephone' is " \
#                                  "empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_20(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["contactPoint"]["faxNumber"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.contactPoint.faxNumber' is " \
#                                  "empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_21(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["contactPoint"]["url"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'buyer.contactPoint.url' is empty " \
#                                  "or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_22(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'tender.items.deliveryAddress." \
#                                  "streetAddress' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_23(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'tender.items.deliveryAddress." \
#                                  "postalCode' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_24(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'deliveryAddress.addressDetails." \
#                                  "locality.scheme' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_25(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'deliveryAddress.addressDetails." \
#                                  "locality.id' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_26(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["description"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'deliveryAddress.addressDetails." \
#                                  "locality.description' is empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_27(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["description"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Incorrect an attribute value.The attribute 'tender.items.description' is " \
#                                  "empty or blank."
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_28(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.06"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Cpv code not found. "
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_29(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["classification"]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.03"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Invalid cpv code. "
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_30(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.05"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Invalid cpvs code. "
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_31(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.10"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Invalid country. "
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_32(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.13"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Region not found. "
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_33(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["quantity"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0][
#                "description"] == "com.fasterxml.jackson.databind.JsonMappingException: (was com.procurement." \
#                                  "mdm.exception.InErrorException) (through reference chain: com.procurement." \
#                                  "mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.procurement.mdm.model." \
#                                  "dto.data.ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com." \
#                                  "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item[\"quantity\"])"
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_34(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["unit"]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.06"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Invalid unit code. "
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_35(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["budget"]["period"]["startDate"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00"
#     assert message_from_kafka["errors"][0][
#                "description"] == "com.fasterxml.jackson.databind.JsonMappingException: Text ' ' could not be " \
#                                  "parsed at index 0 (through reference chain: com.procurement.budget.model.dto." \
#                                  "ei.request.EiCreate[\"planning\"]->com.procurement.budget.model.dto.ei." \
#                                  "request.EiCreate$PlanningEiCreate[\"budget\"]->com.procurement.budget." \
#                                  "model.dto.ei.request.EiCreate$PlanningEiCreate$BudgetEiCreate[\"period\"]" \
#                                  "->com.procurement.budget.model.dto.ocds.Period[\"startDate\"])"
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_36(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["budget"]["period"]["endDate"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00"
#     assert message_from_kafka["errors"][0][
#                "description"] == "com.fasterxml.jackson.databind.JsonMappingException: Text ' ' could not be " \
#                                  "parsed at index 0 (through reference chain: com.procurement.budget.model.dto." \
#                                  "ei.request.EiCreate[\"planning\"]->com.procurement.budget.model.dto.ei." \
#                                  "request.EiCreate$PlanningEiCreate[\"budget\"]->com.procurement.budget." \
#                                  "model.dto.ei.request.EiCreate$PlanningEiCreate$BudgetEiCreate[\"period\"]" \
#                                  "->com.procurement.budget.model.dto.ocds.Period[\"endDate\"])"
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_37(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["scheme"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.12"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Registration scheme not found. "
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_38(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.11"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Country not found. "
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_39(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.13"
#     assert message_from_kafka["errors"][0][
#                "description"] == "Region not found. "
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_40(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["typeOfBuyer"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0][
#                "description"] == "com.fasterxml.jackson.databind.exc.InvalidFormatException: Cannot " \
#                                  "deserialize value of type `com.procurement.mdm.model.dto.data." \
#                                  "TypeOfBuyer` from String \"\": value not one of declared Enum " \
#                                  "instance names: [NATIONAL_AGENCY, REGIONAL_AUTHORITY, REGIONAL_AGENCY, " \
#                                  "BODY_PUBLIC, EU_INSTITUTION, MINISTRY]\n at [Source: UNKNOWN; line: -1, " \
#                                  "column: -1] (through reference chain: com.procurement.mdm.model.dto." \
#                                  "data.ei.EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data." \
#                                  "OrganizationReference[\"details\"]->com.procurement.mdm.model.dto." \
#                                  "data.Details[\"typeOfBuyer\"])"
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_41(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainGeneralActivity"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0][
#                "description"] == "com.fasterxml.jackson.databind.exc.InvalidFormatException: Cannot " \
#                                  "deserialize value of type `com.procurement.mdm.model.dto.data." \
#                                  "MainGeneralActivity` from String \"\": value not one of declared Enum " \
#                                  "instance names: [DEFENCE, PUBLIC_ORDER_AND_SAFETY, ECONOMIC_AND_FINANCIAL_" \
#                                  "AFFAIRS, ENVIRONMENT, RECREATION_CULTURE_AND_RELIGION, EDUCATION, " \
#                                  "SOCIAL_PROTECTION, HEALTH, GENERAL_PUBLIC_SERVICES, HOUSING_AND_" \
#                                  "COMMUNITY_AMENITIES]\n at [Source: UNKNOWN; line: -1, column: -1] " \
#                                  "(through reference chain: com.procurement.mdm.model.dto.data.ei." \
#                                  "EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data." \
#                                  "OrganizationReference[\"details\"]->com.procurement.mdm.model." \
#                                  "dto.data.Details[\"mainGeneralActivity\"])"
#
#
# @pytestrail.case("25301")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_25301_42(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainSectoralActivity"] = " "
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0][
#                "description"] == "com.fasterxml.jackson.databind.exc.InvalidFormatException: Cannot " \
#                                  "deserialize value of type `com.procurement.mdm.model.dto.data." \
#                                  "MainSectoralActivity` from String \"\": value not one of declared Enum " \
#                                  "instance names: [EXPLORATION_EXTRACTION_GAS_OIL, ELECTRICITY, POSTAL_" \
#                                  "SERVICES, PRODUCTION_TRANSPORT_DISTRIBUTION_GAS_HEAT, WATER, URBAN_" \
#                                  "RAILWAY_TRAMWAY_TROLLEYBUS_BUS_SERVICES, PORT_RELATED_ACTIVITIES, " \
#                                  "RAILWAY_SERVICES, EXPLORATION_EXTRACTION_COAL_OTHER_SOLID_FUEL, " \
#                                  "AIRPORT_RELATED_ACTIVITIES]\n at [Source: UNKNOWN; line: -1, " \
#                                  "column: -1] (through reference chain: com.procurement.mdm.model." \
#                                  "dto.data.ei.EIRequest[\"buyer\"]->com.procurement.mdm.model.dto." \
#                                  "data.OrganizationReference[\"details\"]->com.procurement.mdm.model." \
#                                  "dto.data.Details[\"mainSectoralActivity\"])"
#
#
# @pytestrail.case("22180")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22180_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22180")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22180_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     check_cpid = fnmatch.fnmatch(cpid, "ocds-t1s2t3-MD-*")
#     ei_token = is_it_uuid(message_from_kafka["data"]["outcomes"]["ei"][0]["X-TOKEN"], 4)
#     ei.delete_data_from_database(cpid)
#     assert check_cpid == True
#     assert ei_token == True
#
#
# @pytestrail.case("22180")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22180_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     ei_release_id = ei_release["releases"][0]["id"]
#     ei_release_timestamp = int(ei_release_id[29:42])
#     convert_timestamp_to_date = get_human_date_in_utc_format(ei_release_timestamp)
#     assert ei_release_id[0:28] == cpid
#     assert ei_release["releases"][0]["date"] == convert_timestamp_to_date[0]
#     assert ei_release["releases"][0]["id"] == f"{cpid}" + f"-{str(ei_release_timestamp)}"
