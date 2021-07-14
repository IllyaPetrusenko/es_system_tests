import copy
import datetime

import requests
from pytest_testrail.plugin import pytestrail
from tests.bpe_create_ei.payloads import payload_ei_full_data_model
from tests.essences.ei import EI
from useful_functions import compare_actual_result_and_expected_result, get_human_date_in_utc_format, is_it_uuid, \
    calculated_new_date_for_request_sending


class TestCheckTheImpossibilityToCreateEIWithoutObligatoryData(object):
    @pytestrail.case("22132")
    def test_delete_tender_object_from_the_payload_22132_1(self, country, language, instance, cassandra_username,
                                                           cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{'code': '400.00.00.00', 'description': 'Data processing exception.'}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_title_field_from_the_payload_22132_2(self, country, language, instance, cassandra_username,
                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["title"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_classification_object_from_the_payload_22132_3(self, country, language, instance,
                                                                          cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["classification"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_classification_id_field_from_the_payload_22132_4(self, country, language, instance,
                                                                            cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_planning_object_from_the_payload_22132_5(self, country, language, instance, cassandra_username,
                                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_planning_budget_object_from_the_payload_22132_6(self, country, language, instance,
                                                                    cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_planning_budget_period_object_from_the_payload_22132_7(self, country, language, instance,
                                                                           cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]["period"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_planning_budget_period_start_date_field_from_the_payload_22132_8(self, country, language, instance,
                                                                                     cassandra_username,
                                                                                     cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]["period"]["startDate"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_planning_budget_period_end_date_field_from_the_payload_22132_9(self, country, language, instance,
                                                                                   cassandra_username,
                                                                                   cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["planning"]["budget"]["period"]["endDate"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_object_from_the_payload_22132_10(self, country, language, instance, cassandra_username,
                                                           cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_name_field_from_the_payload_22132_11(self, country, language, instance, cassandra_username,
                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["name"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_identifier_field_from_the_payload_22132_12(self, country, language, instance,
                                                                     cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["identifier"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_identifier_scheme_field_from_the_payload_22132_13(self, country, language, instance,
                                                                            cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["identifier"]["scheme"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_identifier_id_field_from_the_payload_22132_14(self, country, language, instance,
                                                                        cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["identifier"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_identifier_legal_name_field_from_the_payload_22132_15(self, country, language, instance,
                                                                                cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["identifier"]["legalName"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_object_from_the_payload_22132_16(self, country, language, instance,
                                                                   cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_street_address_object_from_the_payload_22132_17(self, country, language, instance,
                                                                                  cassandra_username,
                                                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["streetAddress"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_address_details_object_from_the_payload_22132_18(self, country, language, instance,
                                                                                   cassandra_username,
                                                                                   cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_address_details_country_object_from_the_payload_22132_19(self, country, language,
                                                                                           instance,
                                                                                           cassandra_username,
                                                                                           cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["country"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_address_details_country_id_field_from_the_payload_22132_20(self, country, language,
                                                                                             instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["country"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_address_details_region_field_from_the_payload_22132_21(self, country, language,
                                                                                         instance,
                                                                                         cassandra_username,
                                                                                         cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["region"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_address_details_region_id_field_from_the_payload_22132_22(self, country, language,
                                                                                            instance,
                                                                                            cassandra_username,
                                                                                            cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["region"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_address_details_locality_field_from_the_payload_22132_23(self, country, language,
                                                                                           instance,
                                                                                           cassandra_username,
                                                                                           cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["locality"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_address_details_locality_scheme_field_from_the_payload_22132_24(self, country,
                                                                                                  language,
                                                                                                  instance,
                                                                                                  cassandra_username,
                                                                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_address_details_locality_id_field_from_the_payload_22132_25(self, country,
                                                                                              language, instance,
                                                                                              cassandra_username,
                                                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["locality"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_address_details_locality_description_field_22132_26(self, country, language,
                                                                                      instance, cassandra_username,
                                                                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["address"]["addressDetails"]["locality"]["description"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_contact_point_field_from_the_payload_22132_27(self, country, language,
                                                                                instance, cassandra_username,
                                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["contactPoint"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_contact_point_name_field_from_the_payload_22132_28(self, country, language,
                                                                                     instance, cassandra_username,
                                                                                     cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["contactPoint"]["name"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_contact_point_email_field_from_the_payload_22132_29(self, country, language,
                                                                                      instance, cassandra_username,
                                                                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["contactPoint"]["email"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_buyer_address_contact_point_telephone_field_from_the_payload_22132_30(self, country, language,
                                                                                          instance, cassandra_username,
                                                                                          cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["buyer"]["contactPoint"]["telephone"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_id_field_from_the_payload_22132_31(self, country, language,
                                                                    instance, cassandra_username,
                                                                    cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_description_field_from_the_payload_22132_32(self, country, language,
                                                                             instance, cassandra_username,
                                                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["description"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_classification_field_from_the_payload_22132_33(self, country, language,
                                                                                instance, cassandra_username,
                                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["classification"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_classification_id_field_from_the_payload_22132_34(self, country, language,
                                                                                   instance, cassandra_username,
                                                                                   cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_additional_classifications_id_field_from_the_payload_22132_35(self, country, language,
                                                                                               instance,
                                                                                               cassandra_username,
                                                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_delivery_address_field_from_the_payload_22132_36(self, country, language,
                                                                                  instance, cassandra_username,
                                                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_delivery_address_address_details_field_from_the_payload_22132_37(self, country,
                                                                                                  language,
                                                                                                  instance,
                                                                                                  cassandra_username,
                                                                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_delivery_address_address_details_country_field_22132_38(self, country,
                                                                                         language, instance,
                                                                                         cassandra_username,
                                                                                         cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_delivery_address_address_details_country_id_field_22132_39(self, country,
                                                                                            language, instance,
                                                                                            cassandra_username,
                                                                                            cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_delivery_address_address_details_region_field_22132_40(self, country,
                                                                                        language, instance,
                                                                                        cassandra_username,
                                                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_delivery_address_address_details_locality_scheme_22132_41(self, country,
                                                                                           language, instance,
                                                                                           cassandra_username,
                                                                                           cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_delivery_address_address_details_region_id_22132_42(self, country, language,
                                                                                     instance, cassandra_username,
                                                                                     cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_delivery_address_address_details_locality_id_22132_43(self, country,
                                                                                       language, instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_delivery_address_address_details_locality_description_22132_44(self, country,
                                                                                                language, instance,
                                                                                                cassandra_username,
                                                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["description"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_quantity_field_from_the_payload_22132_45(self, country, language, instance,
                                                                          cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["quantity"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_unit_field_from_the_payload_22132_46(self, country, language, instance,
                                                                      cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["unit"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
    def test_delete_tender_items_unit_id_field_from_the_payload_22132_47(self, country, language, instance,
                                                                         cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["unit"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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


class TestCheckThePossibilityToCreateEiOnObligatoryDataModelAddItems(object):
    @pytestrail.case("22133")
    def test_send_the_request_22133_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22133")
    def test_see_the_result_in_feed_point_22133_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_create_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22133")
    def test_check_sent_fields_are_published_in_the_ei_release_22133_3(self, country, language, instance,
                                                                       cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cp_id = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cp_id
        ei_release = requests.get(url=ei_url).json()
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


class TestCheckTheCpIdOfEIisFormedCorrectly(object):
    @pytestrail.case("22157")
    def test_send_the_request_22157_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22157")
    def test_see_the_result_in_feed_point_22157_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_create_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22157")
    def test_check_the_ei_cpid_is_formed_according_to_the_pattern_22157_3(self, country, language, instance,
                                                                          cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cp_id = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        actual_result_date = get_human_date_in_utc_format(int(cp_id[15:28]))[0]
        expected_result_date = message_from_kafka["data"]["operationDate"]
        actual_result_cpid_first_part = cp_id[0:15]
        expected_result_cpid_first_part = "ocds-t1s2t3-MD-"
        assert compare_actual_result_and_expected_result(expected_result=expected_result_date,
                                                         actual_result=actual_result_date)
        assert compare_actual_result_and_expected_result(expected_result=expected_result_cpid_first_part,
                                                         actual_result=actual_result_cpid_first_part)


class TestCheckTheTimestampOfEiOcidOfCoincidesWithRequestSentDate(object):
    @pytestrail.case("22158")
    def test_send_the_request_22158_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22158")
    def test_see_the_result_in_feed_point_22158_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_create_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22158")
    def test_check_the_timestamp_of_the_ei_coincides_with_the_release_date_22158_3(self, country, language,
                                                                                   instance, cassandra_username,
                                                                                   cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cp_id = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cp_id
        ei_release = requests.get(url=ei_url).json()
        release_id = ei_release["releases"][0]["id"]
        timestamp = int(release_id[29:39])
        convert_timestamp_to_date = datetime.datetime.utcfromtimestamp(timestamp)
        convert_date_to_human_date = convert_timestamp_to_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        actual_result = convert_date_to_human_date
        expected_result = message_from_kafka["data"]["operationDate"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheReleaseDateCoincidesWithRequestSentDate(object):
    @pytestrail.case("22159")
    def test_send_the_request_22159_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22159")
    def test_see_the_result_in_feed_point_22159_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_create_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22159")
    def test_check_the_release_date_in_ei_record_coincides_with_the_date_of_request_22159_3(self, country, language,
                                                                                            instance,
                                                                                            cassandra_username,
                                                                                            cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cp_id = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cp_id
        ei_release = requests.get(url=ei_url).json()
        expected_result = message_from_kafka["data"]["operationDate"]
        actual_result = ei_release["releases"][0]["date"]
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheIdentificationOfTenderEqualsTheOCIDofTheEI(object):
    @pytestrail.case("22160")
    def test_send_the_request_22160_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22160")
    def test_see_the_result_in_feed_point_22160_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_create_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22160")
    def test_check_the_tender_id_has_the_same_value_as_cp_id_of_the_ei_22160_3(self, country, language, instance,
                                                                               cassandra_username,
                                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cp_id = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cp_id
        ei_release = requests.get(url=ei_url).json()
        actual_result = str(is_it_uuid(ei_release['releases'][0]['tender']['id'], 4))
        expected_result = "True"
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheIdInCompiledReleaseHasAnAppropriateValueInTheEiRecord(object):
    @pytestrail.case("22180")
    def test_send_the_request_22180_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22180")
    def test_see_the_result_in_feed_point_22180_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_create_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22180")
    def test_check_the_release_id_field_is_formed_on_the_pattern_cp_id_plus_timestamp_22180_3(self, country,
                                                                                              language, instance,
                                                                                              cassandra_username,
                                                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cp_id = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cp_id
        ei_release = requests.get(url=ei_url).json()
        ei_release_id = ei_release["releases"][0]["id"]
        ei_release_timestamp = int(ei_release_id[29:42])
        convert_timestamp_to_date = get_human_date_in_utc_format(ei_release_timestamp)
        assert compare_actual_result_and_expected_result(expected_result=cp_id, actual_result=ei_release_id[0:28])
        assert compare_actual_result_and_expected_result(expected_result=convert_timestamp_to_date[0],
                                                         actual_result=ei_release["releases"][0]["date"])
        assert compare_actual_result_and_expected_result(
            expected_result=f"{cp_id}" + f"-{str(ei_release_timestamp)}",
            actual_result=ei_release["releases"][0]["id"])


class TestCheckTheFieldsWithEmptyStringsAreNotPublishedInThePublicPoint(object):
    @pytestrail.case("22186")
    def test_tender_title_as_empty_string_22186_1(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["title"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'tender.title' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_description_as_empty_string_22186_2(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'tender.description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_planning_rationale_as_empty_string_22186_3(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["rationale"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'planning.rationale' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_name_as_emptystring_22186_4(self, country, language, instance, cassandra_username,
                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["name"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.name' is "
                                               "empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_identifier_id_as_empty_string_22186_5(self, country, language, instance, cassandra_username,
                                                         cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'buyer.identifier.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_identifier_legal_name_as_empty_string_22186_6(self, country, language, instance,
                                                                 cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["legalName"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute "
                                               "'buyer.identifier.legalName' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_identifier_uri_as_empty_string_22186_7(self, country, language, instance, cassandra_username,
                                                          cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["uri"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.identifier.uri' "
                                               "is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_street_address_as_empty_string_22186_8(self, country, language, instance,
                                                                  cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["streetAddress"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "streetAddress' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_postal_code_as_empty_string_22186_9(self, country, language, instance,
                                                               cassandra_username,
                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["postalCode"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "postalCode' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_address_details_locality_scheme_as_empty_string_22186_10(self, country, language,
                                                                                    instance, cassandra_username,
                                                                                    cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "addressDetails.locality.scheme' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_address_details_locality_id_as_empty_string_22186_11(self, country, language, instance,
                                                                                cassandra_username,
                                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "addressDetails.locality.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_address_details_locality_description_as_empty_string_22186_12(self, country, language,
                                                                                         instance,
                                                                                         cassandra_username,
                                                                                         cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "addressDetails.locality.description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_additional_identifiers_id_as_empty_string_22186_13(self, country, language, instance,
                                                                      cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer."
                                               "additionalIdentifiers.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_additional_identifiers_scheme_as_empty_string_22186_14(self, country, language, instance,
                                                                          cassandra_username,
                                                                          cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["scheme"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer."
                                               "additionalIdentifiers.scheme' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_additional_identifiers_legal_name_as_empty_string_22186_15(self, country, language, instance,
                                                                              cassandra_username,
                                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["legalName"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.additional"
                                               "Identifiers.legalName' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_additional_identifiers_uri_as_empty_string_22186_16(self, country, language, instance,
                                                                       cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["uri"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute "
                                               "'buyer.additionalIdentifiers.uri' is empty "
                                               "or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_contact_point_name_as_empty_string_22186_17(self, country, language, instance,
                                                               cassandra_username,
                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["name"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "name' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_contact_point_email_as_empty_string_22186_18(self, country, language, instance,
                                                                cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["email"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "email' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_contact_point_telephone_as_empty_string_22186_19(self, country, language, instance,
                                                                    cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["telephone"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "telephone' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_contact_point_fax_number_as_empty_string_22186_20(self, country, language, instance,
                                                                     cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["faxNumber"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "faxNumber' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_contact_point_url_as_empty_string_22186_21(self, country, language, instance, cassandra_username,
                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["faxNumber"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "faxNumber' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_delivery_address_street_address_as_empty_string_22186_22(self, country, language,
                                                                                   instance,
                                                                                   cassandra_username,
                                                                                   cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "deliveryAddress.streetAddress' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_delivery_address_postal_code_as_empty_string_22186_23(self, country, language, instance,
                                                                                cassandra_username,
                                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "deliveryAddress.postalCode' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_delivery_address_address_details_locality_scheme_as_empty_22186_24(self, country,
                                                                                             language,
                                                                                             instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                               "addressDetails.locality.scheme' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_delivery_address_address_details_locality_id_as_empty_string_22186_25(self, country,
                                                                                                language, instance,
                                                                                                cassandra_username,
                                                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                               "addressDetails.locality.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_delivery_address_address_details_locality_description_22186_26(self,
                                                                                         country, language,
                                                                                         instance,
                                                                                         cassandra_username,
                                                                                         cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                               "addressDetails.locality.description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_description_as_empty_string_22186_27(self, country, language, instance,
                                                               cassandra_username,
                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_classification_id_as_empty_string_22186_28(self, country, language, instance,
                                                               cassandra_username,
                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_classification_id_as_empty_string_22186_29(self, country, language, instance,
                                                                     cassandra_username,
                                                                     cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.03", "description": "Invalid cpv code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_additional_classifications_id_as_empty_string_22186_30(self, country, language, instance,
                                                                                 cassandra_username,
                                                                                 cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.05", "description": "Invalid cpvs code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_delivery_address_address_details_country_id_as_empty_string_22186_31(self, country,
                                                                                               language, instance,
                                                                                               cassandra_username,
                                                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.10", "description": "Invalid country. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_delivery_address_address_details_region_id_22186_32(self, country, language,
                                                                              instance, cassandra_username,
                                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.13", "description": "Region not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_tender_items_quantity_as_empty_string_22186_33(self, country, language, instance, cassandra_username,
                                                            cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["quantity"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_ender_items_unit_id_as_empty_string_22186_34(self, country, language, instance, cassandra_username,
                                                          cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.06", "description": "Invalid unit code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_planning_budget_period_start_date_as_empty_string_22186_35(self, country, language, instance,
                                                                        cassandra_username,
                                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.06", "description": "Invalid unit code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_planning_budget_period_end_date_as_empty_string_22186_36(self, country, language, instance,
                                                                      cassandra_username,
                                                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["endDate"] = ""
        value_of_key = payload["planning"]["budget"]["period"]["endDate"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_identifier_scheme_as_empty_string_22186_37(self, country, language, instance, cassandra_username,
                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["scheme"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.12", "description": "Registration scheme not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_address_details_country_id_as_empty_string_22186_38(self, country, language, instance,
                                                                               cassandra_username,
                                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.11", "description": "Country not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_address_address_details_region_id_as_empty_string_22186_39(self, country, language, instance,
                                                                              cassandra_username,
                                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.13", "description": "Region not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_details_type_of_buyer_as_empty_string_22186_40(self, country, language, instance,
                                                                  cassandra_username,
                                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["typeOfBuyer"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_details_main_general_activity_as_empty_string_22186_41(self, country, language, instance,
                                                                          cassandra_username,
                                                                          cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22186")
    def test_buyer_details_main_sectoral_activity_as_empty_string_22186_42(self, country, language, instance,
                                                                           cassandra_username,
                                                                           cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainSectoralActivity"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckThePossibilityToGetXtokenAndCpidAfterEiCreation(object):
    @pytestrail.case("22830")
    def test_send_the_request_22830_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22830")
    def test_see_the_result_in_feed_point_22830_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_create_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheImpossibilityToCreateEiWithBooleanValueAsTheCpvCode(object):
    @pytestrail.case("22833")
    def test_send_the_request_22833_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22833")
    def test_see_the_result_in_feed_point_22833_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheImpossibilityToCreateEiWithEmptyValueInaCpvCode(object):
    @pytestrail.case("22834")
    def test_send_the_request_22834_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22834")
    def test_see_the_result_in_feed_point_22834_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.06", "description": "Cpv code not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckTheImpossibilityToCreateEiWithBooleanTypeAsTheCpv(object):
    @pytestrail.case("22835")
    def test_send_the_request_22835_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22835")
    def test_see_the_result_in_feed_point_22835_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckOnPossibilityToCreateEiWithFullDataModel(object):
    @pytestrail.case("22908")
    def test_send_the_request_22908_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22908")
    def test_see_the_result_in_feed_point_22908_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_create_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("22908")
    def test_check_the_attributes_of_the_expenditure_item_on_public_point_22908_3(self, country, language, instance,
                                                                                  cassandra_username,
                                                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["uri"] = "test fro uri"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
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
        for i in ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["address"
                                                                                    "Details"]["country"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["address"
                                                                                    "Details"]["region"].keys():
            if i == "scheme":
                keys_list.append(i)
            if i == "id":
                keys_list.append(i)
            if i == "description":
                keys_list.append(i)
            if i == "uri":
                keys_list.append(i)
        for i in ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["address"
                                                                                    "Details"]["locality"].keys():
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
        instance_url = None
        if instance == "dev":
            instance_url = "http://dev.public.eprocurement.systems/budgets/"
        if instance == "sandbox":
            instance_url = "http://public.eprocurement.systems/budgets/"
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[0])
        assert compare_actual_result_and_expected_result(expected_result="version", actual_result=keys_list[1])
        assert compare_actual_result_and_expected_result(expected_result="extensions", actual_result=keys_list[2])
        assert compare_actual_result_and_expected_result(expected_result="publisher", actual_result=keys_list[3])
        assert compare_actual_result_and_expected_result(expected_result="license", actual_result=keys_list[4])
        assert compare_actual_result_and_expected_result(expected_result="publicationPolicy",
                                                         actual_result=keys_list[5])
        assert compare_actual_result_and_expected_result(expected_result="publishedDate",
                                                         actual_result=keys_list[6])
        assert compare_actual_result_and_expected_result(expected_result="releases", actual_result=keys_list[7])
        assert compare_actual_result_and_expected_result(expected_result="name", actual_result=keys_list[8])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[9])
        assert compare_actual_result_and_expected_result(expected_result="ocid", actual_result=keys_list[10])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[11])
        assert compare_actual_result_and_expected_result(expected_result="date", actual_result=keys_list[12])
        assert compare_actual_result_and_expected_result(expected_result="tag", actual_result=keys_list[13])
        assert compare_actual_result_and_expected_result(expected_result="language", actual_result=keys_list[14])
        assert compare_actual_result_and_expected_result(expected_result="initiationType",
                                                         actual_result=keys_list[15])
        assert compare_actual_result_and_expected_result(expected_result="tender", actual_result=keys_list[16])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[17])
        assert compare_actual_result_and_expected_result(expected_result="title", actual_result=keys_list[18])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[19])
        assert compare_actual_result_and_expected_result(expected_result="status", actual_result=keys_list[20])
        assert compare_actual_result_and_expected_result(expected_result="statusDetails",
                                                         actual_result=keys_list[21])
        assert compare_actual_result_and_expected_result(expected_result="items", actual_result=keys_list[22])
        assert compare_actual_result_and_expected_result(expected_result="mainProcurementCategory",
                                                         actual_result=keys_list[23])
        assert compare_actual_result_and_expected_result(expected_result="classification",
                                                         actual_result=keys_list[24])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[25])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[26])
        assert compare_actual_result_and_expected_result(expected_result="classification",
                                                         actual_result=keys_list[27])
        assert compare_actual_result_and_expected_result(expected_result="additionalClassifications",
                                                         actual_result=keys_list[28])
        assert compare_actual_result_and_expected_result(expected_result="quantity", actual_result=keys_list[29])
        assert compare_actual_result_and_expected_result(expected_result="unit", actual_result=keys_list[30])
        assert compare_actual_result_and_expected_result(expected_result="deliveryAddress",
                                                         actual_result=keys_list[31])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[32])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[33])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[34])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[35])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[36])
        assert compare_actual_result_and_expected_result(expected_result="description", actual_result=keys_list[37])
        assert compare_actual_result_and_expected_result(expected_result="name", actual_result=keys_list[38])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[39])
        assert compare_actual_result_and_expected_result(expected_result="streetAddress",
                                                         actual_result=keys_list[40])
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
        assert compare_actual_result_and_expected_result(expected_result="contactPoint",
                                                         actual_result=keys_list[67])
        assert compare_actual_result_and_expected_result(expected_result="details", actual_result=keys_list[68])
        assert compare_actual_result_and_expected_result(expected_result="roles", actual_result=keys_list[69])
        assert compare_actual_result_and_expected_result(expected_result="scheme", actual_result=keys_list[70])
        assert compare_actual_result_and_expected_result(expected_result="id", actual_result=keys_list[71])
        assert compare_actual_result_and_expected_result(expected_result="legalName", actual_result=keys_list[72])
        assert compare_actual_result_and_expected_result(expected_result="uri", actual_result=keys_list[73])
        assert compare_actual_result_and_expected_result(expected_result="streetAddress",
                                                         actual_result=keys_list[74])
        assert compare_actual_result_and_expected_result(expected_result="postalCode", actual_result=keys_list[75])
        assert compare_actual_result_and_expected_result(expected_result="addressDetails",
                                                         actual_result=keys_list[76])
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
        assert compare_actual_result_and_expected_result(expected_result="typeOfBuyer",
                                                         actual_result=keys_list[101])
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
            expected_result=f"{instance_url}{cpid}/{cpid}",
            actual_result=ei_release["uri"])
        assert compare_actual_result_and_expected_result(expected_result="1.1", actual_result=ei_release["version"])
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/"
                            "extension.json", actual_result=ei_release["extensions"][0])
        assert compare_actual_result_and_expected_result(
            expected_result="https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/"
                            "extension.js", actual_result=ei_release["extensions"][1])
        assert compare_actual_result_and_expected_result(
            expected_result="M-Tender", actual_result=ei_release["publisher"]["name"])
        assert compare_actual_result_and_expected_result(
            expected_result="https://www.mtender.gov.md", actual_result=ei_release["publisher"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/", actual_result=ei_release["license"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://opendefinition.org/licenses/", actual_result=ei_release["publicationPolicy"])
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"], actual_result=ei_release["publishedDate"])
        assert compare_actual_result_and_expected_result(
            expected_result=cpid, actual_result=ei_release["releases"][0]["ocid"])
        assert compare_actual_result_and_expected_result(
            expected_result=cpid, actual_result=ei_release["releases"][0]["id"][0:28])
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"], actual_result=convert_timestamp_to_date[0])
        assert compare_actual_result_and_expected_result(
            expected_result=message_from_kafka["data"]["operationDate"],
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
                                                         actual_result=ei_release["releases"][0]["tender"][
                                                             "status"])
        assert compare_actual_result_and_expected_result(expected_result="empty",
                                                         actual_result=ei_release["releases"][0]["tender"][
                                                             "statusDetails"])
        assert compare_actual_result_and_expected_result(expected_result=str(True), actual_result=str(is_it_uuid(
            ei_release["releases"][0]["tender"]["items"][0]["id"], 4)))
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["description"],
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
            expected_result=str(payload["tender"]["items"][0]["quantity"]),
            actual_result=str(ei_release["releases"][0]["tender"]["items"][0]["quantity"]))
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
            expected_result="iso-alpha2",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "country"]["scheme"])
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
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
                "scheme"],
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
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["identifier"]["legalName"],
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
            expected_result="http://statistica.md",
            actual_result=ei_release["releases"][0]["parties"][0]["address"][
                "addressDetails"]["region"]["uri"])
        assert compare_actual_result_and_expected_result(
            expected_result="CUATM",
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
                "scheme"])
        assert compare_actual_result_and_expected_result(
            expected_result=payload["buyer"]["address"]["addressDetails"]["locality"]["id"],
            actual_result=ei_release["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"])
        assert compare_actual_result_and_expected_result(
            expected_result="mun.Cahul", actual_result=ei_release["releases"][0]["parties"][0]["address"][
                "addressDetails"]["locality"]["description"])
        assert compare_actual_result_and_expected_result(
            expected_result="http://statistica.md",
            actual_result=ei_release["releases"][0]["parties"][0]["address"][
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


class TestCheckOnTenderItemsInRelease(object):
    @pytestrail.case("24012")
    def test_send_the_request_24012_1(self, country, language, instance, cassandra_username, cassandra_password):
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
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        create_ei_response = ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(create_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24012")
    def test_see_the_result_in_feed_point_24012_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
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
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_create_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24012")
    def test_check_tender_items_object_24012_3(self, country, language, instance, cassandra_username,
                                               cassandra_password):
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
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        cpid = message_from_kafka["data"]["outcomes"]["ei"][0]["id"]
        ei_url = message_from_kafka["data"]["url"] + "/" + cpid
        ei_release = requests.get(url=ei_url).json()
        assert compare_actual_result_and_expected_result(expected_result=str(True), actual_result=str(is_it_uuid(
            ei_release["releases"][0]["tender"]["items"][0]["id"], 4)))
        assert compare_actual_result_and_expected_result(
            expected_result=payload["tender"]["items"][0]["description"],
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
            expected_result=str(payload["tender"]["items"][0]["quantity"]),
            actual_result=str(ei_release["releases"][0]["tender"]["items"][0]["quantity"]))
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
            expected_result="iso-alpha2",
            actual_result=ei_release["releases"][0]["tender"]["items"][0]["deliveryAddress"]["addressDetails"][
                "country"]["scheme"])
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
            expected_result=payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"][
                "scheme"],
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


class TestCheckTheFieldsWithSpaceDigitInFieldsAreNotPublishedInThePublicPoint(object):
    @pytestrail.case("25301")
    def test_tender_title_as_space_digit_in_field_25301_1(self, country, language, instance, cassandra_username,
                                                          cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["title"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.title' is empty "
                                               "or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_description_as_space_digit_in_field_25301_2(self, country, language, instance,
                                                                cassandra_username,
                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["description"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.description' "
                                               "is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_planning_rationale_as_space_digit_in_field_25301_3(self, country, language, instance,
                                                                cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["rationale"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'planning.rationale' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_name_as_space_digit_in_field_25301_4(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["name"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'buyer.name' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_identifier_id_as_space_digit_in_field_25301_5(self, country, language, instance,
                                                                 cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'buyer.identifier.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_identifier_legal_name_as_space_digit_in_field_25301_6(self, country, language, instance,
                                                                         cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["legalName"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.identifier."
                                               "legalName' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_identifier_uri_as_space_digit_in_field_25301_7(self, country, language, instance,
                                                                  cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["uri"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.identifier.uri' "
                                               "is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_address_street_address_as_space_digit_in_field_25301_8(self, country, language, instance,
                                                                          cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["streetAddress"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "streetAddress' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_address_postal_code_as_space_digit_in_field_25301_9(self, country, language, instance,
                                                                       cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["postalCode"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "postalCode' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_address_address_details_locality_scheme_as_space_digit_in_field_25301_10(self, country, language,
                                                                                            instance,
                                                                                            cassandra_username,
                                                                                            cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11", "description": "Incorrect an attribute value.The attribute "
                                                                       "'buyer.address.addressDetails.locality."
                                                                       "scheme' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_address_address_details_locality_id_as_space_digit_in_field_25301_11(self, country, language,
                                                                                        instance,
                                                                                        cassandra_username,
                                                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "addressDetails.locality.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_address_address_details_locality_description_as_space_digit_25301_12(self, country,
                                                                                        language,
                                                                                        instance,
                                                                                        cassandra_username,
                                                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.address."
                                               "addressDetails.locality.description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_additional_identifiers_id_as_space_digit_in_field_25301_13(self, country, language,
                                                                              instance, cassandra_username,
                                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer."
                                               "additionalIdentifiers.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_additional_identifiers_scheme_as_space_digit_in_field_25301_14(self, country, language,
                                                                                  instance, cassandra_username,
                                                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["scheme"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer."
                                               "additionalIdentifiers.scheme' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_additional_identifiers_legal_name_as_space_digit_in_field_25301_15(self, country, language,
                                                                                      instance, cassandra_username,
                                                                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["legalName"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer."
                                               "additionalIdentifiers.legalName' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_additional_identifiers_uri_as_space_digit_in_field_25301_16(self, country, language,
                                                                               instance, cassandra_username,
                                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["uri"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer."
                                               "additionalIdentifiers.uri' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_contact_point_name_as_space_digit_in_field_25301_17(self, country, language,
                                                                       instance, cassandra_username,
                                                                       cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["name"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contact"
                                               "Point.name' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_contact_point_email_as_space_digit_in_field_25301_18(self, country, language,
                                                                        instance, cassandra_username,
                                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["email"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "email' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_contact_point_telephone_as_space_digit_in_field_25301_19(self, country, language,
                                                                            instance, cassandra_username,
                                                                            cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["telephone"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "telephone' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_contact_point_fax_number_as_space_digit_in_field_25301_20(self, country, language,
                                                                             instance, cassandra_username,
                                                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["faxNumber"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "faxNumber' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_contact_point_url_as_space_digit_in_field_25301_21(self, country, language,
                                                                      instance, cassandra_username,
                                                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["url"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'buyer.contactPoint."
                                               "url' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_delivery_address_street_address_as_space_digit_in_field_25301_22(self, country, language,
                                                                                           instance,
                                                                                           cassandra_username,
                                                                                           cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "deliveryAddress.streetAddress' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_delivery_address_postal_code_as_space_digit_in_field_25301_23(self, country, language,
                                                                                        instance,
                                                                                        cassandra_username,
                                                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "deliveryAddress.postalCode' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_delivery_address_address_details_locality_scheme_as_space_25301_24(self, country,
                                                                                             language,
                                                                                             instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                               "addressDetails.locality.scheme' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_delivery_address_address_details_locality_id_25301_25(self, country, language,
                                                                                instance, cassandra_username,
                                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                               "addressDetails.locality.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_delivery_address_address_details_locality_description_25301_26(self, country, language,
                                                                                         instance,
                                                                                         cassandra_username,
                                                                                         cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["description"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                               "addressDetails.locality.description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_description_as_empty_string_as_space_digit_in_field_25301_27(self, country, language,
                                                                                       instance, cassandra_username,
                                                                                       cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["description"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_classification_id_as_empty_string_as_space_digit_in_field_25301_28(self, country, language,
                                                                                       instance, cassandra_username,
                                                                                       cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.06", "description": "Cpv code not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_classification_id_as_space_digit_in_field_25301_29(self, country, language,
                                                                             instance, cassandra_username,
                                                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.03", "description": "Invalid cpv code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_additional_classifications_id_as_space_digit_in_field_25301_30(self, country, language,
                                                                                         instance,
                                                                                         cassandra_username,
                                                                                         cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.05", "description": "Invalid cpvs code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_delivery_address_address_details_country_id_as_space_digit_25301_31(self, country,
                                                                                              language, instance,
                                                                                              cassandra_username,
                                                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.10", "description": "Invalid country. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_delivery_address_address_details_region_id_as_space_digit_25301_32(self, country,
                                                                                             language,
                                                                                             instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.13", "description": "Region not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_quantity_as_space_digit_in_field_25301_33(self, country, language, instance,
                                                                    cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["quantity"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"quantity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_tender_items_unit_id_as_space_digit_in_field25301_34(self, country, language, instance,
                                                                  cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.01.06", "description": "Invalid unit code. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_planning_budget_period_start_date_as_space_digit_in_field_25301_35(self, country, language, instance,
                                                                                cassandra_username,
                                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["startDate"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00", "description": "com.fasterxml.jackson.databind.JsonMapping"
                                                                    "Exception: Text ' ' could not be parsed at "
                                                                    "index 0 (through reference chain: com."
                                                                    "procurement.budget.model.dto.ei.request.Ei"
                                                                    "Create[\"planning\"]->com.procurement.budget."
                                                                    "model.dto.ei.request.EiCreate$PlanningEi"
                                                                    "Create[\"budget\"]->com.procurement.budget."
                                                                    "model.dto.ei.request.EiCreate$PlanningEi"
                                                                    "Create$BudgetEiCreate[\"period\"]->com."
                                                                    "procurement.budget.model.dto.ocds."
                                                                    "Period[\"startDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_planning_budget_period_end_date_as_space_digit_in_field_25301_36(self, country, language, instance,
                                                                              cassandra_username,
                                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["endDate"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00", "description": "com.fasterxml.jackson.databind.JsonMapping"
                                                                    "Exception: Text ' ' could not be parsed at "
                                                                    "index 0 (through reference chain: com."
                                                                    "procurement.budget.model.dto.ei.request."
                                                                    "EiCreate[\"planning\"]->com.procurement."
                                                                    "budget.model.dto.ei.request.EiCreate$Planning"
                                                                    "EiCreate[\"budget\"]->com.procurement.budget."
                                                                    "model.dto.ei.request.EiCreate$Planning"
                                                                    "EiCreate$BudgetEiCreate[\"period\"]->"
                                                                    "com.procurement.budget.model.dto.ocds."
                                                                    "Period[\"endDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_identifier_scheme_as_space_digit_in_field_25301_37(self, country, language, instance,
                                                                      cassandra_username,
                                                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["scheme"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.12", "description": "Registration scheme not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_address_address_details_country_id_as_space_digit_in_field_25301_38(self, country, language,
                                                                                       instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.11", "description": "Country not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_address_address_details_region_id_as_space_digit_in_field_25301_39(self, country, language,
                                                                                      instance,
                                                                                      cassandra_username,
                                                                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00.13", "description": "Region not found. "}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_details_type_of_buyer_as_space_digit_in_field_25301_40(self, country, language,
                                                                          instance, cassandra_username,
                                                                          cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["typeOfBuyer"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.exc.InvalidFormatException: "
                                               "Cannot deserialize value of type `com.procurement.mdm.model."
                                               "dto.data.TypeOfBuyer` from String \"\": value not one of declared "
                                               "Enum instance names: [NATIONAL_AGENCY, REGIONAL_AUTHORITY, "
                                               "REGIONAL_AGENCY, BODY_PUBLIC, EU_INSTITUTION, MINISTRY]\n at "
                                               "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"buyer\"]->com.procurement.mdm.model.dto.data.Organization"
                                               "Reference[\"details\"]->com.procurement.mdm.model.dto.data."
                                               "Details[\"typeOfBuyer\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_details_main_general_activity_as_space_digit_in_field_25301_41(self, country, language,
                                                                                  instance, cassandra_username,
                                                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.exc.InvalidFormatException: "
                                               "Cannot deserialize value of type `com.procurement.mdm.model.dto."
                                               "data.MainGeneralActivity` from String \"\": value not one of "
                                               "declared Enum instance names: [DEFENCE, PUBLIC_ORDER_AND_SAFETY, "
                                               "ECONOMIC_AND_FINANCIAL_AFFAIRS, ENVIRONMENT, "
                                               "RECREATION_CULTURE_AND_RELIGION, EDUCATION, SOCIAL_PROTECTION, "
                                               "HEALTH, GENERAL_PUBLIC_SERVICES, HOUSING_AND_COMMUNITY_"
                                               "AMENITIES]\n at [Source: UNKNOWN; line: -1, column: -1] "
                                               "(through reference chain: com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"details\"]->com.procurement.mdm.model."
                                               "dto.data.Details[\"mainGeneralActivity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25301")
    def test_buyer_details_main_sectoral_activity_as_space_digit_in_field_25301_42(self, country, language,
                                                                                   instance, cassandra_username,
                                                                                   cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = " "
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.exc.InvalidFormatException: "
                                               "Cannot deserialize value of type `com.procurement.mdm.model.dto."
                                               "data.MainGeneralActivity` from String \"\": value not one of "
                                               "declared Enum instance names: [DEFENCE, PUBLIC_ORDER_AND_SAFETY, "
                                               "ECONOMIC_AND_FINANCIAL_AFFAIRS, ENVIRONMENT, "
                                               "RECREATION_CULTURE_AND_RELIGION, EDUCATION, SOCIAL_PROTECTION, "
                                               "HEALTH, GENERAL_PUBLIC_SERVICES, HOUSING_AND_COMMUNITY_"
                                               "AMENITIES]\n at [Source: UNKNOWN; line: -1, column: -1] "
                                               "(through reference chain: com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"details\"]->com.procurement.mdm.model."
                                               "dto.data.Details[\"mainGeneralActivity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckOnTheImpossibilityToCreateEiWithInvalidDataType(object):
    @pytestrail.case("25302")
    def test_tender_title_as_boolean_25302_1(self, country, language, instance, cassandra_username,
                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["title"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: title "
                                               "(through reference chain: com.procurement.budget.model.dto.ei."
                                               "request.EiCreate[\"tender\"]->com.procurement.budget.model.dto."
                                               "ei.request.EiCreate$TenderEiCreate[\"title\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_description_with_space_digit_in_field_25302_2(self, country, language, instance,
                                                                  cassandra_username,
                                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["description"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00", "description": "com.fasterxml.jackson.databind.JsonMapping"
                                                                    "Exception: description (through reference "
                                                                    "chain: com.procurement.budget.model.dto.ei."
                                                                    "request.EiCreate[\"tender\"]->com.procurement."
                                                                    "budget.model.dto.ei.request.EiCreate$TenderEi"
                                                                    "Create[\"description\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_planning_rationale_as_space_digit_in_field_25302_3(self, country, language, instance,
                                                                cassandra_username,
                                                                cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["rationale"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: rationale "
                                               "(through reference chain: com.procurement.budget.model.dto.ei."
                                               "request.EiCreate[\"planning\"]->com.procurement.budget.model."
                                               "dto.ei.request.EiCreate$PlanningEiCreate[\"rationale\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_name_as_space_digit_in_field_25302_4(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["name"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                               "procurement.mdm.exception.InErrorException) (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]"
                                               "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                               "[\"name\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_identifier_id_as_space_digit_in_field_25302_5(self, country, language, instance,
                                                                 cassandra_username,
                                                                 cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"buyer\"]->com.procurement.mdm.model.dto.data.Organization"
                                               "Reference[\"identifier\"]->com.procurement.mdm.model.dto."
                                               "data.Identifier[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_identifier_legal_name_as_true_25302_6(self, country, language, instance, cassandra_username,
                                                         cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["legalName"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei.EI"
                                               "Request[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"identifier\"]->com.procurement.mdm.model."
                                               "dto.data.Identifier[\"legalName\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_identifier_uri_as_true_25302_7(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["uri"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"identifier\"]->com.procurement.mdm.model."
                                               "dto.data.Identifier[\"uri\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_address_street_address_as_true_25302_8(self, country, language, instance, cassandra_username,
                                                          cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["streetAddress"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) "
                                               "(through reference chain: com.procurement.mdm.model.dto."
                                               "data.ei.EIRequest[\"buyer\"]->com.procurement.mdm.model."
                                               "dto.data.OrganizationReference[\"address\"]->com.procurement."
                                               "mdm.model.dto.data.Address[\"streetAddress\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_address_postal_code_as_true_25302_9(self, country, language, instance, cassandra_username,
                                                       cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["postalCode"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                               "procurement.mdm.exception.InErrorException) (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]"
                                               "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                               "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                               "[\"postalCode\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_address_address_details_locality_scheme_as_true_25302_10(self, country, language, instance,
                                                                            cassandra_username,
                                                                            cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00", "description": "com.fasterxml.jackson.databind.JsonMapping"
                                                                    "Exception: (was com.procurement.mdm.exception."
                                                                    "InErrorException) (through reference chain: "
                                                                    "com.procurement.mdm.model.dto.data.ei."
                                                                    "EIRequest[\"buyer\"]->com.procurement.mdm."
                                                                    "model.dto.data.OrganizationReference"
                                                                    "[\"address\"]->com.procurement.mdm.model.dto."
                                                                    "data.Address[\"addressDetails\"]->com."
                                                                    "procurement.mdm.model.dto.data.AddressDetails"
                                                                    "[\"locality\"]->com.procurement.mdm.model.dto."
                                                                    "data.LocalityDetails[\"scheme\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_address_address_details_locality_id_as_true_25302_11(self, country, language, instance,
                                                                        cassandra_username,
                                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                               "procurement.mdm.exception.InErrorException) (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]"
                                               "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                               "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                               "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                               "AddressDetails[\"locality\"]->com.procurement.mdm.model.dto."
                                               "data.LocalityDetails[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_address_address_details_locality_description_as_true_25302_12(self, country, language, instance,
                                                                                 cassandra_username,
                                                                                 cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"address\"]->com.procurement.mdm.model."
                                               "dto.data.Address[\"addressDetails\"]->com.procurement.mdm.model."
                                               "dto.data.AddressDetails[\"locality\"]->com.procurement.mdm.model."
                                               "dto.data.LocalityDetails[\"description\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_additional_identifiers_id_as_true_25302_13(self, country, language, instance, cassandra_username,
                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00", "description": "com.fasterxml.jackson.databind.JsonMapping"
                                                                    "Exception: (was com.procurement.mdm.exception."
                                                                    "InErrorException) (through reference chain: "
                                                                    "com.procurement.mdm.model.dto.data.ei.EI"
                                                                    "Request[\"buyer\"]->com.procurement.mdm."
                                                                    "model.dto.data.OrganizationReference"
                                                                    "[\"additionalIdentifiers\"]->java.util."
                                                                    "ArrayList[0]->com.procurement.mdm.model.dto."
                                                                    "data.Identifier[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_additional_identifiers_scheme_as_true_25302_14(self, country, language, instance,
                                                                  cassandra_username,
                                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["scheme"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                               "procurement.mdm.exception.InErrorException) (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]"
                                               "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                               "[\"additionalIdentifiers\"]->java.util.ArrayList[0]->com."
                                               "procurement.mdm.model.dto.data.Identifier[\"scheme\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_additional_identifiers_legal_name_as_true_25302_15(self, country, language, instance,
                                                                      cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["legalName"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"additionalIdentifiers\"]->java.util."
                                               "ArrayList[0]->com.procurement.mdm.model.dto.data."
                                               "Identifier[\"legalName\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_additional_identifiers_uri_as_space_digit_in_field_25302_16(self, country, language, instance,
                                                                               cassandra_username,
                                                                               cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["additionalIdentifiers"][0]["uri"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"additionalIdentifiers\"]->java.util."
                                               "ArrayList[0]->com.procurement.mdm.model.dto.data.Identifier"
                                               "[\"uri\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_contact_point_name_as_true_25302_17(self, country, language, instance, cassandra_username,
                                                       cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["name"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"buyer\"]->com.procurement.mdm.model.dto.data.Organization"
                                               "Reference[\"contactPoint\"]->com.procurement.mdm.model.dto."
                                               "data.ContactPoint[\"name\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_contact_point_email_as_true_25302_18(self, country, language, instance, cassandra_username,
                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["email"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) "
                                               "(through reference chain: com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"contactPoint\"]->com.procurement.mdm."
                                               "model.dto.data.ContactPoint[\"email\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_contact_point_telephone_as_true_25302_19(self, country, language, instance, cassandra_username,
                                                            cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["telephone"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"contactPoint\"]->com.procurement."
                                               "mdm.model.dto.data.ContactPoint[\"telephone\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_contact_point_fax_number_as_true_25302_20(self, country, language, instance, cassandra_username,
                                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["faxNumber"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00", "description": "com.fasterxml.jackson.databind.JsonMapping"
                                                                    "Exception: (was com.procurement.mdm."
                                                                    "exception.InErrorException) (through "
                                                                    "reference chain: com.procurement.mdm.model."
                                                                    "dto.data.ei.EIRequest[\"buyer\"]->com."
                                                                    "procurement.mdm.model.dto.data.Organization"
                                                                    "Reference[\"contactPoint\"]->com.procurement."
                                                                    "mdm.model.dto.data.ContactPoint"
                                                                    "[\"faxNumber\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_contact_point_url_as_true_25302_21(self, country, language, instance, cassandra_username,
                                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["contactPoint"]["url"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"contactPoint\"]->com.procurement.mdm."
                                               "model.dto.data.ContactPoint[\"url\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_delivery_address_street_address_as_true_25302_22(self, country, language, instance,
                                                                           cassandra_username,
                                                                           cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) "
                                               "(through reference chain: com.procurement.mdm.model.dto."
                                               "data.ei.EIRequest[\"tender\"]->com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest$Tender[\"items\"]->java.util.ArrayList"
                                               "[0]->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$"
                                               "Item[\"deliveryAddress\"]->com.procurement.mdm.model.dto."
                                               "data.ei.EIRequest$Tender$Item$DeliveryAddress"
                                               "[\"streetAddress\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_delivery_address_postal_code_as_true_25302_23(self, country, language, instance,
                                                                        cassandra_username,
                                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["postalCode"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) "
                                               "(through reference chain: com.procurement.mdm.model.dto."
                                               "data.ei.EIRequest[\"tender\"]->com.procurement.mdm.model.dto."
                                               "data.ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Item$DeliveryAddress[\"postalCode\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_delivery_address_address_details_locality_scheme_as_true_25302_24(self, country, language,
                                                                                            instance,
                                                                                            cassandra_username,
                                                                                            cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$Delivery"
                                               "Address$AddressDetails[\"locality\"]->com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$Address"
                                               "Details$Locality[\"scheme\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_delivery_address_address_details_locality_id_as_true_25302_25(self, country, language,
                                                                                        instance,
                                                                                        cassandra_username,
                                                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest$Tender$Item[\"deliveryAddress\"]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                               "DeliveryAddress[\"addressDetails\"]->com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$AddressDetails"
                                               "[\"locality\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender$Item$DeliveryAddress$AddressDetails$Locality[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_delivery_address_address_details_locality_id_as_true_25302_26(self, country, language,
                                                                                        instance,
                                                                                        cassandra_username,
                                                                                        cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["description"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                               "DeliveryAddress$AddressDetails[\"locality\"]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                               "AddressDetails$Locality[\"description\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_description_as_true_25302_27(self, country, language,
                                                       instance,
                                                       cassandra_username,
                                                       cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["description"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"description\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_classification_id_as_true_25302_28(self, country, language, instance, cassandra_username,
                                                       cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["classification"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) "
                                               "(through reference chain: com.procurement.mdm.model.dto."
                                               "data.ei.EIRequest[\"tender\"]->com.procurement.mdm.model.dto."
                                               "data.ei.EIRequest$Tender[\"classification\"]->com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest$Tender$Classification[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_classification_id_as_true_25302_29(self, country, language,
                                                             instance, cassandra_username,
                                                             cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["classification"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                               "procurement.mdm.exception.InErrorException) (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]"
                                               "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]"
                                               "->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest$Tender$Item[\"classification\"]->com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest$Tender$Item$Classification[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_additional_classifications_id_as_true_25302_30(self, country, language,
                                                                         instance, cassandra_username,
                                                                         cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data."
                                               "ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                               "[\"additionalClassifications\"]->java.util.ArrayList[0]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                               "AdditionalClassification[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_delivery_address_address_details_country_id_as_true_25302_31(self, country, language,
                                                                                       instance,
                                                                                       cassandra_username,
                                                                                       cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                               "[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest$Tender$Item[\"deliveryAddress\"]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                               "DeliveryAddress[\"addressDetails\"]->com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$AddressDetails"
                                               "[\"country\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender$Item$DeliveryAddress$AddressDetails$Country[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_delivery_address_address_details_region_id_as_true_25301_32(self, country, language,
                                                                                      instance,
                                                                                      cassandra_username,
                                                                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                               "procurement.mdm.exception.InErrorException) (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]"
                                               "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender"
                                               "[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm."
                                               "model.dto.data.ei.EIRequest$Tender$Item[\"deliveryAddress\"]->"
                                               "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                               "DeliveryAddress[\"addressDetails\"]->com.procurement.mdm.model."
                                               "dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$AddressDetails"
                                               "[\"region\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                               "Tender$Item$DeliveryAddress$AddressDetails$Region[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_quantity_as_true_25302_33(self, country, language, instance, cassandra_username,
                                                    cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["quantity"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00", "description": "com.fasterxml.jackson.databind.exc."
                                                                    "MismatchedInputException: Cannot deserialize "
                                                                    "instance of `java.math.BigDecimal` out of "
                                                                    "VALUE_TRUE token\n at [Source: UNKNOWN; line: "
                                                                    "-1, column: -1] (through reference chain: com."
                                                                    "procurement.mdm.model.dto.data.ei.EIRequest"
                                                                    "[\"tender\"]->com.procurement.mdm.model.dto."
                                                                    "data.ei.EIRequest$Tender[\"items\"]->"
                                                                    "java.util.ArrayList[0]->com.procurement."
                                                                    "mdm.model.dto.data.ei.EIRequest$"
                                                                    "Tender$Item[\"quantity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_tender_items_unit_id_as_true_25302_34(self, country, language, instance, cassandra_username,
                                                   cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["unit"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00", "description": "com.fasterxml.jackson.databind.JsonMapping"
                                                                    "Exception: (was com.procurement.mdm."
                                                                    "exception.InErrorException) (through "
                                                                    "reference chain: com.procurement.mdm."
                                                                    "model.dto.data.ei.EIRequest[\"tender\"]"
                                                                    "->com.procurement.mdm.model.dto."
                                                                    "data.ei.EIRequest$Tender[\"items\"]->"
                                                                    "java.util.ArrayList[0]->com.procurement."
                                                                    "mdm.model.dto.data.ei.EIRequest$Tender$"
                                                                    "Item[\"unit\"]->com.procurement.mdm.model."
                                                                    "dto.data.ei.EIRequest$"
                                                                    "Tender$Item$Unit[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_planning_budget_period_start_date_as_true_25302_35(self, country, language,
                                                                instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["startDate"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: Text "
                                               "'true' could not be parsed at index 0 (through reference chain: "
                                               "com.procurement.budget.model.dto.ei.request.EiCreate"
                                               "[\"planning\"]->com.procurement.budget.model.dto.ei.request."
                                               "EiCreate$PlanningEiCreate[\"budget\"]->com.procurement.budget."
                                               "model.dto.ei.request.EiCreate$PlanningEiCreate$BudgetEiCreate"
                                               "[\"period\"]->com.procurement.budget.model.dto.ocds.Period"
                                               "[\"startDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_planning_budget_period_end_date_as_true_25302_36(self, country, language, instance, cassandra_username,
                                                              cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["budget"]["period"]["endDate"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.00", "description": "com.fasterxml.jackson.databind.JsonMapping"
                                                                    "Exception: Text 'true' could not be parsed at "
                                                                    "index 0 (through reference chain: com."
                                                                    "procurement.budget.model.dto.ei.request.Ei"
                                                                    "Create[\"planning\"]->com.procurement."
                                                                    "budget.model.dto.ei.request.EiCreate$"
                                                                    "PlanningEiCreate[\"budget\"]->com."
                                                                    "procurement.budget.model.dto."
                                                                    "ei.request.EiCreate$PlanningEiCreate$BudgetEi"
                                                                    "Create[\"period\"]->com.procurement.budget."
                                                                    "model.dto.ocds.Period[\"endDate\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_identifier_scheme_as_true_25302_37(self, country, language, instance, cassandra_username,
                                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["identifier"]["scheme"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: "
                                               "(was com.procurement.mdm.exception.InErrorException) (through "
                                               "reference chain: com.procurement.mdm.model.dto.data.ei."
                                               "EIRequest[\"buyer\"]->com.procurement.mdm.model.dto.data."
                                               "OrganizationReference[\"identifier\"]->com.procurement.mdm."
                                               "model.dto.data.Identifier[\"scheme\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_address_address_details_country_id_as_true_25302_38(self, country, language, instance,
                                                                       cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["country"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was "
                                               "com.procurement.mdm.exception.InErrorException) (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->"
                                               "com.procurement.mdm.model.dto.data.OrganizationReference"
                                               "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                               "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                               "AddressDetails[\"country\"]->com.procurement.mdm.model.dto.data."
                                               "CountryDetails[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_address_address_details_region_id_as_true_25302_39(self, country, language, instance,
                                                                      cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["address"]["addressDetails"]["region"]["id"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.JsonMappingException: (was com."
                                               "procurement.mdm.exception.InErrorException) (through reference "
                                               "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]"
                                               "->com.procurement.mdm.model.dto.data.OrganizationReference"
                                               "[\"address\"]->com.procurement.mdm.model.dto.data.Address"
                                               "[\"addressDetails\"]->com.procurement.mdm.model.dto.data."
                                               "AddressDetails[\"region\"]->com.procurement.mdm.model.dto.data."
                                               "RegionDetails[\"id\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_details_type_of_buyer_as_true_25302_40(self, country, language, instance, cassandra_username,
                                                          cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["typeOfBuyer"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.exc.MismatchedInputException: "
                                               "Cannot deserialize instance of `com.procurement.mdm.model.dto."
                                               "data.TypeOfBuyer` out of VALUE_TRUE token\n at [Source: UNKNOWN; "
                                               "line: -1, column: -1] (through reference chain: com.procurement."
                                               "mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com.procurement.mdm."
                                               "model.dto.data.OrganizationReference[\"details\"]->com."
                                               "procurement.mdm.model.dto.data.Details[\"typeOfBuyer\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_details_main_general_activity_as_true_25302_41(self, country, language, instance,
                                                                  cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.exc.MismatchedInputException: "
                                               "Cannot deserialize instance of `com.procurement.mdm.model.dto."
                                               "data.MainGeneralActivity` out of VALUE_TRUE token\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com."
                                               "procurement.mdm.model.dto.data.OrganizationReference[\"details\"]"
                                               "->com.procurement.mdm.model.dto.data.Details[\"mainGeneral"
                                               "Activity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25302")
    def test_buyer_details_main_sectoral_activity_as_true_25302_42(self, country, language, instance,
                                                                   cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["buyer"]["details"]["mainGeneralActivity"] = True
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.20.00",
                                "description": "com.fasterxml.jackson.databind.exc.MismatchedInputException: "
                                               "Cannot deserialize instance of `com.procurement.mdm.model.dto."
                                               "data.MainGeneralActivity` out of VALUE_TRUE token\n at [Source: "
                                               "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                               "procurement.mdm.model.dto.data.ei.EIRequest[\"buyer\"]->com."
                                               "procurement.mdm.model.dto.data.OrganizationReference[\"details\"]"
                                               "->com.procurement.mdm.model.dto.data.Details[\"mainGeneral"
                                               "Activity\"])"}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)
