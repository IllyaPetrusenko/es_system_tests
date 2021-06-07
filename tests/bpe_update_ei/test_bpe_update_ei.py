import copy
import time
from uuid import uuid4
from pytest_testrail.plugin import pytestrail
from tests.Cassandra_session import Cassandra
from tests.essences.ei import EI
from tests.payloads.ei_payload import payload_ei_obligatory_data_model, payload_ei_full_data_model
from useful_functions import compare_actual_result_and_expected_result, prepared_cp_id


class TestCheckOnPossibilityUpdateEiWithObligatoryFieldsInPayloadWithoutTenderItems(object):
    @pytestrail.case("23890")
    def test_send_the_request_23890_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        del payload["tender"]["items"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        update_ei_response = ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)

    @pytestrail.case("23890")
    def test_see_the_result_in_feed_point_23890_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        del payload["tender"]["items"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_update_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result, actual_result=actual_result)


class TestCheckOnPossibilityUpdateEiWithObligatoryFieldsInPayloadWithTenderItems(object):
    @pytestrail.case("24441")
    def test_send_the_request_24441_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        update_ei_response = ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24441")
    def test_see_the_result_in_feed_point_24441_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_update_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckOnPossibilityUpdateEiWithFullDataInPayload(object):
    @pytestrail.case("24442")
    def test_send_the_request_24442_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_obligatory_data_model(cp_id=cp_id, ei_token=ei_token)
        update_ei_response = ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24442")
    def test_see_the_result_in_feed_point_24442_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_obligatory_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        ei.get_message_from_kafka()
        actual_result = str(ei.check_on_that_message_is_successfully_update_ei())
        expected_result = str(True)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)


class TestCheckOnImpossibilityUpdateEiIfTokenFromRequestNotEqualTokenFromDB(object):
    @pytestrail.case("24443")
    def test_send_the_request_24443_1(self, country, language, instance, cassandra_username,
                                      cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password,
                )
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        update_ei_response = ei.update_ei(cp_id=cp_id, ei_token=str(uuid4()))
        expected_result = str(202)
        actual_result = str(update_ei_response.status_code)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24443")
    def test_see_the_result_in_feed_point_24443_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password
                )
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=str(uuid4()))
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            platform="platform_two"
        )
        ei.insert_ei_full_data_model(
            cp_id=cp_id,
            ei_token=ei_token
        )
        update_ei_response = ei.update_ei(
            cp_id=cp_id,
            ei_token=ei_token
        )
        expected_result = str(202)
        actual_result = str(update_ei_response.status_code)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24444")
    def test_see_the_result_in_feed_point_24444_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_obligatory_data_model)
        ei = EI(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            platform="platform_two"
        )
        ei.insert_ei_full_data_model(
            cp_id=cp_id,
            ei_token=ei_token
        )
        ei.update_ei(
            cp_id=cp_id,
            ei_token=ei_token
        )
        database = Cassandra(
            cp_id=cp_id,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )

        ei_budget_update_ei_task = database.execute_cql_from_orchestrator_operation_step(
            task_id='BudgetUpdateEiTask'
        )
        print(ei_budget_update_ei_task)
        assert compare_actual_result_and_expected_result(
            expected_result=str([{'code': '400.10.00.03', 'description': 'Invalid owner.'}]),
            actual_result=str(ei_budget_update_ei_task["errors"])
        )


class TestCheckOnImpossibilityUpdateEiIfTenderClassificationIdNotEqualTenderItemsClassificationId(object):
    @pytestrail.case("24445")
    def test_send_the_request_24445_1(self, country, language, instance, cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
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
        ei.insert_ei_obligatory_data_model(cp_id=cp_id, ei_token=ei_token)
        update_ei_response = ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        actual_result = str(update_ei_response.status_code)
        expected_result = str(202)
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24445")
    def test_see_the_result_in_feed_point_24445_2(self, country, language, instance, cassandra_username,
                                                  cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
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
        ei.insert_ei_obligatory_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{'code': '400.00.00.00', 'description': 'Data processing exception.'}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("24456")
    def test_delete_tender_title_field_from_the_payload_24456_2(self, country, language, instance,
                                                                cassandra_username,
                                                                cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["title"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["description"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["classification"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["country"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["region"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["quantity"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["unit"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["items"][0]["unit"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["classification"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]["classification"]["id"]
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["title"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["planning"]["rationale"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["streetAddress"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
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
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["id"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = None
        if payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] == "CUATM":
            expected_result = str([{'code': '400.20.00.14', 'description': 'Locality not found. '}])

        elif payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] == "other":
            expected_result = str([{'code': '400.10.20.11',
                                    'description': "Incorrect an attribute value.The attribute 'deliveryAddress."
                                                   "addressDetails.locality.id' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25300")
    def test_delete_tender_items_address_details_locality_description_field_25300_7(self, country,
                                                                                    language, instance,
                                                                                    cassandra_username,
                                                                                    cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["scheme"] = "other"
        payload["tender"]["items"][0]["deliveryAddress"]["addressDetails"]["locality"]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'deliveryAddress."
                                               "addressDetails.locality.description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)

    @pytestrail.case("25300")
    def test_delete_tender_items_description_field_from_the_payload_25300_8(self, country, language, instance,
                                                                            cassandra_username, cassandra_password):
        cp_id = prepared_cp_id()
        ei_token = str(uuid4())
        payload = copy.deepcopy(payload_ei_full_data_model)
        payload["tender"]["items"][0]["description"] = ""
        ei = EI(payload=payload, lang=language, country=country, instance=instance,
                cassandra_username=cassandra_username, cassandra_password=cassandra_password)
        ei.insert_ei_full_data_model(cp_id=cp_id, ei_token=ei_token)
        ei.update_ei(cp_id=cp_id, ei_token=ei_token)
        message_from_kafka = ei.get_message_from_kafka()
        actual_result = str(message_from_kafka["errors"])
        expected_result = str([{"code": "400.10.20.11",
                                "description": "Incorrect an attribute value.The attribute 'tender.items."
                                               "description' is empty or blank."}])
        assert compare_actual_result_and_expected_result(expected_result=expected_result,
                                                         actual_result=actual_result)