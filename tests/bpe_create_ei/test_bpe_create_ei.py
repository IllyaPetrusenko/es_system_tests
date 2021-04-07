import copy

import requests
from pytest_testrail.plugin import pytestrail
from tests.essences.ei import EI
from tests.payloads.ei_payload import payload_ei_full_data_model
from useful_functions import compare_actual_result_and_expected_result


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

#
# @pytestrail.case("22136")
# @pytest.mark.regression
# def test_22136_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     payload["buyer"]["address"]["addressDetails"]["country"]["scheme"] = "sheme for test"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22136")
# @pytest.mark.regression
# def test_22136_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     payload["buyer"]["address"]["addressDetails"]["country"]["scheme"] = "sheme for test"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     check_cpid = fnmatch.fnmatch(cpid, 'ocds-t1s2t3-MD-*')
#     ei_token = is_it_uuid(message_from_kafka["data"]["outcomes"]["ei"][0]["X-TOKEN"], 4)
#     ei.delete_data_from_database(cpid)
#     assert check_cpid == True
#     assert ei_token == True
#
#
# @pytestrail.case("22136")
# @pytest.mark.regression
# def test_22136_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     payload["buyer"]["address"]["addressDetails"]["country"]["scheme"] = "sheme for test"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                "scheme"] == "iso-alpha2"
#
#
# @pytestrail.case("22137")
# @pytest.mark.regression
# def test_22137_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     payload["buyer"]["address"]["addressDetails"]["country"]["uri"] = "uri for test"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22137")
# @pytest.mark.regression
# def test_22137_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     payload["buyer"]["address"]["addressDetails"]["country"]["uri"] = "uri for test"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     check_cpid = fnmatch.fnmatch(cpid, 'ocds-t1s2t3-MD-*')
#     ei_token = is_it_uuid(message_from_kafka['data']['outcomes']['ei'][0]['X-TOKEN'], 4)
#     ei.delete_data_from_database(cpid)
#     assert check_cpid == True
#     assert ei_token == True
#
#
# @pytestrail.case("22137")
# @pytest.mark.regression
# def test_22137_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     payload["buyer"]["address"]["addressDetails"]["country"]["uri"] = "uri for test"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka['data']['outcomes']['ei'][0]['id']
#     ei_url = message_from_kafka["data"]["url"] + '/' + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                "uri"] == "https://www.iso.org"
#
#
# @pytestrail.case("22138")
# @pytest.mark.regression
# def test_22138_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     payload["buyer"]["address"]["addressDetails"]["country"]["description"] = "description for test"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22138")
# @pytest.mark.regression
# def test_22138_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     payload["buyer"]["address"]["addressDetails"]["country"]["description"] = "description for test"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka['data']['outcomes']['ei'][0]['id']
#     check_cpid = fnmatch.fnmatch(cpid, 'ocds-t1s2t3-MD-*')
#     ei_token = is_it_uuid(message_from_kafka['data']['outcomes']['ei'][0]['X-TOKEN'], 4)
#     ei.delete_data_from_database(cpid)
#     assert check_cpid == True
#     assert ei_token == True
#
#
# @pytestrail.case("22138")
# @pytest.mark.regression
# def test_22138_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     payload["buyer"]["address"]["addressDetails"]["country"]["description"] = "description for test"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka['data']['outcomes']['ei'][0]['id']
#     ei_url = message_from_kafka['data']['url'] + '/' + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                "description"] == "Moldova, Republica"
#
#
# @pytestrail.case("22139")
# @pytest.mark.regression
# def test_22139_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "UK"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == 'ok'
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22139")
# @pytest.mark.regression
# def test_22139_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "UK"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.10"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid country. "
#
#
# @pytestrail.case("22140")
# @pytest.mark.regression
# def test_22140_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22140")
# @pytest.mark.regression
# def test_22140_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka['data']['outcomes']['ei'][0]['id']
#     check_cpid = fnmatch.fnmatch(cpid, 'ocds-t1s2t3-MD-*')
#     ei_token = is_it_uuid(message_from_kafka['data']['outcomes']['ei'][0]['X-TOKEN'], 4)
#     ei.delete_data_from_database(cpid)
#     assert check_cpid == True
#     assert ei_token == True
#
#
# @pytestrail.case("22140")
# @pytest.mark.regression
# def test_22140_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka['data']['outcomes']['ei'][0]['id']
#     ei_url = message_from_kafka['data']['url'] + '/' + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"] == "CUATM"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"] == \
#            payload["buyer"]["address"]["addressDetails"]["region"]["id"]
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                "description"] == "Donduşeni"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                "uri"] == "http://statistica.md"
#
#
# @pytestrail.case("22141")
# @pytest.mark.regression
# def test_22141_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["buyer"]["address"]["addressDetails"]["region"]["scheme"] = "other"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22141")
# @pytest.mark.regression
# def test_22141_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["buyer"]["address"]["addressDetails"]["region"]["scheme"] = "other"
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
# @pytestrail.case("22141")
# @pytest.mark.regression
# def test_22141_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["buyer"]["address"]["addressDetails"]["region"]["scheme"] = "other"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"] == "CUATM"
#
#
# @pytestrail.case("22142")
# @pytest.mark.regression
# def test_22142_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["uri"] = "test fro uri"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22142")
# @pytest.mark.regression
# def test_22142_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["uri"] = "test fro uri"
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
# @pytestrail.case("22142")
# @pytest.mark.regression
# def test_22142_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["uri"] = "test fro uri"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                "uri"] == "http://statistica.md"
#
#
# @pytestrail.case("22143")
# @pytest.mark.regression
# def test_22143_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload['buyer']['address']['addressDetails']['region']['id'] = "1700000"
#     payload["buyer"]["address"]["addressDetails"]["region"]["description"] = "test fro uri"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22143")
# @pytest.mark.regression
# def test_22143_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload['buyer']['address']['addressDetails']['region']['id'] = "1700000"
#     payload["buyer"]["address"]["addressDetails"]["region"]["description"] = "test fro uri"
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
# @pytestrail.case("22143")
# @pytest.mark.regression
# def test_22143_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload['buyer']['address']['addressDetails']['region']['id'] = "1700000"
#     payload["buyer"]["address"]["addressDetails"]["region"]["description"] = "test fro uri"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                "description"] == "Cahul"
#
#
# @pytestrail.case("22144")
# @pytest.mark.regression
# def test_22144_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000aa"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22144")
# @pytest.mark.regression
# def test_22144_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000aa"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.13"
#     assert message_from_kafka["errors"][0]["description"] == "Region not found. "
#
#
# @pytestrail.case("22145")
# @pytest.mark.regression
# def test_22145_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "1701000"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22145")
# @pytest.mark.regression
# def test_22145_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "1701000"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.14"
#     assert message_from_kafka["errors"][0]["description"] == "Locality not found. "
#
#
# @pytestrail.case("22146")
# @pytest.mark.regression
# def test_22146_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22146")
# @pytest.mark.regression
# def test_22146_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
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
# @pytestrail.case("22146")
# @pytest.mark.regression
# def test_22146_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                "scheme"] == "CUATM"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"] == \
#            payload["buyer"]["address"]["addressDetails"]["locality"]["id"]
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                "description"] == "or.Donduşeni (r-l Donduşeni)"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                "uri"] == "http://statistica.md"
#
#
# @pytestrail.case("22147")
# @pytest.mark.regression
# def test_22147_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
#     del payload["buyer"]["address"]["addressDetails"]["locality"]["description"]
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22147")
# @pytest.mark.regression
# def test_22147_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
#     del payload["buyer"]["address"]["addressDetails"]["locality"]["description"]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                              "KotlinParameterException: Instantiation of " \
#                                                              "[simple type, class com.procurement.mdm.model." \
#                                                              "dto.data.LocalityDetails] value failed for JSON " \
#                                                              "property description due to missing (therefore " \
#                                                              "NULL) value for creator parameter description " \
#                                                              "which is a non-nullable type\n at [Source: " \
#                                                              "UNKNOWN; line: -1, column: -1] (through reference " \
#                                                              "chain: com.procurement.mdm.model.dto.data.ei." \
#                                                              "EIRequest[\"buyer\"]->com.procurement.mdm.model." \
#                                                              "dto.data.OrganizationReference[\"address\"]->com." \
#                                                              "procurement.mdm.model.dto.data.Address[\"address" \
#                                                              "Details\"]->com.procurement.mdm.model.dto.data." \
#                                                              "AddressDetails[\"locality\"]->com.procurement." \
#                                                              "mdm.model.dto.data.LocalityDetails[\"description\"])"
#
#
# @pytestrail.case("22148")
# @pytest.mark.regression
# def test_22148_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "desc"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22148")
# @pytest.mark.regression
# def test_22148_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "desc"
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
# @pytestrail.case("22148")
# @pytest.mark.regression
# def test_22148_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "3400000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "desc"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                "scheme"] == "CUATM"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"] == \
#            payload["buyer"]["address"]["addressDetails"]["locality"]["id"]
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                "description"] == "or.Donduşeni (r-l Donduşeni)"
#
#
# @pytestrail.case("22149")
# @pytest.mark.regression
# def test_22149_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22149")
# @pytest.mark.regression
# def test_22149_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
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
# @pytestrail.case("22149")
# @pytest.mark.regression
# def test_22149_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["identifier"]["scheme"] == "MD-IDNO"
#
#
# @pytestrail.case("22150")
# @pytest.mark.regression
# def test_22150_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["scheme"] = "MD-NE-DNO"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22150")
# @pytest.mark.regression
# def test_22150_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["scheme"] = "MD-NE-DNO"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.12"
#     assert message_from_kafka["errors"][0]["description"] == "Registration scheme not found. "
#
#
# @pytestrail.case("22151")
# @pytest.mark.regression
# def test_22151_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["typeOfBuyer"] = "MINISTRY"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22151")
# @pytest.mark.regression
# def test_22151_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["typeOfBuyer"] = "MINISTRY"
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
# @pytestrail.case("22151")
# @pytest.mark.regression
# def test_22151_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["typeOfBuyer"] = "MINISTRY"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["details"]["typeOfBuyer"] == payload["buyer"]["details"][
#         "typeOfBuyer"]
#
#
# @pytestrail.case("22152")
# @pytest.mark.regression
# def test_22152_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["typeOfBuyer"] = "SCHOOL IS NOT HOME"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22152")
# @pytest.mark.regression
# def test_22152_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["typeOfBuyer"] = "SCHOOL IS NOT HOME"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc.Invalid" \
#                                                              "FormatException: Cannot deserialize value " \
#                                                              "of type `com.procurement.mdm.model.dto.data." \
#                                                              "TypeOfBuyer` from String \"SCHOOL IS NOT " \
#                                                              "HOME\": value not one of declared Enum " \
#                                                              "instance names: [NATIONAL_AGENCY, REGIONAL_" \
#                                                              "AUTHORITY, REGIONAL_AGENCY, BODY_PUBLIC, " \
#                                                              "EU_INSTITUTION, MINISTRY]\n at [Source: " \
#                                                              "UNKNOWN; line: -1, column: -1] (through " \
#                                                              "reference chain: com.procurement.mdm.model." \
#                                                              "dto.data.ei.EIRequest[\"buyer\"]->com." \
#                                                              "procurement.mdm.model.dto.data.Organization" \
#                                                              "Reference[\"details\"]->com.procurement.mdm." \
#                                                              "model.dto.data.Details[\"typeOfBuyer\"])"
#
#
# @pytestrail.case("22153")
# @pytest.mark.regression
# def test_22153_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainGeneralActivity"] = "SOCIAL_PROTECTION"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22153")
# @pytest.mark.regression
# def test_22153_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainGeneralActivity"] = "SOCIAL_PROTECTION"
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
# @pytestrail.case("22153")
# @pytest.mark.regression
# def test_22153_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainGeneralActivity"] = "SOCIAL_PROTECTION"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["details"]["mainGeneralActivity"] == payload["buyer"]["details"][
#         "mainGeneralActivity"]
#
#
# @pytestrail.case("22154")
# @pytest.mark.regression
# def test_22154_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainGeneralActivity"] = "SOC"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22154")
# @pytest.mark.regression
# def test_22154_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainGeneralActivity"] = "SOC"
#     value_of_key = payload["buyer"]["details"]["mainGeneralActivity"]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.exc.InvalidFormat" \
#                                                              f"Exception: Cannot deserialize value of type " \
#                                                              f"`com.procurement.mdm.model.dto.data." \
#                                                              f"MainGeneralActivity` from String " \
#                                                              f"\"{value_of_key}\": value not one of " \
#                                                              f"declared Enum instance names: [DEFENCE, " \
#                                                              f"PUBLIC_ORDER_AND_SAFETY, " \
#                                                              f"ECONOMIC_AND_FINANCIAL_AFFAIRS, ENVIRONMENT, " \
#                                                              f"RECREATION_CULTURE_AND_RELIGION, EDUCATION, " \
#                                                              f"SOCIAL_PROTECTION, HEALTH, " \
#                                                              f"GENERAL_PUBLIC_SERVICES, " \
#                                                              f"HOUSING_AND_COMMUNITY_AMENITIES]\n at " \
#                                                              f"[Source: UNKNOWN; line: -1, column: -1] " \
#                                                              f"(through reference chain: com.procurement" \
#                                                              f".mdm.model.dto.data.ei.EIRequest[\"buyer\"]->" \
#                                                              f"com.procurement.mdm.model.dto.data.Organization" \
#                                                              f"Reference[\"details\"]->com.procurement.mdm." \
#                                                              f"model.dto.data.Details[\"mainGeneralActivity\"])"
#
#
# @pytestrail.case("22155")
# @pytest.mark.regression
# def test_22155_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainSectoralActivity"] = "WATER"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22155")
# @pytest.mark.regression
# def test_22155_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainSectoralActivity"] = "WATER"
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
# @pytestrail.case("22155")
# @pytest.mark.regression
# def test_22155_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainSectoralActivity"] = "WATER"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["details"]["mainSectoralActivity"] == payload["buyer"][
#         "details"]["mainSectoralActivity"]
#
#
# @pytestrail.case("22156")
# @pytest.mark.regression
# def test_22156_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainSectoralActivity"] = "WAT"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22156")
# @pytest.mark.regression
# def test_22156_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainSectoralActivity"] = "WAT"
#     value_of_key = payload["buyer"]["details"]["mainSectoralActivity"]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.exc." \
#                                                              f"InvalidFormatException: Cannot deserialize " \
#                                                              f"value of type `com.procurement.mdm.model.dto." \
#                                                              f"data.MainSectoralActivity` from String " \
#                                                              f"\"{value_of_key}\": value not one of " \
#                                                              f"declared Enum instance names: " \
#                                                              f"[EXPLORATION_EXTRACTION_GAS_OIL, " \
#                                                              f"ELECTRICITY, POSTAL_SERVICES, " \
#                                                              f"PRODUCTION_TRANSPORT_DISTRIBUTION_GAS_HEAT, " \
#                                                              f"WATER, " \
#                                                              f"URBAN_RAILWAY_TRAMWAY_TROLLEYBUS_BUS_SERVICES, " \
#                                                              f"PORT_RELATED_ACTIVITIES, RAILWAY_SERVICES, " \
#                                                              f"EXPLORATION_EXTRACTION_COAL_OTHER_SOLID_FUEL, " \
#                                                              f"AIRPORT_RELATED_ACTIVITIES]\n at [Source: " \
#                                                              f"UNKNOWN; line: -1, column: -1] " \
#                                                              f"(through reference chain: " \
#                                                              f"com.procurement.mdm.model." \
#                                                              f"dto.data.ei.EIRequest[\"buyer\"]->" \
#                                                              f"com.procurement.mdm.model.dto.data." \
#                                                              f"OrganizationReference[\"details\"]->" \
#                                                              f"com.procurement.mdm.model.dto.data." \
#                                                              f"Details[\"mainSectoralActivity\"])"
#
#
# @pytestrail.case("22157")
# @pytest.mark.regression
# def test_22157_1(self, country, language):
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
# @pytestrail.case("22157")
# @pytest.mark.regression
# def test_22157_2(self, country, language):
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
# @pytestrail.case("22157")
# @pytest.mark.regression
# def test_22157_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     convert_timestamp_to_date = get_human_date_in_utc_format(int(cpid[15:28]))[0]
#     check_cpid_first_part = fnmatch.fnmatch(cpid[0:15], "ocds-t1s2t3-MD-")
#     ei.delete_data_from_database(cpid)
#     assert check_cpid_first_part == True
#     assert convert_timestamp_to_date == message_from_kafka["data"]["operationDate"]
#
#
# @pytestrail.case("22158")
# @pytest.mark.regression
# def test_22158_1(self, country, language):
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
# @pytestrail.case("22158")
# @pytest.mark.regression
# def test_22158_2(self, country, language):
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
# @pytestrail.case("22158")
# @pytest.mark.regression
# def test_22158_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     release_id = ei_release["releases"][0]["id"]
#     timestamp = int(release_id[29:39])
#     convert_timestamp_to_date = datetime.datetime.utcfromtimestamp(timestamp)
#     convert_date_to_human_date = convert_timestamp_to_date.strftime("%Y-%m-%dT%H:%M:%SZ")
#     assert message_from_kafka["data"]["operationDate"] == convert_date_to_human_date
#
#
# @pytestrail.case("22159")
# @pytest.mark.regression
# def test_22159_1(self, country, language):
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
# @pytestrail.case("22159")
# @pytest.mark.regression
# def test_22159_2(self, country, language):
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
# @pytestrail.case("22159")
# @pytest.mark.regression
# def test_22159_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     assert message_from_kafka["data"]["operationDate"] == ei_release["releases"][0]["date"]
#
#
# @pytestrail.case("22160")
# @pytest.mark.regression
# def test_22160_1(self, country, language):
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
# @pytestrail.case("22160")
# @pytest.mark.regression
# def test_22160_2(self, country, language):
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
# @pytestrail.case("22160")
# @pytest.mark.regression
# def test_22160_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     check_tender_id = is_it_uuid(ei_release['releases'][0]['tender']['id'], 4)
#     assert check_tender_id == True
#
#
# @pytestrail.case("22161")
# @pytest.mark.regression
# def test_22161_1(self, country, language):
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
# @pytestrail.case("22161")
# @pytest.mark.regression
# def test_22161_2(self, country, language):
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
# @pytestrail.case("22161")
# @pytest.mark.regression
# def test_22161_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     assert ei_release["releases"][0]["tender"]["status"] == "planning"
#
#
# @pytestrail.case("22162")
# @pytest.mark.regression
# def test_22162_1(self, country, language):
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
# @pytestrail.case("22162")
# @pytest.mark.regression
# def test_22162_2(self, country, language):
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
# @pytestrail.case("22162")
# @pytest.mark.regression
# def test_22162_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     assert ei_release["releases"][0]["tender"]["statusDetails"] == "empty"
#
#
# @pytestrail.case("22163")
# @pytest.mark.regression
# def test_22163_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["id"] = "1010101010"
#     payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22163")
# @pytest.mark.regression
# def test_22163_2(self, country, language):
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
# @pytestrail.case("22163")
# @pytest.mark.regression
# def test_22163_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["id"] = "1010101010"
#     payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     assert ei_release["releases"][0]["buyer"]["id"] == payload["buyer"]["identifier"]["scheme"] + "-" + \
#            payload["buyer"]["identifier"]["id"]
#
#
# @pytestrail.case("22164")
# @pytest.mark.regression
# def test_22164_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "24200000-6"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["classification"]["scheme"] = "CPV"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22164")
# @pytest.mark.regression
# def test_22164_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "24200000-6"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["classification"]["scheme"] = "CPV"
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
# @pytestrail.case("22164")
# @pytest.mark.regression
# def test_22164_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "24200000-6"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["classification"]["scheme"] = "CPV"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     assert ei_release["releases"][0]["tender"]["classification"]["id"] == payload["tender"]["classification"]["id"]
#
#
# @pytestrail.case("22165")
# @pytest.mark.regression
# def test_22165_1(self, country, language):
#     ei = EI()
#     budget_period = get_period()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
#     payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22165")
# @pytest.mark.regression
# def test_22165_2(self, country, language):
#     ei = EI()
#     budget_period = get_period()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
#     payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
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
# @pytestrail.case("22165")
# @pytest.mark.regression
# def test_22165_3(self, country, language):
#     ei = EI()
#     budget_period = get_period()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
#     payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     result = ei_release["releases"][0]["planning"]["budget"]["period"]["endDate"] > \
#              ei_release["releases"][0]["planning"]["budget"]["period"]["startDate"]
#     assert ei_release["releases"][0]["planning"]["budget"]["period"]["startDate"] == \
#            payload["planning"]["budget"]["period"]["startDate"]
#     assert ei_release["releases"][0]["planning"]["budget"]["period"]["endDate"] == \
#            payload["planning"]["budget"]["period"]["endDate"]
#     assert result == True
#
#
# @pytestrail.case("22166")
# @pytest.mark.regression
# def test_22166_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y/%m/%dT%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(minutes=10)
#     end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22166")
# @pytest.mark.regression
# def test_22166_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y/%m/%dT%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(minutes=10)
#     end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00"
#     assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.JsonMapping" \
#                                                              f"Exception: Text '{start_date}' could not be " \
#                                                              f"parsed at index 4 (through reference chain: " \
#                                                              f"com.procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate[\"planning\"]->com.procurement." \
#                                                              f"budget.model.dto.ei.request.EiCreate$Planning" \
#                                                              f"EiCreate[\"budget\"]->com.procurement.budget." \
#                                                              f"model.dto.ei.request.EiCreate$PlanningEi" \
#                                                              f"Create$BudgetEiCreate[\"period\"]->com." \
#                                                              f"procurement.budget.model.dto.ocds." \
#                                                              f"Period[\"startDate\"])"
#
#
# @pytestrail.case("22168")
# @pytest.mark.regression
# def test_22168_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y-%m-34T%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(days=90)
#     end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22168")
# @pytest.mark.regression
# def test_22168_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y-%m-34T%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(days=90)
#     end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00"
#     assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.JsonMapping" \
#                                                              f"Exception: Text '{start_date}' could not be " \
#                                                              f"parsed: Invalid value for DayOfMonth (valid " \
#                                                              f"values 1 - 28/31): 34 (through reference " \
#                                                              f"chain: com.procurement.budget.model.dto.ei." \
#                                                              f"request.EiCreate[\"planning\"]->com." \
#                                                              f"procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate$PlanningEiCreate[\"budget\"]->com." \
#                                                              f"procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate$PlanningEiCreate$BudgetEiCreate" \
#                                                              f"[\"period\"]->com.procurement.budget.model." \
#                                                              f"dto.ocds.Period[\"startDate\"])"
#
#
# @pytestrail.case("22169")
# @pytest.mark.regression
# def test_22169_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y-13-%dT%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(days=365)
#     end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22169")
# @pytest.mark.regression
# def test_22169_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y-13-%dT%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(days=365)
#     end_date = duration_date.strftime("%Y-%m-%dT%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00"
#     assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.JsonMapping" \
#                                                              f"Exception: Text '{start_date}' could " \
#                                                              f"not be parsed: Invalid value for MonthOfYear " \
#                                                              f"(valid values 1 - 12): 13 (through reference " \
#                                                              f"chain: com.procurement.budget.model.dto.ei." \
#                                                              f"request.EiCreate[\"planning\"]->com." \
#                                                              f"procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate$PlanningEiCreate[\"budget\"]->com." \
#                                                              f"procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate$PlanningEiCreate$BudgetEiCreate" \
#                                                              f"[\"period\"]->com.procurement.budget.model." \
#                                                              f"dto.ocds.Period[\"startDate\"])"
#
#
# @pytestrail.case("22170")
# @pytest.mark.regression
# def test_22170_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(minutes=10)
#     end_date = duration_date.strftime("%Y/%m/%dT%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22170")
# @pytest.mark.regression
# def test_22170_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(minutes=10)
#     end_date = duration_date.strftime("%Y/%m/%dT%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00"
#     assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.JsonMapping" \
#                                                              f"Exception: Text '{end_date}' could not be " \
#                                                              f"parsed at index 4 (through reference chain: " \
#                                                              f"com.procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate[\"planning\"]->com.procurement.budget." \
#                                                              f"model.dto.ei.request.EiCreate$PlanningEiCreate" \
#                                                              f"[\"budget\"]->com.procurement.budget.model.dto." \
#                                                              f"ei.request.EiCreate$PlanningEiCreate$BudgetEi" \
#                                                              f"Create[\"period\"]->com.procurement.budget." \
#                                                              f"model.dto.ocds.Period[\"endDate\"])"
#
#
# @pytestrail.case("22171")
# @pytest.mark.regression
# def test_22171_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(days=90)
#     end_date = duration_date.strftime("%Y-%m-34T%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22171")
# @pytest.mark.regression
# def test_22171_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(days=90)
#     end_date = duration_date.strftime("%Y-%m-34T%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00"
#     assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.JsonMapping" \
#                                                              f"Exception: Text '{end_date}' could not be " \
#                                                              f"parsed: Invalid value for DayOfMonth (valid " \
#                                                              f"values 1 - 28/31): 34 (through reference " \
#                                                              f"chain: com.procurement.budget.model.dto.ei." \
#                                                              f"request.EiCreate[\"planning\"]->com." \
#                                                              f"procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate$PlanningEiCreate[\"budget\"]->com." \
#                                                              f"procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate$PlanningEiCreate$BudgetEiCreate" \
#                                                              f"[\"period\"]->com.procurement.budget.model." \
#                                                              f"dto.ocds.Period[\"endDate\"])"
#
#
# @pytestrail.case("22172")
# @pytest.mark.regression
# def test_22172_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(days=365)
#     end_date = duration_date.strftime("%Y-13-%dT%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22172")
# @pytest.mark.regression
# def test_22172_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     date_now = datetime.datetime.now()
#     start_date = date_now.strftime("%Y-%m-%dT%H:%M:%SZ")
#     duration_date = date_now + datetime.timedelta(days=365)
#     end_date = duration_date.strftime("%Y-13-%dT%H:%M:%SZ")
#     payload["planning"]["budget"]["period"]["startDate"] = start_date
#     payload["planning"]["budget"]["period"]["endDate"] = end_date
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00"
#     assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.JsonMapping" \
#                                                              f"Exception: Text '{end_date}' could not be " \
#                                                              f"parsed: Invalid value for MonthOfYear (valid " \
#                                                              f"values 1 - 12): 13 (through reference chain: " \
#                                                              f"com.procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate[\"planning\"]->com.procurement." \
#                                                              f"budget.model.dto.ei.request.EiCreate$Planning" \
#                                                              f"EiCreate[\"budget\"]->com.procurement.budget." \
#                                                              f"model.dto.ei.request.EiCreate$PlanningEiCreate" \
#                                                              f"$BudgetEiCreate[\"period\"]->com.procurement." \
#                                                              f"budget.model.dto.ocds.Period[\"endDate\"])"
#
#
# @pytestrail.case("22173")
# @pytest.mark.regression
# def test_22173_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22173")
# @pytest.mark.regression
# def test_22173_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "45100000-8"
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
# @pytestrail.case("22173")
# @pytest.mark.regression
# def test_22173_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["tender"]["classification"]["id"] == payload["tender"]["classification"]["id"]
#
#
# @pytestrail.case("22174")
# @pytest.mark.regression
# def test_22174_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "03110000-5"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22174")
# @pytest.mark.regression
# def test_22174_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "03110000-5"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00.05"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid CPV."
#
#
# @pytestrail.case("22175")
# @pytest.mark.regression
# def test_22175_1(self, country, language):
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
# @pytestrail.case("22175")
# @pytest.mark.regression
# def test_22175_2(self, country, language):
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
# @pytestrail.case("22175")
# @pytest.mark.regression
# def test_22175_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["tag"][0] == "compiled"
#
#
# @pytestrail.case("22176")
# @pytest.mark.regression
# def test_22176_1(self, country, language):
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
# @pytestrail.case("22176")
# @pytest.mark.regression
# def test_22176_2(self, country, language):
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
# @pytestrail.case("22176")
# @pytest.mark.regression
# def test_22176_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["date"] == message_from_kafka["data"]["operationDate"]
#
#
# @pytestrail.case("22178")
# @pytest.mark.regression
# def test_22178_1(self, country, language):
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
# @pytestrail.case("22178")
# @pytest.mark.regression
# def test_22178_2(self, country, language):
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
# @pytestrail.case("22178")
# @pytest.mark.regression
# def test_22178_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["initiationType"] == "tender"
#
#
# @pytestrail.case("22181")
# @pytest.mark.regression
# def test_22181_1(self, country, language):
#     ei = EI()
#     budget_period = get_period()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
#     payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     payload['planning']['budget']['id'] = payload['tender']['classification']['id']
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22181")
# @pytest.mark.regression
# def test_22181_2(self, country, language):
#     ei = EI()
#     budget_period = get_period()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
#     payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     payload['planning']['budget']['id'] = payload['tender']['classification']['id']
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
# @pytestrail.case("22181")
# @pytest.mark.regression
# def test_22181_3(self, country, language):
#     ei = EI()
#     budget_period = get_period()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["budget"]["period"]["startDate"] = budget_period[0]
#     payload["planning"]["budget"]["period"]["endDate"] = budget_period[1]
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     payload['planning']['budget']['id'] = payload['tender']['classification']['id']
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["planning"]["budget"]["id"] == payload["tender"]["classification"]["id"]
#     assert ei_release["releases"][0]["planning"]["budget"]["period"]["startDate"] == \
#            payload["planning"]["budget"]["period"]["startDate"]
#     assert ei_release["releases"][0]["planning"]["budget"]["period"]["endDate"] == \
#            payload["planning"]["budget"]["period"]["endDate"]
#
#
# @pytestrail.case("22182")
# @pytest.mark.regression
# def test_22182_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["title"] = "This is some text for field"
#     payload["tender"]["description"] = "This is some text for field 22 orange"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22182")
# @pytest.mark.regression
# def test_22182_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["title"] = "This is some text for field"
#     payload["tender"]["description"] = "This is some text for field 22 orange"
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
# @pytestrail.case("22182")
# @pytest.mark.regression
# def test_22182_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["title"] = "This is some text for field"
#     payload["tender"]["description"] = "This is some text for field 22 orange"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["tender"]["title"] == payload["tender"]["title"]
#     assert ei_release["releases"][0]["tender"]["classification"]["id"] == payload["tender"]["classification"]["id"]
#
#
# @pytestrail.case("22183")
# @pytest.mark.regression
# def test_22183_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload['buyer']['name'] = 'Peter Alekseevich'
#     payload['buyer']['identifier']['id'] = '5_channel'
#     payload['buyer']['identifier']['scheme'] = 'MD-IDNO'
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22183")
# @pytest.mark.regression
# def test_22183_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload['buyer']['name'] = 'Peter Alekseevich'
#     payload['buyer']['identifier']['id'] = '5_channel'
#     payload['buyer']['identifier']['scheme'] = 'MD-IDNO'
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
# @pytestrail.case("22183")
# @pytest.mark.regression
# def test_22183_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload['buyer']['name'] = 'Peter Alekseevich'
#     payload['buyer']['identifier']['id'] = '5_channel'
#     payload['buyer']['identifier']['scheme'] = 'MD-IDNO'
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["parties"][0]["id"] == payload["buyer"]["identifier"]["scheme"] + "-" + \
#            payload["buyer"]["identifier"]["id"]
#     assert ei_release["releases"][0]["parties"][0]["roles"][0] == "buyer"
#
#
# @pytestrail.case("22184")
# @pytest.mark.regression
# def test_22184_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     procuring_entity = {
#         "name": "Procuring Entity Name",
#         "identifier": {
#             "id": "444444444444",
#             "scheme": "MD-IDNO",
#             "legalName": "Legal Name",
#             "uri": "http://454.to"
#         },
#         "address": {
#             "streetAddress": "street",
#             "postalCode": "785412",
#             "addressDetails": {
#                 "country": {
#                     "id": "MD"
#                 },
#                 "region": {
#                     "id": "3400000"
#                 },
#                 "locality": {
#                     "scheme": "CUATM",
#                     "id": "3401000",
#                     "description": ""
#                 }
#             }
#         },
#         "additionalIdentifiers": [
#             {
#                 "id": "additional identifier",
#                 "scheme": "MD-K",
#                 "legalName": "legalname",
#                 "uri": "http://k.to"
#             }
#         ],
#         "contactPoint": {
#             "name": "contact person",
#             "email": "string@mail.ccc",
#             "telephone": "98-79-87",
#             "faxNumber": "78-56-55",
#             "url": "http://url.com"
#         }
#     }
#     payload.update({"procuringEntity": procuring_entity})
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22184")
# @pytest.mark.regression
# def test_22184_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     procuring_entity = {
#         "name": "Procuring Entity Name",
#         "identifier": {
#             "id": "444444444444",
#             "scheme": "MD-IDNO",
#             "legalName": "Legal Name",
#             "uri": "http://454.to"
#         },
#         "address": {
#             "streetAddress": "street",
#             "postalCode": "785412",
#             "addressDetails": {
#                 "country": {
#                     "id": "MD"
#                 },
#                 "region": {
#                     "id": "3400000"
#                 },
#                 "locality": {
#                     "scheme": "CUATM",
#                     "id": "3401000",
#                     "description": ""
#                 }
#             }
#         },
#         "additionalIdentifiers": [
#             {
#                 "id": "additional identifier",
#                 "scheme": "MD-K",
#                 "legalName": "legalname",
#                 "uri": "http://k.to"
#             }
#         ],
#         "contactPoint": {
#             "name": "contact person",
#             "email": "string@mail.ccc",
#             "telephone": "98-79-87",
#             "faxNumber": "78-56-55",
#             "url": "http://url.com"
#         }
#     }
#     payload.update({"procuringEntity": procuring_entity})
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
# @pytestrail.case("22184")
# @pytest.mark.regression
# def test_22184_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     procuring_entity = {
#         "name": "Procuring Entity Name",
#         "identifier": {
#             "id": "444444444444",
#             "scheme": "MD-IDNO",
#             "legalName": "Legal Name",
#             "uri": "http://454.to"
#         },
#         "address": {
#             "streetAddress": "street",
#             "postalCode": "785412",
#             "addressDetails": {
#                 "country": {
#                     "id": "MD"
#                 },
#                 "region": {
#                     "id": "3400000"
#                 },
#                 "locality": {
#                     "scheme": "CUATM",
#                     "id": "3401000",
#                     "description": ""
#                 }
#             }
#         },
#         "additionalIdentifiers": [
#             {
#                 "id": "additional identifier",
#                 "scheme": "MD-K",
#                 "legalName": "legalname",
#                 "uri": "http://k.to"
#             }
#         ],
#         "contactPoint": {
#             "name": "contact person",
#             "email": "string@mail.ccc",
#             "telephone": "98-79-87",
#             "faxNumber": "78-56-55",
#             "url": "http://url.com"
#         }
#     }
#     payload.update({"procuringEntity": procuring_entity})
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     parties_obj_list = list()
#     for p in ei_release["releases"][0]["parties"]:
#         if p["roles"] == ["procuringEntity"]:
#             parties_obj_list.append(p)
#     for p in ei_release["releases"][0]["parties"]:
#         if p["roles"] == ["buyer"]:
#             parties_obj_list.append(p)
#     ei.delete_data_from_database(cpid)
#     parties_obj_dict = dict(parties_obj_list[0])
#     check_procuring_entity_role = ["procuringEntity"] in parties_obj_dict.values()
#     check_buyer_role = ["buyer"] in parties_obj_dict.values()
#     assert check_procuring_entity_role == False
#     assert check_buyer_role == True
#
#
# @pytestrail.case("22185")
# @pytest.mark.regression
# def test_22185_1(self, country, language):
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
# @pytestrail.case("22185")
# @pytest.mark.regression
# def test_22185_2(self, country, language):
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
# @pytestrail.case("22185")
# @pytest.mark.regression
# def test_22185_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["buyer"]["id"] == payload["buyer"]["identifier"]["scheme"] + "-" + \
#            payload["buyer"]["identifier"]["id"]
#     assert ei_release["releases"][0]["buyer"]["name"] == payload["buyer"]["name"]
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["title"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'tender.title' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["description"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'tender.description' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["rationale"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'planning.rationale' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_4(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["name"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.name' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_5(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.identifier.id' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_6(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["legalName"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.identifier.legalName' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_7(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["uri"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.identifier.uri' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_8(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["streetAddress"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.address.streetAddress' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_9(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["postalCode"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.address.postalCode' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_10(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.address.addressDetails.locality.scheme' " \
#                                                              "is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_11(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.address.addressDetails.locality.id' " \
#                                                              "is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_12(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
#     payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.address.addressDetails.locality." \
#                                                              "description' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_13(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["additionalIdentifiers"][0]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.additionalIdentifiers.id' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_14(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["additionalIdentifiers"][0]["scheme"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.additionalIdentifiers.scheme' is empty " \
#                                                              "or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_15(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["additionalIdentifiers"][0]["legalName"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.additionalIdentifiers.legalName' is empty " \
#                                                              "or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_16(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["additionalIdentifiers"][0]["uri"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.additionalIdentifiers.uri' " \
#                                                              "is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_17(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["contactPoint"]["name"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.contactPoint.name' is " \
#                                                              "empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_18(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["contactPoint"]["email"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.contactPoint.email' is " \
#                                                              "empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_19(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["contactPoint"]["telephone"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.contactPoint.telephone' is " \
#                                                              "empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_20(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["contactPoint"]["faxNumber"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The " \
#                                                              "attribute 'buyer.contactPoint.faxNumber' is " \
#                                                              "empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_21(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["contactPoint"]["url"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'buyer.contactPoint.url' is empty " \
#                                                              "or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_22(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The " \
#                                                              "attribute 'tender.items.deliveryAddress." \
#                                                              "streetAddress' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_23(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'tender.items.deliveryAddress." \
#                                                              "postalCode' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_24(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'deliveryAddress.addressDetails." \
#                                                              "locality.scheme' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_25(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'deliveryAddress.addressDetails." \
#                                                              "locality.id' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_26(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["description"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'deliveryAddress.addressDetails." \
#                                                              "locality.description' is empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_27(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["description"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.20.11"
#     assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value.The attribute " \
#                                                              "'tender.items.description' is " \
#                                                              "empty or blank."
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_28(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.06"
#     assert message_from_kafka["errors"][0]["description"] == "Cpv code not found. "
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_29(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["classification"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.03"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid cpv code. "
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_30(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.05"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid cpvs code. "
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_31(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.10"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid country. "
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_32(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.13"
#     assert message_from_kafka["errors"][0]["description"] == "Region not found. "
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_33(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["quantity"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                              "Exception: (was com.procurement.mdm.exception." \
#                                                              "InErrorException) (through reference chain: " \
#                                                              "com.procurement.mdm.model.dto.data.ei." \
#                                                              "EIRequest[\"tender\"]->com.procurement.mdm." \
#                                                              "model.dto.data.ei.EIRequest$Tender[\"items\"]" \
#                                                              "->java.util.ArrayList[0]->com.procurement." \
#                                                              "mdm.model.dto.data.ei.EIRequest$Tender$Item" \
#                                                              "[\"quantity\"])"
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_34(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["unit"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.06"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid unit code. "
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_35(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["budget"]["period"]["startDate"] = ""
#     value_of_key = payload["planning"]["budget"]["period"]["startDate"]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00"
#     assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.JsonMapping" \
#                                                              f"Exception: Text '{value_of_key}' could not " \
#                                                              f"be parsed at index 0 (through reference " \
#                                                              f"chain: com.procurement.budget.model.dto.ei." \
#                                                              f"request.EiCreate[\"planning\"]->com." \
#                                                              f"procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate$PlanningEiCreate[\"budget\"]->com." \
#                                                              f"procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate$PlanningEiCreate$BudgetEiCreate" \
#                                                              f"[\"period\"]->com.procurement.budget.model." \
#                                                              f"dto.ocds.Period[\"startDate\"])"
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_36(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["planning"]["budget"]["period"]["endDate"] = ""
#     value_of_key = payload["planning"]["budget"]["period"]["endDate"]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00"
#     assert message_from_kafka["errors"][0]["description"] == f"com.fasterxml.jackson.databind.JsonMapping" \
#                                                              f"Exception: Text '{value_of_key}' could not " \
#                                                              f"be parsed at index 0 (through reference " \
#                                                              f"chain: com.procurement.budget.model.dto.ei." \
#                                                              f"request.EiCreate[\"planning\"]->com." \
#                                                              f"procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate$PlanningEiCreate[\"budget\"]->com." \
#                                                              f"procurement.budget.model.dto.ei.request." \
#                                                              f"EiCreate$PlanningEiCreate$BudgetEiCreate" \
#                                                              f"[\"period\"]->com.procurement.budget.model." \
#                                                              f"dto.ocds.Period[\"endDate\"])"
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_37(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["identifier"]["scheme"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.12"
#     assert message_from_kafka["errors"][0]["description"] == "Registration scheme not found. "
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_38(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.11"
#     assert message_from_kafka["errors"][0]["description"] == "Country not found. "
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_39(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["region"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.13"
#     assert message_from_kafka["errors"][0]["description"] == "Region not found. "
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_40(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["typeOfBuyer"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc.Invalid" \
#                                                              "FormatException: Cannot deserialize value " \
#                                                              "of type `com.procurement.mdm.model.dto.data." \
#                                                              "TypeOfBuyer` from String \"\": value not one " \
#                                                              "of declared Enum instance names: " \
#                                                              "[NATIONAL_AGENCY, REGIONAL_AUTHORITY, " \
#                                                              "REGIONAL_AGENCY, BODY_PUBLIC, EU_INSTITUTION, " \
#                                                              "MINISTRY]\n at [Source: UNKNOWN; line: -1, " \
#                                                              "column: -1] (through reference chain: " \
#                                                              "com.procurement.mdm.model.dto.data.ei." \
#                                                              "EIRequest[\"buyer\"]->com.procurement.mdm." \
#                                                              "model.dto.data.OrganizationReference" \
#                                                              "[\"details\"]->com.procurement.mdm.model." \
#                                                              "dto.data.Details[\"typeOfBuyer\"])"
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_41(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainGeneralActivity"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc.Invalid" \
#                                                              "FormatException: Cannot deserialize value of " \
#                                                              "type `com.procurement.mdm.model.dto.data." \
#                                                              "MainGeneralActivity` from String \"\": value " \
#                                                              "not one of declared Enum instance names: " \
#                                                              "[DEFENCE, PUBLIC_ORDER_AND_SAFETY, " \
#                                                              "ECONOMIC_AND_FINANCIAL_AFFAIRS, ENVIRONMENT, " \
#                                                              "RECREATION_CULTURE_AND_RELIGION, EDUCATION, " \
#                                                              "SOCIAL_PROTECTION, HEALTH, " \
#                                                              "GENERAL_PUBLIC_SERVICES, " \
#                                                              "HOUSING_AND_COMMUNITY_AMENITIES]\n at " \
#                                                              "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                              "(through reference chain: com.procurement." \
#                                                              "mdm.model.dto.data.ei.EIRequest[\"buyer\"]->" \
#                                                              "com.procurement.mdm.model.dto.data." \
#                                                              "OrganizationReference[\"details\"]->com." \
#                                                              "procurement.mdm.model.dto.data.Details" \
#                                                              "[\"mainGeneralActivity\"])"
#
#
# @pytestrail.case("22186")
# @pytest.mark.smoke
# @pytest.mark.regression
# def test_22186_42(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["details"]["mainSectoralActivity"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc.Invalid" \
#                                                              "FormatException: Cannot deserialize value of " \
#                                                              "type `com.procurement.mdm.model.dto.data." \
#                                                              "MainSectoralActivity` from String \"\": " \
#                                                              "value not one of declared Enum instance names: " \
#                                                              "[EXPLORATION_EXTRACTION_GAS_OIL, ELECTRICITY, " \
#                                                              "POSTAL_SERVICES, " \
#                                                              "PRODUCTION_TRANSPORT_DISTRIBUTION_GAS_HEAT, " \
#                                                              "WATER, " \
#                                                              "URBAN_RAILWAY_TRAMWAY_TROLLEYBUS_BUS_SERVICES, " \
#                                                              "PORT_RELATED_ACTIVITIES, RAILWAY_SERVICES, " \
#                                                              "EXPLORATION_EXTRACTION_COAL_OTHER_SOLID_FUEL, " \
#                                                              "AIRPORT_RELATED_ACTIVITIES]\n at " \
#                                                              "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                              "(through reference chain: com.procurement." \
#                                                              "mdm.model.dto.data.ei.EIRequest[\"buyer\"]->" \
#                                                              "com.procurement.mdm.model.dto.data." \
#                                                              "OrganizationReference[\"details\"]->" \
#                                                              "com.procurement.mdm.model.dto.data." \
#                                                              "Details[\"mainSectoralActivity\"])"
#
#
# @pytestrail.case("22830")
# @pytest.mark.regression
# def test_22830_1(self, country, language):
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
# @pytestrail.case("22830")
# @pytest.mark.regression
# def test_22830_2(self, country, language):
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
# @pytestrail.case("22833")
# @pytest.mark.regression
# def test_22833_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = True
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22833")
# @pytest.mark.regression
# def test_22833_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = True
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#     assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                              "Exception: (was com.procurement.mdm.exception." \
#                                                              "InErrorException) (through reference chain: " \
#                                                              "com.procurement.mdm.model.dto.data.ei." \
#                                                              "EIRequest[\"tender\"]->com.procurement.mdm." \
#                                                              "model.dto.data.ei.EIRequest$Tender" \
#                                                              "[\"classification\"]->com.procurement.mdm." \
#                                                              "model.dto.data.ei.EIRequest$Tender$" \
#                                                              "Classification[\"id\"])"
#
#
# @pytestrail.case("22834")
# @pytest.mark.regression
# def test_22834_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = ""
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22834")
# @pytest.mark.regression
# def test_22834_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = ""
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.06"
#     assert message_from_kafka["errors"][0]["description"] == "Cpv code not found. "
#
#
# @pytestrail.case("22835")
# @pytest.mark.regression
# def test_22835_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "12322"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22835")
# @pytest.mark.regression
# def test_22835_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "12322"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.06"
#     assert message_from_kafka["errors"][0]["description"] == "Cpv code not found. "
#
#
# @pytestrail.case("22836")
# @pytest.mark.regression
# def test_22836_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "86655566"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22836")
# @pytest.mark.regression
# def test_22836_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "86655566"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.06"
#     assert message_from_kafka["errors"][0]["description"] == "Cpv code not found. "
#
#
# @pytestrail.case("22837")
# @pytest.mark.regression
# def test_22837_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "76100000-4"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22837")
# @pytest.mark.regression
# def test_22837_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "76100000-4"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
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
# @pytestrail.case("22837")
# @pytest.mark.regression
# def test_22837_4(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "76100000-4"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"]
#     ei_record = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_record["records"][0]["compiledRelease"]["tender"]["mainProcurementCategory"] == "services"
#
#
# @pytestrail.case("22838")
# @pytest.mark.regression
# def test_22838_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22838")
# @pytest.mark.regression
# def test_22838_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
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
# @pytestrail.case("22838")
# @pytest.mark.regression
# def test_22838_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"]
#     ei_record = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_record["records"][0]["compiledRelease"]["tender"]["mainProcurementCategory"] == "works"
#
#
# @pytestrail.case("22839")
# @pytest.mark.regression
# def test_22839_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "76100000-4"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22839")
# @pytest.mark.regression
# def test_22839_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "76100000-4"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
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
# @pytestrail.case("22839")
# @pytest.mark.regression
# def test_22839_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "76100000-4"
#     payload["planning"]["budget"]["id"] = payload["tender"]["classification"]["id"]
#     payload["tender"]["items"][0]["classification"]["id"] = payload["tender"]["classification"]["id"]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"]
#     ei_record = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_record["records"][0]["compiledRelease"]["tender"]["mainProcurementCategory"] == "services"
#
#
# @pytestrail.case("22840")
# @pytest.mark.regression
# def test_22840_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22840")
# @pytest.mark.regression
# def test_22840_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
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
# @pytestrail.case("22840")
# @pytest.mark.regression
# def test_22840_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"]
#     ei_record = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_record["records"][0]["compiledRelease"]["parties"][0]["address"]["addressDetails"]["country"][
#                "id"] == "MD"
#
#
# @pytestrail.case("22841")
# @pytest.mark.regression
# def test_22841_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22841")
# @pytest.mark.regression
# def test_22841_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
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
# @pytestrail.case("22841")
# @pytest.mark.regression
# def test_22841_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"]
#     ei_record = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_record["records"][0]["compiledRelease"]["parties"][0]["address"]["addressDetails"]["country"][
#                "scheme"] == "iso-alpha2"
#
#
# @pytestrail.case("22842")
# @pytest.mark.regression
# def test_22842_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22842")
# @pytest.mark.regression
# def test_22842_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
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
# @pytestrail.case("22842")
# @pytest.mark.regression
# def test_22842_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"]
#     ei_record = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_record["records"][0]["compiledRelease"]["parties"][0]["address"]["addressDetails"]["country"][
#                "description"] == "Moldova, Republica"
#
#
# @pytestrail.case("22843")
# @pytest.mark.regression
# def test_22843_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22843")
# @pytest.mark.regression
# def test_22843_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
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
# @pytestrail.case("22843")
# @pytest.mark.regression
# def test_22843_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"]
#     ei_record = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_record["records"][0]["compiledRelease"]["parties"][0]["address"]["addressDetails"]["country"][
#                "uri"] == "https://www.iso.org"
#
#
# @pytestrail.case("22908")
# @pytest.mark.regression
# def test_22908_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22908")
# @pytest.mark.regression
# def test_22908_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
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
# @pytestrail.case("22908")
# @pytest.mark.regression
# def test_22908_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     is_uuid_tender_id = is_valid_uuid(ei_release["releases"][0]["tender"]["id"], 4)
#     is_uuid_item_id = is_valid_uuid(ei_release["releases"][0]["tender"]["items"][0]["id"], 4)
#     assert is_uuid_tender_id == True
#     assert is_uuid_item_id == True
#     assert ei_release["releases"][0]["tender"]["title"] == payload["tender"]['title']
#
#     assert ei_release["releases"][0]["tender"]["classification"]["scheme"] == payload["tender"]["classification"][
#         "scheme"]
#     assert ei_release["releases"][0]["tender"]["classification"]["id"] == payload["tender"]["classification"]["id"]
#     assert ei_release["releases"][0]["tender"]["classification"][
#                "description"] == "Lucrări de pregătire a şantierului"
#     assert ei_release["releases"][0]["planning"]["budget"]["id"] == payload["tender"]["classification"]["id"]
#     assert ei_release["releases"][0]["planning"]["budget"]["period"]["startDate"] == \
#            payload["planning"]["budget"]["period"]["startDate"]
#     assert ei_release["releases"][0]["planning"]["budget"]["period"]["endDate"] == \
#            payload["planning"]["budget"]["period"]["endDate"]
#     assert ei_release["releases"][0]["planning"]["rationale"] == payload["planning"]["rationale"]
#     assert ei_release["releases"][0]["buyer"]["id"] == payload["buyer"]["identifier"]["scheme"] + "-" + \
#            payload["buyer"]["identifier"]["id"]
#     assert ei_release["releases"][0]["buyer"]["name"] == payload["buyer"]["name"]
#     assert ei_release["releases"][0]["parties"][0]["id"] == payload["buyer"]["identifier"]["scheme"] + "-" + \
#            payload["buyer"]["identifier"]["id"]
#     assert ei_release["releases"][0]["parties"][0]["name"] == payload["buyer"]["name"]
#     assert ei_release["releases"][0]["parties"][0]["identifier"]["scheme"] == payload["buyer"]["identifier"][
#         "scheme"]
#     assert ei_release["releases"][0]["parties"][0]["identifier"]["id"] == payload["buyer"]["identifier"]["id"]
#     assert ei_release["releases"][0]["parties"][0]["identifier"]["legalName"] == payload["buyer"]["identifier"][
#         "legalName"]
#     assert ei_release["releases"][0]["parties"][0]["identifier"]["uri"] == payload["buyer"]["identifier"]["uri"]
#     assert ei_release["releases"][0]["parties"][0]["address"]["streetAddress"] == payload["buyer"]["address"][
#         "streetAddress"]
#     assert ei_release["releases"][0]["parties"][0]["address"]["postalCode"] == payload["buyer"]["address"][
#         "postalCode"]
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                "scheme"] == "iso-alpha2"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"] == \
#            payload["buyer"]["address"]["addressDetails"]["country"]["id"]
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                "description"] == "Moldova, Republica"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                "uri"] == "https://www.iso.org"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"] == "CUATM"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"] == "1700000"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                "description"] == "Cahul"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                "uri"] == "http://statistica.md"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                "scheme"] == "CUATM"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"] == "1701000"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                "uri"] == "http://statistica.md"
#     assert ei_release["releases"][0]["parties"][0]["additionalIdentifiers"][0] == \
#            payload["buyer"]["additionalIdentifiers"][0]
#     assert ei_release["releases"][0]["parties"][0]["contactPoint"] == \
#            payload["buyer"]["contactPoint"]
#     assert ei_release["releases"][0]["parties"][0]["details"] == \
#            payload["buyer"]["details"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["description"] == payload["tender"]["items"][0][
#         "description"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["classification"]["scheme"] == "CPV"
#     assert ei_release["releases"][0]["tender"]["items"][0]["classification"]["id"] == \
#            payload["tender"]["items"][0]["classification"]["id"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["classification"][
#                "description"] == "Lucrări de pregătire a şantierului"
#     assert ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["scheme"] == "CPVS"
#     assert ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
#                "description"] == "Oţel carbon"
#     assert ei_release["releases"][0]["tender"]["items"][0]["quantity"] == payload["tender"]["items"][0]["quantity"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["unit"]["name"] == "Parsec"
#     assert ei_release["releases"][0]["tender"]["items"][0]["unit"]["id"] == payload["tender"]["items"][0]["unit"][
#         "id"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["streetAddress"] == \
#            payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["postalCode"] == \
#            payload["tender"]["items"][0]["deliveryAddress"]["postalCode"]
#
#     if payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] == "MD":
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#                    "id"] == \
#                payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"]
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#                    "scheme"] == "iso-alpha2"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#                    "description"] == "Moldova, Republica"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#                    "uri"] == "https://www.iso.org"
#     if payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] == "1700000":
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#                    "id"] == "1700000"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#                    "scheme"] == "CUATM"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#                    "description"] == "Cahul"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#                    "uri"] == "http://statistica.md"
#
#     if payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] == 'CUATM' and \
#             payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] == '1701000':
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                    "id"] == "1701000"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                    "scheme"] == "CUATM"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                    "description"] == "mun.Cahul"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                    "uri"] == "http://statistica.md"
#     elif payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] != "CUATM" and \
#             payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] == "1701000":
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                    "id"] == "1701000"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                    "scheme"] == payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                    "scheme"]
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                    "description"] == payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                    "description"]
#
#
# @pytestrail.case("23995")
# @pytest.mark.regression
# def test_23995_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["classification"]["id"] = "86655566"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("23995")
# @pytest.mark.regression
# def test_23995_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["classification"]["id"] = "86655566"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.03"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid cpv code. "
#
#
# @pytestrail.case("23993")
# @pytest.mark.regression
# def test_23993_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "866zx"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("23993")
# @pytest.mark.regression
# def test_23993_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "866zx"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.05"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid cpvs code. "
#
#
# @pytestrail.case("23994")
# @pytest.mark.regression
# def test_23994_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22994")
# @pytest.mark.regression
# def test_23994_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
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
# @pytestrail.case("23994")
# @pytest.mark.regression
# def test_23994_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["scheme"] == "CPVS"
#     assert ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"] == \
#            payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
#     if payload["tender"]["items"][0]["additionalClassifications"][0]["id"] == "AA12-4":
#         assert ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
#                    "description"] == "Oţel carbon"
#
#
# @pytestrail.case("23996")
# @pytest.mark.regression
# def test_23996_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["classification"]["id"] = "45100000-8"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22996")
# @pytest.mark.regression
# def test_23996_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["classification"]["id"] = "45100000-8"
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
# @pytestrail.case("23996")
# @pytest.mark.regression
# def test_23996_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["classification"]["id"] = "45100000-8"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     if payload["tender"]["items"][0]["classification"]["id"] == "45100000-8":
#         assert ei_release["releases"][0]["tender"]["items"][0]["classification"]["scheme"] == "CPV"
#         assert ei_release["releases"][0]["tender"]["items"][0]["classification"]["id"] == \
#                payload["tender"]["items"][0]["classification"]["id"]
#         assert ei_release["releases"][0]["tender"]["items"][0]["classification"][
#                    "description"] == "Lucrări de pregătire a şantierului"
#
#
# @pytestrail.case("23997")
# @pytest.mark.regression
# def test_23997_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["unit"]["id"] = "zx10"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("23997")
# @pytest.mark.regression
# def test_23997_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["unit"]["id"] = "zx10"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.06"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid unit code. "
#
#
# @pytestrail.case("23998")
# @pytest.mark.regression
# def test_23998_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["unit"]["id"] = '120'
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("23998")
# @pytest.mark.regression
# def test_23998_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["unit"]["id"] = '120'
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
# @pytestrail.case("23998")
# @pytest.mark.regression
# def test_23998_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["unit"]["id"] = "120"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     if payload["tender"]["items"][0]["unit"]["id"] == "120":
#         assert ei_release["releases"][0]["tender"]["items"][0]["unit"]["name"] == "Milion decalitri"
#         assert ei_release["releases"][0]["tender"]["items"][0]["unit"]["id"] == \
#                payload["tender"]["items"][0]["unit"]["id"]
#
#
# @pytestrail.case("23999")
# @pytest.mark.regression
# def test_23999_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "DE"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("23999")
# @pytest.mark.regression
# def test_23999_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "DE"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     time.sleep(3)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.01.10"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid country. "
#
#
# @pytestrail.case("24000")
# @pytest.mark.regression
# def test_24000_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("24000")
# @pytest.mark.regression
# def test_24000_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
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
# @pytestrail.case("24000")
# @pytest.mark.regression
# def test_24000_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     if payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] == "MD":
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#                    "id"] == payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"]
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#                    "scheme"] == "iso-alpha2"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#                    "description"] == "Moldova, Republica"
#         assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#                    "uri"] == "https://www.iso.org"
#
#
# @pytestrail.case("22133")
# @pytest.mark.regression
# def test_22133_1(self, country, language):
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
# @pytestrail.case("22133")
# @pytest.mark.regression
# def test_22133_2(self, country, language):
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
# @pytestrail.case('22133')
# @pytest.mark.regression
# def test_22133_3(self, language, country):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["tender"]["title"] == payload["tender"]["title"]
#     assert ei_release["releases"][0]["tender"]["classification"]["scheme"] == "CPV"
#     assert ei_release["releases"][0]["tender"]["classification"]["id"] == payload["tender"]["classification"]["id"]
#     assert ei_release["releases"][0]["tender"]["classification"][
#                "description"] == "Lucrări de pregătire a şantierului"
#     assert ei_release["releases"][0]["planning"]["budget"]["id"] == payload["tender"]["classification"]["id"]
#     assert ei_release["releases"][0]["planning"]["budget"]["period"]["startDate"] == \
#            payload["planning"]["budget"]["period"]["startDate"]
#     assert ei_release["releases"][0]["planning"]["budget"]["period"]["endDate"] == \
#            payload["planning"]["budget"]["period"]["endDate"]
#     assert ei_release["releases"][0]["buyer"]["id"] == payload["buyer"]["identifier"]["scheme"] + "-" + \
#            payload["buyer"]["identifier"]["id"]
#     assert ei_release["releases"][0]["buyer"]["name"] == payload["buyer"]["name"]
#     assert ei_release["releases"][0]["parties"][0]["id"] == payload["buyer"]["identifier"]["scheme"] + "-" + \
#            payload["buyer"]["identifier"]["id"]
#     assert ei_release["releases"][0]["parties"][0]["name"] == payload["buyer"]["name"]
#     assert ei_release["releases"][0]["parties"][0]["identifier"]["scheme"] == payload["buyer"]["identifier"][
#         "scheme"]
#     assert ei_release["releases"][0]["parties"][0]["identifier"]["id"] == payload["buyer"]["identifier"]["id"]
#     assert ei_release["releases"][0]["parties"][0]["identifier"]["legalName"] == payload["buyer"]["identifier"][
#         "legalName"]
#     assert ei_release["releases"][0]["parties"][0]["address"]["streetAddress"] == payload["buyer"]["address"][
#         "streetAddress"]
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                "scheme"] == "iso-alpha2"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"]["id"] == \
#            payload["buyer"]["address"]["addressDetails"]["country"]["id"]
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                "description"] == "Moldova, Republica"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                "uri"] == "https://www.iso.org"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["scheme"] == "CUATM"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"]["id"] == "1700000"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                "description"] == "Cahul"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                "uri"] == "http://statistica.md"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                "scheme"] == "CUATM"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                "description"] == "mun.Cahul"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"] == "1701000"
#     assert ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                "uri"] == "http://statistica.md"
#     assert ei_release["releases"][0]["parties"][0]["contactPoint"] == \
#            payload["buyer"]["contactPoint"]
#
#
# @pytestrail.case("22167")
# @pytest.mark.regression
# def test_22167_1(self, country, language):
#     ei = EI()
#     budget_period = get_period()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload['planning']['budget']['period']['startDate'] = budget_period[1]
#     payload["planning"]["budget"]["period"]["endDate"] = budget_period[0]
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("22167")
# @pytest.mark.regression
# def test_22167_2(self, country, language):
#     ei = EI()
#     budget_period = get_period()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload['planning']['budget']['period']['startDate'] = budget_period[1]
#     payload["planning"]["budget"]["period"]["endDate"] = budget_period[0]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.01.01"
#     assert message_from_kafka["errors"][0]["description"] == "Invalid period."
#
#
# @pytestrail.case("24001")
# @pytest.mark.regression
# def test_24001_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "ABCD1234"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("24001")
# @pytest.mark.regression
# def test_24001_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "ABCD1234"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.13"
#     assert message_from_kafka["errors"][0]["description"] == "Region not found. "
#
#
# @pytestrail.case("24002")
# @pytest.mark.regression
# def test_24002_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("24002")
# @pytest.mark.regression
# def test_24002_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
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
# @pytestrail.case("24002")
# @pytest.mark.regression
# def test_24002_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] \
#            == payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#                "scheme"] == "CUATM"
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#                "description"] == "Cahul"
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#                "uri"] == "http://statistica.md"
#
#
# @pytestrail.case("24003")
# @pytest.mark.regression
# def test_24003_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "ABCD1234"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("24003")
# @pytest.mark.regression
# def test_24003_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "ABCD1234"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.14"
#     assert message_from_kafka["errors"][0]["description"] == "Locality not found. "
#
#
# @pytestrail.case("24004")
# @pytest.mark.regression
# def test_24004_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "0101000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("24004")
# @pytest.mark.regression
# def test_24004_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "0101000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.20.00.14"
#     assert message_from_kafka["errors"][0]["description"] == "Locality not found. "
#
#
# @pytestrail.case("24005")
# @pytest.mark.regression
# def test_24005_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("24005")
# @pytest.mark.regression
# def test_24005_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
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
# @pytestrail.case("24005")
# @pytest.mark.regression
# def test_24005_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                "id"] == \
#            payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                "scheme"] == "CUATM"
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                "description"] == "mun.Cahul"
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                "uri"] == "http://statistica.md"
#
#
# @pytestrail.case("24006")
# @pytest.mark.regression
# def test_24006_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "OTHER"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("24006")
# @pytest.mark.regression
# def test_24006_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "OTHER"
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
# @pytestrail.case("24006")
# @pytest.mark.regression
# def test_24006_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "1700000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "1701000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "OTHER"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                "id"] == \
#            payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                "scheme"] == payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                "description"] == payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#                "description"]
#
#
# @pytestrail.case("24011")
# @pytest.mark.regression
# def test_24011_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["id"] = "1"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("24011")
# @pytest.mark.regression
# def test_24011_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["id"] = "1"
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
# @pytestrail.case("24011")
# @pytest.mark.regression
# def test_24011_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["items"][0]["id"] = "1"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     check_id_of_item = is_valid_uuid(ei_release["releases"][0]["tender"]["items"][0]["id"], 4)
#     assert check_id_of_item == True
#
#
# @pytestrail.case("24013")
# @pytest.mark.regression
# def test_24013_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "90900000-6"
#     payload["tender"]["items"][0]["classification"]["id"] = "50100000-6"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("24013")
# @pytest.mark.regression
# def test_24013_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "90900000-6"
#     payload["tender"]["items"][0]["classification"]["id"] = "50100000-6"
#     value_of_key = payload["tender"]["items"][0]["classification"]["id"]
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     assert message_from_kafka["errors"][0]["code"] == "400.10.00.05"
#     assert message_from_kafka["errors"][0]["description"] == f"Invalid CPV.Invalid CPV code in " \
#                                                              f"classification(s) '{value_of_key}'"
#
#
# @pytestrail.case("24012")
# @pytest.mark.regression
# def test_24012_1(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     payload["tender"]["items"][0]["id"] = "1"
#     payload["tender"]["items"][0]["description"] = "item_1"
#     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
#     payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
#     payload["tender"]["items"][0]["quantity"] = 10
#     payload["tender"]["items"][0]["unit"]["id"] = "10"
#     payload["tender"]["items"][0]["unit"]["name"] = "name"
#     payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = "Khreshchatyk"
#     payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = "01124"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#         "description"] = "description_1"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["scheme"] = "scheme_1"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["uri"] = "www.deutch"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "0101000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#         "description"] = "description_2"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["scheme"] = "scheme_2"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["uri"] = "www,regi_16"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "0101000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["uri"] = "ww.io.io"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#         "description"] = "description_test"
#     create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei.delete_data_from_database(cpid)
#     assert create_ei_response.text == "ok"
#     assert create_ei_response.status_code == 202
#
#
# @pytestrail.case("24012")
# @pytest.mark.regression
# def test_24012_2(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     payload["tender"]["items"][0]["id"] = "1"
#     payload["tender"]["items"][0]["description"] = "item_1"
#     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
#     payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
#     payload["tender"]["items"][0]["quantity"] = 10
#     payload["tender"]["items"][0]["unit"]["id"] = "10"
#     payload["tender"]["items"][0]["unit"]["name"] = "name"
#     payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = "Khreshchatyk"
#     payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = "01124"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#         "description"] = "description_1"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["scheme"] = "scheme_1"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["uri"] = "www.deutch"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "0101000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#         "description"] = "description_2"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["scheme"] = "scheme_2"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["uri"] = "www,regi_16"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "0101000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["uri"] = "ww.io.io"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#         "description"] = "description_test"
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
# @pytestrail.case("24012")
# @pytest.mark.regression
# def test_24012_3(self, country, language):
#     ei = EI()
#     payload = copy.deepcopy(payload_ei_full_data_model)
#     payload["tender"]["classification"]["id"] = "45100000-8"
#     payload["tender"]["items"][0]["id"] = "1"
#     payload["tender"]["items"][0]["description"] = "item_1"
#     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
#     payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA12-4"
#     payload["tender"]["items"][0]["quantity"] = 10
#     payload["tender"]["items"][0]["unit"]["id"] = "10"
#     payload["tender"]["items"][0]["unit"]["name"] = "name"
#     payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = "Khreshchatyk"
#     payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = "01124"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = "MD"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#         "description"] = "description_1"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["scheme"] = "scheme_1"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["uri"] = "www.deutch"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = "0101000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#         "description"] = "description_2"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["scheme"] = "scheme_2"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["uri"] = "www,regi_16"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = "0101000"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["uri"] = "ww.io.io"
#     payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
#         "description"] = "description_test"
#     ei.create_request_ei(payload=payload, lang=language, country=country)
#     message_from_kafka = ei.get_message_from_kafka()
#     cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
#     ei_url = message_from_kafka["data"]["url"] + "/" + cpid
#     ei_release = requests.get(url=ei_url).json()
#     ei.delete_data_from_database(cpid)
#     check_id_of_item = is_valid_uuid(ei_release["releases"][0]["tender"]["items"][0]["id"])
#     assert check_id_of_item == True
#     assert ei_release["releases"][0]["tender"]["items"][0]["description"] == \
#            payload["tender"]["items"][0]["description"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["classification"]["scheme"] == "CPV"
#     assert ei_release["releases"][0]["tender"]["items"][0]["classification"]["id"] == \
#            payload["tender"]["items"][0]["classification"]["id"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["classification"]["description"] == \
#            "Lucrări de valorificare a terenurilor virane"
#     assert ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
#                "scheme"] == "CPVS"
#     assert ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"] == \
#            payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
#                "description"] == "Oţel carbon"
#     assert ei_release["releases"][0]["tender"]["items"][0]["quantity"] == 10
#     assert ei_release["releases"][0]["tender"]["items"][0]["unit"]["name"] == "Parsec"
#     assert ei_release["releases"][0]["tender"]["items"][0]["unit"]["id"] == \
#            payload["tender"]["items"][0]["unit"]["id"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["streetAddress"] == \
#            payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["postalCode"] == \
#            payload["tender"]["items"][0]["deliveryAddress"]["postalCode"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#                "scheme"] == "iso-alpha2"
#     assert \
#         ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#             "id"] == "MD"
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"][
#                "description"] == "Moldova, Republica"
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
#                "country"]["uri"] == "https://www.iso.org"
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
#                "region"]["scheme"] == "CUATM"
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
#                "region"]["id"] == payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"][
#                "id"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
#                "region"]["description"] == "mun.Chişinău"
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
#                "region"]["uri"] == "http://statistica.md"
#
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
#                "locality"]["scheme"] == \
#            payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
#                "locality"]["id"] == \
#            payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"]
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
#                "locality"]["description"] == "mun.Chişinău"
#     assert ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
#                "locality"]["uri"] == "http://statistica.md"
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
