import copy
import time
from uuid import uuid4

from pytest_testrail.plugin import pytestrail

from tests.Cassandra_session import Cassandra
from tests.essences.ei import EI
from tests.payloads.ei_payload import payload_ei_obligatory_data_model, payload_ei_full_data_model
from useful_functions import compare_actual_result_and_expected_result


class TestCheckOnPossibilityUpdateEiWithObligatoryFieldsInPayloadWithoutTenderItems(object):
    @pytestrail.case("23890")
    def test_send_the_request_23890_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        del payload["tender"]["items"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model()
        update_ei_response = ei.update_ei()
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23890")
    def test_see_the_result_in_feed_point_23890_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        del payload["tender"]["items"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model()
        ei.update_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_update_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckOnPossibilityUpdateEiWithObligatoryFieldsInPayloadWithTenderItems(object):
    @pytestrail.case("24441")
    def test_send_the_request_24441_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model()
        update_ei_response = ei.update_ei()
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24441")
    def test_see_the_result_in_feed_point_24441_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model()
        ei.update_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_update_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckOnPossibilityUpdateEiWithFullDataInPayload(object):
    @pytestrail.case("24442")
    def test_send_the_request_24442_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_obligatory_data_model()
        update_ei_response = ei.update_ei()
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24442")
    def test_see_the_result_in_feed_point_24442_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_obligatory_data_model()
        ei.update_ei()
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_update_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckOnImpossibilityUpdateEiIfTokenFromRequestNotEqualTokenFromDB(object):
    @pytestrail.case("24443")
    def test_send_the_request_24443_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password,
                ei_token_update_ei=str(uuid4()))
        ei.insert_ei_full_data_model()
        update_ei_response = ei.update_ei()
        expected_result = str(202)
        actual_result = str(update_ei_response.status_code)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24443")
    def test_see_the_result_in_feed_point_24443_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password,
                ei_token_update_ei=str(uuid4()))
        ei.insert_ei_full_data_model()
        ei.update_ei()
        time.sleep(1.8)
        message_from_kafka = ei.get_message_from_kafka()
        expected_result = str([{"code": "400.10.00.04", "description": "Invalid token."}])
        actual_result = str(message_from_kafka["errors"])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckOnImpossibilityUpdateEiIfOwnerFromRequestNotEqualOwnerFromDB(object):
    @pytestrail.case("24444")
    def test_send_the_request_24444_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password, platform="platform_two")
        ei.insert_ei_full_data_model()
        update_ei_response = ei.update_ei()
        expected_result = str(202)
        actual_result = str(update_ei_response.status_code)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24444")
    def test_see_the_result_in_feed_point_24444_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password, platform="platform_two")
        insert_ei = ei.insert_ei_full_data_model()
        ei.update_ei()
        data_base = Cassandra(cp_id=insert_ei[2], task_id='BudgetUpdateEiTask',
                              instance=instance, cassandra_username=cassandra_username,
                              cassandra_password=cassandra_password)
        time.sleep(2.3)
        error_from_DB = data_base.execute_cql_from_orchestrator_operation_step()
        expected_result = str([{"code": "400.10.00.03", "description": "Invalid owner."}])
        actual_result = str(error_from_DB["errors"])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckOnImpossibilityUpdateEiIfTenderClassificationIdNotEqualTenderItemsClassificationId(object):
    @pytestrail.case("24445")
    def test_send_the_request_24445_1(self, country, language, instance, cassandra_username, cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload['tender']['classification']['id'] = "90900000-6"
        payload['tender']['items'] = [{
            "id": "1",
            "description": "item 1",
            "classification": {
                "id": "19700000-3"
            },
            "additionalClassifications": [
                {
                    "id": "AA12-4"
                }
            ],
            "deliveryAddress": {
                "streetAddress": "хрещатик",
                "postalCode": "02235",
                "addressDetails": {
                    "country": {
                        "id": "MD",
                        "description": "ОПИСАНИЕ",
                        "scheme": "other"
                    },
                    "region": {
                        "id": "1700000",
                        "description": "ОПИСАНИЕ",
                        "scheme": "CUATM"
                    },
                    "locality": {
                        "id": "1701000",
                        "description": "ОПИСАНИЕ2",
                        "scheme": "other"
                    }

                }
            },
            "quantity": 1,
            "unit": {
                "id": "10",
                "name": "name"
            }
        },
            {
                "id": "2",
                "description": "item 2",
                "classification": {
                    "id": "45100000-8"
                },
                "additionalClassifications": [
                    {
                        "id": "AA05-3"
                    }
                ],
                "deliveryAddress": {
                    "streetAddress": "хрещатик",
                    "postalCode": "02235",
                    "addressDetails": {
                        "country": {
                            "id": "MD",
                            "description": "ОПИСАНИЕ",
                            "scheme": "other"
                        },
                        "region": {
                            "id": "1700000",
                            "description": "ОПИСАНИЕ",
                            "scheme": "CUATM"
                        },
                        "locality": {
                            "id": "1701000",
                            "description": "ОПИСАНИЕ2",
                            "scheme": "other"
                        }

                    }
                },
                "quantity": 1,
                "unit": {
                    "id": "10",
                    "name": "name"
                }
            }
        ]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                tender_classification_id="45100000-8", tender_item_classification_id="45100000-8",
                planning_budget_id="45100000-8", cassandra_username=cassandra_username,
                cassandra_password=cassandra_password)
        ei.insert_ei_obligatory_data_model()
        update_ei_response = ei.update_ei()
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24445")
    def test_see_the_result_in_feed_point_24445_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload['tender']['classification']['id'] = "90900000-6"
        payload['tender']['items'] = [{
            "id": "1",
            "description": "item 1",
            "classification": {
                "id": "19700000-3"
            },
            "additionalClassifications": [
                {
                    "id": "AA12-4"
                }
            ],
            "deliveryAddress": {
                "streetAddress": "хрещатик",
                "postalCode": "02235",
                "addressDetails": {
                    "country": {
                        "id": "MD",
                        "description": "ОПИСАНИЕ",
                        "scheme": "other"
                    },
                    "region": {
                        "id": "1700000",
                        "description": "ОПИСАНИЕ",
                        "scheme": "CUATM"
                    },
                    "locality": {
                        "id": "1701000",
                        "description": "ОПИСАНИЕ2",
                        "scheme": "other"
                    }

                }
            },
            "quantity": 1,
            "unit": {
                "id": "10",
                "name": "name"
            }
        },
            {
                "id": "2",
                "description": "item 2",
                "classification": {
                    "id": "45100000-8"
                },
                "additionalClassifications": [
                    {
                        "id": "AA05-3"
                    }
                ],
                "deliveryAddress": {
                    "streetAddress": "хрещатик",
                    "postalCode": "02235",
                    "addressDetails": {
                        "country": {
                            "id": "MD",
                            "description": "ОПИСАНИЕ",
                            "scheme": "other"
                        },
                        "region": {
                            "id": "1700000",
                            "description": "ОПИСАНИЕ",
                            "scheme": "CUATM"
                        },
                        "locality": {
                            "id": "1701000",
                            "description": "ОПИСАНИЕ2",
                            "scheme": "other"
                        }
                    }
                },
                "quantity": 1,
                "unit": {
                    "id": "10",
                    "name": "name"
                }
            }
        ]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                tender_classification_id="45100000-8", tender_item_classification_id="45100000-8",
                planning_budget_id="45100000-8", cassandra_username=cassandra_username,
                cassandra_password=cassandra_password)
        ei.insert_ei_obligatory_data_model()
        ei.update_ei()
        time.sleep(1.8)
        message_from_kafka = ei.get_message_from_kafka()
        expected_result = str(
            [{"code": "400.10.00.05",
              "description": "Invalid CPV.Invalid CPV code in classification(s) '19700000-3'"}])
        actual_result = str(message_from_kafka["errors"])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    class TestCheckOnImpossibilityUpdateEiWithoutObligatoryFieldsInPayload(object):
        @pytestrail.case("24456")
        def test_delete_tender_object_from_the_payload_24456_1(self, country, language, instance, cassandra_username,
                                                               cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{'code': '400.00.00.00', 'description': 'Data processing exception.'}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_title_field_from_the_payload_24456_2(self, country, language, instance,
                                                                    cassandra_username,
                                                                    cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["title"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.10.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "budget.model.dto.ei.request.EiUpdate$TenderEiUpdate] value failed "
                                                   "for JSON property title due to missing (therefore NULL) value for "
                                                   "creator parameter title which is a non-nullable type\n at "
                                                   "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                   "chain: com.procurement.budget.model.dto.ei.request.EiUpdate"
                                                   "[\"tender\"]->com.procurement.budget.model.dto.ei.request."
                                                   "EiUpdate$TenderEiUpdate[\"title\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_id_field_from_the_payload_24456_3(self, country, language, instance,
                                                                       cassandra_username, cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["id"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                                   "JSON property id due to missing (therefore NULL) value for creator "
                                                   "parameter id which is a non-nullable type\n at [Source: UNKNOWN; "
                                                   "line: -1, column: -1] (through reference chain: com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest[\"tender\"]->com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util."
                                                   "ArrayList[0]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender$Item[\"id\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_description_field_from_the_payload_24456_4(self, country, language, instance,
                                                                                cassandra_username, cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["description"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                                   "JSON property description due to missing (therefore NULL) value "
                                                   "for creator parameter description which is a non-nullable type\n "
                                                   "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                   "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]"
                                                   "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]"
                                                   "->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data."
                                                   "ei.EIRequest$Tender$Item[\"description\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_classification_field_from_the_payload_24456_5(self, country, language, instance,
                                                                                   cassandra_username,
                                                                                   cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["classification"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                                   "JSON property classification due to missing (therefore NULL) "
                                                   "value for creator parameter classification which is a non-nullable "
                                                   "type\n at [Source: UNKNOWN; line: -1, column: -1] (through "
                                                   "reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                                   "[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                                   "Tender[\"items\"]->java.util.ArrayList[0]->com.procurement.mdm."
                                                   "model.dto.data.ei.EIRequest$Tender$Item[\"classification\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_classification_id_field_from_the_payload_24456_6(self, country, language, instance,
                                                                                      cassandra_username,
                                                                                      cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["classification"]["id"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$Classification] value "
                                                   "failed for JSON property id due to missing (therefore NULL) value "
                                                   "for creator parameter id which is a non-nullable type\n at "
                                                   "[Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                   "chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                                   "[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest"
                                                   "$Tender[\"items\"]->java.util.ArrayList[0]->com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item[\"classification\"]"
                                                   "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                                   "$Classification[\"id\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_additional_classifications_id_field_from_the_payload_24456_7(self, country,
                                                                                                  language, instance,
                                                                                                  cassandra_username,
                                                                                                  cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$Additional"
                                                   "Classification] value failed for JSON property id due to "
                                                   "missing (therefore NULL) value for creator parameter id which is "
                                                   "a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                                   "(through reference chain: com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                                   "[\"additionalClassifications\"]->java.util.ArrayList[0]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$Additional"
                                                   "Classification[\"id\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_delivery_address_field_from_the_payload_24456_8(self, country, language, instance,
                                                                                     cassandra_username,
                                                                                     cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["deliveryAddress"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                                   "JSON property deliveryAddress due to missing (therefore NULL) "
                                                   "value for creator parameter deliveryAddress which is a non-"
                                                   "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                                   "(through reference chain: com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                                   "[\"deliveryAddress\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_delivery_address_address_details_field_24456_9(self, country, language, instance,
                                                                                    cassandra_username,
                                                                                    cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress] value "
                                                   "failed for JSON property addressDetails due to missing (therefore "
                                                   "NULL) value for creator parameter addressDetails which is a non-"
                                                   "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                                   "(through reference chain: com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                                   "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_delivery_address_address_details_country_field_24456_10(self, country, language,
                                                                                             instance,
                                                                                             cassandra_username,
                                                                                             cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                                   "AddressDetails] value failed for JSON property country due to "
                                                   "missing (therefore NULL) value for creator parameter country "
                                                   "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                   "column: -1] (through reference chain: com.procurement.mdm.model."
                                                   "dto.data.ei.EIRequest[\"tender\"]->com.procurement.mdm.model."
                                                   "dto.data.ei.EIRequest$Tender[\"items\"]->java.util.ArrayList[0]"
                                                   "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                                   "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->"
                                                   "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                                   "$DeliveryAddress$AddressDetails[\"country\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_delivery_address_address_details_country_id_field_24456_11(self, country, language,
                                                                                                instance,
                                                                                                cassandra_username,
                                                                                                cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                                   "AddressDetails$Country] value failed for JSON property id due "
                                                   "to missing (therefore NULL) value for creator parameter id which "
                                                   "is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: "
                                                   "-1] (through reference chain: com.procurement.mdm.model.dto.data."
                                                   "ei.EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                                   "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data."
                                                   "ei.EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]"
                                                   "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$"
                                                   "Item$DeliveryAddress$AddressDetails[\"country\"]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                                   "DeliveryAddress$AddressDetails$Country[\"id\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_delivery_address_address_details_region_field_24456_12(self, country, language,
                                                                                            instance,
                                                                                            cassandra_username,
                                                                                            cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                                   "AddressDetails] value failed for JSON property region due to "
                                                   "missing (therefore NULL) value for creator parameter region "
                                                   "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, "
                                                   "column: -1] (through reference chain: com.procurement.mdm."
                                                   "model.dto.data.ei.EIRequest[\"tender\"]->com.procurement.mdm."
                                                   "model.dto.data.ei.EIRequest$Tender[\"items\"]->java.util."
                                                   "ArrayList[0]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender$Item[\"deliveryAddress\"]->com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress"
                                                   "[\"addressDetails\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender$Item$DeliveryAddress$AddressDetails"
                                                   "[\"region\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_delivery_address_address_details_region_id_field_24456_13(self, country, language,
                                                                                               instance,
                                                                                               cassandra_username,
                                                                                               cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                                   "AddressDetails$Region] value failed for JSON property id due "
                                                   "to missing (therefore NULL) value for creator parameter id which "
                                                   "is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: "
                                                   "-1] (through reference chain: com.procurement.mdm.model.dto.data."
                                                   "ei.EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                                   "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->"
                                                   "com.procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$"
                                                   "DeliveryAddress$AddressDetails[\"region\"]->com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$"
                                                   "AddressDetails$Region[\"id\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_delivery_address_address_details_locality_id_field_24456_14(self, country,
                                                                                                 language, instance,
                                                                                                 cassandra_username,
                                                                                                 cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$Address"
                                                   "Details$Locality] value failed for JSON property id due to missing "
                                                   "(therefore NULL) value for creator parameter id which is a non-"
                                                   "nullable type\n at [Source: UNKNOWN; line: -1, column: -1] "
                                                   "(through reference chain: com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                                   "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$Delivery"
                                                   "Address$AddressDetails[\"locality\"]->com.procurement.mdm.model."
                                                   "dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$Address"
                                                   "Details$Locality[\"id\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_delivery_address_address_details_locality_id_field_24456_15(self, country,
                                                                                                 language, instance,
                                                                                                 cassandra_username,
                                                                                                 cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$Address"
                                                   "Details$Locality] value failed for JSON property scheme due to "
                                                   "missing (therefore NULL) value for creator parameter scheme which "
                                                   "is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: "
                                                   "-1] (through reference chain: com.procurement.mdm.model.dto.data."
                                                   "ei.EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender[\"items\"]->java.util.ArrayList[0]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item"
                                                   "[\"deliveryAddress\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender$Item$DeliveryAddress[\"addressDetails\"]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender$Item$Delivery"
                                                   "Address$AddressDetails[\"locality\"]->com.procurement.mdm.model."
                                                   "dto.data.ei.EIRequest$Tender$Item$DeliveryAddress$Address"
                                                   "Details$Locality[\"scheme\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_quantity_field_from_the_payload_24456_16(self, country, language,
                                                                              instance, cassandra_username,
                                                                              cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["quantity"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                                   "JSON property quantity due to missing (therefore NULL) value "
                                                   "for creator parameter quantity which is a non-nullable type\n "
                                                   "at [Source: UNKNOWN; line: -1, column: -1] (through reference "
                                                   "chain: com.procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]"
                                                   "->com.procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]"
                                                   "->java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender$Item[\"quantity\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_unit_field_from_the_payload_24456_17(self, country, language,
                                                                          instance, cassandra_username,
                                                                          cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["unit"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Item] value failed for "
                                                   "JSON property unit due to missing (therefore NULL) value for "
                                                   "creator parameter unit which is a non-nullable type\n at [Source: "
                                                   "UNKNOWN; line: -1, column: -1] (through reference chain: com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest[\"tender\"]->com."
                                                   "procurement.mdm.model.dto.data.ei.EIRequest$Tender[\"items\"]->"
                                                   "java.util.ArrayList[0]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender$Item[\"unit\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_items_unit_id_field_from_the_payload_24456_18(self, country, language,
                                                                             instance, cassandra_username,
                                                                             cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["items"][0]["unit"]["id"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
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
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_classification_field_from_the_payload_24456_19(self, country, language,
                                                                              instance, cassandra_username,
                                                                              cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["classification"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender] value failed for JSON "
                                                   "property classification due to missing (therefore NULL) value "
                                                   "for creator parameter classification which is a non-nullable "
                                                   "type\n at [Source: UNKNOWN; line: -1, column: -1] (through "
                                                   "reference chain: com.procurement.mdm.model.dto.data.ei.EIRequest"
                                                   "[\"tender\"]->com.procurement.mdm.model.dto.data.ei.EIRequest$"
                                                   "Tender[\"classification\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("24456")
        def test_delete_tender_classification_id_field_from_the_payload_24456_20(self, country, language,
                                                                                 instance, cassandra_username,
                                                                                 cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            del payload["tender"]["classification"]["id"]
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00",
                                    "description": "com.fasterxml.jackson.module.kotlin.MissingKotlinParameter"
                                                   "Exception: Instantiation of [simple type, class com.procurement."
                                                   "mdm.model.dto.data.ei.EIRequest$Tender$Classification] value "
                                                   "failed for JSON property id due to missing (therefore NULL) "
                                                   "value for creator parameter id which is a non-nullable "
                                                   "type\n at [Source: UNKNOWN; line: -1, column: -1] (through "
                                                   "reference chain: com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest[\"tender\"]->com.procurement.mdm.model.dto.data.ei."
                                                   "EIRequest$Tender[\"classification\"]->com.procurement.mdm."
                                                   "model.dto.data.ei.EIRequest$Tender$Classification[\"id\"])"}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

    class TestCheckTheFieldsWithEmptyStringsAreNotPublishedInThePublicPoint(object):
        @pytestrail.case("25300")
        def test_delete_tender_title_field_from_the_payload_25300_1(self, country, language,
                                                                    instance, cassandra_username,
                                                                    cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            payload["tender"]["title"] = ""
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.10.20.11",
                                    "description": "Incorrect an attribute value.The attribute 'tender.title' is "
                                                   "empty or blank."}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("25300")
        def test_delete_tender_description_field_from_the_payload_25300_2(self, country, language,
                                                                          instance, cassandra_username,
                                                                          cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            payload["tender"]["description"] = ""
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.10.20.11",
                                    "description": "Incorrect an attribute value.The attribute 'tender.description' "
                                                   "is empty or blank."}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("25300")
        def test_delete_planning_rationale_field_from_the_payload_25300_3(self, country, language,
                                                                          instance, cassandra_username,
                                                                          cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            payload["planning"]["rationale"] = ""
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.10.20.11",
                                    "description": "Incorrect an attribute value.The attribute 'planning.rationale' "
                                                   "is empty or blank."}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("25300")
        def test_delete_tender_items_delivery_address_street_address_field_from_the_payload_25300_4(self, country,
                                                                                                    language, instance,
                                                                                                    cassandra_username,
                                                                                                    cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = ""
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.10.20.11",
                                    "description": "Incorrect an attribute value.The attribute 'tender.items.delivery"
                                                   "Address.streetAddress' is empty or blank."}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("25300")
        def test_delete_tender_items_address_details_locality_scheme_field_from_the_payload_25300_5(self, country,
                                                                                                    language, instance,
                                                                                                    cassandra_username,
                                                                                                    cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = ""
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.10.20.11",
                                    "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                                   "addressDetails.locality.scheme' is empty or blank."}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("25300")
        def test_delete_tender_items_address_details_locality_id_field_from_the_payload_25300_6(self, country,
                                                                                                language, instance,
                                                                                                cassandra_username,
                                                                                                cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = ""
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.20.00.14", "description": "Locality not found. "}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("25300")
        def test_delete_tender_items_address_details_locality_description_field_25300_7(self, country,
                                                                                        language, instance,
                                                                                        cassandra_username,
                                                                                        cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
            payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["description"] = ""
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.10.20.11",
                                    "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                                   "addressDetails.locality.description' is empty or blank."}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)

        @pytestrail.case("25300")
        def test_delete_tender_items_description_field_from_the_payload_25300_7(self, country, language, instance,
                                                                                cassandra_username, cassandra_password):
            payload = copy.deepcopy(payload_ei_full_data_model)
            payload["tender"]["items"][0]["description"] = ""
            ei = EI(payload=payload, lang=language, country=country, instance=instance,
                    cassandra_username=cassandra_username, cassandra_password=cassandra_password)
            ei.insert_ei_full_data_model()
            ei.update_ei()
            message_from_kafka = ei.get_message_from_kafka()
            actual_result = str(message_from_kafka["errors"])
            expected_result = str([{"code": "400.10.20.11",
                                    "description": "Incorrect an attribute value.The attribute 'tender.items."
                                                   "description' is empty or blank."}])
            assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                             actual_result=actual_result)
#
#
# class TestCheckOnImpossibilityUpdateEiIfTenderItemsQuantityIsLessOrEqualZero(object):
#     @pytestrail.case("24446")
#     def test_send_the_request_24446_1(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"][0]["quantity"] = 0
#         ei = EI(payload=payload, lang=language, country=country)
#         ei.insert_ei_full_data_model()
#         update_ei_response = ei.update_ei()
#         expected_result = str(202)
#         actual_result = str(update_ei_response.status_code)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case("24446")
#     def test_see_the_result_in_feed_point_24446_2(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"][0]["quantity"] = 0
#         ei = EI(payload=payload, lang=language, country=country)
#         insert_ei = ei.insert_ei_full_data_model()
#         ei.update_ei()
#         error_from_DB = execute_cql_from_orchestrator_operation_step(insert_ei[2], 'BudgetUpdateEiTask')
#         expected_result = str([{"code": "400.10.20.09",
#                                 "description": "Invalid item quantity.Quantity of item '1' must be greater
#                                 than zero"}])
#         actual_result = str(error_from_DB["errors"])
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#
# class TestCheckOnImpossibilityUpdateEiIfTenderItemsIdIsNotUniqueInTenderItemsArray(object):
#     @pytestrail.case("24447")
#     def test_send_the_request_24447_1(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload['tender']['items'] = [{
#             "id": "1",
#             "description": "item 1",
#             "classification": {
#                 "id": "45100000-8"
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
#         },
#             {
#                 "id": "1",
#                 "description": "item 2",
#                 "classification": {
#                     "id": "45100000-8"
#                 },
#                 "additionalClassifications": [
#                     {
#                         "id": "AA05-3"
#                     }
#                 ],
#                 "deliveryAddress": {
#                     "streetAddress": "хрещатик",
#                     "postalCode": "02235",
#                     "addressDetails": {
#                         "country": {
#                             "id": "MD",
#                             "description": "ОПИСАНИЕ",
#                             "scheme": "other"
#                         },
#                         "region": {
#                             "id": "1700000",
#                             "description": "ОПИСАНИЕ",
#                             "scheme": "CUATM"
#                         },
#                         "locality": {
#                             "id": "1701000",
#                             "description": "ОПИСАНИЕ2",
#                             "scheme": "other"
#                         }
#                     }
#                 },
#                 "quantity": 1,
#                 "unit": {
#                     "id": "10",
#                     "name": "name"
#                 }
#             }
#         ]
#         ei = EI(payload=payload, lang=language, country=country, tender_classification_id="45100000-8",
#                 tender_item_classification_id="45100000-8", planning_budget_id="45100000-8")
#         ei.insert_ei_obligatory_data_model()
#         update_ei_response = ei.update_ei()
#         expected_result = str(202)
#         actual_result = str(update_ei_response.status_code)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case("24447")
#     def test_see_the_result_in_feed_point_24447_2(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload['tender']['items'] = [{
#             "id": "1",
#             "description": "item 1",
#             "classification": {
#                 "id": "45100000-8"
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
#         },
#             {
#                 "id": "1",
#                 "description": "item 2",
#                 "classification": {
#                     "id": "45100000-8"
#                 },
#                 "additionalClassifications": [
#                     {
#                         "id": "AA05-3"
#                     }
#                 ],
#                 "deliveryAddress": {
#                     "streetAddress": "хрещатик",
#                     "postalCode": "02235",
#                     "addressDetails": {
#                         "country": {
#                             "id": "MD",
#                             "description": "ОПИСАНИЕ",
#                             "scheme": "other"
#                         },
#                         "region": {
#                             "id": "1700000",
#                             "description": "ОПИСАНИЕ",
#                             "scheme": "CUATM"
#                         },
#                         "locality": {
#                             "id": "1701000",
#                             "description": "ОПИСАНИЕ2",
#                             "scheme": "other"
#                         }
#                     }
#                 },
#                 "quantity": 1,
#                 "unit": {
#                     "id": "10",
#                     "name": "name"
#                 }
#             }
#         ]
#         ei = EI(payload=payload, lang=language, country=country, tender_classification_id="45100000-8",
#                 tender_item_classification_id="45100000-8", planning_budget_id="45100000-8")
#         insert_ei = ei.insert_ei_obligatory_data_model()
#         ei.update_ei()
#         error_from_DB = execute_cql_from_orchestrator_operation_step(insert_ei[2], 'BudgetUpdateEiTask')
#         expected_result = str(
#             [{"code": "400.10.20.10", "description": "Duplicated items found.Item '1' has a duplicate"}])
#         actual_result = str(error_from_DB["errors"])
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#
# class TestCheckOnImpossibilityToUpdateSomeAttributesInEiRelease(object):
#     @pytestrail.case("24449")
#     def test_send_the_request_24449_1(self, country, language):
#         period = get_new_period()
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["classification"]["scheme"] = "ZVS"
#         payload["tender"]["classification"]["id"] = "45100000-8"
#         payload["tender"]["classification"]["description"] = "Dada"
#         payload["planning"]["budget"]["period"]["startDate"] = period[5]
#         payload["planning"]["budget"]["period"]["endDate"] = period[6]
#         payload["buyer"]["name"] = "zama"
#         payload["buyer"]["identifier"]["id"] = "380632074071"
#         payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
#         payload["buyer"]["identifier"]["legalName"] = "zao"
#         payload["buyer"]["identifier"]["uri"] = "fop"
#         payload["buyer"]["address"]["streetAddress"] = "Romashkova"
#         payload["buyer"]["address"]["postalCode"] = "87"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "1700000"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "1701000"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "mun.Chişinău789"
#         payload["buyer"]["contactPoint"]["name"] = "Petro"
#         payload["buyer"]["contactPoint"]["email"] = "petro@lpo"
#         payload["buyer"]["contactPoint"]["telephone"] = "0574256"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "456"
#         payload["buyer"]["contactPoint"]["url"] = "www url4444"
#         del payload["tender"]["items"]
#         ei = EI(payload=payload, lang=language, country=country, tender_classification_id="50100000-6",
#                 tender_item_classification_id="50100000-6", planning_budget_id="50100000-6",
#                 tender_classification_scheme="CPV", tender_classification_description="Timbre",
#                 planning_budget_period_start_date=get_period()[0], planning_budget_period_end_date=get_period()[1],
#                 buyer_name="Directia Cultura a Primariei mun.Chisinau", buyer_identifier_id="1007601010585",
#                 buyer_identifier_scheme="MD-IDNO", buyer_identifier_legal_name="Directia Cultura",
#                 buyer_identifier_uri="www", buyer_address_street_address="str.Bucuresti 68",
#                 buyer_address_address_details_country_id="MD", buyer_address_address_details_region_id="0101000",
#                 buyer_address_address_details_locality_id="0101000", buyer_contact_point_name="Dumitru Popa",
#                 buyer_address_address_details_locality_scheme="CUATM", buyer_contact_point_telephone="022242290",
#                 buyer_contact_point_email="directiacultшra@yahoo.com", buyer_contact_point_fax_number="123",
#                 buyer_address_address_details_locality_description="mun.Chişinău", buyer_contact_point_url="www url",
#                 buyer_address_postal_code="147")
#         insert = ei.insert_ei_full_data_model_without_item()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         update_ei_response = ei.update_ei()
#         expected_result = str(202)
#         actual_result = str(update_ei_response.status_code)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case("24449")
#     def test_see_the_result_in_feed_point_24449_2(self, country, language):
#         period = get_new_period()
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["classification"]["scheme"] = "ZVS"
#         payload["tender"]["classification"]["id"] = "45100000-8"
#         payload["tender"]["classification"]["description"] = "Dada"
#         payload["planning"]["budget"]["period"]["startDate"] = period[5]
#         payload["planning"]["budget"]["period"]["endDate"] = period[6]
#         payload["buyer"]["name"] = "zama"
#         payload["buyer"]["identifier"]["id"] = "380632074071"
#         payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
#         payload["buyer"]["identifier"]["legalName"] = "zao"
#         payload["buyer"]["identifier"]["uri"] = "fop"
#         payload["buyer"]["address"]["streetAddress"] = "Romashkova"
#         payload["buyer"]["address"]["postalCode"] = "87"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "1700000"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "1701000"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "mun.Chişinău789"
#         payload["buyer"]["contactPoint"]["name"] = "Petro"
#         payload["buyer"]["contactPoint"]["email"] = "petro@lpo"
#         payload["buyer"]["contactPoint"]["telephone"] = "0574256"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "456"
#         payload["buyer"]["contactPoint"]["url"] = "www url4444"
#         del payload["tender"]["items"]
#         ei = EI(payload=payload, lang=language, country=country, tender_classification_id="50100000-6",
#                 tender_item_classification_id="50100000-6", planning_budget_id="50100000-6",
#                 tender_classification_scheme="CPV", tender_classification_description="Timbre",
#                 planning_budget_period_start_date=get_period()[0], planning_budget_period_end_date=get_period()[1],
#                 buyer_name="Directia Cultura a Primariei mun.Chisinau", buyer_identifier_id="1007601010585",
#                 buyer_identifier_scheme="MD-IDNO", buyer_identifier_legal_name="Directia Cultura",
#                 buyer_identifier_uri="www", buyer_address_street_address="str.Bucuresti 68",
#                 buyer_address_address_details_country_id="MD", buyer_address_address_details_region_id="0101000",
#                 buyer_address_address_details_locality_id="0101000", buyer_contact_point_name="Dumitru Popa",
#                 buyer_address_address_details_locality_scheme="CUATM", buyer_contact_point_telephone="022242290",
#                 buyer_contact_point_email="directiacultшra@yahoo.com", buyer_contact_point_fax_number="123",
#                 buyer_address_address_details_locality_description="mun.Chişinău", buyer_contact_point_url="www url",
#                 buyer_address_postal_code="147")
#         insert = ei.insert_ei_full_data_model_without_item()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         ei.get_message_from_kafka()
#         actual_result = str(ei.check_on_that_message_is_successfull_update_ei())
#         expected_result = str(True)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)
#
#     @pytestrail.case("24449")
#     def test_compare_data_of_EI_release_before_updating_and_after_updating_24449_3(self, country, language):
#         period = get_new_period()
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["classification"]["scheme"] = "ZVS"
#         payload["tender"]["classification"]["id"] = "45100000-8"
#         payload["tender"]["classification"]["description"] = "Dada"
#         payload["planning"]["budget"]["period"]["startDate"] = period[5]
#         payload["planning"]["budget"]["period"]["endDate"] = period[6]
#         payload["buyer"]["name"] = "zama"
#         payload["buyer"]["identifier"]["id"] = "380632074071"
#         payload["buyer"]["identifier"]["scheme"] = "MD-IDNO"
#         payload["buyer"]["identifier"]["legalName"] = "zao"
#         payload["buyer"]["identifier"]["uri"] = "fop"
#         payload["buyer"]["address"]["streetAddress"] = "Romashkova"
#         payload["buyer"]["address"]["postalCode"] = "87"
#         payload["buyer"]["address"]["addressDetails"]["country"]["id"] = "MD"
#         payload["buyer"]["address"]["addressDetails"]["region"]["id"] = "1700000"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["scheme"] = "other"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["id"] = "1701000"
#         payload["buyer"]["address"]["addressDetails"]["locality"]["description"] = "mun.Chişinău789"
#         payload["buyer"]["contactPoint"]["name"] = "Petro"
#         payload["buyer"]["contactPoint"]["email"] = "petro@lpo"
#         payload["buyer"]["contactPoint"]["telephone"] = "0574256"
#         payload["buyer"]["contactPoint"]["faxNumber"] = "456"
#         payload["buyer"]["contactPoint"]["url"] = "www url4444"
#         del payload["tender"]["items"]
#         ei = EI(payload=payload, lang=language, country=country, tender_classification_id="50100000-6",
#                 tender_item_classification_id="50100000-6", planning_budget_id="50100000-6",
#                 tender_classification_scheme="CPV", tender_classification_description="Timbre",
#                 planning_budget_period_start_date=get_period()[0], planning_budget_period_end_date=get_period()[1],
#                 buyer_name="Directia Cultura a Primariei mun.Chisinau", buyer_identifier_id="1007601010585",
#                 buyer_identifier_scheme="MD-IDNO", buyer_identifier_legal_name="Directia Cultura",
#                 buyer_identifier_uri="www", buyer_address_street_address="str.Bucuresti 68",
#                 buyer_address_address_details_country_id="MD", buyer_address_address_details_region_id="0101000",
#                 buyer_address_address_details_locality_id="0101000", buyer_contact_point_name="Dumitru Popa",
#                 buyer_address_address_details_locality_scheme="CUATM", buyer_contact_point_telephone="022242290",
#                 buyer_contact_point_email="directiacultшra@yahoo.com", buyer_contact_point_fax_number="123",
#                 buyer_address_address_details_locality_description="mun.Chişinău", buyer_contact_point_url="www url",
#                 buyer_address_postal_code="147")
#         insert = ei.insert_ei_full_data_model_without_item()
#         ei_release_before_updating = requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         message_from_kafka = ei.get_message_from_kafka()
#         ei_release_after_updating = requests.get(url=message_from_kafka["data"]["url"]).json()
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["tender"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["tender"]["status"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["status"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["tender"]["statusDetails"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["statusDetails"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["tender"]["classification"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["classification"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["tender"]["classification"]["scheme"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["classification"]["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["tender"]["classification"]["description"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["classification"]["description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["tender"]["mainProcurementCategory"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["mainProcurementCategory"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["planning"]["budget"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["planning"]["budget"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["planning"]["budget"]["period"]["startDate"],
#             actual_result=ei_release_after_updating["releases"][0]["planning"]["budget"]["period"]["startDate"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["planning"]["budget"]["period"]["endDate"],
#             actual_result=ei_release_after_updating["releases"][0]["planning"]["budget"]["period"]["endDate"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["buyer"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["buyer"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["buyer"]["name"],
#             actual_result=ei_release_after_updating["releases"][0]["buyer"]["name"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["parties"][0]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["parties"][0]["name"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["name"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["parties"][0]["identifier"]["scheme"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["identifier"]["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["parties"][0]["identifier"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["identifier"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["parties"][0]["identifier"]["legalName"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["identifier"]["legalName"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["parties"][0]["identifier"]["uri"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["identifier"]["uri"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=ei_release_before_updating["releases"][0]["parties"][0]["address"]["streetAddress"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["address"]["streetAddress"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                 "scheme"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                 "scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                 "id"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                 "id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                 "description"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                 "description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                 "uri"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["country"][
#                 "uri"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                 "scheme"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                 "scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                 "id"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"][
#             "region"][
#                 "id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                 "description"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"][
#             "region"][
#                 "description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["region"][
#                 "uri"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"][
#             "region"][
#                 "uri"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#             "scheme"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                 "scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["id"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                 "id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                 "description"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                 "description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"]["uri"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["parties"][0]["address"]["addressDetails"]["locality"][
#                 "uri"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["contactPoint"]["name"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["contactPoint"]["name"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["contactPoint"]["email"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["contactPoint"]["email"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["contactPoint"]["telephone"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["contactPoint"]["telephone"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["contactPoint"]["faxNumber"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["contactPoint"]["faxNumber"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["contactPoint"]["url"],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["contactPoint"]["url"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=
#             ei_release_before_updating["releases"][0]["parties"][0]["roles"][0],
#             actual_result=ei_release_after_updating["releases"][0]["parties"][0]["roles"][0])
#
#
# class TestCheckOnPossibilityUpdateTenderTitleTenderDescriptionAttributesInEiRelease(object):
#     @pytestrail.case("24450")
#     def test_send_the_request_24450_1(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["description"] = "fada"
#         payload["tender"]["title"] = "zayac"
#         ei = EI(payload=payload, lang=language, country=country, tender_title="volk", tender_description="kola")
#         insert = ei.insert_ei_full_data_model_without_item()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         update_ei_response = ei.update_ei()
#         expected_result = str(202)
#         actual_result = str(update_ei_response.status_code)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case("24450")
#     def test_see_the_result_in_feed_point_24450_2(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["description"] = "fada"
#         payload["tender"]["title"] = "zayac"
#         ei = EI(payload=payload, lang=language, country=country, tender_title="volk", tender_description="kola")
#         insert = ei.insert_ei_full_data_model_without_item()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         ei.get_message_from_kafka()
#         actual_result = str(ei.check_on_that_message_is_successfull_update_ei())
#         expected_result = str(True)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)
#
#     @pytestrail.case("24450")
#     def test_compare_data_of_EI_release_before_updating_and_after_updating_24450_3(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["description"] = "fada"
#         payload["tender"]["title"] = "zayac"
#         ei = EI(payload=payload, lang=language, country=country, tender_title="volk", tender_description="kola")
#         insert = ei.insert_ei_full_data_model_without_item()
#         ei_release_before_updating = requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         message_from_kafka = ei.get_message_from_kafka()
#         ei_release_after_updating = requests.get(url=message_from_kafka["data"]["url"]).json()
#         assert compare_actual_result_and_expected_result(
#             expected_result="volk",
#             actual_result=ei_release_before_updating["releases"][0]["tender"]["title"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="kola",
#             actual_result=ei_release_before_updating["releases"][0]["tender"]["description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]["title"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["title"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]["description"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["description"])
#
#
# class TestCheckOnPossibilityUpdatePlanningRationaleInEiRelease(object):
#     @pytestrail.case("24451")
#     def test_send_the_request_24451_1(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["planning"]["rationale"] = "fada"
#         ei = EI(payload=payload, lang=language, country=country, planning_rationale="gf")
#         insert = ei.insert_ei_full_data_model_without_item()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         update_ei_response = ei.update_ei()
#         expected_result = str(202)
#         actual_result = str(update_ei_response.status_code)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case("24451")
#     def test_see_the_result_in_feed_point_24451_2(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["planning"]["rationale"] = "fada"
#         ei = EI(payload=payload, lang=language, country=country, planning_rationale="gf")
#         insert = ei.insert_ei_full_data_model_without_item()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         ei.get_message_from_kafka()
#         actual_result = str(ei.check_on_that_message_is_successfull_update_ei())
#         expected_result = str(True)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)
#
#     @pytestrail.case("24451")
#     def test_compare_data_of_EI_release_before_updating_and_after_updating_24451_3(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["planning"]["rationale"] = "fada"
#         ei = EI(payload=payload, lang=language, country=country, planning_rationale="gf")
#         insert = ei.insert_ei_full_data_model_without_item()
#         ei_release_before_updating = requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         message_from_kafka = ei.get_message_from_kafka()
#         ei_release_after_updating = requests.get(url=message_from_kafka["data"]["url"]).json()
#         assert compare_actual_result_and_expected_result(
#             expected_result="gf",
#             actual_result=ei_release_before_updating["releases"][0]["planning"]["rationale"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["planning"]["rationale"],
#             actual_result=ei_release_after_updating["releases"][0]["planning"]["rationale"])
#
#
# class TestCheckOnPossibilityUpdateTenderItemsDescriptionInEiRelease(object):
#     @pytestrail.case("24452")
#     def test_send_the_request_24452_1(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"][0]["description"] = "popo"
#         payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
#         payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA04-0"
#         ei = EI(payload=payload, lang=language, country=country, tender_item_classification_id="45100000-8",
#                 tender_items_additional_classifications_id="AA12-4", tender_items_description="gaga")
#         insert = ei.insert_ei_full_data_model()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         update_ei_response = ei.update_ei()
#         expected_result = str(202)
#         actual_result = str(update_ei_response.status_code)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case("24452")
#     def test_see_the_result_in_feed_point_24452_2(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"][0]["description"] = "popo"
#         payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
#         payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA04-0"
#         ei = EI(payload=payload, lang=language, country=country, tender_item_classification_id="45100000-8",
#                 tender_items_additional_classifications_id="AA12-4", tender_items_description="gaga")
#         insert = ei.insert_ei_full_data_model()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         ei.get_message_from_kafka()
#         actual_result = str(ei.check_on_that_message_is_successfull_update_ei())
#         expected_result = str(True)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)
#
#     @pytestrail.case("24452")
#     def test_compare_data_of_EI_release_before_updating_and_after_updating_24452_3(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"][0]["description"] = "popo"
#         payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
#         payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = "AA04-0"
#         ei = EI(payload=payload, lang=language, country=country, tender_item_classification_id="45100000-8",
#                 tender_items_additional_classifications_id="AA12-4", tender_items_description="gaga")
#         insert = ei.insert_ei_full_data_model()
#         ei_release_before_updating = requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         message_from_kafka = ei.get_message_from_kafka()
#         ei_release_after_updating = requests.get(url=message_from_kafka["data"]["url"]).json()
#         assert compare_actual_result_and_expected_result(
#             expected_result="gaga",
#             actual_result=ei_release_before_updating["releases"][0]["tender"]["items"][0]["description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="45100000-8",
#             actual_result=ei_release_before_updating["releases"][0]["tender"]["items"][0]["classification"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="AA12-4",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]["items"][0]["description"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["items"][0]["description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]["items"][0]["classification"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]["items"][0]["classification"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]["items"][0]["additionalClassifications"][0]["id"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"])
#
#
# class TestCheckOnPossibilityUpdateTenderItemsDeliveryAddressInEiRelease(object):
#     @pytestrail.case("24453")
#     def test_send_the_request_24453_1(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload['tender']['items'][0]['deliveryAddress']['streetAddress'] = "Vladimirskaya"
#         payload['tender']['items'][0]['deliveryAddress']['postalCode'] = "33344"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = "Re_44"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = "scheme_1_1"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = "www.poland"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = "1700000"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['description'] = "
#         description_44_2"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = "sheme_region_78"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = "www,regi_12"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = "other"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = "locality_1"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = "www.vbn.ko"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
#             'description'] = "description_test_22"
#         payload['tender']['items'][0]['quantity'] = 256
#         payload['tender']['items'][0]['unit']['id'] = '120'
#         payload['tender']['items'][0]['unit']['name'] = 'name_2'
#         ei = EI(payload=payload, lang=language, country=country, tender_items_delivery_street="Khreshchatyk",
#                 tender_items_delivery_postal="01124", tender_items_delivery_details_country_id="MD",
#                 tender_items_delivery_details_region_id="0101000", tender_items_delivery_details_locality_id="
#                 0101000",
#                 tender_items_delivery_details_locality_scheme="CUATM", tender_items_quantity=10,
#                 tender_items_unit_id="10", tender_items_unit_name="name")
#         insert = ei.insert_ei_full_data_model()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         update_ei_response = ei.update_ei()
#         expected_result = str(202)
#         actual_result = str(update_ei_response.status_code)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case("24453")
#     def test_see_the_result_in_feed_point_24453_2(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload['tender']['items'][0]['deliveryAddress']['streetAddress'] = "Vladimirskaya"
#         payload['tender']['items'][0]['deliveryAddress']['postalCode'] = "33344"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = "Re_44"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = "scheme_1_1"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = "www.poland"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = "1700000"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['description'] = "
#         description_44_2"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = "sheme_region_78"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = "www,regi_12"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = "other"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = "locality_1"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = "www.vbn.ko"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
#             'description'] = "description_test_22"
#         payload['tender']['items'][0]['quantity'] = 256
#         payload['tender']['items'][0]['unit']['id'] = '120'
#         payload['tender']['items'][0]['unit']['name'] = 'name_2'
#         ei = EI(payload=payload, lang=language, country=country, tender_items_delivery_street="Khreshchatyk",
#                 tender_items_delivery_postal="01124", tender_items_delivery_details_country_id="MD",
#                 tender_items_delivery_details_region_id="0101000", tender_items_delivery_details_locality_id="
#                 0101000",
#                 tender_items_delivery_details_locality_scheme="CUATM", tender_items_quantity=10,
#                 tender_items_unit_id="10", tender_items_unit_name="name")
#         insert = ei.insert_ei_full_data_model()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         ei.get_message_from_kafka()
#         actual_result = str(ei.check_on_that_message_is_successfull_update_ei())
#         expected_result = str(True)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)
#
#     @pytestrail.case("24453")
#     def test_compare_data_of_EI_release_before_updating_and_after_updating_24453_3(self, country, language):
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload['tender']['items'][0]['deliveryAddress']['streetAddress'] = "Vladimirskaya"
#         payload['tender']['items'][0]['deliveryAddress']['postalCode'] = "33344"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = 'MD'
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = "Re_44"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = "scheme_1_1"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['uri'] = "www.poland"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = "1700000"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['description'] = "
#         description_44_2"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = "sheme_region_78"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['uri'] = "www,regi_12"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = "other"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = "locality_1"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['uri'] = "www.vbn.ko"
#         payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality'][
#             'description'] = "description_test_22"
#         payload['tender']['items'][0]['quantity'] = 256.0
#         payload['tender']['items'][0]['unit']['id'] = '120'
#         payload['tender']['items'][0]['unit']['name'] = 'name_2'
#         ei = EI(payload=payload, lang=language, country=country, tender_items_delivery_street="Khreshchatyk",
#                 tender_items_delivery_postal="01124", tender_items_delivery_details_country_id="MD",
#                 tender_items_delivery_details_region_id="0101000", tender_items_delivery_details_locality_id="
#                 0101000",
#                 tender_items_delivery_details_locality_scheme="CUATM", tender_items_quantity=10,
#                 tender_items_unit_id="10", tender_items_unit_name="Parsec")
#         insert = ei.insert_ei_full_data_model()
#         ei_release_before_updating = requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         message_from_kafka = ei.get_message_from_kafka()
#         ei_release_after_updating = requests.get(url=message_from_kafka["data"]["url"]).json()
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload['tender']['items'][0]['deliveryAddress']['streetAddress'],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress'][
#                 'streetAddress'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Khreshchatyk",
#             actual_result=ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress'][
#                 'streetAddress'])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload['tender']['items'][0]['deliveryAddress']['postalCode'],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress'][
#                 'postalCode'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="01124",
#             actual_result=ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress'][
#                 'postalCode'])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'],
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'country']['id'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="MD",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'country']['id'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Moldova, Republica",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'country']['description'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Moldova, Republica",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'country']['description'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="iso-alpha2",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'country']['scheme'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="iso-alpha2",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'country']['scheme'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="https://www.iso.org",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'country']['uri'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="https://www.iso.org",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'country']['uri'])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'],
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'region']['id'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="0101000",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'region']['id'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Cahul",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'region']['description'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="mun.Chişinău",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'region']['description'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="CUATM",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'region']['scheme'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="CUATM",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'region']['scheme'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="http://statistica.md",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'region']['uri'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="http://statistica.md",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'region']['uri'])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'],
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'locality']['id'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="0101000",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'locality']['id'])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'locality']['description'],
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'locality']['description'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="mun.Chişinău",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'locality']['description'])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'locality']['scheme'],
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'locality']['scheme'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="CUATM",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'locality']['scheme'])
#
#         assert compare_actual_result_and_expected_result(
#             expected_result="http://statistica.md",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['deliveryAddress']['addressDetails'][
#                 'locality']['uri'])
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(payload["tender"]['items'][0]["quantity"]),
#             actual_result=
#             str(ei_release_after_updating["releases"][0]["tender"]['items'][0]['quantity']))
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(10),
#             actual_result=
#             str(ei_release_before_updating["releases"][0]["tender"]['items'][0]['quantity']))
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]["unit"]["id"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['unit']["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="10",
#             actual_result=
#             str(ei_release_before_updating["releases"][0]["tender"]['items'][0]['unit']["id"]))
#         assert compare_actual_result_and_expected_result(
#             expected_result="Milion decalitri",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['unit']["name"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Parsec",
#             actual_result=
#             ei_release_before_updating["releases"][0]["tender"]['items'][0]['unit']["name"])
#
#
# class TestCheckOnThatSystemAddsNewItemObjectInEiRelease(object):
#     @pytestrail.case("24454")
#     def test_send_the_request_24454_1(self, country, language):
#         tender_items_id = "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9"
#         tender_items_description = " item_1"
#         tender_classification_id = "45100000-8"
#         tender_item_classification_id = tender_classification_id
#         tender_items_additional_classifications_id = "AA12-4"
#         tender_items_delivery_street = "Khreshchatyk"
#         tender_items_delivery_postal = "01124"
#         tender_items_delivery_details_country_id = "MD"
#         tender_items_delivery_details_region_id = "0101000"
#         tender_items_delivery_details_locality_id = "0101000"
#         tender_items_delivery_details_locality_scheme = "CUATM"
#         tender_items_quantity = 10
#         tender_items_unit_id = "10"
#         tender_items_unit_name = "Parsec"
#
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"] = [{
#             "id": tender_items_id,
#             "description": tender_items_description,
#             "classification": {
#                 "id": tender_item_classification_id
#             },
#             "additionalClassifications": [
#                 {
#                     "id": tender_items_additional_classifications_id
#                 }
#             ],
#             "deliveryAddress": {
#                 "streetAddress": tender_items_delivery_street,
#                 "postalCode": tender_items_delivery_postal,
#                 "addressDetails": {
#                     "country": {
#                         "id": tender_items_delivery_details_country_id,
#                         "description": "description_1",
#                         "scheme": "scheme_1",
#                         "uri": "www.deutch"
#                     },
#                     "region": {
#                         "id": tender_items_delivery_details_region_id,
#                         "description": "description_2",
#                         "scheme": "scheme_2",
#                         "uri": "www,regi_16"
#                     },
#                     "locality": {
#                         "id": tender_items_delivery_details_locality_id,
#                         "description": "description_test",
#                         "scheme": tender_items_delivery_details_locality_scheme,
#                         "uri": "ww.io.io"
#                     }
#
#                 }
#             },
#             "quantity": tender_items_quantity,
#             "unit": {
#                 "id": tender_items_unit_id,
#                 "name": tender_items_unit_name
#             }
#         },
#             {"id": "2",
#              "description": "item 2",
#              "classification": {
#                  "id": '45112360-6'
#              },
#              "additionalClassifications": [
#                  {
#                      "id": "AA04-0"
#                  }
#              ],
#              "deliveryAddress": {
#                  "streetAddress": "Voloshkina",
#                  "postalCode": "55555",
#                  "addressDetails": {
#                      "country": {
#                          "id": "MD",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.55"
#                      },
#                      "region": {
#                          "id": "1700000",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.regi_55"
#                      },
#                      "locality": {
#                          "id": "555555",
#                          "description": "description_test_55",
#                          "scheme": 'other',
#                          "uri": "ww.io.55"
#                      }
#
#                  }
#              },
#              "quantity": 20,
#              "unit": {
#                  "id": "120",
#                  "name": "name_2"
#              }
#              }
#         ]
#         ei = EI(payload=payload, lang=language, country=country,
#                 tender_items_id=tender_items_id, tender_items_description=tender_items_description,
#                 tender_item_classification_id=tender_item_classification_id,
#                 tender_classification_id=tender_classification_id,
#                 tender_items_additional_classifications_id=tender_items_additional_classifications_id,
#                 tender_items_delivery_street=tender_items_delivery_street,
#                 tender_items_delivery_postal=tender_items_delivery_postal,
#                 tender_items_delivery_details_country_id=tender_items_delivery_details_country_id,
#                 tender_items_delivery_details_region_id=tender_items_delivery_details_region_id,
#                 tender_items_delivery_details_locality_id=tender_items_delivery_details_locality_id,
#                 tender_items_delivery_details_locality_scheme=tender_items_delivery_details_locality_scheme,
#                 tender_items_quantity=tender_items_quantity, tender_items_unit_id=tender_items_unit_id,
#                 tender_items_unit_name=tender_items_unit_name)
#         insert = ei.insert_ei_full_data_model()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         update_ei_response = ei.update_ei()
#         expected_result = str(202)
#         actual_result = str(update_ei_response.status_code)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case("24454")
#     def test_see_the_result_in_feed_point_24454_2(self, country, language):
#         tender_items_id = "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9"
#         tender_items_description = " item_1"
#         tender_classification_id = "45100000-8"
#         tender_item_classification_id = tender_classification_id
#         tender_items_additional_classifications_id = "AA12-4"
#         tender_items_delivery_street = "Khreshchatyk"
#         tender_items_delivery_postal = "01124"
#         tender_items_delivery_details_country_id = "MD"
#         tender_items_delivery_details_region_id = "0101000"
#         tender_items_delivery_details_locality_id = "0101000"
#         tender_items_delivery_details_locality_scheme = "CUATM"
#         tender_items_quantity = 10
#         tender_items_unit_id = "10"
#         tender_items_unit_name = "Parsec"
#
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"] = [{
#             "id": tender_items_id,
#             "description": tender_items_description,
#             "classification": {
#                 "id": tender_item_classification_id
#             },
#             "additionalClassifications": [
#                 {
#                     "id": tender_items_additional_classifications_id
#                 }
#             ],
#             "deliveryAddress": {
#                 "streetAddress": tender_items_delivery_street,
#                 "postalCode": tender_items_delivery_postal,
#                 "addressDetails": {
#                     "country": {
#                         "id": tender_items_delivery_details_country_id,
#                         "description": "description_1",
#                         "scheme": "scheme_1",
#                         "uri": "www.deutch"
#                     },
#                     "region": {
#                         "id": tender_items_delivery_details_region_id,
#                         "description": "description_2",
#                         "scheme": "scheme_2",
#                         "uri": "www,regi_16"
#                     },
#                     "locality": {
#                         "id": tender_items_delivery_details_locality_id,
#                         "description": "description_test",
#                         "scheme": tender_items_delivery_details_locality_scheme,
#                         "uri": "ww.io.io"
#                     }
#
#                 }
#             },
#             "quantity": tender_items_quantity,
#             "unit": {
#                 "id": tender_items_unit_id,
#                 "name": tender_items_unit_name
#             }
#         },
#             {"id": "2",
#              "description": "item 2",
#              "classification": {
#                  "id": '45112360-6'
#              },
#              "additionalClassifications": [
#                  {
#                      "id": "AA04-0"
#                  }
#              ],
#              "deliveryAddress": {
#                  "streetAddress": "Voloshkina",
#                  "postalCode": "55555",
#                  "addressDetails": {
#                      "country": {
#                          "id": "MD",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.55"
#                      },
#                      "region": {
#                          "id": "1700000",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.regi_55"
#                      },
#                      "locality": {
#                          "id": "555555",
#                          "description": "description_test_55",
#                          "scheme": 'other',
#                          "uri": "ww.io.55"
#                      }
#
#                  }
#              },
#              "quantity": 20,
#              "unit": {
#                  "id": "120",
#                  "name": "name_2"
#              }
#              }
#         ]
#         ei = EI(payload=payload, lang=language, country=country,
#                 tender_items_id=tender_items_id, tender_items_description=tender_items_description,
#                 tender_item_classification_id=tender_item_classification_id,
#                 tender_classification_id=tender_classification_id,
#                 tender_items_additional_classifications_id=tender_items_additional_classifications_id,
#                 tender_items_delivery_street=tender_items_delivery_street,
#                 tender_items_delivery_postal=tender_items_delivery_postal,
#                 tender_items_delivery_details_country_id=tender_items_delivery_details_country_id,
#                 tender_items_delivery_details_region_id=tender_items_delivery_details_region_id,
#                 tender_items_delivery_details_locality_id=tender_items_delivery_details_locality_id,
#                 tender_items_delivery_details_locality_scheme=tender_items_delivery_details_locality_scheme,
#                 tender_items_quantity=tender_items_quantity, tender_items_unit_id=tender_items_unit_id,
#                 tender_items_unit_name=tender_items_unit_name)
#         insert = ei.insert_ei_full_data_model()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         ei.get_message_from_kafka()
#         actual_result = str(ei.check_on_that_message_is_successfull_update_ei())
#         expected_result = str(True)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)
#
#     @pytestrail.case("24454")
#     def test_compare_data_of_EI_release_before_updating_and_after_updating_24454_3(self, country, language):
#         tender_items_id = "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9"
#         tender_items_description = " item_1"
#         tender_classification_id = "45100000-8"
#         tender_item_classification_id = tender_classification_id
#         tender_items_additional_classifications_id = "AA12-4"
#         tender_items_delivery_street = "Khreshchatyk"
#         tender_items_delivery_postal = "01124"
#         tender_items_delivery_details_country_id = "MD"
#         tender_items_delivery_details_region_id = "0101000"
#         tender_items_delivery_details_locality_id = "0101000"
#         tender_items_delivery_details_locality_scheme = "CUATM"
#         tender_items_quantity = 10
#         tender_items_unit_id = "10"
#         tender_items_unit_name = "Parsec"
#
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"] = [{
#             "id": tender_items_id,
#             "description": tender_items_description,
#             "classification": {
#                 "id": tender_item_classification_id
#             },
#             "additionalClassifications": [
#                 {
#                     "id": tender_items_additional_classifications_id
#                 }
#             ],
#             "deliveryAddress": {
#                 "streetAddress": tender_items_delivery_street,
#                 "postalCode": tender_items_delivery_postal,
#                 "addressDetails": {
#                     "country": {
#                         "id": tender_items_delivery_details_country_id,
#                         "description": "description_1",
#                         "scheme": "scheme_1",
#                         "uri": "www.deutch"
#                     },
#                     "region": {
#                         "id": tender_items_delivery_details_region_id,
#                         "description": "description_2",
#                         "scheme": "scheme_2",
#                         "uri": "www,regi_16"
#                     },
#                     "locality": {
#                         "id": tender_items_delivery_details_locality_id,
#                         "description": "description_test",
#                         "scheme": tender_items_delivery_details_locality_scheme,
#                         "uri": "ww.io.io"
#                     }
#
#                 }
#             },
#             "quantity": tender_items_quantity,
#             "unit": {
#                 "id": tender_items_unit_id,
#                 "name": tender_items_unit_name
#             }
#         },
#             {"id": "2",
#              "description": "item 2",
#              "classification": {
#                  "id": '45112360-6'
#              },
#              "additionalClassifications": [
#                  {
#                      "id": "AA04-0"
#                  }
#              ],
#              "deliveryAddress": {
#                  "streetAddress": "Voloshkina",
#                  "postalCode": "55555",
#                  "addressDetails": {
#                      "country": {
#                          "id": "MD",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.55"
#                      },
#                      "region": {
#                          "id": "1700000",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.regi_55"
#                      },
#                      "locality": {
#                          "id": "555555",
#                          "description": "description_test_55",
#                          "scheme": 'other',
#                          "uri": "ww.io.55"
#                      }
#
#                  }
#              },
#              "quantity": 20,
#              "unit": {
#                  "id": "120",
#                  "name": "name_2"
#              }
#              }
#         ]
#         ei = EI(payload=payload, lang=language, country=country,
#                 tender_items_id=tender_items_id, tender_items_description=tender_items_description,
#                 tender_item_classification_id=tender_item_classification_id,
#                 tender_classification_id=tender_classification_id,
#                 tender_items_additional_classifications_id=tender_items_additional_classifications_id,
#                 tender_items_delivery_street=tender_items_delivery_street,
#                 tender_items_delivery_postal=tender_items_delivery_postal,
#                 tender_items_delivery_details_country_id=tender_items_delivery_details_country_id,
#                 tender_items_delivery_details_region_id=tender_items_delivery_details_region_id,
#                 tender_items_delivery_details_locality_id=tender_items_delivery_details_locality_id,
#                 tender_items_delivery_details_locality_scheme=tender_items_delivery_details_locality_scheme,
#                 tender_items_quantity=tender_items_quantity, tender_items_unit_id=tender_items_unit_id,
#                 tender_items_unit_name=tender_items_unit_name)
#         ei.insert_ei_full_data_model()
#         ei.update_ei()
#         message_from_kafka = ei.get_message_from_kafka()
#         ei_release_after_updating = requests.get(url=message_from_kafka["data"]["url"]).json()
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(True),
#             actual_result=str(is_valid_uuid(ei_release_after_updating["releases"][0]["tender"]['items'][0]['id'], 4)))
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]['description'],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]['description'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="CPV",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]['classification']["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]["items"][0]["classification"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]['classification']["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Lucrări de pregătire a şantierului",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]['classification'][
#                 "description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="CPVS",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['additionalClassifications'][0]["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]['additionalClassifications'][0]["id"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['additionalClassifications'][0]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Oţel carbon",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][0]['additionalClassifications'][0][
#                 "description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]["quantity"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["quantity"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]["unit"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["unit"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Parsec",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["unit"]["name"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]["deliveryAddress"]["streetAddress"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "streetAddress"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]["deliveryAddress"]["postalCode"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "postalCode"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]["deliveryAddress"]["addressDetails"]["country"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["country"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="iso-alpha2",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["country"]["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Moldova, Republica",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["country"]["description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="https://www.iso.org",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["country"]["uri"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="CUATM",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["region"]["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]["deliveryAddress"]["addressDetails"]["region"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["region"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="mun.Chişinău",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["region"]["description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="http://statistica.md",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["region"]["uri"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="CUATM",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["locality"]["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][0]["deliveryAddress"]["addressDetails"]["locality"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["locality"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="mun.Chişinău",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["locality"]["description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="http://statistica.md",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][0]["deliveryAddress"][
#                 "addressDetails"]["locality"]["uri"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(True),
#             actual_result=str(is_valid_uuid(ei_release_after_updating["releases"][0]["tender"]['items'][1]['id'], 4)))
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]['description'],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]['description'])
#         assert compare_actual_result_and_expected_result(
#             expected_result="CPV",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]['classification']["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]["items"][1]["classification"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]['classification']["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Lucrări de reabilitare a terenului",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]['classification'][
#                 "description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="CPVS",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][1]['additionalClassifications'][0]["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]['additionalClassifications'][0]["id"],
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][1]['additionalClassifications'][0]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Cupru",
#             actual_result=
#             ei_release_after_updating["releases"][0]["tender"]['items'][1]['additionalClassifications'][0][
#                 "description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]["quantity"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["quantity"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]["unit"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["unit"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Milion decalitri",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["unit"]["name"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]["deliveryAddress"]["streetAddress"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "streetAddress"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]["deliveryAddress"]["postalCode"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "postalCode"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]["deliveryAddress"]["addressDetails"]["country"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["country"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="iso-alpha2",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["country"]["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Moldova, Republica",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["country"]["description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="https://www.iso.org",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["country"]["uri"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="CUATM",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["region"]["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]["deliveryAddress"]["addressDetails"]["region"]["id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["region"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="Cahul",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["region"]["description"])
#         assert compare_actual_result_and_expected_result(
#             expected_result="http://statistica.md",
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["region"]["uri"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["locality"]["scheme"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["locality"]["scheme"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]["deliveryAddress"]["addressDetails"]["locality"][
#                 "id"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["locality"]["id"])
#         assert compare_actual_result_and_expected_result(
#             expected_result=payload["tender"]['items'][1]["deliveryAddress"]["addressDetails"]["locality"][
#                 "description"],
#             actual_result=ei_release_after_updating["releases"][0]["tender"]['items'][1]["deliveryAddress"][
#                 "addressDetails"]["locality"]["description"])
#
#
# class TestCheckOnThatSystemReleasesTenderItemsIdIsUuid4(object):
#     @pytestrail.case("24455")
#     def test_send_the_request_24455_1(self, country, language):
#         tender_items_id = "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9"
#         tender_items_description = " item_1"
#         tender_classification_id = "45100000-8"
#         tender_item_classification_id = tender_classification_id
#         tender_items_additional_classifications_id = "AA12-4"
#         tender_items_delivery_street = "Khreshchatyk"
#         tender_items_delivery_postal = "01124"
#         tender_items_delivery_details_country_id = "MD"
#         tender_items_delivery_details_region_id = "0101000"
#         tender_items_delivery_details_locality_id = "0101000"
#         tender_items_delivery_details_locality_scheme = "CUATM"
#         tender_items_quantity = 10
#         tender_items_unit_id = "10"
#         tender_items_unit_name = "Parsec"
#
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"] = [{
#             "id": tender_items_id,
#             "description": tender_items_description,
#             "classification": {
#                 "id": tender_item_classification_id
#             },
#             "additionalClassifications": [
#                 {
#                     "id": tender_items_additional_classifications_id
#                 }
#             ],
#             "deliveryAddress": {
#                 "streetAddress": tender_items_delivery_street,
#                 "postalCode": tender_items_delivery_postal,
#                 "addressDetails": {
#                     "country": {
#                         "id": tender_items_delivery_details_country_id,
#                         "description": "description_1",
#                         "scheme": "scheme_1",
#                         "uri": "www.deutch"
#                     },
#                     "region": {
#                         "id": tender_items_delivery_details_region_id,
#                         "description": "description_2",
#                         "scheme": "scheme_2",
#                         "uri": "www,regi_16"
#                     },
#                     "locality": {
#                         "id": tender_items_delivery_details_locality_id,
#                         "description": "description_test",
#                         "scheme": tender_items_delivery_details_locality_scheme,
#                         "uri": "ww.io.io"
#                     }
#
#                 }
#             },
#             "quantity": tender_items_quantity,
#             "unit": {
#                 "id": tender_items_unit_id,
#                 "name": tender_items_unit_name
#             }
#         },
#             {"id": "2",
#              "description": "item 2",
#              "classification": {
#                  "id": '45112360-6'
#              },
#              "additionalClassifications": [
#                  {
#                      "id": "AA04-0"
#                  }
#              ],
#              "deliveryAddress": {
#                  "streetAddress": "Voloshkina",
#                  "postalCode": "55555",
#                  "addressDetails": {
#                      "country": {
#                          "id": "MD",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.55"
#                      },
#                      "region": {
#                          "id": "1700000",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.regi_55"
#                      },
#                      "locality": {
#                          "id": "555555",
#                          "description": "description_test_55",
#                          "scheme": 'other',
#                          "uri": "ww.io.55"
#                      }
#
#                  }
#              },
#              "quantity": 20,
#              "unit": {
#                  "id": "120",
#                  "name": "name_2"
#              }
#              }
#         ]
#         ei = EI(payload=payload, lang=language, country=country,
#                 tender_items_id=tender_items_id, tender_items_description=tender_items_description,
#                 tender_item_classification_id=tender_item_classification_id,
#                 tender_classification_id=tender_classification_id,
#                 tender_items_additional_classifications_id=tender_items_additional_classifications_id,
#                 tender_items_delivery_street=tender_items_delivery_street,
#                 tender_items_delivery_postal=tender_items_delivery_postal,
#                 tender_items_delivery_details_country_id=tender_items_delivery_details_country_id,
#                 tender_items_delivery_details_region_id=tender_items_delivery_details_region_id,
#                 tender_items_delivery_details_locality_id=tender_items_delivery_details_locality_id,
#                 tender_items_delivery_details_locality_scheme=tender_items_delivery_details_locality_scheme,
#                 tender_items_quantity=tender_items_quantity, tender_items_unit_id=tender_items_unit_id,
#                 tender_items_unit_name=tender_items_unit_name)
#         insert = ei.insert_ei_full_data_model()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         update_ei_response = ei.update_ei()
#         expected_result = str(202)
#         actual_result = str(update_ei_response.status_code)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result,
#                                                          actual_result=actual_result)
#
#     @pytestrail.case("24455")
#     def test_see_the_result_in_feed_point_24455_2(self, country, language):
#         tender_items_id = "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9"
#         tender_items_description = " item_1"
#         tender_classification_id = "45100000-8"
#         tender_item_classification_id = tender_classification_id
#         tender_items_additional_classifications_id = "AA12-4"
#         tender_items_delivery_street = "Khreshchatyk"
#         tender_items_delivery_postal = "01124"
#         tender_items_delivery_details_country_id = "MD"
#         tender_items_delivery_details_region_id = "0101000"
#         tender_items_delivery_details_locality_id = "0101000"
#         tender_items_delivery_details_locality_scheme = "CUATM"
#         tender_items_quantity = 10
#         tender_items_unit_id = "10"
#         tender_items_unit_name = "Parsec"
#
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"] = [{
#             "id": tender_items_id,
#             "description": tender_items_description,
#             "classification": {
#                 "id": tender_item_classification_id
#             },
#             "additionalClassifications": [
#                 {
#                     "id": tender_items_additional_classifications_id
#                 }
#             ],
#             "deliveryAddress": {
#                 "streetAddress": tender_items_delivery_street,
#                 "postalCode": tender_items_delivery_postal,
#                 "addressDetails": {
#                     "country": {
#                         "id": tender_items_delivery_details_country_id,
#                         "description": "description_1",
#                         "scheme": "scheme_1",
#                         "uri": "www.deutch"
#                     },
#                     "region": {
#                         "id": tender_items_delivery_details_region_id,
#                         "description": "description_2",
#                         "scheme": "scheme_2",
#                         "uri": "www,regi_16"
#                     },
#                     "locality": {
#                         "id": tender_items_delivery_details_locality_id,
#                         "description": "description_test",
#                         "scheme": tender_items_delivery_details_locality_scheme,
#                         "uri": "ww.io.io"
#                     }
#
#                 }
#             },
#             "quantity": tender_items_quantity,
#             "unit": {
#                 "id": tender_items_unit_id,
#                 "name": tender_items_unit_name
#             }
#         },
#             {"id": "2",
#              "description": "item 2",
#              "classification": {
#                  "id": '45112360-6'
#              },
#              "additionalClassifications": [
#                  {
#                      "id": "AA04-0"
#                  }
#              ],
#              "deliveryAddress": {
#                  "streetAddress": "Voloshkina",
#                  "postalCode": "55555",
#                  "addressDetails": {
#                      "country": {
#                          "id": "MD",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.55"
#                      },
#                      "region": {
#                          "id": "1700000",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.regi_55"
#                      },
#                      "locality": {
#                          "id": "555555",
#                          "description": "description_test_55",
#                          "scheme": 'other',
#                          "uri": "ww.io.55"
#                      }
#
#                  }
#              },
#              "quantity": 20,
#              "unit": {
#                  "id": "120",
#                  "name": "name_2"
#              }
#              }
#         ]
#         ei = EI(payload=payload, lang=language, country=country,
#                 tender_items_id=tender_items_id, tender_items_description=tender_items_description,
#                 tender_item_classification_id=tender_item_classification_id,
#                 tender_classification_id=tender_classification_id,
#                 tender_items_additional_classifications_id=tender_items_additional_classifications_id,
#                 tender_items_delivery_street=tender_items_delivery_street,
#                 tender_items_delivery_postal=tender_items_delivery_postal,
#                 tender_items_delivery_details_country_id=tender_items_delivery_details_country_id,
#                 tender_items_delivery_details_region_id=tender_items_delivery_details_region_id,
#                 tender_items_delivery_details_locality_id=tender_items_delivery_details_locality_id,
#                 tender_items_delivery_details_locality_scheme=tender_items_delivery_details_locality_scheme,
#                 tender_items_quantity=tender_items_quantity, tender_items_unit_id=tender_items_unit_id,
#                 tender_items_unit_name=tender_items_unit_name)
#         insert = ei.insert_ei_full_data_model()
#         requests.get(url=insert[0] + "/" + insert[2]).json()
#         ei.update_ei()
#         ei.get_message_from_kafka()
#         actual_result = str(ei.check_on_that_message_is_successfull_update_ei())
#         expected_result = str(True)
#         assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)
#
#     @pytestrail.case("24455")
#     def test_CheckOnThatReleasesTenderItemsIdIsUuid4_24455_3(self, country, language):
#         tender_items_id = "6a565c47-ff11-4e2d-8ea1-3f34c5d751f9"
#         tender_items_description = " item_1"
#         tender_classification_id = "45100000-8"
#         tender_item_classification_id = tender_classification_id
#         tender_items_additional_classifications_id = "AA12-4"
#         tender_items_delivery_street = "Khreshchatyk"
#         tender_items_delivery_postal = "01124"
#         tender_items_delivery_details_country_id = "MD"
#         tender_items_delivery_details_region_id = "0101000"
#         tender_items_delivery_details_locality_id = "0101000"
#         tender_items_delivery_details_locality_scheme = "CUATM"
#         tender_items_quantity = 10
#         tender_items_unit_id = "10"
#         tender_items_unit_name = "Parsec"
#
#         payload = copy.deepcopy(payload_ei_full_data_model)
#         payload["tender"]["items"] = [{
#             "id": tender_items_id,
#             "description": tender_items_description,
#             "classification": {
#                 "id": tender_item_classification_id
#             },
#             "additionalClassifications": [
#                 {
#                     "id": tender_items_additional_classifications_id
#                 }
#             ],
#             "deliveryAddress": {
#                 "streetAddress": tender_items_delivery_street,
#                 "postalCode": tender_items_delivery_postal,
#                 "addressDetails": {
#                     "country": {
#                         "id": tender_items_delivery_details_country_id,
#                         "description": "description_1",
#                         "scheme": "scheme_1",
#                         "uri": "www.deutch"
#                     },
#                     "region": {
#                         "id": tender_items_delivery_details_region_id,
#                         "description": "description_2",
#                         "scheme": "scheme_2",
#                         "uri": "www,regi_16"
#                     },
#                     "locality": {
#                         "id": tender_items_delivery_details_locality_id,
#                         "description": "description_test",
#                         "scheme": tender_items_delivery_details_locality_scheme,
#                         "uri": "ww.io.io"
#                     }
#
#                 }
#             },
#             "quantity": tender_items_quantity,
#             "unit": {
#                 "id": tender_items_unit_id,
#                 "name": tender_items_unit_name
#             }
#         },
#             {"id": "2",
#              "description": "item 2",
#              "classification": {
#                  "id": '45112360-6'
#              },
#              "additionalClassifications": [
#                  {
#                      "id": "AA04-0"
#                  }
#              ],
#              "deliveryAddress": {
#                  "streetAddress": "Voloshkina",
#                  "postalCode": "55555",
#                  "addressDetails": {
#                      "country": {
#                          "id": "MD",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.55"
#                      },
#                      "region": {
#                          "id": "1700000",
#                          "description": "description_55",
#                          "scheme": "scheme_55",
#                          "uri": "www.regi_55"
#                      },
#                      "locality": {
#                          "id": "555555",
#                          "description": "description_test_55",
#                          "scheme": 'other',
#                          "uri": "ww.io.55"
#                      }
#
#                  }
#              },
#              "quantity": 20,
#              "unit": {
#                  "id": "120",
#                  "name": "name_2"
#              }
#              }
#         ]
#         ei = EI(payload=payload, lang=language, country=country,
#                 tender_items_id=tender_items_id, tender_items_description=tender_items_description,
#                 tender_item_classification_id=tender_item_classification_id,
#                 tender_classification_id=tender_classification_id,
#                 tender_items_additional_classifications_id=tender_items_additional_classifications_id,
#                 tender_items_delivery_street=tender_items_delivery_street,
#                 tender_items_delivery_postal=tender_items_delivery_postal,
#                 tender_items_delivery_details_country_id=tender_items_delivery_details_country_id,
#                 tender_items_delivery_details_region_id=tender_items_delivery_details_region_id,
#                 tender_items_delivery_details_locality_id=tender_items_delivery_details_locality_id,
#                 tender_items_delivery_details_locality_scheme=tender_items_delivery_details_locality_scheme,
#                 tender_items_quantity=tender_items_quantity, tender_items_unit_id=tender_items_unit_id,
#                 tender_items_unit_name=tender_items_unit_name)
#         ei.insert_ei_full_data_model()
#         ei.update_ei()
#         message_from_kafka = ei.get_message_from_kafka()
#         ei_release_after_updating = requests.get(url=message_from_kafka["data"]["url"]).json()
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(True),
#             actual_result=str(is_valid_uuid(ei_release_after_updating["releases"][0]["tender"]['items'][0]['id'], 4)))
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(True),
#             actual_result=str(is_valid_uuid(ei_release_after_updating["releases"][0]["tender"]['items'][1]['id'], 4)))
#
#

#
