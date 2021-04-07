import copy
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
        actual_result = str(message_from_kafka['errors'])
        expected_result = str([{'code': '400.00.00.00', 'description': 'Data processing exception.'}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("22132")
    def test_delete_tender_title_field_from_the_payload_22132_2(self, country, language):
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["title"]
        ei = EI(payload=payload, lang=language, country=country)
        ei.create_ei()
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka['errors'])
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
        actual_result = str(message_from_kafka['errors'])
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