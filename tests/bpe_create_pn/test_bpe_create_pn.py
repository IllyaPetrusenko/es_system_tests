import copy
import fnmatch
import json
import time
import uuid

import requests
from pytest_testrail.plugin import pytestrail

from tests.Cassandra_session import execute_cql_from_orchestrator_context
from tests.TestRail_set_status_case import client
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id

from tests.bpe_create_pn.create_pn import bpe_create_pn_one_fs, bpe_create_pn_two_fs
from tests.bpe_create_pn.payloads import pn_create_full_data_model_with_documents, \
    pn_create_obligatory_data_model_with_documents, pn_create_obligatory_data_model_without_documents
from tests.cassandra_inserts_into_Database import insert_into_db_create_fs
from tests.kafka_messages import get_message_from_kafka
from tests.presets import set_instance_for_request, create_pn
from useful_functions import prepared_cpid, get_access_token_for_platform_two

procurement_method_details = {
    "SV": "smallValue",
    "MV": "microValue",
    "OT": "openTender"
}

procurement_method_rationale = {
    "SV": "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice",
    "MV": "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice",
    "OT": "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"
}

submission_method_details = {
    "SV": "Lista platformelor: achizitii, ebs, licitatie, yptender",
    "MV": "Lista platformelor: achizitii, ebs, licitatie, yptender",
    "OT": "Lista platformelor: achizitii, ebs, licitatie, yptender"
}

eligibility_criteria = {
    "SV": "Regulile generale privind naționalitatea și originea, precum și alte criterii de eligibilitate sunt "
          "enumerate în Ghidul practic privind procedurile de contractare a acțiunilor externe ale UE (PRAG)",
    "MV": "Regulile generale privind naționalitatea și originea, precum și alte criterii de eligibilitate sunt "
          "enumerate în Ghidul practic privind procedurile de contractare a acțiunilor externe ale UE (PRAG)",
    "OT": "Regulile generale privind naționalitatea și originea, precum și alte criterii de eligibilitate sunt "
          "enumerate în Ghidul practic privind procedurile de contractare a acțiunilor externe ale UE (PRAG)"
}


class TestBpeCreatePN(object):
    @pytestrail.case("27008")
    def test_27008_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27008")
    def test_27008_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
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

    # You can delete these cases
    # ================================
    # @pytestrail.case("27010")
    # def test_27010_1(self):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_obligatory_data_model_with_documents)
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, "MV")
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27010")
    # def test_27010_2(self):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_obligatory_data_model_with_documents)
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, "MV")
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
    # @pytestrail.case("27011")
    # def test_27011_1(self):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, "OT")
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #     assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
    #
    # @pytestrail.case("27011")
    # def test_27011_2(self):
    #     cpid = prepared_cpid()
    #     payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
    #     create_pn_response = bpe_create_pn_one_fs(cpid, payload, "OT")
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
    # ===========================================
    @pytestrail.case("27009")
    def test_27009_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["planning"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin." \
                                                                    "MissingKotlinParameterException: Instantiation " \
                                                                    "of [simple type, class com.procurement.budget." \
                                                                    "model.dto.check.CheckRq] value failed for JSON " \
                                                                    "property planning due to missing (therefore " \
                                                                    "NULL) value for creator parameter planning " \
                                                                    "which is a non-nullable type\n at [Source: " \
                                                                    "UNKNOWN; line: -1, column: -1] (through " \
                                                                    "reference chain: com.procurement.budget.model." \
                                                                    "dto.check.CheckRq[\"planning\"])"

    @pytestrail.case("27009")
    def test_27009_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["planning"]["budget"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.budget." \
                                                                    "model.dto.check.PlanningCheckRq] value failed " \
                                                                    "for JSON property budget due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "budget which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "budget.model.dto.check.CheckRq[\"planning\"]->" \
                                                                    "com.procurement.budget.model.dto.check." \
                                                                    "PlanningCheckRq[\"budget\"])"

    @pytestrail.case("27009")
    def test_27009_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["planning"]["budget"]["budgetBreakdown"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.budget." \
                                                                    "model.dto.check.BudgetCheckRq] value failed " \
                                                                    "for JSON property budgetBreakdown due to " \
                                                                    "missing (therefore NULL) value for creator " \
                                                                    "parameter budgetBreakdown which is a non-" \
                                                                    "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.budget.model.dto.check.CheckRq" \
                                                                    "[\"planning\"]->com.procurement.budget.model." \
                                                                    "dto.check.PlanningCheckRq[\"budget\"]->" \
                                                                    "com.procurement.budget.model.dto.check." \
                                                                    "BudgetCheckRq[\"budgetBreakdown\"])"

    @pytestrail.case("27009")
    def test_27009_4(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["planning"]["budget"]["budgetBreakdown"][0]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.budget." \
                                                                    "model.dto.check.BudgetBreakdownCheckRq] value " \
                                                                    "failed for JSON property id due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "id which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "budget.model.dto.check.CheckRq[\"planning\"]->" \
                                                                    "com.procurement.budget.model.dto.check.Planning" \
                                                                    "CheckRq[\"budget\"]->com.procurement.budget." \
                                                                    "model.dto.check.BudgetCheckRq[\"budget" \
                                                                    "Breakdown\"]->java.util.ArrayList[0]->com." \
                                                                    "procurement.budget.model.dto.check.Budget" \
                                                                    "BreakdownCheckRq[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_5(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.budget." \
                                                                    "model.dto.check.BudgetBreakdownCheckRq] value " \
                                                                    "failed for JSON property amount due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "amount which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "budget.model.dto.check.CheckRq[\"planning\"]->" \
                                                                    "com.procurement.budget.model.dto.check." \
                                                                    "PlanningCheckRq[\"budget\"]->com.procurement." \
                                                                    "budget.model.dto.check.BudgetCheckRq[\"budget" \
                                                                    "Breakdown\"]->java.util.ArrayList[0]->com.p" \
                                                                    "rocurement.budget.model.dto.check.BudgetB" \
                                                                    "reakdownCheckRq[\"amount\"])"

    @pytestrail.case("27009")
    def test_27009_6(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.budget." \
                                                                    "model.dto.check.CheckValue] value failed for " \
                                                                    "JSON property amount due to missing (therefore " \
                                                                    "NULL) value for creator parameter amount which " \
                                                                    "is a non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference chain: " \
                                                                    "com.procurement.budget.model.dto.check.CheckRq" \
                                                                    "[\"planning\"]->com.procurement.budget.model." \
                                                                    "dto.check.PlanningCheckRq[\"budget\"]->com." \
                                                                    "procurement.budget.model.dto.check.Budget" \
                                                                    "CheckRq[\"budgetBreakdown\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.budget.model." \
                                                                    "dto.check.BudgetBreakdownCheckRq[\"amount\"]->" \
                                                                    "com.procurement.budget.model.dto.check." \
                                                                    "CheckValue[\"amount\"])"

    @pytestrail.case("27009")
    def test_27009_7(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.budget." \
                                                                    "model.dto.check.CheckValue] value failed for " \
                                                                    "JSON property currency due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "currency which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "budget.model.dto.check.CheckRq[\"planning\"]->" \
                                                                    "com.procurement.budget.model.dto.check." \
                                                                    "PlanningCheckRq[\"budget\"]->com.procurement." \
                                                                    "budget.model.dto.check.BudgetCheckRq" \
                                                                    "[\"budgetBreakdown\"]->java.util.ArrayList[0]->" \
                                                                    "com.procurement.budget.model.dto.check.Budget" \
                                                                    "BreakdownCheckRq[\"amount\"]->com.procurement." \
                                                                    "budget.model.dto.check.CheckValue[\"currency\"])"

    @pytestrail.case("27009")
    def test_27009_8(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.00.00.00"
        assert create_pn_response[1]["errors"][0]["description"] == "Data processing exception."

    @pytestrail.case("27009")
    def test_27009_9(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["title"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender] value failed for " \
                                                                    "JSON property title due to missing (therefore " \
                                                                    "NULL) value for creator parameter title which " \
                                                                    "is a non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference " \
                                                                    "chain: com.procurement.access.infrastructure." \
                                                                    "handler.v1.model.request.PnCreateRequest" \
                                                                    "[\"tender\"]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"title\"])"

    @pytestrail.case("27009")
    def test_27009_10(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["description"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender] value failed for JSON " \
                                                                    "property description due to missing (therefore " \
                                                                    "NULL) value for creator parameter description " \
                                                                    "which is a non-nullable type\n at [Source: " \
                                                                    "UNKNOWN; line: -1, column: -1] (through " \
                                                                    "reference chain: com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model." \
                                                                    "request.PnCreateRequest$Tender[\"description\"])"

    @pytestrail.case("27009")
    def test_27009_11(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["legalBasis"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender] value failed for " \
                                                                    "JSON property legalBasis due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "legalBasis which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model." \
                                                                    "request.PnCreateRequest[\"tender\"]->com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest$Tender" \
                                                                    "[\"legalBasis\"])"

    @pytestrail.case("27009")
    def test_27009_12(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["tenderPeriod"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender] value failed for JSON " \
                                                                    "property tenderPeriod due to missing (therefore " \
                                                                    "NULL) value for creator parameter tenderPeriod " \
                                                                    "which is a non-nullable type\n at [Source: " \
                                                                    "UNKNOWN; line: -1, column: -1] (through " \
                                                                    "reference chain: com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model." \
                                                                    "request.PnCreateRequest$Tender[\"tenderPeriod\"])"

    @pytestrail.case("27009")
    def test_27009_13(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["tenderPeriod"]["startDate"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$TenderPeriod] value " \
                                                                    "failed for JSON property startDate due to " \
                                                                    "missing (therefore NULL) value for creator " \
                                                                    "parameter startDate which is a non-nullable " \
                                                                    "type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest[\"tender\"]->" \
                                                                    "com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.PnCreateRequest$Tender" \
                                                                    "[\"tenderPeriod\"]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$TenderPeriod" \
                                                                    "[\"startDate\"])"

    @pytestrail.case("27009")
    def test_27009_14(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender] value failed for JSON " \
                                                                    "property procuringEntity due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "procuringEntity which is a non-nullable " \
                                                                    "type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest[\"tender\"]->" \
                                                                    "com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.PnCreateRequest$Tender" \
                                                                    "[\"procuringEntity\"])"

    @pytestrail.case("27009")
    def test_27009_15(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["name"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.PnCreate" \
                                                                    "Request$Tender$ProcuringEntity] value failed " \
                                                                    "for JSON property name due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "name which is a non-nullable type\n at [Source: " \
                                                                    "UNKNOWN; line: -1, column: -1] (through " \
                                                                    "reference chain: com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"procuringEntity\"]->" \
                                                                    "com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.PnCreateRequest$Tender$" \
                                                                    "ProcuringEntity[\"name\"])"

    @pytestrail.case("27009")
    def test_27009_16(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["identifier"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$ProcuringEntity] value " \
                                                                    "failed for JSON property identifier due to " \
                                                                    "missing (therefore NULL) value for creator " \
                                                                    "parameter identifier which is a non-nullable " \
                                                                    "type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest[\"tender\"]->com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest$Tender" \
                                                                    "[\"procuringEntity\"]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$ProcuringEntity" \
                                                                    "[\"identifier\"])"

    @pytestrail.case("27009")
    def test_27009_17(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["identifier"]["scheme"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.Identifier] value failed for JSON " \
                                                                    "property scheme due to missing (therefore NULL) " \
                                                                    "value for creator parameter scheme which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference chain: " \
                                                                    "com.procurement.mdm.model.dto.data.TD" \
                                                                    "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                    "data.TenderTD[\"procuringEntity\"]->com." \
                                                                    "procurement.mdm.model.dto.data.Organization" \
                                                                    "Reference[\"identifier\"]->com.procurement." \
                                                                    "mdm.model.dto.data.Identifier[\"scheme\"])"

    @pytestrail.case("27009")
    def test_27009_18(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["identifier"]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation " \
                                                                    "of [simple type, class com.procurement.mdm." \
                                                                    "model.dto.data.Identifier] value failed for " \
                                                                    "JSON property id due to missing (therefore " \
                                                                    "NULL) value for creator parameter id which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference" \
                                                                    "[\"identifier\"]->com.procurement.mdm.model." \
                                                                    "dto.data.Identifier[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_19(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["identifier"]["legalName"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$ProcuringEntity$" \
                                                                    "Identifier] value failed for JSON property " \
                                                                    "legalName due to missing (therefore NULL) value " \
                                                                    "for creator parameter legalName which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest[\"tender\"]->com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest$Tender[\"procuring" \
                                                                    "Entity\"]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.PnCreate" \
                                                                    "Request$Tender$ProcuringEntity[\"identifier\"]->" \
                                                                    "com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.PnCreateRequest$Tender$" \
                                                                    "ProcuringEntity$Identifier[\"legalName\"])"

    @pytestrail.case("27009")
    def test_27009_20(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["scheme"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.Identifier] value failed for JSON " \
                                                                    "property scheme due to missing (therefore NULL) " \
                                                                    "value for creator parameter scheme which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference" \
                                                                    "[\"additionalIdentifiers\"]->java.util.ArrayList" \
                                                                    "[0]->com.procurement.mdm.model.dto.data." \
                                                                    "Identifier[\"scheme\"])"

    @pytestrail.case("27009")
    def test_27009_21(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.Identifier] value failed for JSON " \
                                                                    "property id due to missing (therefore NULL) " \
                                                                    "value for creator parameter id which is a non-" \
                                                                    "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference" \
                                                                    "[\"additionalIdentifiers\"]->java.util.ArrayList" \
                                                                    "[0]->com.procurement.mdm.model.dto.data." \
                                                                    "Identifier[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_22(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["additionalIdentifiers"][0]["legalName"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.PnCreate" \
                                                                    "Request$Tender$ProcuringEntity$Additional" \
                                                                    "Identifier] value failed for JSON property " \
                                                                    "legalName due to missing (therefore NULL) value " \
                                                                    "for creator parameter legalName which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest[\"tender\"]->com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest$Tender[\"procuring" \
                                                                    "Entity\"]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.PnCreate" \
                                                                    "Request$Tender$ProcuringEntity[\"additional" \
                                                                    "Identifiers\"]->java.util.ArrayList[0]->com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest$Tender$Procuring" \
                                                                    "Entity$AdditionalIdentifier[\"legalName\"])"

    @pytestrail.case("27009")
    def test_27009_23(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.PnCreate" \
                                                                    "Request$Tender$ProcuringEntity] value failed " \
                                                                    "for JSON property address due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "address which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"procuringEntity\"]->" \
                                                                    "com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.PnCreateRequest$Tender$" \
                                                                    "ProcuringEntity[\"address\"])"

    @pytestrail.case("27009")
    def test_27009_24(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]["streetAddress"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.Address] value failed for JSON " \
                                                                    "property streetAddress due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "streetAddress which is a non-nullable type\n " \
                                                                    "at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement.mdm." \
                                                                    "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                    "mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference" \
                                                                    "[\"address\"]->com.procurement.mdm.model.dto." \
                                                                    "data.Address[\"streetAddress\"])"

    @pytestrail.case("27009")
    def test_27009_25(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin." \
                                                                    "MissingKotlinParameterException: Instantiation " \
                                                                    "of [simple type, class com.procurement.mdm." \
                                                                    "model.dto.data.Address] value failed for JSON " \
                                                                    "property addressDetails due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "addressDetails which is a non-nullable type\n " \
                                                                    "at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement.mdm." \
                                                                    "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                    "mdm.model.dto.data.TenderTD[\"procuring" \
                                                                    "Entity\"]->com.procurement.mdm.model.dto.data." \
                                                                    "OrganizationReference[\"address\"]->com." \
                                                                    "procurement.mdm.model.dto.data.Address" \
                                                                    "[\"addressDetails\"])"

    @pytestrail.case("27009")
    def test_27009_26(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.AddressDetails] value failed for JSON " \
                                                                    "property country due to missing (therefore " \
                                                                    "NULL) value for creator parameter country which " \
                                                                    "is a non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference chain: " \
                                                                    "com.procurement.mdm.model.dto.data.TD" \
                                                                    "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                    "data.TenderTD[\"procuringEntity\"]->com." \
                                                                    "procurement.mdm.model.dto.data.Organization" \
                                                                    "Reference[\"address\"]->com.procurement.mdm." \
                                                                    "model.dto.data.Address[\"addressDetails\"]->com." \
                                                                    "procurement.mdm.model.dto.data.AddressDetails" \
                                                                    "[\"country\"])"

    @pytestrail.case("27009")
    def test_27009_27(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.CountryDetails] value failed for JSON " \
                                                                    "property id due to missing (therefore NULL) " \
                                                                    "value for creator parameter id which is a non-" \
                                                                    "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference" \
                                                                    "[\"address\"]->com.procurement.mdm.model.dto." \
                                                                    "data.Address[\"addressDetails\"]->com." \
                                                                    "procurement.mdm.model.dto.data.AddressDetails" \
                                                                    "[\"country\"]->com.procurement.mdm.model.dto." \
                                                                    "data.CountryDetails[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_28(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.AddressDetails] value failed for JSON " \
                                                                    "property region due to missing (therefore NULL) " \
                                                                    "value for creator parameter region which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference" \
                                                                    "[\"address\"]->com.procurement.mdm.model.dto." \
                                                                    "data.Address[\"addressDetails\"]->com." \
                                                                    "procurement.mdm.model.dto.data.Address" \
                                                                    "Details[\"region\"])"

    @pytestrail.case("27009")
    def test_27009_29(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin." \
                                                                    "MissingKotlinParameterException: Instantiation " \
                                                                    "of [simple type, class com.procurement.mdm." \
                                                                    "model.dto.data.RegionDetails] value failed for " \
                                                                    "JSON property id due to missing (therefore " \
                                                                    "NULL) value for creator parameter id which is " \
                                                                    "a non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference chain: " \
                                                                    "com.procurement.mdm.model.dto.data.TD" \
                                                                    "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                    "data.TenderTD[\"procuringEntity\"]->com." \
                                                                    "procurement.mdm.model.dto.data.Organization" \
                                                                    "Reference[\"address\"]->com.procurement.mdm." \
                                                                    "model.dto.data.Address[\"addressDetails\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.Address" \
                                                                    "Details[\"region\"]->com.procurement.mdm." \
                                                                    "model.dto.data.RegionDetails[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_30(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.AddressDetails] value failed for " \
                                                                    "JSON property locality due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "locality which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement.mdm." \
                                                                    "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                    "mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference" \
                                                                    "[\"address\"]->com.procurement.mdm.model.dto." \
                                                                    "data.Address[\"addressDetails\"]->com." \
                                                                    "procurement.mdm.model.dto.data.AddressDetails" \
                                                                    "[\"locality\"])"

    @pytestrail.case("27009")
    def test_27009_31(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["scheme"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.LocalityDetails] value failed for JSON " \
                                                                    "property scheme due to missing (therefore NULL) " \
                                                                    "value for creator parameter scheme which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference" \
                                                                    "[\"address\"]->com.procurement.mdm.model.dto." \
                                                                    "data.Address[\"addressDetails\"]->com." \
                                                                    "procurement.mdm.model.dto.data.AddressDetails" \
                                                                    "[\"locality\"]->com.procurement.mdm.model.dto." \
                                                                    "data.LocalityDetails[\"scheme\"])"

    @pytestrail.case("27009")
    def test_27009_32(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.LocalityDetails] value failed for JSON " \
                                                                    "property id due to missing (therefore NULL) " \
                                                                    "value for creator parameter id which is a non-" \
                                                                    "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference" \
                                                                    "[\"address\"]->com.procurement.mdm.model.dto." \
                                                                    "data.Address[\"addressDetails\"]->com." \
                                                                    "procurement.mdm.model.dto.data.AddressDetails" \
                                                                    "[\"locality\"]->com.procurement.mdm.model.dto." \
                                                                    "data.LocalityDetails[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_33(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["description"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.LocalityDetails] value failed for " \
                                                                    "JSON property description due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "description which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement.mdm." \
                                                                    "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                    "mdm.model.dto.data.TenderTD[\"procuring" \
                                                                    "Entity\"]->com.procurement.mdm.model.dto.data." \
                                                                    "OrganizationReference[\"address\"]->com." \
                                                                    "procurement.mdm.model.dto.data.Address" \
                                                                    "[\"addressDetails\"]->com.procurement.mdm.model." \
                                                                    "dto.data.AddressDetails[\"locality\"]->com." \
                                                                    "procurement.mdm.model.dto.data.LocalityDetails" \
                                                                    "[\"description\"])"

    @pytestrail.case("27009")
    def test_27009_34(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["contactPoint"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Pn" \
                                                                    "CreateRequest$Tender$ProcuringEntity] value " \
                                                                    "failed for JSON property contactPoint due to " \
                                                                    "missing (therefore NULL) value for creator " \
                                                                    "parameter contactPoint which is a non-nullable " \
                                                                    "type\n at [Source: UNKNOWN; line: -1, column: " \
                                                                    "-1] (through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"procuringEntity\"]->" \
                                                                    "com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.PnCreateRequest$Tender$" \
                                                                    "ProcuringEntity[\"contactPoint\"])"

    @pytestrail.case("27009")
    def test_27009_35(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["contactPoint"]["name"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.ContactPoint] value failed for JSON " \
                                                                    "property name due to missing (therefore NULL) " \
                                                                    "value for creator parameter name which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference" \
                                                                    "[\"contactPoint\"]->com.procurement.mdm.model." \
                                                                    "dto.data.ContactPoint[\"name\"])"

    @pytestrail.case("27009")
    def test_27009_36(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["contactPoint"]["email"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.ContactPoint] value failed for JSON " \
                                                                    "property email due to missing (therefore NULL) " \
                                                                    "value for creator parameter email which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"procuringEntity\"]->com.procurement.mdm." \
                                                                    "model.dto.data.OrganizationReference[\"contact" \
                                                                    "Point\"]->com.procurement.mdm.model.dto.data." \
                                                                    "ContactPoint[\"email\"])"

    @pytestrail.case("27009")
    def test_27009_37(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["procuringEntity"]["contactPoint"]["telephone"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.ContactPoint] value failed for JSON " \
                                                                    "property telephone due to missing (therefore " \
                                                                    "NULL) value for creator parameter telephone " \
                                                                    "which is a non-nullable type\n at [Source: " \
                                                                    "UNKNOWN; line: -1, column: -1] (through " \
                                                                    "reference chain: com.procurement.mdm.model.dto." \
                                                                    "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                    "dto.data.TenderTD[\"procuringEntity\"]->com." \
                                                                    "procurement.mdm.model.dto.data.Organization" \
                                                                    "Reference[\"contactPoint\"]->com.procurement." \
                                                                    "mdm.model.dto.data.ContactPoint[\"telephone\"])"

    @pytestrail.case("27009")
    def test_27009_38(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.PnCreate" \
                                                                    "Request$Tender$Lot] value failed for JSON " \
                                                                    "property id due to missing (therefore NULL) " \
                                                                    "value for creator parameter id which is a non-" \
                                                                    "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest[\"tender\"]->com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest$Tender[\"lots\"]->" \
                                                                    "java.util.ArrayList[0]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.PnCreate" \
                                                                    "Request$Tender$Lot[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_39(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["title"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access.in" \
                                                                    "frastructure.handler.v1.model.request.PnCreate" \
                                                                    "Request$Tender$Lot] value failed for JSON " \
                                                                    "property title due to missing (therefore NULL) " \
                                                                    "value for creator parameter title which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest[\"tender\"]->com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest$Tender[\"lots\"]" \
                                                                    "->java.util.ArrayList[0]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$Lot[\"title\"])"

    @pytestrail.case("27009")
    def test_27009_40(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["description"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Pn" \
                                                                    "CreateRequest$Tender$Lot] value failed for " \
                                                                    "JSON property description due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "description which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"lots\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.access.in" \
                                                                    "frastructure.handler.v1.model.request.Pn" \
                                                                    "CreateRequest$Tender$Lot[\"description\"])"

    @pytestrail.case("27009")
    def test_27009_41(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["value"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Pn" \
                                                                    "CreateRequest$Tender$Lot] value failed for " \
                                                                    "JSON property value due to missing (therefore " \
                                                                    "NULL) value for creator parameter value which " \
                                                                    "is a non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference chain: " \
                                                                    "com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.PnCreateRequest[\"tender\"]->" \
                                                                    "com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.PnCreateRequest$Tender" \
                                                                    "[\"lots\"]->java.util.ArrayList[0]->com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.PnCreateRequest$Tender$Lot" \
                                                                    "[\"value\"])"

    @pytestrail.case("27009")
    def test_27009_42(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["value"]["amount"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                    "Exception: Attribute 'amount' is an invalid " \
                                                                    "type 'NULL', the required type is number. " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"lots\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.access.in" \
                                                                    "frastructure.handler.v1.model.request.Pn" \
                                                                    "CreateRequest$Tender$Lot[\"value\"])"

    @pytestrail.case("27009")
    def test_27009_43(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["value"]["currency"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
                                                                    "Exception: Attribute 'currency' is an invalid " \
                                                                    "type 'NULL', the required type is text. " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"lots\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Pn" \
                                                                    "CreateRequest$Tender$Lot[\"value\"])"

    @pytestrail.case("27009")
    def test_27009_44(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["contractPeriod"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Pn" \
                                                                    "CreateRequest$Tender$Lot] value failed for " \
                                                                    "JSON property contractPeriod due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "contractPeriod which is a non-nullable type\n " \
                                                                    "at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"lots\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$Lot[\"contractPeriod\"])"

    @pytestrail.case("27009")
    def test_27009_45(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["contractPeriod"]["startDate"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Pn" \
                                                                    "CreateRequest$Tender$Lot$ContractPeriod] value " \
                                                                    "failed for JSON property startDate due to " \
                                                                    "missing (therefore NULL) value for creator " \
                                                                    "parameter startDate which is a non-nullable " \
                                                                    "type\n at [Source: UNKNOWN; line: -1, column: " \
                                                                    "-1] (through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"lots\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$Lot[\"contractPeriod\"]" \
                                                                    "->com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.PnCreateRequest$Tender$Lot$" \
                                                                    "ContractPeriod[\"startDate\"])"

    @pytestrail.case("27009")
    def test_27009_46(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["contractPeriod"]["endDate"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$Lot$ContractPeriod] " \
                                                                    "value failed for JSON property endDate due " \
                                                                    "to missing (therefore NULL) value for creator " \
                                                                    "parameter endDate which is a non-nullable " \
                                                                    "type\n at [Source: UNKNOWN; line: -1, column: " \
                                                                    "-1] (through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"lots\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.access.in" \
                                                                    "frastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$Lot[\"contractPeriod\"]" \
                                                                    "->com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.PnCreateRequest$Tender$Lot$" \
                                                                    "ContractPeriod[\"endDate\"])"

    @pytestrail.case("27009")
    def test_27009_47(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.PnCreate" \
                                                                    "Request$Tender$Lot] value failed for JSON " \
                                                                    "property placeOfPerformance due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "placeOfPerformance which is a non-nullable " \
                                                                    "type\n at [Source: UNKNOWN; line: -1, column:" \
                                                                    " -1] (through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"lots\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.access.infrastruc" \
                                                                    "ture.handler.v1.model.request.PnCreateRequest$" \
                                                                    "Tender$Lot[\"placeOfPerformance\"])"

    @pytestrail.case("27009")
    def test_27009_48(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.PlaceOfPerformance] value failed for " \
                                                                    "JSON property address due to missing (therefore " \
                                                                    "NULL) value for creator parameter address which " \
                                                                    "is a non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference chain:" \
                                                                    " com.procurement.mdm.model.dto.data.TD" \
                                                                    "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                    "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
                                                                    "->com.procurement.mdm.model.dto.data.LotTD" \
                                                                    "[\"placeOfPerformance\"]->com.procurement.mdm." \
                                                                    "model.dto.data.PlaceOfPerformance[\"address\"])"

    @pytestrail.case("27009")
    def test_27009_49(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin." \
                                                                    "MissingKotlinParameterException: Instantiation " \
                                                                    "of [simple type, class com.procurement.mdm." \
                                                                    "model.dto.data.Address] value failed for JSON " \
                                                                    "property streetAddress due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "streetAddress which is a non-nullable type\n " \
                                                                    "at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement.mdm." \
                                                                    "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                    "mdm.model.dto.data.TenderTD[\"lots\"]->java." \
                                                                    "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                    "dto.data.LotTD[\"placeOfPerformance\"]->com." \
                                                                    "procurement.mdm.model.dto.data.PlaceOf" \
                                                                    "Performance[\"address\"]->com.procurement." \
                                                                    "mdm.model.dto.data.Address[\"streetAddress\"])"

    @pytestrail.case("27009")
    def test_27009_50(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.Address] value failed for JSON " \
                                                                    "property addressDetails due to missing (there" \
                                                                    "fore NULL) value for creator parameter address" \
                                                                    "Details which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement.mdm." \
                                                                    "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                    "mdm.model.dto.data.TenderTD[\"lots\"]->java." \
                                                                    "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                    "dto.data.LotTD[\"placeOfPerformance\"]->com." \
                                                                    "procurement.mdm.model.dto.data.PlaceOfPer" \
                                                                    "formance[\"address\"]->com.procurement.mdm." \
                                                                    "model.dto.data.Address[\"addressDetails\"])"

    @pytestrail.case("27009")
    def test_27009_51(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.AddressDetails] value failed for JSON " \
                                                                    "property country due to missing (therefore " \
                                                                    "NULL) value for creator parameter country which " \
                                                                    "is a non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference chain: " \
                                                                    "com.procurement.mdm.model.dto.data.TD" \
                                                                    "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                    "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
                                                                    "->com.procurement.mdm.model.dto.data.LotTD" \
                                                                    "[\"placeOfPerformance\"]->com.procurement.mdm." \
                                                                    "model.dto.data.PlaceOfPerformance[\"address\"]" \
                                                                    "->com.procurement.mdm.model.dto.data.Address" \
                                                                    "[\"addressDetails\"]->com.procurement.mdm.model." \
                                                                    "dto.data.AddressDetails[\"country\"])"

    @pytestrail.case("27009")
    def test_27009_52(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.CountryDetails] value failed for JSON " \
                                                                    "property id due to missing (therefore NULL) " \
                                                                    "value for creator parameter id which is a non-" \
                                                                    "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"lots\"]->java.util.ArrayList[0]->com." \
                                                                    "procurement.mdm.model.dto.data.LotTD[\"placeOf" \
                                                                    "Performance\"]->com.procurement.mdm.model.dto." \
                                                                    "data.PlaceOfPerformance[\"address\"]->com." \
                                                                    "procurement.mdm.model.dto.data.Address" \
                                                                    "[\"addressDetails\"]->com.procurement.mdm." \
                                                                    "model.dto.data.AddressDetails[\"country\"]->" \
                                                                    "com.procurement.mdm.model.dto.data." \
                                                                    "CountryDetails[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_53(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.AddressDetails] value failed for JSON " \
                                                                    "property region due to missing (therefore NULL) " \
                                                                    "value for creator parameter region which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: " \
                                                                    "com.procurement.mdm.model.dto.data.TD" \
                                                                    "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                    "data.TenderTD[\"lots\"]->java.util.ArrayList[0]->" \
                                                                    "com.procurement.mdm.model.dto.data.LotTD" \
                                                                    "[\"placeOfPerformance\"]->com.procurement.mdm." \
                                                                    "model.dto.data.PlaceOfPerformance[\"address\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.Address" \
                                                                    "[\"addressDetails\"]->com.procurement.mdm." \
                                                                    "model.dto.data.AddressDetails[\"region\"])"

    @pytestrail.case("27009")
    def test_27009_54(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.RegionDetails] value failed for JSON " \
                                                                    "property id due to missing (therefore NULL) " \
                                                                    "value for creator parameter id which is a non-" \
                                                                    "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"lots\"]->java.util.ArrayList[0]->com." \
                                                                    "procurement.mdm.model.dto.data.LotTD[\"place" \
                                                                    "OfPerformance\"]->com.procurement.mdm.model." \
                                                                    "dto.data.PlaceOfPerformance[\"address\"]->com." \
                                                                    "procurement.mdm.model.dto.data.Address" \
                                                                    "[\"addressDetails\"]->com.procurement.mdm.model." \
                                                                    "dto.data.AddressDetails[\"region\"]->com." \
                                                                    "procurement.mdm.model.dto.data.RegionDetails" \
                                                                    "[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_55(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.AddressDetails] value failed for JSON " \
                                                                    "property locality due to missing (therefore " \
                                                                    "NULL) value for creator parameter locality " \
                                                                    "which is a non-nullable type\n at [Source: " \
                                                                    "UNKNOWN; line: -1, column: -1] (through " \
                                                                    "reference chain: com.procurement.mdm.model.dto." \
                                                                    "data.TD[\"tender\"]->com.procurement.mdm.model." \
                                                                    "dto.data.TenderTD[\"lots\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                    "data.LotTD[\"placeOfPerformance\"]->com." \
                                                                    "procurement.mdm.model.dto.data.PlaceOfPer" \
                                                                    "formance[\"address\"]->com.procurement.mdm." \
                                                                    "model.dto.data.Address[\"addressDetails\"]->" \
                                                                    "com.procurement.mdm.model.dto.data." \
                                                                    "AddressDetails[\"locality\"])"

    @pytestrail.case("27009")
    def test_27009_56(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.LocalityDetails] value failed for " \
                                                                    "JSON property scheme due to missing (therefore " \
                                                                    "NULL) value for creator parameter scheme which " \
                                                                    "is a non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference " \
                                                                    "chain: com.procurement.mdm.model.dto.data." \
                                                                    "TD[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                    "data.TenderTD[\"lots\"]->java.util.ArrayList" \
                                                                    "[0]->com.procurement.mdm.model.dto.data.LotTD" \
                                                                    "[\"placeOfPerformance\"]->com.procurement.mdm." \
                                                                    "model.dto.data.PlaceOfPerformance[\"address\"]" \
                                                                    "->com.procurement.mdm.model.dto.data.Address" \
                                                                    "[\"addressDetails\"]->com.procurement.mdm.model." \
                                                                    "dto.data.AddressDetails[\"locality\"]->com." \
                                                                    "procurement.mdm.model.dto.data.Locality" \
                                                                    "Details[\"scheme\"])"

    @pytestrail.case("27009")
    def test_27009_57(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.LocalityDetails] value failed for " \
                                                                    "JSON property id due to missing (therefore " \
                                                                    "NULL) value for creator parameter id which " \
                                                                    "is a non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference chain: " \
                                                                    "com.procurement.mdm.model.dto.data.TD" \
                                                                    "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                    "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
                                                                    "->com.procurement.mdm.model.dto.data.LotTD" \
                                                                    "[\"placeOfPerformance\"]->com.procurement.mdm." \
                                                                    "model.dto.data.PlaceOfPerformance[\"address\"]" \
                                                                    "->com.procurement.mdm.model.dto.data.Address" \
                                                                    "[\"addressDetails\"]->com.procurement.mdm." \
                                                                    "model.dto.data.AddressDetails[\"locality\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.Locality" \
                                                                    "Details[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_58(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["description"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm." \
                                                                    "model.dto.data.LocalityDetails] value failed " \
                                                                    "for JSON property description due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "description which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement.mdm." \
                                                                    "model.dto.data.TD[\"tender\"]->com.procurement." \
                                                                    "mdm.model.dto.data.TenderTD[\"lots\"]->java." \
                                                                    "util.ArrayList[0]->com.procurement.mdm.model." \
                                                                    "dto.data.LotTD[\"placeOfPerformance\"]->com." \
                                                                    "procurement.mdm.model.dto.data.PlaceOf" \
                                                                    "Performance[\"address\"]->com.procurement.mdm." \
                                                                    "model.dto.data.Address[\"addressDetails\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.Address" \
                                                                    "Details[\"locality\"]->com.procurement.mdm." \
                                                                    "model.dto.data.LocalityDetails[\"description\"])"

    @pytestrail.case("27009")
    def test_27009_59(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["items"][0]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "CheckItemsRequest$Item] value failed for JSON " \
                                                                    "property id due to missing (therefore NULL) " \
                                                                    "value for creator parameter id which is a non-" \
                                                                    "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.access.infrastructure.handler.v1." \
                                                                    "model.request.CheckItemsRequest[\"items\"]->" \
                                                                    "java.util.ArrayList[0]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Check" \
                                                                    "ItemsRequest$Item[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_60(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["items"][0]["classification"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Check" \
                                                                    "ItemsRequest$Item] value failed for JSON " \
                                                                    "property classification due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "classification which is a non-nullable type\n " \
                                                                    "at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "CheckItemsRequest[\"items\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Check" \
                                                                    "ItemsRequest$Item[\"classification\"])"

    @pytestrail.case("27009")
    def test_27009_61(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["items"][0]["classification"]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "CheckItemsRequest$Item$Classification] value " \
                                                                    "failed for JSON property id due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "id which is a non-nullable type\n at [Source: " \
                                                                    "UNKNOWN; line: -1, column: -1] (through " \
                                                                    "reference chain: com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "CheckItemsRequest[\"items\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "CheckItemsRequest$Item[\"classification\"]->" \
                                                                    "com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.CheckItemsRequest$Item$" \
                                                                    "Classification[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_62(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.ClassificationTD] value failed for " \
                                                                    "JSON property id due to missing (therefore " \
                                                                    "NULL) value for creator parameter id which is " \
                                                                    "a non-nullable type\n at [Source: UNKNOWN; " \
                                                                    "line: -1, column: -1] (through reference chain: " \
                                                                    "com.procurement.mdm.model.dto.data.TD" \
                                                                    "[\"tender\"]->com.procurement.mdm.model.dto." \
                                                                    "data.TenderTD[\"items\"]->java.util.ArrayList" \
                                                                    "[0]->com.procurement.mdm.model.dto.data.ItemTD" \
                                                                    "[\"additionalClassifications\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.mdm.model.dto." \
                                                                    "data.ClassificationTD[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_63(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["items"][0]["quantity"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.ItemTD] value failed for JSON property " \
                                                                    "quantity due to missing (therefore NULL) value " \
                                                                    "for creator parameter quantity which is a non-" \
                                                                    "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"items\"]->java.util.ArrayList[0]->com." \
                                                                    "procurement.mdm.model.dto.data.ItemTD" \
                                                                    "[\"quantity\"])"

    @pytestrail.case("27009")
    def test_27009_64(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["items"][0]["unit"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin." \
                                                                    "MissingKotlinParameterException: Instantiation " \
                                                                    "of [simple type, class com.procurement.mdm." \
                                                                    "model.dto.data.ItemTD] value failed for JSON " \
                                                                    "property unit due to missing (therefore NULL) " \
                                                                    "value for creator parameter unit which is a non-" \
                                                                    "nullable type\n at [Source: UNKNOWN; line: -1, " \
                                                                    "column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
                                                                    "com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"items\"]->java.util.ArrayList[0]->com." \
                                                                    "procurement.mdm.model.dto.data.ItemTD[\"unit\"])"

    @pytestrail.case("27009")
    def test_27009_65(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["items"][0]["unit"]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.mdm.model." \
                                                                    "dto.data.ItemUnitTD] value failed for JSON " \
                                                                    "property id due to missing (therefore NULL) " \
                                                                    "value for creator parameter id which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.mdm.model.dto.data.TD[\"tender\"]" \
                                                                    "->com.procurement.mdm.model.dto.data.TenderTD" \
                                                                    "[\"items\"]->java.util.ArrayList[0]->com." \
                                                                    "procurement.mdm.model.dto.data.ItemTD[\"unit\"]" \
                                                                    "->com.procurement.mdm.model.dto.data.ItemUnitTD" \
                                                                    "[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_66(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["items"][0]["description"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$Item] value failed for " \
                                                                    "JSON property description due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "description which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"items\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.PnCreate" \
                                                                    "Request$Tender$Item[\"description\"])"

    @pytestrail.case("27009")
    def test_27009_67(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["items"][0]["relatedLot"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "CheckItemsRequest$Item] value failed for JSON " \
                                                                    "property relatedLot due to missing (therefore " \
                                                                    "NULL) value for creator parameter relatedLot " \
                                                                    "which is a non-nullable type\n at [Source: " \
                                                                    "UNKNOWN; line: -1, column: -1] (through " \
                                                                    "reference chain: com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Check" \
                                                                    "ItemsRequest[\"items\"]->java.util.ArrayList[0]" \
                                                                    "->com.procurement.access.infrastructure.handler." \
                                                                    "v1.model.request.CheckItemsRequest$Item" \
                                                                    "[\"relatedLot\"])"

    @pytestrail.case("27009")
    def test_27009_68(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["documents"][0]["documentType"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$Document] value failed " \
                                                                    "for JSON property documentType due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "documentType which is a non-nullable type\n " \
                                                                    "at [Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender[\"documents\"]->java." \
                                                                    "util.ArrayList[0]->com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$Document[\"documentType\"])"

    @pytestrail.case("27009")
    def test_27009_69(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["documents"][0]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "500.14.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.storage." \
                                                                    "model.dto.registration.Document] value failed " \
                                                                    "for JSON property id due to missing (therefore " \
                                                                    "NULL) value for creator parameter id which is a " \
                                                                    "non-nullable type\n at [Source: UNKNOWN; line: " \
                                                                    "-1, column: -1] (through reference chain: com." \
                                                                    "procurement.storage.model.dto.registration." \
                                                                    "DocumentsRq[\"documents\"]->java.util." \
                                                                    "ArrayList[0]->com.procurement.storage.model." \
                                                                    "dto.registration.Document[\"id\"])"

    @pytestrail.case("27009")
    def test_27009_70(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["documents"][0]["title"]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
                                                                    "KotlinParameterException: Instantiation of " \
                                                                    "[simple type, class com.procurement.access." \
                                                                    "infrastructure.handler.v1.model.request.Pn" \
                                                                    "CreateRequest$Tender$Document] value failed " \
                                                                    "for JSON property title due to missing " \
                                                                    "(therefore NULL) value for creator parameter " \
                                                                    "title which is a non-nullable type\n at " \
                                                                    "[Source: UNKNOWN; line: -1, column: -1] " \
                                                                    "(through reference chain: com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest[\"tender\"]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model." \
                                                                    "request.PnCreateRequest$Tender[\"documents\"]" \
                                                                    "->java.util.ArrayList[0]->com.procurement." \
                                                                    "access.infrastructure.handler.v1.model.request." \
                                                                    "PnCreateRequest$Tender$Document[\"title\"])"

    @pytestrail.case("27013")
    def test_27013_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        access_token = get_access_token_for_platform_two()
        x_operation_id = get_x_operation_id(access_token)
        access_token = "ZZZ"
        time.sleep(2)
        test_create_fs = insert_into_db_create_fs(cpid)
        payload["planning"]["budget"]["budgetBreakdown"][0]["id"] = test_create_fs[2]
        host = set_instance_for_request()
        request_to_create_pn = requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": additional_value},
            json=payload)
        time.sleep(2)
        dict = json.loads(request_to_create_pn.text.replace("'", '"'))
        assert request_to_create_pn.status_code == 401
        assert dict["errors"][0]["code"] == "401.81.03.04"
        assert dict["errors"][0]["description"] == "The error of verification of the authentication token."

    @pytestrail.case("27014")
    def test_27014_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["documents"][0]["id"] = str(uuid.uuid4())
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27014")
    def test_27014_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["documents"][0]["id"] = str(uuid.uuid4())
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.14.00.14"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"Files not found: [{payload['tender']['documents'][0]['id']}]"

    @pytestrail.case("27015")
    def test_27015_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27015")
    def test_27015_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
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

    @pytestrail.case("27015")
    def test_27015_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        language = execute_cql_from_orchestrator_context(cpid)["language"]
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert language == "ro"

    @pytestrail.case("27016")
    def test_27016_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "24200000-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27016")
    def test_27016_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "24200000-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.53"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "CPV codes of all items must have minimum 3 the same starting symbols."

    @pytestrail.case("27017")
    def test_27017_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27017")
    def test_27017_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
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

    @pytestrail.case("27017")
    def test_27017_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert planning_notice["releases"][0]["tender"]["classification"]["id"] == "45112300-8"
        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27018")
    def test_27018_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27018")
    def test_27018_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
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

    @pytestrail.case("27018")
    def test_27018_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert planning_notice["releases"][0]["tender"]["classification"]["id"] == "45112300-8"
            assert planning_notice["releases"][0]["tender"]["classification"]["scheme"] == "CPV"
            assert planning_notice["releases"][0]["tender"]["classification"][
                       "description"] == "Lucrări de rambleiere şi de asanare a terenului"
        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27019")
    def test_27019_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27019")
    def test_27019_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
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

    @pytestrail.case("27019")
    def test_27019_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert multistage["releases"][0]["tender"]["mainProcurementCategory"] == "works"
        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27020")
    def test_27020_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["additionalClassifications"] = [
            {"id": "AA12-4"},
            {"id": "AA01-1"}
        ]

        payload["tender"]["items"][1]["additionalClassifications"] = [
            {"id": "AA12-4"},
            {"id": "AA01-1"}
        ]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27020")
    def test_27020_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["additionalClassifications"] = [
            {"id": "AA12-4"},
            {"id": "AA01-1"}
        ]

        payload["tender"]["items"][1]["additionalClassifications"] = [
            {"id": "AA12-4"},
            {"id": "AA01-1"}
        ]
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

    @pytestrail.case("27020")
    def test_27020_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["additionalClassifications"] = [
            {"id": "AA12-4"},
            {"id": "AA01-1"}
        ]

        payload["tender"]["items"][1]["additionalClassifications"] = [
            {"id": "AA12-4"},
            {"id": "AA01-1"}
        ]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
                       "scheme"] == "CPVS"
            assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"] == \
                   payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
            assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
                       "description"] == "Oţel carbon"

            assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][1][
                       "scheme"] == "CPVS"
            assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][1]["id"] == \
                   payload["tender"]["items"][0]["additionalClassifications"][1]["id"]
            assert planning_notice["releases"][0]["tender"]["items"][0]["additionalClassifications"][1][
                       "description"] == "Metal"
        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27020")
    def test_27020_4(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["additionalClassifications"] = [
            {"id": "AA12-4"},
            {"id": "AA01-1"}
        ]

        payload["tender"]["items"][1]["additionalClassifications"] = [
            {"id": "AA12-4"},
            {"id": "AA01-1"}
        ]
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][0][
                       "scheme"] == "CPVS"
            assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][0]["id"] == \
                   payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
            assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][0][
                       "description"] == "Oţel carbon"

            assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][1][
                       "scheme"] == "CPVS"
            assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][1]["id"] == \
                   payload["tender"]["items"][0]["additionalClassifications"][1]["id"]
            assert planning_notice["releases"][0]["tender"]["items"][1]["additionalClassifications"][1][
                       "description"] == "Metal"
        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27021")
    def test_27021_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27021")
    def test_27021_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
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

    @pytestrail.case("27021")
    def test_27021_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert planning_notice["releases"][0]["tender"]["items"][0]["classification"]["scheme"] == "CPV"
            assert planning_notice["releases"][0]["tender"]["items"][0]["classification"]["id"] == \
                   payload["tender"]["items"][0]["classification"]["id"]
            assert planning_notice["releases"][0]["tender"]["items"][0]["classification"][
                       "description"] == "Lucrări de valorificare a terenurilor virane"
        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27021")
    def test_27021_4(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert planning_notice["releases"][0]["tender"]["items"][1]["classification"]["scheme"] == "CPV"
            assert planning_notice["releases"][0]["tender"]["items"][1]["classification"]["id"] == \
                   payload["tender"]["items"][1]["classification"]["id"]
            assert planning_notice["releases"][0]["tender"]["items"][1]["classification"][
                       "description"] == "Lucrări de reabilitare a terenului"
        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27022")
    def test_27022_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["unit"]["id"] = "10"
        payload["tender"]["items"][1]["unit"]["id"] = "120"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27022")
    def test_27022_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["unit"]["id"] = "10"
        payload["tender"]["items"][1]["unit"]["id"] = "120"
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

    @pytestrail.case("27022")
    def test_27022_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["unit"]["id"] = "10"
        payload["tender"]["items"][1]["unit"]["id"] = "120"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert planning_notice["releases"][0]["tender"]["items"][0]["unit"]["id"] == \
                   payload["tender"]["items"][0]["unit"]["id"]
            assert planning_notice["releases"][0]["tender"]["items"][0]["unit"]["name"] == "Parsec"
        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27022")
    def test_27022_4(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["unit"]["id"] = "10"
        payload["tender"]["items"][1]["unit"]["id"] = "120"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert planning_notice["releases"][0]["tender"]["items"][1]["unit"]["id"] == \
                   payload["tender"]["items"][1]["unit"]["id"]
            assert planning_notice["releases"][0]["tender"]["items"][1]["unit"]["name"] == "Milion decalitri"
        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27023")
    def test_27023_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"] = "MD"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27023")
    def test_27023_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"] = "MD"
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

    @pytestrail.case("27023")
    def test_27023_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"] = "MD"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "country"]["id"] == \
                payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"]

            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "country"]["scheme"] == "iso-alpha2"
            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "country"]["description"] == "Moldova, Republica"
            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "country"]["uri"] == "https://www.iso.org"

        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27024")
    def test_27024_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27024")
    def test_27024_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = "3400000"
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

    @pytestrail.case("27024")
    def test_27024_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "region"]["id"] == \
                payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"]

            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "region"]["scheme"] == "CUATM"
            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "region"]["description"] == "Donduşeni"
            assert \
                planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"][
                    "region"]["uri"] == "http://statistica.md"

        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

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
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
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
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27026")
    def test_27026_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27026")
    def test_27026_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
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

    @pytestrail.case("27026")
    def test_27026_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()

            assert multistage["releases"][0]["tender"]["procurementMethodDetails"] == procurement_method_details[
                additional_value]
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27029")
    def test_27029_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27029")
    def test_27029_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
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

    @pytestrail.case("27029")
    def test_27029_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert planning_notice["releases"][0]["tender"]["submissionMethodRationale"][0] == \
                   procurement_method_rationale[
                       additional_value]
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27030")
    def test_27030_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27030")
    def test_27030_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
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

    @pytestrail.case("27030")
    def test_27030_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_obligatory_data_model_without_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "planning")
        if check_record == True:
            planning_notice = requests.get(
                url=get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert planning_notice["releases"][0]["tender"]["submissionMethodDetails"] == \
                   submission_method_details[additional_value]
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        else:
            assert get_url["records"][0]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "planning"

    @pytestrail.case("27031")
    def test_27031_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27031")
    def test_27031_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
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

    @pytestrail.case("27031")
    def test_27031_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            assert multistage["releases"][0]["tender"]["eligibilityCriteria"] == \
                   eligibility_criteria[additional_value]
            assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27032")
    def test_27032_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "MD"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27032")
    def test_27032_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "MD"
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

    @pytestrail.case("27032")
    def test_27032_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"] = "MD"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            list_of_dictionaries = multistage["releases"][0]["parties"]
            for d in list_of_dictionaries:
                if d["roles"][0] == "procuringEntity":
                    assert d["address"]["addressDetails"]["country"]["id"] == \
                           payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"]
                    assert d["address"]["addressDetails"]["country"]["scheme"] == "iso-alpha2"
                    assert d["address"]["addressDetails"]["country"]["description"] == "Moldova, Republica"
                    assert d["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27033")
    def test_27033_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27033")
    def test_27033_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
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

    @pytestrail.case("27033")
    def test_27033_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            list_of_dictionaries = multistage["releases"][0]["parties"]
            for d in list_of_dictionaries:
                if d["roles"][0] == "procuringEntity":
                    assert d["address"]["addressDetails"]["region"]["id"] == \
                           payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"]
                    assert d["address"]["addressDetails"]["region"][
                               "scheme"] == "CUATM"
                    assert d["address"]["addressDetails"]["region"][
                               "description"] == "Donduşeni"
                    assert d["address"]["addressDetails"]["region"][
                               "uri"] == "http://statistica.md"
        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27034")
    def test_27034_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

    @pytestrail.case("27034")
    def test_27034_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
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

    @pytestrail.case("27034")
    def test_27034_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"] = "3400000"
        payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"] = "3401000"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            list_of_dictionaries = multistage["releases"][0]["parties"]
            for d in list_of_dictionaries:
                if d["roles"][0] == "procuringEntity":
                    assert d["address"]["addressDetails"]["locality"]["id"] == \
                           payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
                    assert d["address"]["addressDetails"]["locality"][
                               "scheme"] == "CUATM"
                    assert d["address"]["addressDetails"]["locality"][
                               "description"] == "or.Donduşeni (r-l Donduşeni)"
                    assert d["address"]["addressDetails"]["locality"][
                               "uri"] == "http://statistica.md"
        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27035")
    def test_27035_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "brbrbr"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27035")
    def test_27035_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["identifier"]["scheme"] = "brbrbr"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00.12"
        assert create_pn_response[1]["errors"][0]["description"] == "Registration scheme not found. "

    @pytestrail.case("27036")
    def test_27036_1(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payer_name = "name of payer"
        payer_identifier_scheme = "scheme of payer"
        payer_identifier_legal_name = "legal of payer"
        payer_identifier_legal_uri = "uri of payer"
        payer_address_street = "street"
        payer_address_postal = "postalCode"
        country_id = "MD"
        country_scheme = "iso-alpha2"
        country_description = "Moldova, Republica"
        region_id = "3400000"
        region_scheme = "CUATM"
        region_description = "Donduşeni"
        locality_scheme = "CUATM"
        locality_id = "3401000"
        locality_description = "or.Donduşeni (r-l Donduşeni)"
        payer_additional_id = "test id"
        payer_additional_scheme = "test scheme"
        payer_additional_uri = "test uri"
        payer_additional_legal = "test legal"
        contact_point_name = "name of contact"
        contact_point_email = "email of contact"
        contact_point_telephone = "telephone of contact"
        contact_point_fax = "fax of contact"
        contact_point_url = "url of contact"

        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, payer_name=payer_name,
                                                  payer_identifier_scheme=payer_identifier_scheme,
                                                  pmd=additional_value, country_id=country_id, region_id=region_id,
                                                  payer_identifier_legal_name=payer_identifier_legal_name,
                                                  payer_identifier_legal_uri=payer_identifier_legal_uri,
                                                  payer_address_street=payer_address_street,
                                                  locality_scheme=locality_scheme,
                                                  locality_id=locality_id,
                                                  payer_address_postal=payer_address_postal,
                                                  payer_additional_id=payer_additional_id,
                                                  payer_additional_scheme=payer_additional_scheme,
                                                  payer_additional_uri=payer_additional_uri,
                                                  payer_additional_legal=payer_additional_legal,
                                                  contact_point_name=contact_point_name,
                                                  contact_point_email=contact_point_email,
                                                  contact_point_telephone=contact_point_telephone,
                                                  contact_point_fax=contact_point_fax,
                                                  contact_point_url=contact_point_url,
                                                  country_scheme=country_scheme,
                                                  country_description=country_description,
                                                  region_scheme=region_scheme, region_description=region_description,
                                                  locality_description=locality_description)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27036")
    def test_27036_2(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payer_name = "name of payer"
        payer_identifier_scheme = "scheme of payer"
        payer_identifier_legal_name = "legal of payer"
        payer_identifier_legal_uri = "uri of payer"
        payer_address_street = "street"
        payer_address_postal = "postalCode"
        country_id = "MD"
        country_scheme = "iso-alpha2"
        country_description = "Moldova, Republica"
        region_id = "3400000"
        region_scheme= "CUATM"
        region_description = "Donduşeni"
        locality_scheme = "CUATM"
        locality_id = "3401000"
        locality_description = "or.Donduşeni (r-l Donduşeni)"
        payer_additional_id = "test id"
        payer_additional_scheme = "test scheme"
        payer_additional_uri = "test uri"
        payer_additional_legal = "test legal"
        contact_point_name = "name of contact"
        contact_point_email = "email of contact"
        contact_point_telephone = "telephone of contact"
        contact_point_fax = "fax of contact"
        contact_point_url = "url of contact"

        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, payer_name=payer_name,
                                                  payer_identifier_scheme=payer_identifier_scheme,
                                                  pmd=additional_value, country_id=country_id, region_id=region_id,
                                                  payer_identifier_legal_name=payer_identifier_legal_name,
                                                  payer_identifier_legal_uri=payer_identifier_legal_uri,
                                                  payer_address_street=payer_address_street,
                                                  locality_scheme=locality_scheme,
                                                  locality_id=locality_id,
                                                  payer_address_postal=payer_address_postal,
                                                  payer_additional_id=payer_additional_id,
                                                  payer_additional_scheme=payer_additional_scheme,
                                                  payer_additional_uri=payer_additional_uri,
                                                  payer_additional_legal=payer_additional_legal,
                                                  contact_point_name=contact_point_name,
                                                  contact_point_email=contact_point_email,
                                                  contact_point_telephone=contact_point_telephone,
                                                  contact_point_fax=contact_point_fax,
                                                  contact_point_url=contact_point_url,
                                                  country_scheme=country_scheme, country_description=country_description,
                                                  region_scheme=region_scheme,region_description=region_description,
                                                  locality_description=locality_description)
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

    @pytestrail.case("27036")
    def test_27036_3(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payer_name = "name of payer"
        payer_identifier_scheme = "scheme of payer"
        payer_identifier_legal_name = "legal of payer"
        payer_identifier_legal_uri = "uri of payer"
        payer_address_street = "street"
        payer_address_postal = "postalCode"
        country_id = "MD"
        country_scheme = "iso-alpha2"
        country_description = "Moldova, Republica"
        region_id = "3400000"
        region_scheme = "CUATM"
        region_description = "Donduşeni"
        locality_scheme = "CUATM"
        locality_id = "3401000"
        locality_description = "or.Donduşeni (r-l Donduşeni)"
        payer_additional_id = "test id"
        payer_additional_scheme = "test scheme"
        payer_additional_uri = "test uri"
        payer_additional_legal = "test legal"
        contact_point_name = "name of contact"
        contact_point_email = "email of contact"
        contact_point_telephone = "telephone of contact"
        contact_point_fax = "fax of contact"
        contact_point_url = "url of contact"

        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, payer_name=payer_name,
                                                  payer_identifier_scheme=payer_identifier_scheme,
                                                  pmd=additional_value, country_id=country_id, region_id=region_id,
                                                  payer_identifier_legal_name=payer_identifier_legal_name,
                                                  payer_identifier_legal_uri=payer_identifier_legal_uri,
                                                  payer_address_street=payer_address_street,
                                                  locality_scheme=locality_scheme,
                                                  locality_id=locality_id,
                                                  payer_address_postal=payer_address_postal,
                                                  payer_additional_id=payer_additional_id,
                                                  payer_additional_scheme=payer_additional_scheme,
                                                  payer_additional_uri=payer_additional_uri,
                                                  payer_additional_legal=payer_additional_legal,
                                                  contact_point_name=contact_point_name,
                                                  contact_point_email=contact_point_email,
                                                  contact_point_telephone=contact_point_telephone,
                                                  contact_point_fax=contact_point_fax,
                                                  contact_point_url=contact_point_url,
                                                  country_scheme=country_scheme,
                                                  country_description=country_description,
                                                  region_scheme=region_scheme, region_description=region_description,
                                                  locality_description=locality_description)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            list_of_dictionaries = multistage["releases"][0]["parties"]
            payer_section = list()
            for d in list_of_dictionaries:
                if d["roles"][0] == "payer":
                    payer_section.append(d)

            assert payer_section[0]["id"] == f"{payer_identifier_scheme}-{payer_1}"
            assert payer_section[0]["identifier"]["id"] == payer_1
            assert payer_section[0]["name"] == payer_name
            assert payer_section[0]["identifier"]["scheme"] == payer_identifier_scheme
            assert payer_section[0]["identifier"]["legalName"] == payer_identifier_legal_name
            assert payer_section[0]["identifier"]["uri"] == payer_identifier_legal_uri
            assert payer_section[0]["address"]["streetAddress"] == payer_address_street
            assert payer_section[0]["address"]["postalCode"] == payer_address_postal
            assert payer_section[0]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
            assert payer_section[0]["address"]["addressDetails"]["locality"]["id"] == locality_id
            assert payer_section[0]["address"]["addressDetails"]["country"]["id"] == country_id
            assert payer_section[0]["address"]["addressDetails"]["region"]["id"] == region_id
            assert payer_section[0]["additionalIdentifiers"][0]["scheme"] == payer_additional_scheme
            assert payer_section[0]["additionalIdentifiers"][0]["id"] == payer_additional_id
            assert payer_section[0]["additionalIdentifiers"][0]["legalName"] == payer_additional_legal
            assert payer_section[0]["additionalIdentifiers"][0]["uri"] == payer_additional_uri
            assert payer_section[0]["contactPoint"]["name"] == contact_point_name
            assert payer_section[0]["contactPoint"]["email"] == contact_point_email
            assert payer_section[0]["contactPoint"]["telephone"] == contact_point_telephone
            assert payer_section[0]["contactPoint"]["faxNumber"] == contact_point_fax
            assert payer_section[0]["contactPoint"]["url"] == contact_point_url
            assert payer_section[0]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
            assert payer_section[0]["address"]["addressDetails"]["country"]["description"] == country_description
            assert payer_section[0]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
            assert payer_section[0]["address"]["addressDetails"]["region"]["description"] == region_description
            assert payer_section[0]["address"]["addressDetails"]["locality"][
                       "description"] == locality_description
            assert payer_section[0]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
            assert payer_section[0]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
            assert payer_section[0]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

            assert payer_section[1]["id"] == f"{payer_identifier_scheme}-{payer_2}"
            assert payer_section[1]["identifier"]["id"] == payer_2
            assert payer_section[1]["name"] == payer_name
            assert payer_section[1]["identifier"]["scheme"] == payer_identifier_scheme
            assert payer_section[1]["identifier"]["legalName"] == payer_identifier_legal_name
            assert payer_section[1]["identifier"]["uri"] == payer_identifier_legal_uri
            assert payer_section[1]["address"]["streetAddress"] == payer_address_street
            assert payer_section[1]["address"]["postalCode"] == payer_address_postal
            assert payer_section[1]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
            assert payer_section[1]["address"]["addressDetails"]["locality"]["id"] == locality_id
            assert payer_section[1]["address"]["addressDetails"]["country"]["id"] == country_id
            assert payer_section[1]["address"]["addressDetails"]["region"]["id"] == region_id
            assert payer_section[1]["additionalIdentifiers"][0]["scheme"] == payer_additional_scheme
            assert payer_section[1]["additionalIdentifiers"][0]["id"] == payer_additional_id
            assert payer_section[1]["additionalIdentifiers"][0]["legalName"] == payer_additional_legal
            assert payer_section[1]["additionalIdentifiers"][0]["uri"] == payer_additional_uri
            assert payer_section[1]["contactPoint"]["name"] == contact_point_name
            assert payer_section[1]["contactPoint"]["email"] == contact_point_email
            assert payer_section[1]["contactPoint"]["telephone"] == contact_point_telephone
            assert payer_section[1]["contactPoint"]["faxNumber"] == contact_point_fax
            assert payer_section[1]["contactPoint"]["url"] == contact_point_url
            assert payer_section[1]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
            assert payer_section[1]["address"]["addressDetails"]["country"]["description"] == country_description
            assert payer_section[1]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
            assert payer_section[1]["address"]["addressDetails"]["region"]["description"] == region_description
            assert payer_section[1]["address"]["addressDetails"]["locality"][
                       "description"] == locality_description
            assert payer_section[1]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
            assert payer_section[1]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
            assert payer_section[1]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27037")
    def test_27037_1(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        funder_name = "name of funder"
        funder_identifier_scheme = "scheme of funder"
        funder_identifier_legal_name = "legal of funder"
        funder_identifier_legal_uri = "uri of funder"
        funder_address_street = "street"
        funder_address_postal = "postalCode"
        country_id = "MD"
        country_scheme = "iso-alpha2"
        country_description = "Moldova, Republica"
        region_id = "3400000"
        region_scheme = "CUATM"
        region_description = "Donduşeni"
        locality_scheme = "CUATM"
        locality_id = "3401000"
        locality_description = "or.Donduşeni (r-l Donduşeni)"
        funder_additional_id = "test id"
        funder_additional_scheme = "test scheme"
        funder_additional_uri = "test uri"
        funder_additional_legal = "test legal"
        contact_point_name = "name of contact"
        contact_point_email = "email of contact"
        contact_point_telephone = "telephone of contact"
        contact_point_fax = "fax of contact"
        contact_point_url = "url of contact"

        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, funder_name=funder_name,
                                                  funder_identifier_scheme=funder_identifier_scheme,
                                                  pmd=additional_value, country_id=country_id, region_id=region_id,
                                                  funder_identifier_legal_name=funder_identifier_legal_name,
                                                  funder_identifier_legal_uri=funder_identifier_legal_uri,
                                                  funder_address_street=funder_address_street,
                                                  locality_scheme=locality_scheme,
                                                  locality_id=locality_id,
                                                  funder_address_postal=funder_address_postal,
                                                  funder_additional_id=funder_additional_id,
                                                  funder_additional_scheme=funder_additional_scheme,
                                                  funder_additional_uri=funder_additional_uri,
                                                  funder_additional_legal=funder_additional_legal,
                                                  contact_point_name=contact_point_name,
                                                  contact_point_email=contact_point_email,
                                                  contact_point_telephone=contact_point_telephone,
                                                  contact_point_fax=contact_point_fax,
                                                  contact_point_url=contact_point_url,
                                                  country_scheme=country_scheme,
                                                  country_description=country_description,
                                                  region_scheme=region_scheme, region_description=region_description,
                                                  locality_description=locality_description)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27037")
    def test_27037_2(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        funder_name = "name of funder"
        funder_identifier_scheme = "scheme of funder"
        funder_identifier_legal_name = "legal of funder"
        funder_identifier_legal_uri = "uri of funder"
        funder_address_street = "street"
        funder_address_postal = "postalCode"
        country_id = "MD"
        country_scheme = "iso-alpha2"
        country_description = "Moldova, Republica"
        region_id = "3400000"
        region_scheme = "CUATM"
        region_description = "Donduşeni"
        locality_scheme = "CUATM"
        locality_id = "3401000"
        locality_description = "or.Donduşeni (r-l Donduşeni)"
        funder_additional_id = "test id"
        funder_additional_scheme = "test scheme"
        funder_additional_uri = "test uri"
        funder_additional_legal = "test legal"
        contact_point_name = "name of contact"
        contact_point_email = "email of contact"
        contact_point_telephone = "telephone of contact"
        contact_point_fax = "fax of contact"
        contact_point_url = "url of contact"

        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, funder_name=funder_name,
                                                  funder_identifier_scheme=funder_identifier_scheme,
                                                  pmd=additional_value, country_id=country_id, region_id=region_id,
                                                  funder_identifier_legal_name=funder_identifier_legal_name,
                                                  funder_identifier_legal_uri=funder_identifier_legal_uri,
                                                  funder_address_street=funder_address_street,
                                                  locality_scheme=locality_scheme,
                                                  locality_id=locality_id,
                                                  funder_address_postal=funder_address_postal,
                                                  funder_additional_id=funder_additional_id,
                                                  funder_additional_scheme=funder_additional_scheme,
                                                  funder_additional_uri=funder_additional_uri,
                                                  funder_additional_legal=funder_additional_legal,
                                                  contact_point_name=contact_point_name,
                                                  contact_point_email=contact_point_email,
                                                  contact_point_telephone=contact_point_telephone,
                                                  contact_point_fax=contact_point_fax,
                                                  contact_point_url=contact_point_url,
                                                  country_scheme=country_scheme,
                                                  country_description=country_description,
                                                  region_scheme=region_scheme, region_description=region_description,
                                                  locality_description=locality_description)
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

    @pytestrail.case("27037")
    def test_27037_3(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        funder_name = "name of funder"
        funder_identifier_scheme = "scheme of funder"
        funder_identifier_legal_name = "legal of funder"
        funder_identifier_legal_uri = "uri of funder"
        funder_address_street = "street"
        funder_address_postal = "postalCode"
        country_id = "MD"
        country_scheme = "iso-alpha2"
        country_description = "Moldova, Republica"
        region_id = "3400000"
        region_scheme = "CUATM"
        region_description = "Donduşeni"
        locality_scheme = "CUATM"
        locality_id = "3401000"
        locality_description = "or.Donduşeni (r-l Donduşeni)"
        funder_additional_id = "test id"
        funder_additional_scheme = "test scheme"
        funder_additional_uri = "test uri"
        funder_additional_legal = "test legal"
        contact_point_name = "name of contact"
        contact_point_email = "email of contact"
        contact_point_telephone = "telephone of contact"
        contact_point_fax = "fax of contact"
        contact_point_url = "url of contact"

        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, funder_name=funder_name,
                                                  funder_identifier_scheme=funder_identifier_scheme,
                                                  pmd=additional_value, country_id=country_id, region_id=region_id,
                                                  funder_identifier_legal_name=funder_identifier_legal_name,
                                                  funder_identifier_legal_uri=funder_identifier_legal_uri,
                                                  funder_address_street=funder_address_street,
                                                  locality_scheme=locality_scheme,
                                                  locality_id=locality_id,
                                                  funder_address_postal=funder_address_postal,
                                                  funder_additional_id=funder_additional_id,
                                                  funder_additional_scheme=funder_additional_scheme,
                                                  funder_additional_uri=funder_additional_uri,
                                                  funder_additional_legal=funder_additional_legal,
                                                  contact_point_name=contact_point_name,
                                                  contact_point_email=contact_point_email,
                                                  contact_point_telephone=contact_point_telephone,
                                                  contact_point_fax=contact_point_fax,
                                                  contact_point_url=contact_point_url,
                                                  country_scheme=country_scheme,
                                                  country_description=country_description,
                                                  region_scheme=region_scheme, region_description=region_description,
                                                  locality_description=locality_description)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            list_of_dictionaries = multistage["releases"][0]["parties"]
            funder_section = list()
            for d in list_of_dictionaries:
                if d["roles"][0] == "funder":
                    funder_section.append(d)

            assert funder_section[0]["id"] == f"{funder_identifier_scheme}-{funder_1}"
            assert funder_section[0]["name"] == funder_name
            assert funder_section[0]["identifier"]["scheme"] == funder_identifier_scheme
            assert funder_section[0]["identifier"]["id"] == funder_1
            assert funder_section[0]["identifier"]["legalName"] == funder_identifier_legal_name
            assert funder_section[0]["identifier"]["uri"] == funder_identifier_legal_uri
            assert funder_section[0]["address"]["streetAddress"] == funder_address_street
            assert funder_section[0]["address"]["postalCode"] == funder_address_postal
            assert funder_section[0]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
            assert funder_section[0]["address"]["addressDetails"]["country"]["id"] == country_id
            assert funder_section[0]["address"]["addressDetails"]["country"]["description"] == country_description
            assert funder_section[0]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
            assert funder_section[0]["address"]["addressDetails"]["region"]["id"] == region_id
            assert funder_section[0]["address"]["addressDetails"]["region"]["description"] == region_description
            assert funder_section[0]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
            assert funder_section[0]["address"]["addressDetails"]["locality"]["id"] == locality_id
            assert funder_section[0]["address"]["addressDetails"]["locality"][
                       "description"] == locality_description
            assert funder_section[0]["additionalIdentifiers"][0]["scheme"] == funder_additional_scheme
            assert funder_section[0]["additionalIdentifiers"][0]["id"] == funder_additional_id
            assert funder_section[0]["additionalIdentifiers"][0]["legalName"] == funder_additional_legal
            assert funder_section[0]["additionalIdentifiers"][0]["uri"] == funder_additional_uri
            assert funder_section[0]["contactPoint"]["name"] == contact_point_name
            assert funder_section[0]["contactPoint"]["email"] == contact_point_email
            assert funder_section[0]["contactPoint"]["telephone"] == contact_point_telephone
            assert funder_section[0]["contactPoint"]["faxNumber"] == contact_point_fax
            assert funder_section[0]["contactPoint"]["url"] == contact_point_url
            assert funder_section[0]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
            assert funder_section[0]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
            assert funder_section[0]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

            assert funder_section[1]["id"] == f"{funder_identifier_scheme}-{funder_2}"
            assert funder_section[1]["name"] == funder_name
            assert funder_section[1]["identifier"]["scheme"] == funder_identifier_scheme
            assert funder_section[1]["identifier"]["id"] == funder_2
            assert funder_section[1]["identifier"]["legalName"] == funder_identifier_legal_name
            assert funder_section[1]["identifier"]["uri"] == funder_identifier_legal_uri
            assert funder_section[1]["address"]["streetAddress"] == funder_address_street
            assert funder_section[1]["address"]["postalCode"] == funder_address_postal
            assert funder_section[1]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
            assert funder_section[1]["address"]["addressDetails"]["country"]["id"] == country_id
            assert funder_section[1]["address"]["addressDetails"]["country"]["description"] == country_description
            assert funder_section[1]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
            assert funder_section[1]["address"]["addressDetails"]["region"]["id"] == region_id
            assert funder_section[1]["address"]["addressDetails"]["region"]["description"] == region_description
            assert funder_section[1]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
            assert funder_section[1]["address"]["addressDetails"]["locality"]["id"] == locality_id
            assert funder_section[1]["address"]["addressDetails"]["locality"][
                       "description"] == locality_description
            assert funder_section[1]["additionalIdentifiers"][0]["scheme"] == funder_additional_scheme
            assert funder_section[1]["additionalIdentifiers"][0]["id"] == funder_additional_id
            assert funder_section[1]["additionalIdentifiers"][0]["legalName"] == funder_additional_legal
            assert funder_section[1]["additionalIdentifiers"][0]["uri"] == funder_additional_uri
            assert funder_section[1]["contactPoint"]["name"] == contact_point_name
            assert funder_section[1]["contactPoint"]["email"] == contact_point_email
            assert funder_section[1]["contactPoint"]["telephone"] == contact_point_telephone
            assert funder_section[1]["contactPoint"]["faxNumber"] == contact_point_fax
            assert funder_section[1]["contactPoint"]["url"] == contact_point_url
            assert funder_section[1]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
            assert funder_section[1]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
            assert funder_section[1]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27038")
    def test_27038_1(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        buyer_name = "name of buyer"
        buyer_identifier_scheme = "scheme of buyer"
        buyer_identifier_legal_name = "legal of buyer"
        buyer_identifier_legal_uri = "uri of buyer"
        buyer_address_street = "street"
        buyer_address_postal = "postalCode"
        country_id = "MD"
        country_scheme = "iso-alpha2"
        country_description = "Moldova, Republica"
        region_id = "3400000"
        region_scheme = "CUATM"
        region_description = "Donduşeni"
        locality_scheme = "CUATM"
        locality_id = "3401000"
        locality_description = "or.Donduşeni (r-l Donduşeni)"
        buyer_additional_id = "test id"
        buyer_additional_scheme = "test scheme"
        buyer_additional_uri = "test uri"
        buyer_additional_legal = "test legal"
        contact_point_name = "name of contact"
        contact_point_email = "email of contact"
        contact_point_telephone = "telephone of contact"
        contact_point_fax = "fax of contact"
        contact_point_url = "url of contact"
        buyer_details_type = "NATIONAL_AGENCY"
        buyer_details_general_activity = "HEALTH"
        buyer_details_sectoral_activity = "WATER"

        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, buyer_name=buyer_name,
                                                  buyer_identifier_scheme=buyer_identifier_scheme,
                                                  pmd=additional_value, country_id=country_id, region_id=region_id,
                                                  buyer_identifier_legal_name=buyer_identifier_legal_name,
                                                  buyer_identifier_uri=buyer_identifier_legal_uri,
                                                  buyer_address_street=buyer_address_street,
                                                  locality_scheme=locality_scheme,
                                                  locality_id=locality_id,
                                                  buyer_address_postal=buyer_address_postal,
                                                  buyer_additional_id=buyer_additional_id,
                                                  buyer_additional_scheme=buyer_additional_scheme,
                                                  buyer_additional_uri=buyer_additional_uri,
                                                  buyer_additional_legal=buyer_additional_legal,
                                                  contact_point_name=contact_point_name,
                                                  contact_point_email=contact_point_email,
                                                  contact_point_telephone=contact_point_telephone,
                                                  contact_point_fax=contact_point_fax,
                                                  contact_point_url=contact_point_url,
                                                  country_scheme=country_scheme,
                                                  country_description=country_description,
                                                  region_scheme=region_scheme, region_description=region_description,
                                                  locality_description=locality_description,
                                                  buyer_details_type=buyer_details_type,
                                                  buyer_details_general_activity=buyer_details_general_activity,
                                                  buyer_details_sectoral_activity=buyer_details_sectoral_activity)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27038")
    def test_27038_2(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        buyer_name = "name of buyer"
        buyer_identifier_scheme = "scheme of buyer"
        buyer_identifier_legal_name = "legal of buyer"
        buyer_identifier_legal_uri = "uri of buyer"
        buyer_address_street = "street"
        buyer_address_postal = "postalCode"
        country_id = "MD"
        country_scheme = "iso-alpha2"
        country_description = "Moldova, Republica"
        region_id = "3400000"
        region_scheme = "CUATM"
        region_description = "Donduşeni"
        locality_scheme = "CUATM"
        locality_id = "3401000"
        locality_description = "or.Donduşeni (r-l Donduşeni)"
        buyer_additional_id = "test id"
        buyer_additional_scheme = "test scheme"
        buyer_additional_uri = "test uri"
        buyer_additional_legal = "test legal"
        contact_point_name = "name of contact"
        contact_point_email = "email of contact"
        contact_point_telephone = "telephone of contact"
        contact_point_fax = "fax of contact"
        contact_point_url = "url of contact"
        buyer_details_type = "NATIONAL_AGENCY"
        buyer_details_general_activity = "HEALTH"
        buyer_details_sectoral_activity = "WATER"

        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, buyer_name=buyer_name,
                                                  buyer_identifier_scheme=buyer_identifier_scheme,
                                                  pmd=additional_value, country_id=country_id, region_id=region_id,
                                                  buyer_identifier_legal_name=buyer_identifier_legal_name,
                                                  buyer_identifier_uri=buyer_identifier_legal_uri,
                                                  buyer_address_street=buyer_address_street,
                                                  locality_scheme=locality_scheme,
                                                  locality_id=locality_id,
                                                  buyer_address_postal=buyer_address_postal,
                                                  buyer_additional_id=buyer_additional_id,
                                                  buyer_additional_scheme=buyer_additional_scheme,
                                                  buyer_additional_uri=buyer_additional_uri,
                                                  buyer_additional_legal=buyer_additional_legal,
                                                  contact_point_name=contact_point_name,
                                                  contact_point_email=contact_point_email,
                                                  contact_point_telephone=contact_point_telephone,
                                                  contact_point_fax=contact_point_fax,
                                                  contact_point_url=contact_point_url,
                                                  country_scheme=country_scheme,
                                                  country_description=country_description,
                                                  region_scheme=region_scheme, region_description=region_description,
                                                  locality_description=locality_description,
                                                  buyer_details_type=buyer_details_type,
                                                  buyer_details_general_activity=buyer_details_general_activity,
                                                  buyer_details_sectoral_activity=buyer_details_sectoral_activity)
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

    @pytestrail.case("27038")
    def test_27038_3(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        buyer_name = "name of buyer"
        buyer_identifier_scheme = "scheme of buyer"
        buyer_identifier_legal_name = "legal of buyer"
        buyer_identifier_legal_uri = "uri of buyer"
        buyer_address_street = "street"
        buyer_address_postal = "postalCode"
        country_id = "MD"
        country_scheme = "iso-alpha2"
        country_description = "Moldova, Republica"
        region_id = "3400000"
        region_scheme = "CUATM"
        region_description = "Donduşeni"
        locality_scheme = "CUATM"
        locality_id = "3401000"
        locality_description = "or.Donduşeni (r-l Donduşeni)"
        buyer_additional_id = "test id"
        buyer_additional_scheme = "test scheme"
        buyer_additional_uri = "test uri"
        buyer_additional_legal = "test legal"
        contact_point_name = "name of contact"
        contact_point_email = "email of contact"
        contact_point_telephone = "telephone of contact"
        contact_point_fax = "fax of contact"
        contact_point_url = "url of contact"
        buyer_details_type = "NATIONAL_AGENCY"
        buyer_details_general_activity = "HEALTH"
        buyer_details_sectoral_activity = "WATER"

        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, buyer_name=buyer_name,
                                                  buyer_identifier_scheme=buyer_identifier_scheme,
                                                  pmd=additional_value, country_id=country_id, region_id=region_id,
                                                  buyer_identifier_legal_name=buyer_identifier_legal_name,
                                                  buyer_identifier_uri=buyer_identifier_legal_uri,
                                                  buyer_address_street=buyer_address_street,
                                                  locality_scheme=locality_scheme,
                                                  locality_id=locality_id,
                                                  buyer_address_postal=buyer_address_postal,
                                                  buyer_additional_id=buyer_additional_id,
                                                  buyer_additional_scheme=buyer_additional_scheme,
                                                  buyer_additional_uri=buyer_additional_uri,
                                                  buyer_additional_legal=buyer_additional_legal,
                                                  contact_point_name=contact_point_name,
                                                  contact_point_email=contact_point_email,
                                                  contact_point_telephone=contact_point_telephone,
                                                  contact_point_fax=contact_point_fax,
                                                  contact_point_url=contact_point_url,
                                                  country_scheme=country_scheme,
                                                  country_description=country_description,
                                                  region_scheme=region_scheme, region_description=region_description,
                                                  locality_description=locality_description,
                                                  buyer_details_type=buyer_details_type,
                                                  buyer_details_general_activity=buyer_details_general_activity,
                                                  buyer_details_sectoral_activity=buyer_details_sectoral_activity)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            list_of_dictionaries = multistage["releases"][0]["parties"]
            buyer_section = list()
            for d in list_of_dictionaries:
                if d["roles"][0] == "buyer":
                    buyer_section.append(d)

            assert buyer_section[0]["id"] == f"{buyer_identifier_scheme}-{buyer_1}"
            assert buyer_section[0]["name"] == buyer_name
            assert buyer_section[0]["identifier"]["scheme"] == buyer_identifier_scheme
            assert buyer_section[0]["identifier"]["id"] == buyer_1
            assert buyer_section[0]["identifier"]["legalName"] == buyer_identifier_legal_name
            assert buyer_section[0]["identifier"]["uri"] == buyer_identifier_legal_uri
            assert buyer_section[0]["address"]["streetAddress"] == buyer_address_street
            assert buyer_section[0]["address"]["postalCode"] == buyer_address_postal
            assert buyer_section[0]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
            assert buyer_section[0]["address"]["addressDetails"]["country"]["id"] == country_id
            assert buyer_section[0]["address"]["addressDetails"]["country"]["description"] == country_description
            assert buyer_section[0]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
            assert buyer_section[0]["address"]["addressDetails"]["region"]["id"] == region_id
            assert buyer_section[0]["address"]["addressDetails"]["region"]["description"] == region_description
            assert buyer_section[0]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
            assert buyer_section[0]["address"]["addressDetails"]["locality"]["id"] == locality_id
            assert buyer_section[0]["address"]["addressDetails"]["locality"][
                       "description"] == locality_description
            assert buyer_section[0]["additionalIdentifiers"][0]["scheme"] == buyer_additional_scheme
            assert buyer_section[0]["additionalIdentifiers"][0]["id"] == buyer_additional_id
            assert buyer_section[0]["additionalIdentifiers"][0]["legalName"] == buyer_additional_legal
            assert buyer_section[0]["additionalIdentifiers"][0]["uri"] == buyer_additional_uri
            assert buyer_section[0]["contactPoint"]["name"] == contact_point_name
            assert buyer_section[0]["contactPoint"]["email"] == contact_point_email
            assert buyer_section[0]["contactPoint"]["telephone"] == contact_point_telephone
            assert buyer_section[0]["contactPoint"]["faxNumber"] == contact_point_fax
            assert buyer_section[0]["contactPoint"]["url"] == contact_point_url
            assert buyer_section[0]["details"]["typeOfBuyer"] == buyer_details_type
            assert buyer_section[0]["details"]["mainGeneralActivity"] == buyer_details_general_activity
            assert buyer_section[0]["details"]["mainSectoralActivity"] == buyer_details_sectoral_activity
            assert buyer_section[0]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
            assert buyer_section[0]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
            assert buyer_section[0]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

            assert buyer_section[1]["id"] == f"{buyer_identifier_scheme}-{buyer_2}"
            assert buyer_section[1]["name"] == buyer_name
            assert buyer_section[1]["identifier"]["scheme"] == buyer_identifier_scheme
            assert buyer_section[1]["identifier"]["id"] == buyer_2
            assert buyer_section[1]["identifier"]["legalName"] == buyer_identifier_legal_name
            assert buyer_section[1]["identifier"]["uri"] == buyer_identifier_legal_uri
            assert buyer_section[1]["address"]["streetAddress"] == buyer_address_street
            assert buyer_section[1]["address"]["postalCode"] == buyer_address_postal
            assert buyer_section[1]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
            assert buyer_section[1]["address"]["addressDetails"]["country"]["id"] == country_id
            assert buyer_section[1]["address"]["addressDetails"]["country"]["description"] == country_description
            assert buyer_section[1]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
            assert buyer_section[1]["address"]["addressDetails"]["region"]["id"] == region_id
            assert buyer_section[1]["address"]["addressDetails"]["region"]["description"] == region_description
            assert buyer_section[1]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
            assert buyer_section[1]["address"]["addressDetails"]["locality"]["id"] == locality_id
            assert buyer_section[1]["address"]["addressDetails"]["locality"][
                       "description"] == locality_description
            assert buyer_section[1]["additionalIdentifiers"][0]["scheme"] == buyer_additional_scheme
            assert buyer_section[1]["additionalIdentifiers"][0]["id"] == buyer_additional_id
            assert buyer_section[1]["additionalIdentifiers"][0]["legalName"] == buyer_additional_legal
            assert buyer_section[1]["additionalIdentifiers"][0]["uri"] == buyer_additional_uri
            assert buyer_section[1]["contactPoint"]["name"] == contact_point_name
            assert buyer_section[1]["contactPoint"]["email"] == contact_point_email
            assert buyer_section[1]["contactPoint"]["telephone"] == contact_point_telephone
            assert buyer_section[1]["contactPoint"]["faxNumber"] == contact_point_fax
            assert buyer_section[1]["contactPoint"]["url"] == contact_point_url
            assert buyer_section[1]["details"]["typeOfBuyer"] == buyer_details_type
            assert buyer_section[1]["details"]["mainGeneralActivity"] == buyer_details_general_activity
            assert buyer_section[1]["details"]["mainSectoralActivity"] == buyer_details_sectoral_activity
            assert buyer_section[1]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
            assert buyer_section[1]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
            assert buyer_section[1]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27039")
    def test_27039_1(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27039")
    def test_27039_2(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27039")
    def test_27039_3(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            list_of_dictionaries = multistage["releases"][0]["relatedProcesses"]
            related_processes_section = list()
            for d in list_of_dictionaries:
                if d["relationship"][0] == "x_fundingSource":
                    related_processes_section.append(d)

            url_fs_1 = related_processes_section[0]["uri"]
            url_fs_2 = related_processes_section[1]["uri"]
            source_entity_fs_1 = requests.get(url=url_fs_1).json()["releases"][0]["planning"]["budget"]["sourceEntity"]
            source_entity_fs_2 = requests.get(url=url_fs_2).json()["releases"][0]["planning"]["budget"]["sourceEntity"]

            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["id"] == \
                   related_processes_section[0]["identifier"]
            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["sourceParty"]["id"] == \
                   source_entity_fs_1["id"]
            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["sourceParty"]["name"] == \
                   source_entity_fs_1["name"]

            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][1]["id"] == \
                   related_processes_section[1]["identifier"]
            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][1]["sourceParty"]["id"] == \
                   source_entity_fs_2["id"]
            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][1]["sourceParty"]["name"] == \
                   source_entity_fs_2["name"]
        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27040")
    def test_27040_1(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value,
                                                  seconds=60)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27040")
    def test_27040_2(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value,
                                                  seconds=60)
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

    @pytestrail.case("27040")
    def test_27040_3(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value,
                                                  seconds=60)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            list_of_dictionaries = multistage["releases"][0]["relatedProcesses"]
            related_processes_section = list()
            for d in list_of_dictionaries:
                if d["relationship"][0] == "x_fundingSource":
                    related_processes_section.append(d)

            url_fs_1 = related_processes_section[0]["uri"]
            url_fs_2 = related_processes_section[1]["uri"]
            period_fs_1 = requests.get(url=url_fs_1).json()["releases"][0]["planning"]["budget"]["period"]
            period_fs_2 = requests.get(url=url_fs_2).json()["releases"][0]["planning"]["budget"]["period"]

            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["id"] == \
                   related_processes_section[0]["identifier"]
            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["period"]["startDate"] == \
                   period_fs_1["startDate"]
            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][0]["period"]["endDate"] == \
                   period_fs_1["endDate"]

            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][1]["id"] == \
                   related_processes_section[1]["identifier"]
            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][1]["period"]["startDate"] == \
                   period_fs_2["startDate"]
            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][1]["period"]["endDate"] == \
                   period_fs_2["endDate"]
        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27041")
    def test_27041_1(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27041")
    def test_27041_2(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27041")
    def test_27041_3(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            list_of_dictionaries = multistage["releases"][0]["relatedProcesses"]
            related_processes_section = list()
            for d in list_of_dictionaries:
                if d["relationship"][0] == "x_expenditureItem":
                    related_processes_section.append(d)

            id_1 = fnmatch.fnmatch(related_processes_section[0]["id"], "*")
            assert id_1 == True
            assert related_processes_section[0]["relationship"] == ["x_expenditureItem"]
            assert related_processes_section[0]["scheme"] == "ocid"
            assert related_processes_section[0]["identifier"] == cpid_1
            assert related_processes_section[0][
                       "uri"] == f"http://dev.public.eprocurement.systems/budgets/{cpid_1}/{cpid_1}"

            id_2 = fnmatch.fnmatch(related_processes_section[1]["id"], "*")
            assert id_2 == True
            assert related_processes_section[1]["relationship"] == ["x_expenditureItem"]
            assert related_processes_section[1]["scheme"] == "ocid"
            assert related_processes_section[1]["identifier"] == cpid_2
            assert related_processes_section[1][
                       "uri"] == f"http://dev.public.eprocurement.systems/budgets/{cpid_2}/{cpid_2}"

        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    @pytestrail.case("27042")
    def test_27042_1(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27042")
    def test_27042_2(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27042")
    def test_27042_3(self, additional_value):
        cpid_1 = prepared_cpid()
        buyer_1 = "1"
        payer_1 = "2"
        funder_1 = "3"
        cpid_2 = prepared_cpid()
        buyer_2 = "11"
        payer_2 = "22"
        funder_2 = "33"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 1000,
                    "currency": "EUR"
                }
            }
        ]

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
                                                  cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
                                                  funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
        check_record = fnmatch.fnmatch(
            get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
        if check_record == True:
            multistage = requests.get(
                url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
            list_of_dictionaries = multistage["releases"][0]["relatedProcesses"]
            related_processes_section = list()
            for d in list_of_dictionaries:
                if d["relationship"][0] == "x_fundingSource":
                    related_processes_section.append(d)
            url_fs_1 = related_processes_section[0]["uri"]
            url_fs_2 = related_processes_section[1]["uri"]
            description_fs_1 = requests.get(url=url_fs_1).json()["releases"][0]["planning"]["budget"]["description"]

            description_fs_2 = requests.get(url=url_fs_2).json()["releases"][0]["planning"]["budget"]["description"]

            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][0][
                       "description"] == description_fs_1
            assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][0][
                       "description"] == description_fs_2
        else:
            assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"

    # @pytestrail.case("27043")
    # def test_27043_1(self, additional_value):
    #     cpid_1 = prepared_cpid()
    #     buyer_1 = "1"
    #     payer_1 = "2"
    #     funder_1 = "3"
    #     cpid_2 = prepared_cpid()
    #     buyer_2 = "11"
    #     payer_2 = "22"
    #     funder_2 = "33"
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["planning"]["budget"]["budgetBreakdown"] = [
    #         {
    #             "id": "{{fs-id}}",
    #             "amount": {
    #                 "amount": 1000,
    #                 "currency": "EUR"
    #             }
    #         },
    #         {
    #             "id": "{{fs-id}}",
    #             "amount": {
    #                 "amount": 1000,
    #                 "currency": "EUR"
    #             }
    #         }
    #     ]
    #
    #     create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
    #                                               cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
    #                                               funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
    #     assert create_pn_response[0].text == "ok"
    #     assert create_pn_response[0].status_code == 202
    #
    # @pytestrail.case("27043")
    # def test_27043_2(self, additional_value):
    #     cpid_1 = prepared_cpid()
    #     buyer_1 = "1"
    #     payer_1 = "2"
    #     funder_1 = "3"
    #     cpid_2 = prepared_cpid()
    #     buyer_2 = "11"
    #     payer_2 = "22"
    #     funder_2 = "33"
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["planning"]["budget"]["budgetBreakdown"] = [
    #         {
    #             "id": "{{fs-id}}",
    #             "amount": {
    #                 "amount": 1000,
    #                 "currency": "EUR"
    #             }
    #         },
    #         {
    #             "id": "{{fs-id}}",
    #             "amount": {
    #                 "amount": 1000,
    #                 "currency": "EUR"
    #             }
    #         }
    #     ]
    #
    #     create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
    #                                               cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
    #                                               funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
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
    # @pytestrail.case("27043")
    # def test_27043_3(self, additional_value):
    #     cpid_1 = prepared_cpid()
    #     buyer_1 = "1"
    #     payer_1 = "2"
    #     funder_1 = "3"
    #     cpid_2 = prepared_cpid()
    #     buyer_2 = "11"
    #     payer_2 = "22"
    #     funder_2 = "33"
    #     payload = copy.deepcopy(pn_create_full_data_model_with_documents)
    #     payload["planning"]["budget"]["budgetBreakdown"] = [
    #         {
    #             "id": "{{fs-id}}",
    #             "amount": {
    #                 "amount": 1000,
    #                 "currency": "EUR"
    #             }
    #         },
    #         {
    #             "id": "{{fs-id}}",
    #             "amount": {
    #                 "amount": 1000,
    #                 "currency": "EUR"
    #             }
    #         }
    #     ]
    #
    #     create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, buyer_1=buyer_1, payer_1=payer_1, funder_1=funder_1,
    #                                               cpid_2=cpid_2, buyer_2=buyer_2, payer_2=payer_2,
    #                                               funder_2=funder_2, pn_create_payload=payload, pmd=additional_value)
    #     get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()
    #     check_record = fnmatch.fnmatch(
    #         get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0], "parent")
    #     if check_record == True:
    #         multistage = requests.get(
    #             url=get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
    #         list_of_dictionaries = multistage["releases"][0]["relatedProcesses"]
    #         related_processes_section = list()
    #         for d in list_of_dictionaries:
    #             if d["relationship"][0] == "x_fundingSource":
    #                 related_processes_section.append(d)
    #         url_fs_1 = related_processes_section[0]["uri"]
    #         url_fs_2 = related_processes_section[1]["uri"]
    #         description_fs_1 = requests.get(url=url_fs_1).json()["releases"][0]["planning"]["budget"]["description"]
    #
    #         description_fs_2 = requests.get(url=url_fs_2).json()["releases"][0]["planning"]["budget"]["description"]
    #
    #         assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][0][
    #                    "description"] == description_fs_1
    #         assert multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"][0][
    #                    "description"] == description_fs_2
    #     else:
    #         assert get_url["records"][1]["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent"
