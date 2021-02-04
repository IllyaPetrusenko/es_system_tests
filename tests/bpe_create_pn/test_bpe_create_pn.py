import copy
import fnmatch
import json
import time
import uuid

import requests
from pytest_testrail.plugin import pytestrail

from tests.Cassandra_session import execute_cql_from_orchestrator_context
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id

from tests.bpe_create_pn.create_pn import bpe_create_pn_one_fs
from tests.bpe_create_pn.payloads import pn_create_full_data_model_with_documents, \
    pn_create_obligatory_data_model_with_documents, pn_create_obligatory_data_model_without_documents
from tests.cassandra_inserts_into_Database import insert_into_db_create_fs
from tests.kafka_messages import get_message_from_kafka
from tests.presets import set_instance_for_request, create_pn
from useful_functions import prepared_cpid, get_access_token_for_platform_two


class TestBpeCreatePN(object):
    # @pytestrail.case("27008")
    # def test_27008_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27008")
    # def test_27008_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert x_operation_id == True
    #     assert x_response_id == True
    #     assert initiator == True
    #     assert ocid == True
    #     assert url == True
    #     assert operation_date == True
    #     assert outcomes_pn_id == True
    #     assert outcomes_pn_token == True
    #
    # # You can delete these cases
    # # ================================
    # # @pytestrail.case("27010")
    # # def test_27010_1(self):
    # #     cpid = prepared_cpid()
    # #     payload = copy.deepcopy(pn_create_obligatory_data_model_with_documents)
    # #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, "MV")
    # #     assert create_pn_response[0].text == "ok"
    # #     assert create_pn_response[0].status_code == 202
    # #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    # #
    # # @pytestrail.case("27010")
    # # def test_27010_2(self):
    # #     cpid = prepared_cpid()
    # #     payload = copy.deepcopy(pn_create_obligatory_data_model_with_documents)
    # #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, "MV")
    # #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    # #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    # #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    # #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    # #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    # #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    # #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    # #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    # #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    # #     assert x_operation_id == True
    # #     assert x_response_id == True
    # #     assert initiator == True
    # #     assert ocid == True
    # #     assert url == True
    # #     assert operation_date == True
    # #     assert outcomes_pn_id == True
    # #     assert outcomes_pn_token == True
    # #
    # # @pytestrail.case("27011")
    # # def test_27011_1(self):
    # #     cpid = prepared_cpid()
    # #     payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
    # #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, "OT")
    # #     assert create_pn_response[0].text == "ok"
    # #     assert create_pn_response[0].status_code == 202
    # #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    # #
    # # @pytestrail.case("27011")
    # # def test_27011_2(self):
    # #     cpid = prepared_cpid()
    # #     payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
    # #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, "OT")
    # #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    # #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    # #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    # #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    # #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    # #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    # #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    # #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    # #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    # #     assert x_operation_id == True
    # #     assert x_response_id == True
    # #     assert initiator == True
    # #     assert ocid == True
    # #     assert url == True
    # #     assert operation_date == True
    # #     assert outcomes_pn_id == True
    # #     assert outcomes_pn_token == True
    # # ===========================================
    # @pytestrail.case("27009")
    # def test_27009_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["planning"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin." \
    #                                                                 "MissingKotlinParameterException: Instantiation " \
    #                                                                 "of [simple type, class com.procurement.budget." \
    #                                                                 "model.dto.check.CheckRq] value failed for JSON " \
    #                                                                 "property planning due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter planning " \
    #                                                                 "which is a non-nullable type\n at [Source: " \
    #                                                                 "UNKNOWN; line: -1, column: -1] (through " \
    #                                                                 "reference chain: com.procurement.budget.model." \
    #                                                                 "dto.check.CheckRq[\"planning\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["planning"]["budget"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.budget." \
    #                                                                 "model.dto.check.PlanningCheckRq] value failed " \
    #                                                                 "for JSON property budget due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "budget which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "budget.model.dto.check.CheckRq[\"planning\"]->" \
    #                                                                 "com.procurement.budget.model.dto.check." \
    #                                                                 "PlanningCheckRq[\"budget\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_3(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["planning"]["budget"]["budgetBreakdown"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.budget." \
    #                                                                 "model.dto.check.BudgetCheckRq] value failed " \
    #                                                                 "for JSON property budgetBreakdown due to " \
    #                                                                 "missing (therefore NULL) value for creator " \
    #                                                                 "parameter budgetBreakdown which is a non-" \
    #                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.budget.model.dto.check.CheckRq" \
    #                                                                 "[\"planning\"]->com.procurement.budget.model." \
    #                                                                 "dto.check.PlanningCheckRq[\"budget\"]->" \
    #                                                                 "com.procurement.budget.model.dto.check." \
    #                                                                 "BudgetCheckRq[\"budgetBreakdown\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_4(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["planning"]["budget"]["budgetBreakdown"][0]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.budget." \
    #                                                                 "model.dto.check.BudgetBreakdownCheckRq] value " \
    #                                                                 "failed for JSON property id due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "id which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "budget.model.dto.check.CheckRq[\"planning\"]->" \
    #                                                                 "com.procurement.budget.model.dto.check.Planning" \
    #                                                                 "CheckRq[\"budget\"]->com.procurement.budget." \
    #                                                                 "model.dto.check.BudgetCheckRq[\"budget" \
    #                                                                 "Breakdown\"]->java.util.ArrayList[0]->com." \
    #                                                                 "procurement.budget.model.dto.check.Budget" \
    #                                                                 "BreakdownCheckRq[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_5(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.budget." \
    #                                                                 "model.dto.check.BudgetBreakdownCheckRq] value " \
    #                                                                 "failed for JSON property amount due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "amount which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "budget.model.dto.check.CheckRq[\"planning\"]->" \
    #                                                                 "com.procurement.budget.model.dto.check." \
    #                                                                 "PlanningCheckRq[\"budget\"]->com.procurement." \
    #                                                                 "budget.model.dto.check.BudgetCheckRq[\"budget" \
    #                                                                 "Breakdown\"]->java.util.ArrayList[0]->com.p" \
    #                                                                 "rocurement.budget.model.dto.check.BudgetB" \
    #                                                                 "reakdownCheckRq[\"amount\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_6(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.budget." \
    #                                                                 "model.dto.check.CheckValue] value failed for " \
    #                                                                 "JSON property amount due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter amount which " \
    #                                                                 "is a non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference chain: " \
    #                                                                 "com.procurement.budget.model.dto.check.CheckRq" \
    #                                                                 "[\"planning\"]->com.procurement.budget.model." \
    #                                                                 "dto.check.PlanningCheckRq[\"budget\"]->com." \
    #                                                                 "procurement.budget.model.dto.check.Budget" \
    #                                                                 "CheckRq[\"budgetBreakdown\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.budget.model." \
    #                                                                 "dto.check.BudgetBreakdownCheckRq[\"amount\"]->" \
    #                                                                 "com.procurement.budget.model.dto.check." \
    #                                                                 "CheckValue[\"amount\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_7(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.budget." \
    #                                                                 "model.dto.check.CheckValue] value failed for " \
    #                                                                 "JSON property currency due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "currency which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "budget.model.dto.check.CheckRq[\"planning\"]->" \
    #                                                                 "com.procurement.budget.model.dto.check." \
    #                                                                 "PlanningCheckRq[\"budget\"]->com.procurement." \
    #                                                                 "budget.model.dto.check.BudgetCheckRq" \
    #                                                                 "[\"budgetBreakdown\"]->java.util.ArrayList[0]->" \
    #                                                                 "com.procurement.budget.model.dto.check.Budget" \
    #                                                                 "BreakdownCheckRq[\"amount\"]->com.procurement." \
    #                                                                 "budget.model.dto.check.CheckValue[\"currency\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_8(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.00.00.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "Data processing exception."
    #
    # @pytestrail.case("27009")
    # def test_27009_9(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["title"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender] value failed for " \
    #                                                                 "JSON property title due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter title which " \
    #                                                                 "is a non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference " \
    #                                                                 "chain: com.procurement.access.infrastructure." \
    #                                                                 "handler.v1.model.request.PnCreateRequest" \
    #                                                                 "[\"tender\"]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"title\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_10(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["description"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender] value failed for JSON " \
    #                                                                 "property description due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter description " \
    #                                                                 "which is a non-nullable type\n at [Source: " \
    #                                                                 "UNKNOWN; line: -1, column: -1] (through " \
    #                                                                 "reference chain: com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model." \
    #                                                                 "request.PnCreateRequest$Tender[\"description\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_11(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["legalBasis"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender] value failed for " \
    #                                                                 "JSON property legalBasis due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "legalBasis which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model." \
    #                                                                 "request.PnCreateRequest[\"tender\"]->com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest$Tender" \
    #                                                                 "[\"legalBasis\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_12(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["tenderPeriod"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender] value failed for JSON " \
    #                                                                 "property tenderPeriod due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter tenderPeriod " \
    #                                                                 "which is a non-nullable type\n at [Source: " \
    #                                                                 "UNKNOWN; line: -1, column: -1] (through " \
    #                                                                 "reference chain: com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model." \
    #                                                                 "request.PnCreateRequest$Tender[\"tenderPeriod\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_13(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["tenderPeriod"]["startDate"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$TenderPeriod] value " \
    #                                                                 "failed for JSON property startDate due to " \
    #                                                                 "missing (therefore NULL) value for creator " \
    #                                                                 "parameter startDate which is a non-nullable " \
    #                                                                 "type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest[\"tender\"]->" \
    #                                                                 "com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.PnCreateRequest$Tender" \
    #                                                                 "[\"tenderPeriod\"]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$TenderPeriod" \
    #                                                                 "[\"startDate\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_14(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender] value failed for JSON " \
    #                                                                 "property procuringEntity due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "procuringEntity which is a non-nullable " \
    #                                                                 "type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest[\"tender\"]->" \
    #                                                                 "com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.PnCreateRequest$Tender" \
    #                                                                 "[\"procuringEntity\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_15(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["name"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.PnCreate" \
    #                                                                 "Request$Tender$ProcuringEntity] value failed " \
    #                                                                 "for JSON property name due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "name which is a non-nullable type\n at [Source: " \
    #                                                                 "UNKNOWN; line: -1, column: -1] (through " \
    #                                                                 "reference chain: com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"procuringEntity\"]->" \
    #                                                                 "com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.PnCreateRequest$Tender$" \
    #                                                                 "ProcuringEntity[\"name\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_16(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["identifier"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$ProcuringEntity] value " \
    #                                                                 "failed for JSON property identifier due to " \
    #                                                                 "missing (therefore NULL) value for creator " \
    #                                                                 "parameter identifier which is a non-nullable " \
    #                                                                 "type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest[\"tender\"]->com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest$Tender" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$ProcuringEntity" \
    #                                                                 "[\"identifier\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_17(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["identifier"]["scheme"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.Identifier] value failed for JSON " \
    #                                                                 "property scheme due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter scheme which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference chain: " \
    #                                                                 "com.procurement.mdm.model.dto.data.TD" \
    #                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.Organization" \
    #                                                                 "Reference[\"identifier\"]->com.procurement." \
    #                                                                 "mdm.model.dto.data.Identifier[\"scheme\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_18(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["identifier"]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation " \
    #                                                                 "of [simple type, class com.procurement.mdm." \
    #                                                                 "model.dto.data.Identifier] value failed for " \
    #                                                                 "JSON property id due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter id which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference" \
    #                                                                 "[\"identifier\"]->com.procurement.mdm.model." \
    #                                                                 "dto.data.Identifier[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_19(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["identifier"]["legalName"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$ProcuringEntity$" \
    #                                                                 "Identifier] value failed for JSON property " \
    #                                                                 "legalName due to missing (therefore NULL) value " \
    #                                                                 "for creator parameter legalName which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest[\"tender\"]->com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest$Tender[\"procuring" \
    #                                                                 "Entity\"]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.PnCreate" \
    #                                                                 "Request$Tender$ProcuringEntity[\"identifier\"]->" \
    #                                                                 "com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.PnCreateRequest$Tender$" \
    #                                                                 "ProcuringEntity$Identifier[\"legalName\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_20(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.Identifier] value failed for JSON " \
    #                                                                 "property scheme due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter scheme which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference" \
    #                                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList" \
    #                                                                 "[0]->com.procurement.mdm.model.dto.data." \
    #                                                                 "Identifier[\"scheme\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_21(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.Identifier] value failed for JSON " \
    #                                                                 "property id due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter id which is a non-" \
    #                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference" \
    #                                                                 "[\"additionalIdentifiers\"]->java.util.ArrayList" \
    #                                                                 "[0]->com.procurement.mdm.model.dto.data." \
    #                                                                 "Identifier[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_22(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.PnCreate" \
    #                                                                 "Request$Tender$ProcuringEntity$Additional" \
    #                                                                 "Identifier] value failed for JSON property " \
    #                                                                 "legalName due to missing (therefore NULL) value " \
    #                                                                 "for creator parameter legalName which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest[\"tender\"]->com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest$Tender[\"procuring" \
    #                                                                 "Entity\"]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.PnCreate" \
    #                                                                 "Request$Tender$ProcuringEntity[\"additional" \
    #                                                                 "Identifiers\"]->java.util.ArrayList[0]->com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest$Tender$Procuring" \
    #                                                                 "Entity$AdditionalIdentifier[\"legalName\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_23(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.PnCreate" \
    #                                                                 "Request$Tender$ProcuringEntity] value failed " \
    #                                                                 "for JSON property address due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "address which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"procuringEntity\"]->" \
    #                                                                 "com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.PnCreateRequest$Tender$" \
    #                                                                 "ProcuringEntity[\"address\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_24(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]["streetAddress"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.Address] value failed for JSON " \
    #                                                                 "property streetAddress due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "streetAddress which is a non-nullable type\n " \
    #                                                                 "at [Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement.mdm." \
    #                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
    #                                                                 "mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference" \
    #                                                                 "[\"address\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.Address[\"streetAddress\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_25(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]["addressDetails"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin." \
    #                                                                 "MissingKotlinParameterException: Instantiation " \
    #                                                                 "of [simple type, class com.procurement.mdm." \
    #                                                                 "model.dto.data.Address] value failed for JSON " \
    #                                                                 "property addressDetails due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "addressDetails which is a non-nullable type\n " \
    #                                                                 "at [Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement.mdm." \
    #                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
    #                                                                 "mdm.model.dto.data.TenderTD[\"procuring" \
    #                                                                 "Entity\"]->com.procurement.mdm.model.dto.data." \
    #                                                                 "OrganizationReference[\"address\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.Address" \
    #                                                                 "[\"addressDetails\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_26(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.AddressDetails] value failed for JSON " \
    #                                                                 "property country due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter country which " \
    #                                                                 "is a non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference chain: " \
    #                                                                 "com.procurement.mdm.model.dto.data.TD" \
    #                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.Organization" \
    #                                                                 "Reference[\"address\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.Address[\"addressDetails\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.AddressDetails" \
    #                                                                 "[\"country\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_27(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.CountryDetails] value failed for JSON " \
    #                                                                 "property id due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter id which is a non-" \
    #                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference" \
    #                                                                 "[\"address\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.Address[\"addressDetails\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.AddressDetails" \
    #                                                                 "[\"country\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.CountryDetails[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_28(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.AddressDetails] value failed for JSON " \
    #                                                                 "property region due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter region which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference" \
    #                                                                 "[\"address\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.Address[\"addressDetails\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.Address" \
    #                                                                 "Details[\"region\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_29(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin." \
    #                                                                 "MissingKotlinParameterException: Instantiation " \
    #                                                                 "of [simple type, class com.procurement.mdm." \
    #                                                                 "model.dto.data.RegionDetails] value failed for " \
    #                                                                 "JSON property id due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter id which is " \
    #                                                                 "a non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference chain: " \
    #                                                                 "com.procurement.mdm.model.dto.data.TD" \
    #                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.TenderTD[\"procuringEntity\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.Organization" \
    #                                                                 "Reference[\"address\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.Address[\"addressDetails\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.Address" \
    #                                                                 "Details[\"region\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.RegionDetails[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_30(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.AddressDetails] value failed for " \
    #                                                                 "JSON property locality due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "locality which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement.mdm." \
    #                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
    #                                                                 "mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference" \
    #                                                                 "[\"address\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.Address[\"addressDetails\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.AddressDetails" \
    #                                                                 "[\"locality\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_31(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.LocalityDetails] value failed for JSON " \
    #                                                                 "property scheme due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter scheme which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference" \
    #                                                                 "[\"address\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.Address[\"addressDetails\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.AddressDetails" \
    #                                                                 "[\"locality\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.LocalityDetails[\"scheme\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_32(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.LocalityDetails] value failed for JSON " \
    #                                                                 "property id due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter id which is a non-" \
    #                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference" \
    #                                                                 "[\"address\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.Address[\"addressDetails\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.AddressDetails" \
    #                                                                 "[\"locality\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.LocalityDetails[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_33(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["description"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.LocalityDetails] value failed for " \
    #                                                                 "JSON property description due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "description which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement.mdm." \
    #                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
    #                                                                 "mdm.model.dto.data.TenderTD[\"procuring" \
    #                                                                 "Entity\"]->com.procurement.mdm.model.dto.data." \
    #                                                                 "OrganizationReference[\"address\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.Address" \
    #                                                                 "[\"addressDetails\"]->com.procurement.mdm.model." \
    #                                                                 "dto.data.AddressDetails[\"locality\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.LocalityDetails" \
    #                                                                 "[\"description\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_34(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["contactPoint"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Pn" \
    #                                                                 "CreateRequest$Tender$ProcuringEntity] value " \
    #                                                                 "failed for JSON property contactPoint due to " \
    #                                                                 "missing (therefore NULL) value for creator " \
    #                                                                 "parameter contactPoint which is a non-nullable " \
    #                                                                 "type\n at [Source: UNKNOWN; line: -1, column: " \
    #                                                                 "-1] (through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"procuringEntity\"]->" \
    #                                                                 "com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.PnCreateRequest$Tender$" \
    #                                                                 "ProcuringEntity[\"contactPoint\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_35(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["contactPoint"]["name"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.ContactPoint] value failed for JSON " \
    #                                                                 "property name due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter name which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference" \
    #                                                                 "[\"contactPoint\"]->com.procurement.mdm.model." \
    #                                                                 "dto.data.ContactPoint[\"name\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_36(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["contactPoint"]["email"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.ContactPoint] value failed for JSON " \
    #                                                                 "property email due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter email which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"procuringEntity\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.OrganizationReference[\"contact" \
    #                                                                 "Point\"]->com.procurement.mdm.model.dto.data." \
    #                                                                 "ContactPoint[\"email\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_37(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["procuringEntity"]["contactPoint"]["telephone"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.ContactPoint] value failed for JSON " \
    #                                                                 "property telephone due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter telephone " \
    #                                                                 "which is a non-nullable type\n at [Source: " \
    #                                                                 "UNKNOWN; line: -1, column: -1] (through " \
    #                                                                 "reference chain: com.procurement.mdm.model.dto." \
    #                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
    #                                                                 "dto.data.TenderTD[\"procuringEntity\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.Organization" \
    #                                                                 "Reference[\"contactPoint\"]->com.procurement." \
    #                                                                 "mdm.model.dto.data.ContactPoint[\"telephone\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_38(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.PnCreate" \
    #                                                                 "Request$Tender$Lot] value failed for JSON " \
    #                                                                 "property id due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter id which is a non-" \
    #                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest[\"tender\"]->com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest$Tender[\"lots\"]->" \
    #                                                                 "java.util.ArrayList[0]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.PnCreate" \
    #                                                                 "Request$Tender$Lot[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_39(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["title"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access.in" \
    #                                                                 "frastructure.handler.v1.model.request.PnCreate" \
    #                                                                 "Request$Tender$Lot] value failed for JSON " \
    #                                                                 "property title due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter title which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest[\"tender\"]->com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest$Tender[\"lots\"]" \
    #                                                                 "->java.util.ArrayList[0]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$Lot[\"title\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_40(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["description"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Pn" \
    #                                                                 "CreateRequest$Tender$Lot] value failed for " \
    #                                                                 "JSON property description due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "description which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"lots\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.access.in" \
    #                                                                 "frastructure.handler.v1.model.request.Pn" \
    #                                                                 "CreateRequest$Tender$Lot[\"description\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_41(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["value"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Pn" \
    #                                                                 "CreateRequest$Tender$Lot] value failed for " \
    #                                                                 "JSON property value due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter value which " \
    #                                                                 "is a non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference chain: " \
    #                                                                 "com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.PnCreateRequest[\"tender\"]->" \
    #                                                                 "com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.PnCreateRequest$Tender" \
    #                                                                 "[\"lots\"]->java.util.ArrayList[0]->com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.PnCreateRequest$Tender$Lot" \
    #                                                                 "[\"value\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_42(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["value"]["amount"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
    #                                                                 "Exception: Attribute 'amount' is an invalid " \
    #                                                                 "type 'NULL', the required type is number. " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"lots\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.access.in" \
    #                                                                 "frastructure.handler.v1.model.request.Pn" \
    #                                                                 "CreateRequest$Tender$Lot[\"value\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_43(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["value"]["currency"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
    #                                                                 "Exception: Attribute 'currency' is an invalid " \
    #                                                                 "type 'NULL', the required type is text. " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"lots\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Pn" \
    #                                                                 "CreateRequest$Tender$Lot[\"value\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_44(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["contractPeriod"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Pn" \
    #                                                                 "CreateRequest$Tender$Lot] value failed for " \
    #                                                                 "JSON property contractPeriod due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "contractPeriod which is a non-nullable type\n " \
    #                                                                 "at [Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"lots\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$Lot[\"contractPeriod\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_45(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["contractPeriod"]["startDate"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Pn" \
    #                                                                 "CreateRequest$Tender$Lot$ContractPeriod] value " \
    #                                                                 "failed for JSON property startDate due to " \
    #                                                                 "missing (therefore NULL) value for creator " \
    #                                                                 "parameter startDate which is a non-nullable " \
    #                                                                 "type\n at [Source: UNKNOWN; line: -1, column: " \
    #                                                                 "-1] (through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"lots\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$Lot[\"contractPeriod\"]" \
    #                                                                 "->com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.PnCreateRequest$Tender$Lot$" \
    #                                                                 "ContractPeriod[\"startDate\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_46(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["contractPeriod"]["endDate"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$Lot$ContractPeriod] " \
    #                                                                 "value failed for JSON property endDate due " \
    #                                                                 "to missing (therefore NULL) value for creator " \
    #                                                                 "parameter endDate which is a non-nullable " \
    #                                                                 "type\n at [Source: UNKNOWN; line: -1, column: " \
    #                                                                 "-1] (through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"lots\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.access.in" \
    #                                                                 "frastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$Lot[\"contractPeriod\"]" \
    #                                                                 "->com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.PnCreateRequest$Tender$Lot$" \
    #                                                                 "ContractPeriod[\"endDate\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_47(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.PnCreate" \
    #                                                                 "Request$Tender$Lot] value failed for JSON " \
    #                                                                 "property placeOfPerformance due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "placeOfPerformance which is a non-nullable " \
    #                                                                 "type\n at [Source: UNKNOWN; line: -1, column:" \
    #                                                                 " -1] (through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"lots\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.access.infrastruc" \
    #                                                                 "ture.handler.v1.model.request.PnCreateRequest$" \
    #                                                                 "Tender$Lot[\"placeOfPerformance\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_48(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.PlaceOfPerformance] value failed for " \
    #                                                                 "JSON property address due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter address which " \
    #                                                                 "is a non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference chain:" \
    #                                                                 " com.procurement.mdm.model.dto.data.TD" \
    #                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
    #                                                                 "->com.procurement.mdm.model.dto.data.LotTD" \
    #                                                                 "[\"placeOfPerformance\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.PlaceOfPerformance[\"address\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_49(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin." \
    #                                                                 "MissingKotlinParameterException: Instantiation " \
    #                                                                 "of [simple type, class com.procurement.mdm." \
    #                                                                 "model.dto.data.Address] value failed for JSON " \
    #                                                                 "property streetAddress due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "streetAddress which is a non-nullable type\n " \
    #                                                                 "at [Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement.mdm." \
    #                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
    #                                                                 "mdm.model.dto.data.TenderTD[\"lots\"]->java." \
    #                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
    #                                                                 "dto.data.LotTD[\"placeOfPerformance\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.PlaceOf" \
    #                                                                 "Performance[\"address\"]->com.procurement." \
    #                                                                 "mdm.model.dto.data.Address[\"streetAddress\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_50(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.Address] value failed for JSON " \
    #                                                                 "property addressDetails due to missing (there" \
    #                                                                 "fore NULL) value for creator parameter address" \
    #                                                                 "Details which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement.mdm." \
    #                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
    #                                                                 "mdm.model.dto.data.TenderTD[\"lots\"]->java." \
    #                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
    #                                                                 "dto.data.LotTD[\"placeOfPerformance\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.PlaceOfPer" \
    #                                                                 "formance[\"address\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.Address[\"addressDetails\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_51(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.AddressDetails] value failed for JSON " \
    #                                                                 "property country due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter country which " \
    #                                                                 "is a non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference chain: " \
    #                                                                 "com.procurement.mdm.model.dto.data.TD" \
    #                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
    #                                                                 "->com.procurement.mdm.model.dto.data.LotTD" \
    #                                                                 "[\"placeOfPerformance\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.PlaceOfPerformance[\"address\"]" \
    #                                                                 "->com.procurement.mdm.model.dto.data.Address" \
    #                                                                 "[\"addressDetails\"]->com.procurement.mdm.model." \
    #                                                                 "dto.data.AddressDetails[\"country\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_52(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.CountryDetails] value failed for JSON " \
    #                                                                 "property id due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter id which is a non-" \
    #                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"lots\"]->java.util.ArrayList[0]->com." \
    #                                                                 "procurement.mdm.model.dto.data.LotTD[\"placeOf" \
    #                                                                 "Performance\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.PlaceOfPerformance[\"address\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.Address" \
    #                                                                 "[\"addressDetails\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.AddressDetails[\"country\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data." \
    #                                                                 "CountryDetails[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_53(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.AddressDetails] value failed for JSON " \
    #                                                                 "property region due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter region which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: " \
    #                                                                 "com.procurement.mdm.model.dto.data.TD" \
    #                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList[0]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.LotTD" \
    #                                                                 "[\"placeOfPerformance\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.PlaceOfPerformance[\"address\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.Address" \
    #                                                                 "[\"addressDetails\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.AddressDetails[\"region\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_54(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.RegionDetails] value failed for JSON " \
    #                                                                 "property id due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter id which is a non-" \
    #                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"lots\"]->java.util.ArrayList[0]->com." \
    #                                                                 "procurement.mdm.model.dto.data.LotTD[\"place" \
    #                                                                 "OfPerformance\"]->com.procurement.mdm.model." \
    #                                                                 "dto.data.PlaceOfPerformance[\"address\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.Address" \
    #                                                                 "[\"addressDetails\"]->com.procurement.mdm.model." \
    #                                                                 "dto.data.AddressDetails[\"region\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.RegionDetails" \
    #                                                                 "[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_55(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.AddressDetails] value failed for JSON " \
    #                                                                 "property locality due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter locality " \
    #                                                                 "which is a non-nullable type\n at [Source: " \
    #                                                                 "UNKNOWN; line: -1, column: -1] (through " \
    #                                                                 "reference chain: com.procurement.mdm.model.dto." \
    #                                                                 "data.TD[\"tender\"]->com.procurement.mdm.model." \
    #                                                                 "dto.data.TenderTD[\"lots\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
    #                                                                 "data.LotTD[\"placeOfPerformance\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.PlaceOfPer" \
    #                                                                 "formance[\"address\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.Address[\"addressDetails\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data." \
    #                                                                 "AddressDetails[\"locality\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_56(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.LocalityDetails] value failed for " \
    #                                                                 "JSON property scheme due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter scheme which " \
    #                                                                 "is a non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference " \
    #                                                                 "chain: com.procurement.mdm.model.dto.data." \
    #                                                                 "TD[\"tender\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList" \
    #                                                                 "[0]->com.procurement.mdm.model.dto.data.LotTD" \
    #                                                                 "[\"placeOfPerformance\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.PlaceOfPerformance[\"address\"]" \
    #                                                                 "->com.procurement.mdm.model.dto.data.Address" \
    #                                                                 "[\"addressDetails\"]->com.procurement.mdm.model." \
    #                                                                 "dto.data.AddressDetails[\"locality\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.Locality" \
    #                                                                 "Details[\"scheme\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_57(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.LocalityDetails] value failed for " \
    #                                                                 "JSON property id due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter id which " \
    #                                                                 "is a non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference chain: " \
    #                                                                 "com.procurement.mdm.model.dto.data.TD" \
    #                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
    #                                                                 "->com.procurement.mdm.model.dto.data.LotTD" \
    #                                                                 "[\"placeOfPerformance\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.PlaceOfPerformance[\"address\"]" \
    #                                                                 "->com.procurement.mdm.model.dto.data.Address" \
    #                                                                 "[\"addressDetails\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.AddressDetails[\"locality\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.Locality" \
    #                                                                 "Details[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_58(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["description"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm." \
    #                                                                 "model.dto.data.LocalityDetails] value failed " \
    #                                                                 "for JSON property description due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "description which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement.mdm." \
    #                                                                 "model.dto.data.TD[\"tender\"]->com.procurement." \
    #                                                                 "mdm.model.dto.data.TenderTD[\"lots\"]->java." \
    #                                                                 "util.ArrayList[0]->com.procurement.mdm.model." \
    #                                                                 "dto.data.LotTD[\"placeOfPerformance\"]->com." \
    #                                                                 "procurement.mdm.model.dto.data.PlaceOf" \
    #                                                                 "Performance[\"address\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.Address[\"addressDetails\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.Address" \
    #                                                                 "Details[\"locality\"]->com.procurement.mdm." \
    #                                                                 "model.dto.data.LocalityDetails[\"description\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_59(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["items"][0]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "CheckItemsRequest$Item] value failed for JSON " \
    #                                                                 "property id due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter id which is a non-" \
    #                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.access.infrastructure.handler.v1." \
    #                                                                 "model.request.CheckItemsRequest[\"items\"]->" \
    #                                                                 "java.util.ArrayList[0]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Check" \
    #                                                                 "ItemsRequest$Item[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_60(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["items"][0]["classification"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Check" \
    #                                                                 "ItemsRequest$Item] value failed for JSON " \
    #                                                                 "property classification due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "classification which is a non-nullable type\n " \
    #                                                                 "at [Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "CheckItemsRequest[\"items\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Check" \
    #                                                                 "ItemsRequest$Item[\"classification\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_61(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["items"][0]["classification"]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "CheckItemsRequest$Item$Classification] value " \
    #                                                                 "failed for JSON property id due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "id which is a non-nullable type\n at [Source: " \
    #                                                                 "UNKNOWN; line: -1, column: -1] (through " \
    #                                                                 "reference chain: com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "CheckItemsRequest[\"items\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "CheckItemsRequest$Item[\"classification\"]->" \
    #                                                                 "com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.CheckItemsRequest$Item$" \
    #                                                                 "Classification[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_62(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.ClassificationTD] value failed for " \
    #                                                                 "JSON property id due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter id which is " \
    #                                                                 "a non-nullable type\n at [Source: UNKNOWN; " \
    #                                                                 "line: -1, column: -1] (through reference chain: " \
    #                                                                 "com.procurement.mdm.model.dto.data.TD" \
    #                                                                 "[\"tender\"]->com.procurement.mdm.model.dto." \
    #                                                                 "data.TenderTD[\"items\"]->java.util.ArrayList" \
    #                                                                 "[0]->com.procurement.mdm.model.dto.data.ItemTD" \
    #                                                                 "[\"additionalClassifications\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.mdm.model.dto." \
    #                                                                 "data.ClassificationTD[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_63(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["items"][0]["quantity"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.ItemTD] value failed for JSON property " \
    #                                                                 "quantity due to missing (therefore NULL) value " \
    #                                                                 "for creator parameter quantity which is a non-" \
    #                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"items\"]->java.util.ArrayList[0]->com." \
    #                                                                 "procurement.mdm.model.dto.data.ItemTD" \
    #                                                                 "[\"quantity\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_64(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["items"][0]["unit"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin." \
    #                                                                 "MissingKotlinParameterException: Instantiation " \
    #                                                                 "of [simple type, class com.procurement.mdm." \
    #                                                                 "model.dto.data.ItemTD] value failed for JSON " \
    #                                                                 "property unit due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter unit which is a non-" \
    #                                                                 "nullable type\n at [Source: UNKNOWN; line: -1, " \
    #                                                                 "column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
    #                                                                 "com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"items\"]->java.util.ArrayList[0]->com." \
    #                                                                 "procurement.mdm.model.dto.data.ItemTD[\"unit\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_65(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["items"][0]["unit"]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.mdm.model." \
    #                                                                 "dto.data.ItemUnitTD] value failed for JSON " \
    #                                                                 "property id due to missing (therefore NULL) " \
    #                                                                 "value for creator parameter id which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.mdm.model.dto.data.TD[\"tender\"]" \
    #                                                                 "->com.procurement.mdm.model.dto.data.TenderTD" \
    #                                                                 "[\"items\"]->java.util.ArrayList[0]->com." \
    #                                                                 "procurement.mdm.model.dto.data.ItemTD[\"unit\"]" \
    #                                                                 "->com.procurement.mdm.model.dto.data.ItemUnitTD" \
    #                                                                 "[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_66(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["items"][0]["description"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$Item] value failed for " \
    #                                                                 "JSON property description due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "description which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"items\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.PnCreate" \
    #                                                                 "Request$Tender$Item[\"description\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_67(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["items"][0]["relatedLot"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "CheckItemsRequest$Item] value failed for JSON " \
    #                                                                 "property relatedLot due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter relatedLot " \
    #                                                                 "which is a non-nullable type\n at [Source: " \
    #                                                                 "UNKNOWN; line: -1, column: -1] (through " \
    #                                                                 "reference chain: com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Check" \
    #                                                                 "ItemsRequest[\"items\"]->java.util.ArrayList[0]" \
    #                                                                 "->com.procurement.access.infrastructure.handler." \
    #                                                                 "v1.model.request.CheckItemsRequest$Item" \
    #                                                                 "[\"relatedLot\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_68(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["documents"][0]["documentType"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$Document] value failed " \
    #                                                                 "for JSON property documentType due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "documentType which is a non-nullable type\n " \
    #                                                                 "at [Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender[\"documents\"]->java." \
    #                                                                 "util.ArrayList[0]->com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$Document[\"documentType\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_69(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["documents"][0]["id"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "500.14.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.storage." \
    #                                                                 "model.dto.registration.Document] value failed " \
    #                                                                 "for JSON property id due to missing (therefore " \
    #                                                                 "NULL) value for creator parameter id which is a " \
    #                                                                 "non-nullable type\n at [Source: UNKNOWN; line: " \
    #                                                                 "-1, column: -1] (through reference chain: com." \
    #                                                                 "procurement.storage.model.dto.registration." \
    #                                                                 "DocumentsRq[\"documents\"]->java.util." \
    #                                                                 "ArrayList[0]->com.procurement.storage.model." \
    #                                                                 "dto.registration.Document[\"id\"])"
    #
    # @pytestrail.case("27009")
    # def test_27009_70(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     del payload["tender"]["documents"][0]["title"]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
    #     assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
    #                                                                 "KotlinParameterException: Instantiation of " \
    #                                                                 "[simple type, class com.procurement.access." \
    #                                                                 "infrastructure.handler.v1.model.request.Pn" \
    #                                                                 "CreateRequest$Tender$Document] value failed " \
    #                                                                 "for JSON property title due to missing " \
    #                                                                 "(therefore NULL) value for creator parameter " \
    #                                                                 "title which is a non-nullable type\n at " \
    #                                                                 "[Source: UNKNOWN; line: -1, column: -1] " \
    #                                                                 "(through reference chain: com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest[\"tender\"]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model." \
    #                                                                 "request.PnCreateRequest$Tender[\"documents\"]" \
    #                                                                 "->java.util.ArrayList[0]->com.procurement." \
    #                                                                 "access.infrastructure.handler.v1.model.request." \
    #                                                                 "PnCreateRequest$Tender$Document[\"title\"])"
    #
    # @pytestrail.case("27013")
    # def test_27013_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     access_token = get_access_token_for_platform_two()
    #     x_operation_id = get_x_operation_id(access_token)
    #     access_token = "ZZZ"
    #     time.sleep(2)
    #     test_create_fs = insert_into_db_create_fs(cpid)
    #     payload["planning"]["budget"]["budgetBreakdown"][0]["id"] = test_create_fs[2]
    #     host = set_instance_for_request()
    #     request_to_create_pn = requests.post(
    #         url=host + create_pn,
    #         headers={
    #             'Authorization': 'Bearer ' + access_token,
    #             'X-OPERATION-ID': x_operation_id,
    #             'Content-Type': 'application/json'},
    #         params={"country": "MD", "pmd": additional_value},
    #         json=payload)
    #     time.sleep(2)
    #     dict = json.loads(request_to_create_pn.text.replace("'", '"'))
    #     assert request_to_create_pn.status_code == 401
    #     assert dict["errors"][0]["code"] == "401.81.03.04"
    #     assert dict["errors"][0]["description"] == "The error of verification of the authentication token."
    #
    # @pytestrail.case("27014")
    # def test_27014_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["documents"][0]["id"] = str(uuid.uuid4())
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #
    # @pytestrail.case("27014")
    # def test_27014_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["documents"][0]["id"] = str(uuid.uuid4())
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.14.00.14"
    #     assert create_pn_response[1]["errors"][0][
    #                "description"] == f"Files not found: [{payload['tender']['documents'][0]['id']}]"

    # @pytestrail.case("27015")
    # def test_27015_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27015")
    # def test_27015_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert x_operation_id == True
    #     assert x_response_id == True
    #     assert initiator == True
    #     assert ocid == True
    #     assert url == True
    #     assert operation_date == True
    #     assert outcomes_pn_id == True
    #     assert outcomes_pn_token == True
    #
    # @pytestrail.case("27015")
    # def test_27015_3(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     language = execute_cql_from_orchestrator_context(cpid)["language"]
    #     print(language)
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert language == "ro"

    # @pytestrail.case("27016")
    # def test_27016_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "24200000-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27016")
    # def test_27016_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "24200000-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.53"
    #     assert create_pn_response[1]["errors"][0][
    #                "description"] == "CPV codes of all items must have minimum 3 the same starting symbols."

    # @pytestrail.case("27017")
    # def test_27017_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27017")
    # def test_27017_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert x_operation_id == True
    #     assert x_response_id == True
    #     assert initiator == True
    #     assert ocid == True
    #     assert url == True
    #     assert operation_date == True
    #     assert outcomes_pn_id == True
    #     assert outcomes_pn_token == True
    #
    # @pytestrail.case("27017")
    # def test_27017_3(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":
    #         planning_notice = requests.get(
    #             url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert planning_notice["releases"][0]["tender"]["classification"]["id"] == "45112300-8"
    #     else:
    #         print("Check the url")
    #
    # @pytestrail.case("27018")
    # def test_27018_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27018")
    # def test_27018_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert x_operation_id == True
    #     assert x_response_id == True
    #     assert initiator == True
    #     assert ocid == True
    #     assert url == True
    #     assert operation_date == True
    #     assert outcomes_pn_id == True
    #     assert outcomes_pn_token == True
    #
    # @pytestrail.case("27018")
    # def test_27018_3(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":
    #         planning_notice = requests.get(
    #             url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert planning_notice["releases"][0]["tender"]["classification"]["id"] == "45112300-8"
    #         assert planning_notice["releases"][0]["tender"]["classification"]["scheme"] == "CPV"
    #         assert planning_notice["releases"][0]["tender"]["classification"][
    #                    "description"] == "Lucrări de rambleiere şi de asanare a terenului"
    #     else:
    #         print("Check url")
    #
    # @pytestrail.case("27019")
    # def test_27019_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27019")
    # def test_27019_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert x_operation_id == True
    #     assert x_response_id == True
    #     assert initiator == True
    #     assert ocid == True
    #     assert url == True
    #     assert operation_date == True
    #     assert outcomes_pn_id == True
    #     assert outcomes_pn_token == True
    #
    # @pytestrail.case("27019")
    # def test_27019_3(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent":
    #         multistage = requests.get(
    #             url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert multistage["releases"][0]["tender"]["mainProcurementCategory"] == "works"
    #     else:
    #         print("Check url")
    #
    # @pytestrail.case("27020")
    # def test_27020_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["additionalClassifications"] = [
    #         {"id": "AA12-4"},
    #         {"id": "AA01-1"}
    #     ]
    #
    #     payload["tender"]["items"][1]["additionalClassifications"] = [
    #         {"id": "AA12-4"},
    #         {"id": "AA01-1"}
    #     ]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27020")
    # def test_27020_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["additionalClassifications"] = [
    #         {"id": "AA12-4"},
    #         {"id": "AA01-1"}
    #     ]
    #
    #     payload["tender"]["items"][1]["additionalClassifications"] = [
    #         {"id": "AA12-4"},
    #         {"id": "AA01-1"}
    #     ]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert x_operation_id == True
    #     assert x_response_id == True
    #     assert initiator == True
    #     assert ocid == True
    #     assert url == True
    #     assert operation_date == True
    #     assert outcomes_pn_id == True
    #     assert outcomes_pn_token == True
    #
    # @pytestrail.case("27020")
    # def test_27020_3(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["additionalClassifications"] = [
    #         {"id": "AA12-4"},
    #         {"id": "AA01-1"}
    #     ]
    #
    #     payload["tender"]["items"][1]["additionalClassifications"] = [
    #         {"id": "AA12-4"},
    #         {"id": "AA01-1"}
    #     ]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":
    #         planning_notice = requests.get(
    #             url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
    #                    "scheme"] == "CPVS"
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"] == \
    #                payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
    #                    "description"] == "Oţel carbon"
    #
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][1][
    #                    "scheme"] == "CPVS"
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][1]["id"] == \
    #                payload["tender"]["items"][0]["additionalClassifications"][1]["id"]
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][1][
    #                    "description"] == "Metal"
    #     else:
    #         print("Check url")
    #
    # @pytestrail.case("27020")
    # def test_27020_4(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["additionalClassifications"] = [
    #         {"id": "AA12-4"},
    #         {"id": "AA01-1"}
    #     ]
    #
    #     payload["tender"]["items"][1]["additionalClassifications"] = [
    #         {"id": "AA12-4"},
    #         {"id": "AA01-1"}
    #     ]
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":
    #         planning_notice = requests.get(
    #             url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][0][
    #                    "scheme"] == "CPVS"
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][0]["id"] == \
    #                payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][0][
    #                    "description"] == "Oţel carbon"
    #
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][1][
    #                    "scheme"] == "CPVS"
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][1]["id"] == \
    #                payload["tender"]["items"][0]["additionalClassifications"][1]["id"]
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][1][
    #                    "description"] == "Metal"
    #     else:
    #         print("Check url")
    #
    # @pytestrail.case("27021")
    # def test_27021_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27021")
    # def test_27021_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert x_operation_id == True
    #     assert x_response_id == True
    #     assert initiator == True
    #     assert ocid == True
    #     assert url == True
    #     assert operation_date == True
    #     assert outcomes_pn_id == True
    #     assert outcomes_pn_token == True
    #
    # @pytestrail.case("27021")
    # def test_27021_3(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":
    #
    #         planning_notice = requests.get(
    #             url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["classification"]["scheme"] == "CPV"
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["classification"]["id"] == \
    #                payload["tender"]["items"][0]["classification"]["id"]
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["classification"][
    #                    "description"] == "Lucrări de valorificare a terenurilor virane"
    #     else:
    #         print("Check url")
    #
    # @pytestrail.case("27021")
    # def test_27021_4(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
    #     payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":
    #         planning_notice = requests.get(
    #             url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["classification"]["scheme"] == "CPV"
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["classification"]["id"] == \
    #                payload["tender"]["items"][1]["classification"]["id"]
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["classification"][
    #                    "description"] == "Lucrări de reabilitare a terenului"
    #     else:
    #         print("Check url")

    # @pytestrail.case("27022")
    # def test_27022_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["unit"]["id"] = "10"
    #     payload["tender"]["items"][1]["unit"]["id"] = "120"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27022")
    # def test_27022_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["unit"]["id"] = "10"
    #     payload["tender"]["items"][1]["unit"]["id"] = "120"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert x_operation_id == True
    #     assert x_response_id == True
    #     assert initiator == True
    #     assert ocid == True
    #     assert url == True
    #     assert operation_date == True
    #     assert outcomes_pn_id == True
    #     assert outcomes_pn_token == True
    #
    # @pytestrail.case("27022")
    # def test_27022_3(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["unit"]["id"] = "10"
    #     payload["tender"]["items"][1]["unit"]["id"] = "120"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":
    #
    #         planning_notice = requests.get(
    #             url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["unit"]["id"] == \
    #                payload["tender"]["items"][0]["unit"]["id"]
    #         assert planning_notice["releases"][0]["tender"]["items"][0]["unit"]["name"] == "Parsec"
    #     else:
    #         print("Check url")
    #
    # @pytestrail.case("27022")
    # def test_27022_4(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["items"][0]["unit"]["id"] = "10"
    #     payload["tender"]["items"][1]["unit"]["id"] = "120"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":
    #         planning_notice = requests.get(
    #             url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["unit"]["id"] == \
    #                payload["tender"]["items"][1]["unit"]["id"]
    #         assert planning_notice["releases"][0]["tender"]["items"][1]["unit"]["name"] == "Milion decalitri"
    #     else:
    #         print("Check url")

    # @pytestrail.case("27023")
    # def test_27023_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"] = "MD"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27023")
    # def test_27023_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"] = "MD"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert x_operation_id == True
    #     assert x_response_id == True
    #     assert initiator == True
    #     assert ocid == True
    #     assert url == True
    #     assert operation_date == True
    #     assert outcomes_pn_id == True
    #     assert outcomes_pn_token == True
    #
    # @pytestrail.case("27023")
    # def test_27023_3(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"] = "MD"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":
    #
    #         planning_notice = requests.get(
    #             url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert \
    #             planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
    #                 "country"]["id"] == \
    #             payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"]
    #
    #         assert \
    #             planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
    #                 "country"]["scheme"] == "iso-alpha2"
    #         assert \
    #             planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
    #                 "country"]["description"] == "Moldova, Republica"
    #         assert \
    #             planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
    #                 "country"]["uri"] == "https://www.iso.org"
    #
    #     else:
    #         print("Check url")

    # @pytestrail.case("27024")
    # def test_27024_1(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = "3400000"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27024")
    # def test_27024_2(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = "3400000"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
    #     x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
    #     initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
    #     ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
    #     url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
    #     operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
    #     outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
    #     outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #     assert x_operation_id == True
    #     assert x_response_id == True
    #     assert initiator == True
    #     assert ocid == True
    #     assert url == True
    #     assert operation_date == True
    #     assert outcomes_pn_id == True
    #     assert outcomes_pn_token == True
    #
    # @pytestrail.case("27024")
    # def test_27024_3(self, additional_value):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = "3400000"
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":
    #
    #         planning_notice = requests.get(
    #             url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #         assert \
    #             planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
    #                 "region"]["id"] == \
    #             payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"]
    #
    #         assert \
    #             planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
    #                 "region"]["scheme"] == "CUATM"
    #         assert \
    #             planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
    #                 "region"]["description"] == "Donduşeni"
    #         assert \
    #             planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
    #                 "region"]["uri"] == "http://statistica.md"
    #
    #     else:
    #         print("Check url")

    @pytestrail.case("27025")
    def test_27025_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27025")
    def test_27025_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True

    @pytestrail.case("27025")
    def test_27025_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"] = "CUATM"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        if get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning":

            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "locality"]["id"] == \
                payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"]

            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "locality"]["scheme"] == \
                payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"]
            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "locality"]["description"] == "or.Donduşeni (r-l Donduşeni)"
            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "locality"]["uri"] == "http://statistica.md"

        else:
            print("Check url")
