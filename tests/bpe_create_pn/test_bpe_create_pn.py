import copy
import datetime
import fnmatch
import json
import time
import uuid

import requests
from pytest_testrail.plugin import pytestrail
from tests.Cassandra_session import execute_cql_from_orchestrator_context
from tests.authorization import get_x_operation_id, get_access_token_for_platform_one
from tests.bpe_create_pn.create_pn import bpe_create_pn_one_fs, bpe_create_pn_two_fs
from tests.bpe_create_pn.payloads import pn_create_full_data_model_with_documents, \
    pn_create_obligatory_data_model_without_documents
from tests.cassandra_inserts_into_Database import insert_into_db_create_fs
from tests.kafka_messages import get_message_from_kafka
from tests.presets import set_instance_for_request, create_pn
from useful_functions import prepared_cpid, get_access_token_for_platform_two, is_it_uuid, prepared_fs_ocid, \
    prepared_test_cpid, get_contract_period, get_human_date_in_utc_format, get_timestamp_from_human_date, get_period, \
    is_valid_uuid

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
procurement_method = {
    "SV": "open",
    "MV": "open",
    "OT": "open"
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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert planning_notice["releases"][0]["tender"]["classification"]["id"] == "45112300-8"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert planning_notice["releases"][0]["tender"]["classification"]["id"] == "45112300-8"
        assert planning_notice["releases"][0]["tender"]["classification"]["scheme"] == "CPV"
        assert planning_notice["releases"][0]["tender"]["classification"][
                   "description"] == "Lucrări de rambleiere şi de asanare a terenului"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert multistage["releases"][0]["tender"]["mainProcurementCategory"] == "works"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert planning_notice["releases"][0]["tender"]["items"][0]["classification"]["scheme"] == "CPV"
        assert planning_notice["releases"][0]["tender"]["items"][0]["classification"]["id"] == \
               payload["tender"]["items"][0]["classification"]["id"]
        assert planning_notice["releases"][0]["tender"]["items"][0]["classification"][
                   "description"] == "Lucrări de valorificare a terenurilor virane"

    @pytestrail.case("27021")
    def test_27021_4(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["classification"]["id"] = "45112350-3"
        payload["tender"]["items"][1]["classification"]["id"] = "45112360-6"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert planning_notice["releases"][0]["tender"]["items"][1]["classification"]["scheme"] == "CPV"
        assert planning_notice["releases"][0]["tender"]["items"][1]["classification"]["id"] == \
               payload["tender"]["items"][1]["classification"]["id"]
        assert planning_notice["releases"][0]["tender"]["items"][1]["classification"][
                   "description"] == "Lucrări de reabilitare a terenului"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert planning_notice["releases"][0]["tender"]["items"][0]["unit"]["id"] == \
               payload["tender"]["items"][0]["unit"]["id"]
        assert planning_notice["releases"][0]["tender"]["items"][0]["unit"]["name"] == "Parsec"

    @pytestrail.case("27022")
    def test_27022_4(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["unit"]["id"] = "10"
        payload["tender"]["items"][1]["unit"]["id"] = "120"
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert planning_notice["releases"][0]["tender"]["items"][1]["unit"]["id"] == \
               payload["tender"]["items"][1]["unit"]["id"]
        assert planning_notice["releases"][0]["tender"]["items"][1]["unit"]["name"] == "Milion decalitri"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "country"]["id"] == \
            payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"]

        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "country"]["scheme"] == "iso-alpha2"
        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "country"]["description"] == "Moldova, Republica"
        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "country"]["uri"] == "https://www.iso.org"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "region"]["id"] == \
            payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"]

        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "region"]["scheme"] == "CUATM"
        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "region"]["description"] == "Donduşeni"
        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "region"]["uri"] == "http://statistica.md"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "locality"]["id"] == \
            payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"]

        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "locality"]["scheme"] == \
            payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
                "scheme"]
        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "locality"]["description"] == "or.Donduşeni (r-l Donduşeni)"
        assert \
            planning_notice["releases"][0]["tender"]["lots"][0]["placeOfPerformance"]["address"][
                "addressDetails"][
                "locality"]["uri"] == "http://statistica.md"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["procurementMethodDetails"] == procurement_method_details[
            additional_value]
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert planning_notice["releases"][0]["tender"]["submissionMethodRationale"][0] == \
               procurement_method_rationale[
                   additional_value]
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    related_processes_list.append(d_1)
        planning_notice = requests.get(url=related_processes_list[0]["uri"]).json()
        assert planning_notice["releases"][0]["tender"]["submissionMethodDetails"] == \
               submission_method_details[additional_value]
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["eligibilityCriteria"] == \
               eligibility_criteria[additional_value]
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[0]["uri"]).json()
        list_of_dictionaries = list()
        for f in multistage["releases"][0]["parties"]:
            if f["roles"] == ["procuringEntity"]:
                list_of_dictionaries.append(f)
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["id"] == \
               payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"]
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["scheme"] == "iso-alpha2"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["description"] == "Moldova, Republica"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[0]["uri"]).json()
        list_of_dictionaries = list()
        for f in multistage["releases"][0]["parties"]:
            if f["roles"] == ["procuringEntity"]:
                list_of_dictionaries.append(f)
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["id"] == \
               payload["tender"]["procuringEntity"]["address"]["addressDetails"]["region"]["id"]
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"][
                   "scheme"] == "CUATM"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"][
                   "description"] == "Donduşeni"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"][
                   "uri"] == "http://statistica.md"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[0]["uri"]).json()
        list_of_dictionaries = list()
        for f in multistage["releases"][0]["parties"]:
            if f["roles"] == ["procuringEntity"]:
                list_of_dictionaries.append(f)
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"]["id"] == \
               payload["tender"]["procuringEntity"]["address"]["addressDetails"]["locality"]["id"]
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"][
                   "scheme"] == "CUATM"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"][
                   "description"] == "or.Donduşeni (r-l Donduşeni)"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"][
                   "uri"] == "http://statistica.md"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[0]["uri"]).json()
        list_of_dictionaries = list()
        for f in multistage["releases"][0]["parties"]:
            if f["roles"] == ["payer"]:
                list_of_dictionaries.append(f)
        assert list_of_dictionaries[0]["id"] == f"{payer_identifier_scheme}-{payer_1}"
        assert list_of_dictionaries[0]["identifier"]["id"] == payer_1
        assert list_of_dictionaries[0]["name"] == payer_name
        assert list_of_dictionaries[0]["identifier"]["scheme"] == payer_identifier_scheme
        assert list_of_dictionaries[0]["identifier"]["legalName"] == payer_identifier_legal_name
        assert list_of_dictionaries[0]["identifier"]["uri"] == payer_identifier_legal_uri
        assert list_of_dictionaries[0]["address"]["streetAddress"] == payer_address_street
        assert list_of_dictionaries[0]["address"]["postalCode"] == payer_address_postal
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"]["id"] == locality_id
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["id"] == country_id
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["id"] == region_id
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["scheme"] == payer_additional_scheme
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["id"] == payer_additional_id
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["legalName"] == payer_additional_legal
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["uri"] == payer_additional_uri
        assert list_of_dictionaries[0]["contactPoint"]["name"] == contact_point_name
        assert list_of_dictionaries[0]["contactPoint"]["email"] == contact_point_email
        assert list_of_dictionaries[0]["contactPoint"]["telephone"] == contact_point_telephone
        assert list_of_dictionaries[0]["contactPoint"]["faxNumber"] == contact_point_fax
        assert list_of_dictionaries[0]["contactPoint"]["url"] == contact_point_url
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["description"] == country_description
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["description"] == region_description
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"][
                   "description"] == locality_description
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

        assert list_of_dictionaries[1]["id"] == f"{payer_identifier_scheme}-{payer_2}"
        assert list_of_dictionaries[1]["identifier"]["id"] == payer_2
        assert list_of_dictionaries[1]["name"] == payer_name
        assert list_of_dictionaries[1]["identifier"]["scheme"] == payer_identifier_scheme
        assert list_of_dictionaries[1]["identifier"]["legalName"] == payer_identifier_legal_name
        assert list_of_dictionaries[1]["identifier"]["uri"] == payer_identifier_legal_uri
        assert list_of_dictionaries[1]["address"]["streetAddress"] == payer_address_street
        assert list_of_dictionaries[1]["address"]["postalCode"] == payer_address_postal
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"]["id"] == locality_id
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["id"] == country_id
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["id"] == region_id
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["scheme"] == payer_additional_scheme
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["id"] == payer_additional_id
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["legalName"] == payer_additional_legal
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["uri"] == payer_additional_uri
        assert list_of_dictionaries[1]["contactPoint"]["name"] == contact_point_name
        assert list_of_dictionaries[1]["contactPoint"]["email"] == contact_point_email
        assert list_of_dictionaries[1]["contactPoint"]["telephone"] == contact_point_telephone
        assert list_of_dictionaries[1]["contactPoint"]["faxNumber"] == contact_point_fax
        assert list_of_dictionaries[1]["contactPoint"]["url"] == contact_point_url
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["description"] == country_description
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["description"] == region_description
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"][
                   "description"] == locality_description
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[0]["uri"]).json()
        list_of_dictionaries = list()
        for f in multistage["releases"][0]["parties"]:
            if f["roles"] == ["funder"]:
                list_of_dictionaries.append(f)
        assert list_of_dictionaries[0]["id"] == f"{funder_identifier_scheme}-{funder_1}"
        assert list_of_dictionaries[0]["name"] == funder_name
        assert list_of_dictionaries[0]["identifier"]["scheme"] == funder_identifier_scheme
        assert list_of_dictionaries[0]["identifier"]["id"] == funder_1
        assert list_of_dictionaries[0]["identifier"]["legalName"] == funder_identifier_legal_name
        assert list_of_dictionaries[0]["identifier"]["uri"] == funder_identifier_legal_uri
        assert list_of_dictionaries[0]["address"]["streetAddress"] == funder_address_street
        assert list_of_dictionaries[0]["address"]["postalCode"] == funder_address_postal
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["id"] == country_id
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["description"] == country_description
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["id"] == region_id
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["description"] == region_description
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"]["id"] == locality_id
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"][
                   "description"] == locality_description
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["scheme"] == funder_additional_scheme
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["id"] == funder_additional_id
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["legalName"] == funder_additional_legal
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["uri"] == funder_additional_uri
        assert list_of_dictionaries[0]["contactPoint"]["name"] == contact_point_name
        assert list_of_dictionaries[0]["contactPoint"]["email"] == contact_point_email
        assert list_of_dictionaries[0]["contactPoint"]["telephone"] == contact_point_telephone
        assert list_of_dictionaries[0]["contactPoint"]["faxNumber"] == contact_point_fax
        assert list_of_dictionaries[0]["contactPoint"]["url"] == contact_point_url
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

        assert list_of_dictionaries[1]["id"] == f"{funder_identifier_scheme}-{funder_2}"
        assert list_of_dictionaries[1]["name"] == funder_name
        assert list_of_dictionaries[1]["identifier"]["scheme"] == funder_identifier_scheme
        assert list_of_dictionaries[1]["identifier"]["id"] == funder_2
        assert list_of_dictionaries[1]["identifier"]["legalName"] == funder_identifier_legal_name
        assert list_of_dictionaries[1]["identifier"]["uri"] == funder_identifier_legal_uri
        assert list_of_dictionaries[1]["address"]["streetAddress"] == funder_address_street
        assert list_of_dictionaries[1]["address"]["postalCode"] == funder_address_postal
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["id"] == country_id
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["description"] == country_description
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["id"] == region_id
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["description"] == region_description
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"]["id"] == locality_id
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"][
                   "description"] == locality_description
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["scheme"] == funder_additional_scheme
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["id"] == funder_additional_id
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["legalName"] == funder_additional_legal
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["uri"] == funder_additional_uri
        assert list_of_dictionaries[1]["contactPoint"]["name"] == contact_point_name
        assert list_of_dictionaries[1]["contactPoint"]["email"] == contact_point_email
        assert list_of_dictionaries[1]["contactPoint"]["telephone"] == contact_point_telephone
        assert list_of_dictionaries[1]["contactPoint"]["faxNumber"] == contact_point_fax
        assert list_of_dictionaries[1]["contactPoint"]["url"] == contact_point_url
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[0]["uri"]).json()
        list_of_dictionaries = list()
        for f in multistage["releases"][0]["parties"]:
            if f["roles"] == ["buyer"]:
                list_of_dictionaries.append(f)
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["id"] == \
               payload["tender"]["procuringEntity"]["address"]["addressDetails"]["country"]["id"]
        assert list_of_dictionaries[0]["id"] == f"{buyer_identifier_scheme}-{buyer_1}"
        assert list_of_dictionaries[0]["name"] == buyer_name
        assert list_of_dictionaries[0]["identifier"]["scheme"] == buyer_identifier_scheme
        assert list_of_dictionaries[0]["identifier"]["id"] == buyer_1
        assert list_of_dictionaries[0]["identifier"]["legalName"] == buyer_identifier_legal_name
        assert list_of_dictionaries[0]["identifier"]["uri"] == buyer_identifier_legal_uri
        assert list_of_dictionaries[0]["address"]["streetAddress"] == buyer_address_street
        assert list_of_dictionaries[0]["address"]["postalCode"] == buyer_address_postal
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["id"] == country_id
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["description"] == country_description
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["id"] == region_id
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["description"] == region_description
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"]["id"] == locality_id
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"][
                   "description"] == locality_description
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["scheme"] == buyer_additional_scheme
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["id"] == buyer_additional_id
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["legalName"] == buyer_additional_legal
        assert list_of_dictionaries[0]["additionalIdentifiers"][0]["uri"] == buyer_additional_uri
        assert list_of_dictionaries[0]["contactPoint"]["name"] == contact_point_name
        assert list_of_dictionaries[0]["contactPoint"]["email"] == contact_point_email
        assert list_of_dictionaries[0]["contactPoint"]["telephone"] == contact_point_telephone
        assert list_of_dictionaries[0]["contactPoint"]["faxNumber"] == contact_point_fax
        assert list_of_dictionaries[0]["contactPoint"]["url"] == contact_point_url
        assert list_of_dictionaries[0]["details"]["typeOfBuyer"] == buyer_details_type
        assert list_of_dictionaries[0]["details"]["mainGeneralActivity"] == buyer_details_general_activity
        assert list_of_dictionaries[0]["details"]["mainSectoralActivity"] == buyer_details_sectoral_activity
        assert list_of_dictionaries[0]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
        assert list_of_dictionaries[0]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

        assert list_of_dictionaries[1]["id"] == f"{buyer_identifier_scheme}-{buyer_2}"
        assert list_of_dictionaries[1]["name"] == buyer_name
        assert list_of_dictionaries[1]["identifier"]["scheme"] == buyer_identifier_scheme
        assert list_of_dictionaries[1]["identifier"]["id"] == buyer_2
        assert list_of_dictionaries[1]["identifier"]["legalName"] == buyer_identifier_legal_name
        assert list_of_dictionaries[1]["identifier"]["uri"] == buyer_identifier_legal_uri
        assert list_of_dictionaries[1]["address"]["streetAddress"] == buyer_address_street
        assert list_of_dictionaries[1]["address"]["postalCode"] == buyer_address_postal
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["scheme"] == country_scheme
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["id"] == country_id
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["description"] == country_description
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["scheme"] == region_scheme
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["id"] == region_id
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["description"] == region_description
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"]["scheme"] == locality_scheme
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"]["id"] == locality_id
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"][
                   "description"] == locality_description
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["scheme"] == buyer_additional_scheme
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["id"] == buyer_additional_id
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["legalName"] == buyer_additional_legal
        assert list_of_dictionaries[1]["additionalIdentifiers"][0]["uri"] == buyer_additional_uri
        assert list_of_dictionaries[1]["contactPoint"]["name"] == contact_point_name
        assert list_of_dictionaries[1]["contactPoint"]["email"] == contact_point_email
        assert list_of_dictionaries[1]["contactPoint"]["telephone"] == contact_point_telephone
        assert list_of_dictionaries[1]["contactPoint"]["faxNumber"] == contact_point_fax
        assert list_of_dictionaries[1]["contactPoint"]["url"] == contact_point_url
        assert list_of_dictionaries[1]["details"]["typeOfBuyer"] == buyer_details_type
        assert list_of_dictionaries[1]["details"]["mainGeneralActivity"] == buyer_details_general_activity
        assert list_of_dictionaries[1]["details"]["mainSectoralActivity"] == buyer_details_sectoral_activity
        assert list_of_dictionaries[1]["address"]["addressDetails"]["country"]["uri"] == "https://www.iso.org"
        assert list_of_dictionaries[1]["address"]["addressDetails"]["region"]["uri"] == "http://statistica.md"
        assert list_of_dictionaries[1]["address"]["addressDetails"]["locality"]["uri"] == "http://statistica.md"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)

        url_fs_1 = related_processes_list[0]["uri"]
        url_fs_2 = related_processes_list[1]["uri"]
        multistage = requests.get(url=related_processes_list[2]["uri"]).json()
        fs_1 = requests.get(url=url_fs_1).json()
        fs_2 = requests.get(url=url_fs_2).json()
        ocid_fs_1 = fs_1["releases"][0]["ocid"]
        source_entity_fs_1 = fs_1["releases"][0]["planning"]["budget"]["sourceEntity"]
        ocid_fs_2 = fs_2["releases"][0]["ocid"]
        source_entity_fs_2 = fs_2["releases"][0]["planning"]["budget"]["sourceEntity"]
        for r in multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"]:
            if r["id"] == ocid_fs_1:
                assert r["sourceParty"]["id"] == source_entity_fs_1["id"]
                assert r["sourceParty"]["name"] == source_entity_fs_1["name"]
            if r["id"] == ocid_fs_2:
                assert r["sourceParty"]["id"] == source_entity_fs_2["id"]
                assert r["sourceParty"]["name"] == source_entity_fs_2["name"]

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[2]["uri"]).json()
        fs_1 = requests.get(url=related_processes_list[0]["uri"]).json()
        fs_2 = requests.get(url=related_processes_list[1]["uri"]).json()
        for r in multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"]:
            if r["id"] == fs_1["releases"][0]["ocid"]:
                assert r["period"]["startDate"] == fs_1["releases"][0]["planning"]["budget"]["period"]["startDate"]
                assert r["period"]["endDate"] == fs_1["releases"][0]["planning"]["budget"]["period"]["endDate"]
            if r["id"] == fs_2["releases"][0]["ocid"]:
                assert r["period"]["startDate"] == fs_2["releases"][0]["planning"]["budget"]["period"]["startDate"]
                assert r["period"]["endDate"] == fs_2["releases"][0]["planning"]["budget"]["period"]["endDate"]

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        multistage = requests.get(url=related_processes_list[0]["uri"]).json()
        related_processes_section = list()
        for f in multistage["releases"][0]["relatedProcesses"]:
            if f["relationship"] == ["x_expenditureItem"]:
                related_processes_section.append(f)
        id_1 = is_it_uuid(related_processes_section[0]["id"], 1)
        assert id_1 == True
        assert related_processes_section[0]["relationship"] == ["x_expenditureItem"]
        assert related_processes_section[0]["scheme"] == "ocid"
        assert related_processes_section[0]["identifier"] == cpid_1
        assert related_processes_section[0][
                   "uri"] == f"http://dev.public.eprocurement.systems/budgets/{cpid_1}/{cpid_1}"

        id_2 = is_it_uuid(related_processes_section[1]["id"], 1)
        assert id_2 == True
        assert related_processes_section[1]["relationship"] == ["x_expenditureItem"]
        assert related_processes_section[1]["scheme"] == "ocid"
        assert related_processes_section[1]["identifier"] == cpid_2
        assert related_processes_section[1][
                   "uri"] == f"http://dev.public.eprocurement.systems/budgets/{cpid_2}/{cpid_2}"

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
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)

        url_fs_1 = related_processes_list[0]["uri"]
        url_fs_2 = related_processes_list[1]["uri"]
        multistage = requests.get(url=related_processes_list[2]["uri"]).json()
        fs_1 = requests.get(url=url_fs_1).json()
        fs_2 = requests.get(url=url_fs_2).json()
        ocid_fs_1 = fs_1["releases"][0]["ocid"]
        ocid_fs_2 = fs_2["releases"][0]["ocid"]
        for r in multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"]:
            if r["id"] == ocid_fs_1:
                assert r["description"] == fs_1["releases"][0]["planning"]["budget"]["description"]
            if r["id"] == ocid_fs_2:
                assert r["description"] == fs_2["releases"][0]["planning"]["budget"]["description"]

    @pytestrail.case("27043")
    def test_27043_1(self, additional_value):
        cpid_1 = prepared_cpid()
        cpid_2 = prepared_cpid()

        is_european_union_fund_fs_1 = False
        is_european_union_fund_fs_2 = True
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

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value,
                                                  is_european_funding_1=is_european_union_fund_fs_1,
                                                  is_european_funding_2=is_european_union_fund_fs_2)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27043")
    def test_27043_2(self, additional_value):
        cpid_1 = prepared_cpid()
        cpid_2 = prepared_cpid()

        is_european_union_fund_fs_1 = False
        is_european_union_fund_fs_2 = True
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

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value,
                                                  is_european_funding_1=is_european_union_fund_fs_1,
                                                  is_european_funding_2=is_european_union_fund_fs_2)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
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

    @pytestrail.case("27043")
    def test_27043_3(self, additional_value):
        cpid_1 = prepared_cpid()
        cpid_2 = prepared_cpid()

        is_european_union_fund_fs_1 = False
        is_european_union_fund_fs_2 = True
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

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value,
                                                  is_european_funding_1=is_european_union_fund_fs_1,
                                                  is_european_funding_2=is_european_union_fund_fs_2)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        url_fs_1 = related_processes_list[0]["uri"]
        url_fs_2 = related_processes_list[1]["uri"]
        multistage = requests.get(url=related_processes_list[2]["uri"]).json()
        fs_1 = requests.get(url=url_fs_1).json()
        fs_2 = requests.get(url=url_fs_2).json()
        is_european_funded_fs_1 = fs_1["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"]
        is_european_funded_fs_2 = fs_2["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"]
        if is_european_funded_fs_1 == True and is_european_funded_fs_2 == False:
            assert multistage["releases"][0]["planning"]["budget"][
                       "isEuropeanUnionFunded"] == is_european_funded_fs_1
            assert multistage["releases"][0]["planning"]["budget"][
                       "isEuropeanUnionFunded"] != is_european_funded_fs_2
        elif is_european_funded_fs_1 == False and is_european_funded_fs_2 == True:
            assert multistage["releases"][0]["planning"]["budget"][
                       "isEuropeanUnionFunded"] != is_european_funded_fs_1
            assert multistage["releases"][0]["planning"]["budget"][
                       "isEuropeanUnionFunded"] == is_european_funded_fs_2

    @pytestrail.case("27044")
    def test_27044_1(self, additional_value):
        cpid_1 = prepared_cpid()
        cpid_2 = prepared_cpid()

        is_european_union_fund_fs_1 = False
        is_european_union_fund_fs_2 = True
        european_project_name = "The new eropean name"
        european_project_id = "The new european id"
        european_project_uri = "The new eripean uri"
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

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value,
                                                  is_european_funding_1=is_european_union_fund_fs_1,
                                                  is_european_funding_2=is_european_union_fund_fs_2,
                                                  european_project_name=european_project_name,
                                                  european_project_id=european_project_id,
                                                  european_project_uri=european_project_uri
                                                  )
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27044")
    def test_27044_2(self, additional_value):
        cpid_1 = prepared_cpid()
        cpid_2 = prepared_cpid()

        is_european_union_fund_fs_1 = False
        is_european_union_fund_fs_2 = True
        european_project_name = "The new eropean name"
        european_project_id = "The new european id"
        european_project_uri = "The new eripean uri"
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

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value,
                                                  is_european_funding_1=is_european_union_fund_fs_1,
                                                  is_european_funding_2=is_european_union_fund_fs_2,
                                                  european_project_name=european_project_name,
                                                  european_project_id=european_project_id,
                                                  european_project_uri=european_project_uri
                                                  )
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
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

    @pytestrail.case("27044")
    def test_27044_3(self, additional_value):
        cpid_1 = prepared_cpid()
        cpid_2 = prepared_cpid()

        is_european_union_fund_fs_1 = False
        is_european_union_fund_fs_2 = True
        european_project_name = "The new eropean name"
        european_project_id = "The new european id"
        european_project_uri = "The new eripean uri"
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

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value,
                                                  is_european_funding_1=is_european_union_fund_fs_1,
                                                  is_european_funding_2=is_european_union_fund_fs_2,
                                                  european_project_name=european_project_name,
                                                  european_project_id=european_project_id,
                                                  european_project_uri=european_project_uri
                                                  )
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        related_processes_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_processes_list.append(d_1)
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        url_fs_1 = related_processes_list[0]["uri"]
        url_fs_2 = related_processes_list[1]["uri"]
        multistage = requests.get(url=related_processes_list[2]["uri"]).json()
        fs_1 = requests.get(url=url_fs_1).json()
        fs_2 = requests.get(url=url_fs_2).json()
        european_union_funded_list = list()
        if fs_1["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"] == True:
            european_union_funded_list.append(fs_1["releases"][0]["ocid"])
            european_union_funded_list.append(fs_1["releases"][0]["planning"]["budget"]["europeanUnionFunding"])
        if fs_2["releases"][0]["planning"]["budget"]["isEuropeanUnionFunded"] == True:
            european_union_funded_list.append(fs_2["releases"][0]["ocid"])
            european_union_funded_list.append(fs_2["releases"][0]["planning"]["budget"]["europeanUnionFunding"])
        for r in multistage["releases"][0]["planning"]["budget"]["budgetBreakdown"]:
            if r["id"] == european_union_funded_list[0]:
                assert r["europeanUnionFunding"]["projectIdentifier"] == european_union_funded_list[1][
                    "projectIdentifier"]
                assert r["europeanUnionFunding"]["projectName"] == european_union_funded_list[1]["projectName"]
                assert r["europeanUnionFunding"]["uri"] == european_union_funded_list[1]["uri"]

    @pytestrail.case("27045")
    def test_27045_1(self, additional_value):
        cpid_1 = prepared_cpid()
        cpid_2 = prepared_cpid()

        amount_fs_1 = 150.00
        amount_fs_2 = 155.00
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 98,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 99,
                    "currency": "EUR"
                }
            }
        ]
        payload["tender"]["lots"][0]["value"]["amount"] = 95
        payload["tender"]["lots"][1]["value"]["amount"] = 95

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value, amount_1=amount_fs_1, amount_2=amount_fs_2
                                                  )

        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27045")
    def test_27045_2(self, additional_value):
        cpid_1 = prepared_cpid()
        cpid_2 = prepared_cpid()

        amount_fs_1 = 150.00
        amount_fs_2 = 155.00
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 98,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 99,
                    "currency": "EUR"
                }
            }
        ]
        payload["tender"]["lots"][0]["value"]["amount"] = 95
        payload["tender"]["lots"][1]["value"]["amount"] = 95

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value, amount_1=amount_fs_1, amount_2=amount_fs_2
                                                  )
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
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

    @pytestrail.case("27045")
    def test_27045_3(self, additional_value):
        cpid_1 = prepared_cpid()
        cpid_2 = prepared_cpid()

        amount_fs_1 = 150.00
        amount_fs_2 = 155.00
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 98,
                    "currency": "EUR"
                }
            },
            {
                "id": "{{fs-id}}",
                "amount": {
                    "amount": 99,
                    "currency": "EUR"
                }
            }
        ]
        payload["tender"]["lots"][0]["value"]["amount"] = 95
        payload["tender"]["lots"][1]["value"]["amount"] = 95

        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value, amount_1=amount_fs_1, amount_2=amount_fs_2
                                                  )
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        for d in get_url:
            if d["compiledRelease"]["relatedProcesses"][0]["relationship"][0] == "parent":
                multistage = requests.get(url=d["compiledRelease"]["relatedProcesses"][0]["uri"]).json()
                assert multistage["releases"][0]["planning"]["budget"]["amount"]["amount"] == \
                       payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"] + \
                       payload["planning"]["budget"]["budgetBreakdown"][1]["amount"]["amount"]
                assert multistage["releases"][0]["planning"]["budget"]["amount"]["currency"] == \
                       payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"]

    @pytestrail.case("27046")
    def test_27046_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        fake_cpid = copy.deepcopy(prepared_cpid())
        fake_fs_id = prepared_fs_ocid(fake_cpid)
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["id"] = fake_fs_id
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        time.sleep(2)
        insert_into_db_create_fs(cpid)
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
        assert request_to_create_pn.text == "ok"
        assert request_to_create_pn.status_code == 202

    @pytestrail.case("27046")
    def test_27046_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        fake_cpid = copy.deepcopy(prepared_cpid())
        fake_fs_id = prepared_fs_ocid(fake_cpid)
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["id"] = fake_fs_id
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        time.sleep(2)
        insert_into_db_create_fs(cpid)
        host = set_instance_for_request()
        requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": additional_value},
            json=payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
        assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
        assert message_from_kafka["errors"][0]["code"] == "400.10.00.02"
        assert message_from_kafka["errors"][0]["description"] == "FS not found."

    @pytestrail.case("27047")
    def test_27047_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        amount_fs = 1000.00
        create_fs = insert_into_db_create_fs(cpid)
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": str(create_fs[2]),
                "amount": {
                    "amount": amount_fs,
                    "currency": "EUR"
                }
            },
            {
                "id": str(create_fs[2]),
                "amount": {
                    "amount": amount_fs,
                    "currency": "EUR"
                }
            }
        ]
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        time.sleep(2)
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
        assert request_to_create_pn.text == "ok"
        assert request_to_create_pn.status_code == 202

    @pytestrail.case("27047")
    def test_27047_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        amount_fs = 1000.00
        create_fs = insert_into_db_create_fs(cpid)
        print(create_fs[2])
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"] = [
            {
                "id": str(create_fs[2]),
                "amount": {
                    "amount": amount_fs,
                    "currency": "EUR"
                }
            },
            {
                "id": str(create_fs[2]),
                "amount": {
                    "amount": amount_fs,
                    "currency": "EUR"
                }
            }
        ]
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        time.sleep(2)
        host = set_instance_for_request()
        requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": additional_value},
            json=payload)
        time.sleep(2)
        message_from_kafka = get_message_from_kafka(x_operation_id)
        assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
        assert message_from_kafka["errors"][0]["code"] == "400.10.00.14"
        assert message_from_kafka["errors"][0]["description"] == "Invalid budget breakdown id "

    @pytestrail.case("27048")
    def test_27048_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value, status="cancelled")
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27048")
    def test_27048_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value, status="cancelled")
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00.08"
        assert create_pn_response[1]["errors"][0]["description"] == "Financial source status invalid."

    @pytestrail.case("27049")
    def test_27049_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value, statusDetails="cancelled")
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27049")
    def test_27049_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value, statusDetails="cancelled")
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00.08"
        assert create_pn_response[1]["errors"][0]["description"] == "Financial source status invalid."

    @pytestrail.case("27050")
    def test_27050_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"] = 90009.99
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value, amount=1000.00)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27050")
    def test_27050_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"] = 90009.99
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value, statusDetails=1000.00)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"com.fasterxml.jackson.databind.exc.MismatchedInputException: Cannot " \
                                     f"construct instance of `com.procurement.budget.model.dto.check.CheckValue` " \
                                     f"(although at least one Creator exists): no suitable creator method found to " \
                                     f"deserialize from Number value (" \
                                     f"{payload['planning']['budget']['budgetBreakdown'][0]['amount']})\n at " \
                                     f"[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     f"procurement.budget.model.dto.check.CheckRq[\"planning\"]->com.procurement." \
                                     f"budget.model.dto.check.PlanningCheckRq[\"budget\"]->com.procurement.budget." \
                                     f"model.dto.check.BudgetCheckRq[\"budgetBreakdown\"]->java.util.ArrayList[0]->" \
                                     f"com.procurement.budget.model.dto.check.BudgetBreakdownCheckRq[\"amount\"])"

    @pytestrail.case("27052")
    def test_27052_1(self, additional_value):
        cpid_1 = copy.deepcopy(prepared_cpid())
        cpid_2 = copy.deepcopy(prepared_cpid())
        currency_1 = "USD"
        currency_2 = "EUR"
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
        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value, currency_1=currency_1, currency_2=currency_2)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27052")
    def test_27052_2(self, additional_value):
        cpid_1 = copy.deepcopy(prepared_cpid())
        cpid_2 = copy.deepcopy(prepared_cpid())
        currency_1 = "USD"
        currency_2 = "EUR"
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
        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value, currency_1=currency_1, currency_2=currency_2)
        message_from_kafka = get_message_from_kafka(create_pn_response[2])
        assert message_from_kafka["X-OPERATION-ID"] == create_pn_response[2]
        assert message_from_kafka["errors"][0]["code"] == "400.10.00.06"
        assert message_from_kafka["errors"][0]["description"] == "Invalid currency."

    @pytestrail.case("27053")
    def test_27053_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        currency_1 = "EUR"
        currency_2 = "USD"
        amount = 2000.00
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = currency_1
        payload["tender"]["lots"][0]["value"]["currency"] = currency_2
        create_pn_response = bpe_create_pn_one_fs(cpid=cpid, pn_create_payload=payload, pmd=additional_value,
                                                  amount=amount)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27053")
    def test_27053_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        currency_1 = "EUR"
        currency_2 = "USD"
        amount = 2000.00
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = currency_1
        payload["tender"]["lots"][0]["value"]["currency"] = currency_2
        create_pn_response = bpe_create_pn_one_fs(cpid=cpid, pn_create_payload=payload, pmd=additional_value,
                                                  amount=amount)
        message_from_kafka = get_message_from_kafka(create_pn_response[2])
        assert message_from_kafka["X-OPERATION-ID"] == create_pn_response[2]
        assert message_from_kafka["errors"][0]["code"] == "400.03.10.15"
        assert message_from_kafka["errors"][0][
                   "description"] == "Invalid lot currency. Lot with id: '1' contains invalid currency (lot " \
                                     "currency: 'USD', budget amount currency: 'EUR')"

    @pytestrail.case("27054")
    def test_27054_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        currency_1 = "USD"
        currency_2 = "EUR"
        amount = 2000.00
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = currency_1

        create_pn_response = bpe_create_pn_one_fs(cpid=cpid, pn_create_payload=payload, pmd=additional_value,
                                                  amount=amount, currency=currency_2)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27054")
    def test_27054_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        currency_1 = "USD"
        currency_2 = "EUR"
        amount = 2000.00
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = currency_1

        create_pn_response = bpe_create_pn_one_fs(cpid=cpid, pn_create_payload=payload, pmd=additional_value,
                                                  amount=amount, currency=currency_2)
        message_from_kafka = get_message_from_kafka(create_pn_response[2])
        assert message_from_kafka["X-OPERATION-ID"] == create_pn_response[2]
        assert message_from_kafka["errors"][0]["code"] == "400.10.00.06"
        assert message_from_kafka["errors"][0]["description"] == "Invalid currency."

    @pytestrail.case("27055")
    def test_27055_1(self, additional_value):
        cpid_1 = copy.deepcopy(prepared_cpid())
        cpid_2 = copy.deepcopy(prepared_cpid())
        classification_id_1 = "45100000-8"
        classification_id_2 = "24200000-6"
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
        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value, classification_id_1=classification_id_1,
                                                  classification_id_2=classification_id_2)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27055")
    def test_27055_2(self, additional_value):
        cpid_1 = copy.deepcopy(prepared_cpid())
        cpid_2 = copy.deepcopy(prepared_cpid())
        classification_id_1 = "45100000-8"
        classification_id_2 = "24200000-6"
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
        create_pn_response = bpe_create_pn_two_fs(cpid_1=cpid_1, cpid_2=cpid_2, pn_create_payload=payload,
                                                  pmd=additional_value, classification_id_1=classification_id_1,
                                                  classification_id_2=classification_id_2)
        message_from_kafka = get_message_from_kafka(create_pn_response[2])
        assert message_from_kafka["X-OPERATION-ID"] == create_pn_response[2]
        assert message_from_kafka["errors"][0]["code"] == "400.10.00.05"
        assert message_from_kafka["errors"][0]["description"] == "Invalid CPV."

    @pytestrail.case("27056")
    def test_27056_1(self, additional_value):
        cpid = copy.deepcopy(prepared_test_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27056")
    def test_27056_2(self, additional_value):
        cpid = copy.deepcopy(prepared_test_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.76"
        assert create_pn_response[1]["errors"][0]["description"] == f"Invalid FS.  Cannot create PN based on test FS." \
                                                                    f" Invalid ids: [{create_pn_response[3]}]" + "}. "

    @pytestrail.case("27057")
    def test_27057_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["documents"][0]["documentType"] = "incorrect attribute"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27057")
    def test_27057_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["documents"][0]["documentType"] = "incorrect attribute"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0]["description"] == f'com.fasterxml.jackson.databind.exc.Invalid' \
                                                                    f'DefinitionException: Cannot construct instance ' \
                                                                    f'of `com.procurement.access.domain.model.enums.' \
                                                                    f'DocumentType`, problem: Unknown value for enum' \
                                                                    f'Type com.procurement.access.domain.model.enums.' \
                                                                    f'DocumentType: incorrect attribute, Allowed ' \
                                                                    f'values are evaluationCriteria, eligibility' \
                                                                    f'Criteria, billOfQuantity, illustration, market' \
                                                                    f'Studies, tenderNotice, biddingDocuments, ' \
                                                                    f'procurementPlan, technicalSpecifications, ' \
                                                                    f'contractDraft, hearingNotice, clarifications, ' \
                                                                    f'environmentalImpact, assetAndLiabilityAssessmen' \
                                                                    f't, riskProvisions, complaints, needsAssessmen' \
                                                                    f't, feasibilityStudy, projectPlan, ' \
                                                                    f'conflictOfInterest, cancellationDetails, ' \
                                                                    f'shortlistedFirms, evaluationReports, contract' \
                                                                    f'Arrangements, contractGuarantees\n at [Source: ' \
                                                                    f'UNKNOWN; line: -1, column: -1] (through ' \
                                                                    f'reference chain: com.procurement.access.infras' \
                                                                    f'tructure.handler.v1.model.request.PnCreate' \
                                                                    f'Request[\"tender\"]->com.procurement.access.' \
                                                                    f'infrastructure.handler.v1.model.request.Pn' \
                                                                    f'CreateRequest$Tender[\"documents\"]->java.util.' \
                                                                    f'ArrayList[0]->com.procurement.access.' \
                                                                    f'infrastructure.handler.v1.model.request.Pn' \
                                                                    f'CreateRequest$Tender$Document[\"documentType\"])'

    @pytestrail.case("27058")
    def test_27058_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "tenderNotice"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "biddingDocuments"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_3(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "technicalSpecifications"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_4(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "evaluationCriteria"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_5(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "clarifications"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_6(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "eligibilityCriteria"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_7(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "riskProvisions"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_8(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "billOfQuantity"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_9(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "conflictOfInterest"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_10(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "procurementPlan"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_11(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "contractDraft"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_12(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "complaints"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_13(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "illustration"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_14(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "cancellationDetails"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_15(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "evaluationReports"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_16(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "shortlistedFirms"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_17(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "contractArrangements"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27058")
    def test_27058_18(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        document_type = "contractGuarantees"
        payload["tender"]["documents"][0]["documentType"] = document_type
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        document_list = list()
        for k in planning_notice["releases"][0]["tender"]["documents"]:
            if k["documentType"] == document_type:
                document_list.append(k)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert document_list[0]["documentType"] == document_type

    @pytestrail.case("27059")
    def test_27059_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["documents"] = []
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27059")
    def test_27059_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["documents"] = []
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.70"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "List is empty. The tender contain empty list of the documents."

    @pytestrail.case("27060")
    def test_27060_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["documents"][1] = payload["tender"]["documents"][0]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27060")
    def test_27060_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["documents"][1] = payload["tender"]["documents"][0]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.91"
        assert create_pn_response[1]["errors"][0]["description"] == "Document id duplicated."

    @pytestrail.case("27061")
    def test_27061_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["documents"][1] = payload["tender"]["documents"][0]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27061")
    def test_27061_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["documents"][1] = payload["tender"]["documents"][0]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.91"
        assert create_pn_response[1]["errors"][0]["description"] == "Document id duplicated."

    @pytestrail.case("27062")
    def test_27062_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        legal_basis = "DIRECTIVE_2014_23_EU"
        payload["tender"]["legalBasis"] = legal_basis
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert multistage["releases"][0]["tender"]["legalBasis"] == legal_basis

    @pytestrail.case("27062")
    def test_27062_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        legal_basis = "DIRECTIVE_2014_24_EU"
        payload["tender"]["legalBasis"] = legal_basis
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert multistage["releases"][0]["tender"]["legalBasis"] == legal_basis

    @pytestrail.case("27062")
    def test_27062_3(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        legal_basis = "DIRECTIVE_2014_25_EU"
        payload["tender"]["legalBasis"] = legal_basis
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert multistage["releases"][0]["tender"]["legalBasis"] == legal_basis

    @pytestrail.case("27062")
    def test_27062_4(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        legal_basis = "DIRECTIVE_2009_81_EC"
        payload["tender"]["legalBasis"] = legal_basis
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert multistage["releases"][0]["tender"]["legalBasis"] == legal_basis

    @pytestrail.case("27062")
    def test_27062_5(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        legal_basis = "REGULATION_966_2012"
        payload["tender"]["legalBasis"] = legal_basis
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert multistage["releases"][0]["tender"]["legalBasis"] == legal_basis

    @pytestrail.case("27062")
    def test_27062_6(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        legal_basis = "NATIONAL_PROCUREMENT_LAW"
        payload["tender"]["legalBasis"] = legal_basis
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True
        assert multistage["releases"][0]["tender"]["legalBasis"] == legal_basis

    @pytestrail.case("27063")
    def test_27063_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["legalBasis"] = "incorrect attribute"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27063")
    def test_27063_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["legalBasis"] = "incorrect attribute"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"com.fasterxml.jackson.databind.exc.InvalidDefinitionException: Cannot " \
                                     f"construct instance of `com.procurement.access.domain.model.enums.LegalBasis`, " \
                                     f"problem: Unknown value for enumType com.procurement.access.domain.model.enums." \
                                     f"LegalBasis: {payload['tender']['legalBasis']}, Allowed values are " \
                                     f"DIRECTIVE_2014_23_EU, DIRECTIVE_2014_24_EU, DIRECTIVE_2014_25_EU, " \
                                     f"DIRECTIVE_2009_81_EC, REGULATION_966_2012, NATIONAL_PROCUREMENT_LAW, " \
                                     f"NULL\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: " \
                                     f"com.procurement.access.infrastructure.handler.v1.model.request." \
                                     f"PnCreateRequest[\"tender\"]->com.procurement.access.infrastructure.handler." \
                                     f"v1.model.request.PnCreateRequest$Tender[\"legalBasis\"])"

    @pytestrail.case("27064")
    def test_27064_1(self):
        pmd = "incorrect"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        time.sleep(2)
        host = set_instance_for_request()
        create_pn_response = requests.post(
            url=host + create_pn,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            params={"country": "MD", "pmd": pmd},
            json=payload)
        assert create_pn_response.status_code == 400
        assert create_pn_response.json()["errors"][0]["code"] == "400.00.00.00"
        assert create_pn_response.json()["errors"][0][
                   "description"] == f"Operation impossible. Process type is not found (country: 'MD', pmd: '{pmd}', " \
                                     f"process: 'createPN')."

    @pytestrail.case("27065")
    def test_27065_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["tenderPeriod"]["startDate"] = "2021-02-0200:00:00Z"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27065")
    def test_27065_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        date = "2021-02-0200:00:00Z"
        payload["tender"]["tenderPeriod"]["startDate"] = date
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"com.fasterxml.jackson.databind.JsonMappingException: Text '{date}' " \
                                     f"could not be parsed at index 10 (through reference chain: com.procurement." \
                                     f"access.infrastructure.handler.v1.model.request.PnCreateRequest[\"tender\"]->" \
                                     f"com.procurement.access.infrastructure.handler.v1.model.request.PnCreate" \
                                     f"Request$Tender[\"tenderPeriod\"]->com.procurement.access.infrastructure." \
                                     f"handler.v1.model.request.PnCreateRequest$Tender$TenderPeriod[\"startDate\"])"

    @pytestrail.case("27066")
    def test_27066_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["title"] = ""
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27066")
    def test_27066_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["title"] = ""
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "Incorrect an attribute value. The attribute 'tender.title' is empty or blank."

    @pytestrail.case("27067")
    def test_27067_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["description"] = ""
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27067")
    def test_27067_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["description"] = ""
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "Incorrect an attribute value. The attribute 'tender.description' " \
                                     "is empty or blank."

    @pytestrail.case("27068")
    def test_27068_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"] = [
            {
                "scheme": "md-idno",
                "id": "445521",
                "legalName": "legalName",
                "uri": "uri"
            },
            {
                "scheme": "md-idno",
                "id": "445521",
                "legalName": "legalName",
                "uri": "uri"
            }
        ]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27068")
    def test_27068_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["procuringEntity"]["additionalIdentifiers"] = [
            {
                "scheme": "md-idno",
                "id": "445521",
                "legalName": "legalName",
                "uri": "uri"
            },
            {
                "scheme": "md-idno",
                "id": "445521",
                "legalName": "legalName",
                "uri": "uri"
            }
        ]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.66"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "Invalid procuring entity. Additional identifiers of procuring entity are " \
                                     "duplicated"

    @pytestrail.case("27069")
    def test_27069_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"] = 2000.00
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = "EUR"
        payload["tender"]["lots"][0]["value"]["amount"] = 1500.00
        payload["tender"]["lots"][0]["value"]["currency"] = "EUR"
        payload["tender"]["lots"][1]["value"]["amount"] = 150
        payload["tender"]["lots"][1]["value"]["currency"] = "EUR"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27069")
    def test_27069_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"] = 2000.00
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = "EUR"
        payload["tender"]["lots"][0]["value"]["amount"] = 1500.00
        payload["tender"]["lots"][0]["value"]["currency"] = "EUR"
        payload["tender"]["lots"][1]["value"]["amount"] = 150
        payload["tender"]["lots"][1]["value"]["currency"] = "EUR"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        x_operation_id = fnmatch.fnmatch(create_pn_response[1]["X-OPERATION-ID"], "*")
        x_response_id = fnmatch.fnmatch(create_pn_response[1]["X-RESPONSE-ID"], "*")
        initiator = fnmatch.fnmatch(create_pn_response[1]["initiator"], "platform")
        ocid = fnmatch.fnmatch(create_pn_response[1]["data"]["ocid"], "*")
        url = fnmatch.fnmatch(create_pn_response[1]["data"]["url"], "*")
        operation_date = fnmatch.fnmatch(create_pn_response[1]["data"]["operationDate"], "*")
        outcomes_pn_id = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"], "*")
        outcomes_pn_token = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["X-TOKEN"], "*")
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert x_operation_id == True
        assert x_response_id == True
        assert initiator == True
        assert ocid == True
        assert url == True
        assert operation_date == True
        assert outcomes_pn_id == True
        assert outcomes_pn_token == True

    @pytestrail.case("27069")
    def test_27069_3(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"] = 2000.00
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = "EUR"
        payload["tender"]["lots"][0]["value"]["amount"] = 1500.00
        payload["tender"]["lots"][0]["value"]["currency"] = "EUR"
        payload["tender"]["lots"][1]["value"]["amount"] = 150
        payload["tender"]["lots"][1]["value"]["currency"] = "EUR"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert planning_notice["releases"][0]["tender"]["value"]["amount"] == payload["tender"]["lots"][0]["value"][
            "amount"] + payload["tender"]["lots"][1]["value"]["amount"]
        assert planning_notice["releases"][0]["tender"]["value"]["currency"] == "EUR"

    @pytestrail.case("27070")
    def test_27070_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"] = 1999.00
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = "EUR"
        payload["tender"]["lots"][0]["value"]["amount"] = 1500.00
        payload["tender"]["lots"][0]["value"]["currency"] = "EUR"
        payload["tender"]["lots"][1]["value"]["amount"] = 501
        payload["tender"]["lots"][1]["value"]["currency"] = "EUR"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27070")
    def test_27070_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"] = 1999.00
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = "EUR"
        payload["tender"]["lots"][0]["value"]["amount"] = 1500.00
        payload["tender"]["lots"][0]["value"]["currency"] = "EUR"
        payload["tender"]["lots"][1]["value"]["amount"] = 501.00
        payload["tender"]["lots"][1]["value"]["currency"] = "EUR"
        amount = payload["tender"]["lots"][0]["value"]["amount"] + payload["tender"]["lots"][1]["value"]["amount"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.52"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"Invalid amount of the tender. The amount of the tender [2001.00] more that " \
                                     f"the amount of the budget [1999.00]."

    @pytestrail.case("27071")
    def test_27071_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"] = 2000.00
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = "EUR"
        payload["tender"]["lots"][0]["value"]["amount"] = 1500.00
        payload["tender"]["lots"][0]["value"]["currency"] = "USD"
        payload["tender"]["lots"][1]["value"]["amount"] = 150.00
        payload["tender"]["lots"][1]["value"]["currency"] = "EUR"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27071")
    def test_27071_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["amount"] = 2000.00
        payload["planning"]["budget"]["budgetBreakdown"][0]["amount"]["currency"] = "EUR"
        payload["tender"]["lots"][0]["value"]["amount"] = 1500.00
        payload["tender"]["lots"][0]["value"]["currency"] = "USD"
        payload["tender"]["lots"][1]["value"]["amount"] = 150.00
        payload["tender"]["lots"][1]["value"]["currency"] = "EUR"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.15"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"Invalid lot currency. Lot with id: '1' contains invalid currency (lot " \
                                     f"currency: 'USD', budget amount currency: 'EUR')"

    @pytestrail.case("27072")
    def test_27072_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["quantity"] = 0
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27072")
    def test_27072_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["quantity"] = 0
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.51"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"Invalid quantity value in item."

    @pytestrail.case("27073")
    def test_27073_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        period_1 = get_contract_period()
        time.sleep(15)
        period_2 = get_contract_period()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["tenderPeriod"]["startDate"] = period_1[2]
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = period_1[0]
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = period_1[1]
        payload["tender"]["lots"][1]["contractPeriod"]["startDate"] = period_2[0]
        payload["tender"]["lots"][1]["contractPeriod"]["endDate"] = period_2[1]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27073")
    def test_27073_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        period_1 = get_contract_period()
        time.sleep(15)
        period_2 = get_contract_period()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["tenderPeriod"]["startDate"] = period_1[2]
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = period_1[0]
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = period_1[1]
        payload["tender"]["lots"][1]["contractPeriod"]["startDate"] = period_2[0]
        payload["tender"]["lots"][1]["contractPeriod"]["endDate"] = period_2[1]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27073")
    def test_27073_3(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        period_1 = get_contract_period()
        time.sleep(15)
        period_2 = get_contract_period()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["tenderPeriod"]["startDate"] = period_1[2]
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = period_1[0]
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = period_1[1]
        payload["tender"]["lots"][1]["contractPeriod"]["startDate"] = period_2[0]
        payload["tender"]["lots"][1]["contractPeriod"]["endDate"] = period_2[1]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["contractPeriod"]["startDate"] == \
               payload["tender"]["lots"][0]["contractPeriod"]["startDate"]
        assert multistage["releases"][0]["tender"]["contractPeriod"]["endDate"] == \
               payload["tender"]["lots"][1]["contractPeriod"]["endDate"]

    # This is BUG -> check description -> date without 'Z' digit
    @pytestrail.case("27074")
    def test_27074_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        date= get_period()
        budget_start_date = date[0]
        budget_end_date = date[1]
        budget_timestamp = date[2]
        tomorrow_date = get_human_date_in_utc_format(get_timestamp_from_human_date(budget_end_date))
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = tomorrow_date[2]
        payload["tender"]["lots"][1]["contractPeriod"]["startDate"] = tomorrow_date[2]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value,
                                                  start_date=budget_start_date, end_date=budget_end_date,
                                                  timestamp=budget_timestamp)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27074")
    def test_27074_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        date = get_period()
        budget_start_date = date[0]
        budget_end_date = date[1]
        budget_timestamp = date[2]
        tomorrow_date = get_human_date_in_utc_format(get_timestamp_from_human_date(budget_end_date))
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = tomorrow_date[2]
        payload["tender"]["lots"][1]["contractPeriod"]["startDate"] = tomorrow_date[2]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value,
                                                  start_date=budget_start_date, end_date=budget_end_date,
                                                  timestamp=budget_timestamp)
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.12"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"Invalid contract period of lot. The start date of the tender contract period " \
                                     f"[{tomorrow_date}] after than the end date of the budget breakdown " \
                                     f"period [{budget_end_date}]"

    # This is BUG -> check description -> date without 'Z' digit
    @pytestrail.case("27075")
    def test_27075_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        date = get_period()
        budget_start_date = date[0]
        budget_end_date = date[1]
        budget_timestamp = date[2]
        yesterday_date = get_human_date_in_utc_format(get_timestamp_from_human_date(budget_start_date))
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = yesterday_date[1]
        payload["tender"]["lots"][1]["contractPeriod"]["endDate"] = yesterday_date[1]
        payload["tender"]["tenderPeriod"]["startDate"] = date[3]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value,
                                                  start_date=budget_start_date, end_date=budget_end_date,
                                                  timestamp=budget_timestamp)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27075")
    def test_27075_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        date = get_period()
        budget_start_date = date[0]
        budget_end_date = date[1]
        budget_timestamp = date[2]
        yesterday_date = get_human_date_in_utc_format(get_timestamp_from_human_date(budget_start_date))
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = yesterday_date[1]
        payload["tender"]["lots"][1]["contractPeriod"]["endDate"] = yesterday_date[1]
        payload["tender"]["tenderPeriod"]["startDate"] = date[3]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value,
                                                  start_date=budget_start_date, end_date=budget_end_date,
                                                  timestamp=budget_timestamp)
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.12"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"Invalid contract period of lot. The end date of the tender contract " \
                                     f"period [{yesterday_date[1]}] before than the start date of the budget " \
                                     f"breakdown period [{budget_start_date}]"

    @pytestrail.case("27076")
    def test_27076_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        date = get_period()
        budget_start_date = date[0]
        budget_end_date = date[1]
        budget_timestamp = date[2]
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = date[1]
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = date[0]
        payload["tender"]["lots"][1]["contractPeriod"]["startDate"] = date[0]
        payload["tender"]["lots"][1]["contractPeriod"]["endDate"] = date[1]
        payload["tender"]["tenderPeriod"]["startDate"] = date[3]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value,
                                                  start_date=budget_start_date, end_date=budget_end_date,
                                                  timestamp=budget_timestamp)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27076")
    def test_27076_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        date = get_period()
        budget_start_date = date[0]
        budget_end_date = date[1]
        budget_timestamp = date[2]
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = date[1]
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = date[0]
        payload["tender"]["lots"][1]["contractPeriod"]["startDate"] = date[0]
        payload["tender"]["lots"][1]["contractPeriod"]["endDate"] = date[1]
        payload["tender"]["tenderPeriod"]["startDate"] = date[3]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value,
                                                  start_date=budget_start_date, end_date=budget_end_date,
                                                  timestamp=budget_timestamp)
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.12"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "Invalid contract period of lot."

    # This is BUG -> check description -> date without 'Z' digit
    @pytestrail.case("27077")
    def test_27077_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        date = get_period()
        budget_start_date = date[0]
        budget_end_date = date[1]
        budget_timestamp = date[2]
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = date[0]
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = date[1]
        payload["tender"]["lots"][1]["contractPeriod"]["startDate"] = date[0]
        payload["tender"]["lots"][1]["contractPeriod"]["endDate"] = date[1]
        payload["tender"]["tenderPeriod"]["startDate"] = date[4]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value,
                                                  start_date=budget_start_date, end_date=budget_end_date,
                                                  timestamp=budget_timestamp)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27077")
    def test_27077_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        date = get_period()
        budget_start_date = date[0]
        budget_end_date = date[1]
        budget_timestamp = date[2]
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = date[0]
        payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = date[1]
        payload["tender"]["lots"][1]["contractPeriod"]["startDate"] = date[0]
        payload["tender"]["lots"][1]["contractPeriod"]["endDate"] = date[1]
        payload["tender"]["tenderPeriod"]["startDate"] = date[4]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value,
                                                  start_date=budget_start_date, end_date=budget_end_date,
                                                  timestamp=budget_timestamp)
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.12"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"Invalid contract period of lot. The start date [{date[0]}] of " \
                                     f"the contract period of the lot [1] before or eq that the end date of the " \
                                     f"tender period [{date[4]}]."

    @pytestrail.case("27078")
    def test_27078_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        budget_start_date = "2021-14-17T00:00:00Z"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value,
                                                  start_date=budget_start_date)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27078")
    def test_27078_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        budget_start_date = "2021-14-17T00:00:00Z"
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value,
                                                  start_date=budget_start_date)
        assert create_pn_response[1]["errors"][0]["code"] == "400.10.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == f"com.fasterxml.jackson.databind.JsonMappingException: Text " \
                                     f"'{budget_start_date}' could not be parsed: Invalid value for MonthOfYear " \
                                     f"(valid values 1 - 12): 14 (through reference chain: com.procurement.budget." \
                                     f"model.dto.fs.Fs[\"planning\"]->com.procurement.budget.model.dto.fs." \
                                     f"PlanningFs[\"budget\"]->com.procurement.budget.model.dto.fs.BudgetFs" \
                                     f"[\"period\"]->com.procurement.budget.model.dto.ocds.Period[\"startDate\"])"

    @pytestrail.case("27079")
    def test_27079_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["id"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.PnCreateRequest$Tender$Lot] value failed for JSON " \
                                     "property id due to missing (therefore NULL) value for creator parameter id " \
                                     "which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: -1] " \
                                     "(through reference chain: com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.PnCreateRequest[\"tender\"]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.PnCreateRequest$Tender[\"lots\"]->" \
                                     "java.util.ArrayList[0]->com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.PnCreateRequest$Tender$Lot[\"id\"])"

    @pytestrail.case("27079")
    def test_27079_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["title"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.PnCreateRequest$Tender$Lot] value failed for JSON " \
                                     "property title due to missing (therefore NULL) value for creator parameter " \
                                     "title which is a non-nullable type\n at [Source: UNKNOWN; line: -1, column: " \
                                     "-1] (through reference chain: com.procurement.access.infrastructure.handler." \
                                     "v1.model.request.PnCreateRequest[\"tender\"]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.PnCreateRequest$Tender[\"lots\"]->" \
                                     "java.util.ArrayList[0]->com.procurement.access.infrastructure.handler.v1." \
                                     "model.request.PnCreateRequest$Tender$Lot[\"title\"])"

    @pytestrail.case("27079")
    def test_27079_3(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["description"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.PnCreateRequest$Tender$Lot] value failed for JSON " \
                                     "property description due to missing (therefore NULL) value for creator " \
                                     "parameter description which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.PnCreateRequest[\"tender\"]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.PnCreateRequest$" \
                                     "Tender[\"lots\"]->java.util.ArrayList[0]->com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.PnCreateRequest$Tender$Lot" \
                                     "[\"description\"])"

    @pytestrail.case("27079")
    def test_27079_4(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["value"]["amount"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: Attribute 'amount' is an " \
                                     "invalid type 'NULL', the required type is number. (through reference chain: " \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.PnCreateRequest" \
                                     "[\"tender\"]->com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "PnCreateRequest$Tender[\"lots\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.PnCreateRequest$" \
                                     "Tender$Lot[\"value\"])"

    @pytestrail.case("27079")
    def test_27079_5(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["value"]["currency"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.JsonMappingException: Attribute 'currency' is " \
                                     "an invalid type 'NULL', the required type is text. (through reference chain: " \
                                     "com.procurement.access.infrastructure.handler.v1.model.request.PnCreate" \
                                     "Request[\"tender\"]->com.procurement.access.infrastructure.handler.v1.model." \
                                     "request.PnCreateRequest$Tender[\"lots\"]->java.util.ArrayList[0]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request." \
                                     "PnCreateRequest$Tender$Lot[\"value\"])"

    @pytestrail.case("27079")
    def test_27079_6(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["contractPeriod"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.PnCreateRequest$Tender$Lot] value failed for JSON " \
                                     "property contractPeriod due to missing (therefore NULL) value for creator " \
                                     "parameter contractPeriod which is a non-nullable type\n at [Source: UNKNOWN; " \
                                     "line: -1, column: -1] (through reference chain: com.procurement.access." \
                                     "infrastructure.handler.v1.model.request.PnCreateRequest[\"tender\"]->com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.PnCreateRequest$" \
                                     "Tender[\"lots\"]->java.util.ArrayList[0]->com.procurement.access.in" \
                                     "frastructure.handler.v1.model.request.PnCreateRequest$Tender$Lot" \
                                     "[\"contractPeriod\"])"

    @pytestrail.case("27079")
    def test_27079_7(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        del payload["tender"]["lots"][0]["placeOfPerformance"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "com.fasterxml.jackson.module.kotlin.MissingKotlinParameterException: " \
                                     "Instantiation of [simple type, class com.procurement.access.infrastructure." \
                                     "handler.v1.model.request.PnCreateRequest$Tender$Lot] value failed for JSON " \
                                     "property placeOfPerformance due to missing (therefore NULL) value for " \
                                     "creator parameter placeOfPerformance which is a non-nullable type\n at " \
                                     "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: com." \
                                     "procurement.access.infrastructure.handler.v1.model.request.PnCreateRequest" \
                                     "[\"tender\"]->com.procurement.access.infrastructure.handler.v1.model.request." \
                                     "PnCreateRequest$Tender[\"lots\"]->java.util.ArrayList[0]->com.procurement." \
                                     "access.infrastructure.handler.v1.model.request.PnCreateRequest$Tender$Lot" \
                                     "[\"placeOfPerformance\"])"

    @pytestrail.case("27080")
    def test_27080_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0] = []
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27080")
    def test_27080_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0] = []
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["errors"][0]["code"] == "400.20.00"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "com.fasterxml.jackson.databind.exc.MismatchedInputException: Cannot " \
                                     "deserialize instance of `com.procurement.mdm.model.dto.data.LotTD` out of " \
                                     "START_ARRAY token\n at [Source: UNKNOWN; line: -1, column: -1] (through " \
                                     "reference chain: com.procurement.mdm.model.dto.data.TD[\"tender\"]->com." \
                                     "procurement.mdm.model.dto.data.TenderTD[\"lots\"]->java.util.ArrayList[0])"

    @pytestrail.case("27081")
    def test_27081_1(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["id"] = "1"
        payload["tender"]["lots"][1]["id"] = "2"
        payload["tender"]["items"][0]["relatedLot"] = "44"
        payload["tender"]["items"][1]["relatedLot"] = "2"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27081")
    def test_27081_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["id"] = "1"
        payload["tender"]["lots"][1]["id"] = "2"
        payload["tender"]["items"][0]["relatedLot"] = "44"
        payload["tender"]["items"][1]["relatedLot"] = "2"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.46"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "Lot id in the tender do not match related lot in the items. "

    @pytestrail.case("27082")
    def test_27081_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["id"] = "1"
        payload["tender"]["lots"][1]["id"] = "1"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27082")
    def test_27082_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["id"] = "1"
        payload["tender"]["lots"][1]["id"] = "1"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.47"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "Lot id duplicated."

    @pytestrail.case("27083")
    def test_27083_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27083")
    def test_27083_2(self, additional_value):
        cpid = copy.deepcopy(prepared_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["id"] = "1"
        payload["tender"]["items"][1]["id"] = "1"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[1]["errors"][0]["code"] == "400.03.10.50"
        assert create_pn_response[1]["errors"][0][
                   "description"] == "Item id duplicated."

    @pytestrail.case("27084")
    def test_27084_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27084")
    def test_27084_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27084")
    def test_27084_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        assert planning_notice["releases"][0]["tender"]["lots"][0]["status"] == "planning"
        assert planning_notice["releases"][0]["tender"]["lots"][1]["status"] == "planning"

    @pytestrail.case("27084")
    def test_27084_4(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        assert planning_notice["releases"][0]["tender"]["lots"][0]["statusDetails"] == "empty"
        assert planning_notice["releases"][0]["tender"]["lots"][1]["statusDetails"] == "empty"

    @pytestrail.case("27085")
    def test_27085_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()

        assert planning_notice["releases"][0]["tender"]["status"] == "planning"

    @pytestrail.case("27085")
    def test_27085_4(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        assert planning_notice["releases"][0]["tender"]["statusDetails"] == "planning"

    @pytestrail.case("27086")
    def test_27086_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27086")
    def test_27086_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27086")
    def test_27086_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        assert planning_notice["releases"][0]["ocid"] == f"{record_list[0]['uri'][76:121]}"

    @pytestrail.case("27087")
    def test_27087_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27087")
    def test_27087_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27087")
    def test_27087_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        assert planning_notice["releases"][0][
                   "id"] == f"{record_list[0]['uri'][76:121]}-{record_list[0]['uri'][108:121]}"

    @pytestrail.case("27088")
    def test_27088_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["id"] = "1"
        payload["tender"]["lots"][1]["id"] = "2"
        payload["tender"]["items"][0]["relatedLot"] = "1"
        payload["tender"]["items"][1]["relatedLot"] = "2"
        payload["tender"]["documents"][0]["relatedLots"] = ["1"]
        payload["tender"]["documents"][1]["relatedLots"] = ["2"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27088")
    def test_27088_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["id"] = "1"
        payload["tender"]["lots"][1]["id"] = "2"
        payload["tender"]["items"][0]["relatedLot"] = "1"
        payload["tender"]["items"][1]["relatedLot"] = "2"
        payload["tender"]["documents"][0]["relatedLots"] = ["1"]
        payload["tender"]["documents"][1]["relatedLots"] = ["2"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27088")
    def test_27088_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["lots"][0]["id"] = "1"
        payload["tender"]["lots"][1]["id"] = "2"
        payload["tender"]["items"][0]["relatedLot"] = "1"
        payload["tender"]["items"][1]["relatedLot"] = "2"
        payload["tender"]["documents"][0]["relatedLots"] = ["1"]
        payload["tender"]["documents"][1]["relatedLots"] = ["2"]
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        lot_id_1 = is_valid_uuid(planning_notice["releases"][0]["tender"]["lots"][0]["id"], version=4)
        lot_id_2 = is_valid_uuid(planning_notice["releases"][0]["tender"]["lots"][1]["id"], version=4)
        assert lot_id_1 == True
        assert lot_id_2 == True
        assert planning_notice["releases"][0]["tender"]["items"][0]["relatedLot"] == \
               planning_notice["releases"][0]["tender"]["lots"][0]["id"]
        assert planning_notice["releases"][0]["tender"]["items"][1]["relatedLot"] == \
               planning_notice["releases"][0]["tender"]["lots"][1]["id"]
        assert planning_notice["releases"][0]["tender"]["documents"][0]["relatedLots"][0] == \
               planning_notice["releases"][0]["tender"]["lots"][0]["id"]
        assert planning_notice["releases"][0]["tender"]["documents"][1]["relatedLots"][0] == \
               planning_notice["releases"][0]["tender"]["lots"][1]["id"]

    @pytestrail.case("27089")
    def test_27089_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["id"] = "1"
        payload["tender"]["items"][1]["id"] = "2"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27089")
    def test_27089_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["id"] = "1"
        payload["tender"]["items"][1]["id"] = "2"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27089")
    def test_27089_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        payload["tender"]["items"][0]["id"] = "1"
        payload["tender"]["items"][1]["id"] = "2"
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        lot_id_1 = is_valid_uuid(planning_notice["releases"][0]["tender"]["items"][0]["id"], version=4)
        lot_id_2 = is_valid_uuid(planning_notice["releases"][0]["tender"]["items"][1]["id"], version=4)
        assert lot_id_1 == True
        assert lot_id_2 == True

    @pytestrail.case("27090")
    def test_27090_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27090")
    def test_27090_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)

        outcomes_pn_id_ocds = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][0:5], "ocds-")
        outcomes_pn_id_prefix = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][5:12],
                                                "t1s2t3-")
        outcomes_pn_id_iso = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][12:15],
                                             "MD-")
        outcomes_pn_id_timestamp_1 = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][15:29],
                                                     "*")
        outcomes_pn_id_timestamp_stage = fnmatch.fnmatch(
            create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][29:32],
            "PN-")
        outcomes_pn_id_timestamp_2 = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][32:47],
                                                     "*")
        assert outcomes_pn_id_ocds == True
        assert outcomes_pn_id_prefix == True
        assert outcomes_pn_id_iso == True
        assert outcomes_pn_id_timestamp_1 == True
        assert outcomes_pn_id_timestamp_stage == True
        assert outcomes_pn_id_timestamp_2 == True

    @pytestrail.case("27091")
    def test_27091_1(self, additional_value):
        cpid = copy.deepcopy(prepared_test_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value, test_mode=True)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27091")
    def test_27091_2(self, additional_value):
        cpid = copy.deepcopy(prepared_test_cpid())
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value, test_mode=True)

        outcomes_pn_id_test = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][0:5], "test-")
        outcomes_pn_id_prefix = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][5:12],
                                                "t1s2t3-")
        outcomes_pn_id_iso = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][12:15],
                                             "MD-")
        outcomes_pn_id_timestamp_1 = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][15:29],
                                                     "*")
        outcomes_pn_id_timestamp_stage = fnmatch.fnmatch(
            create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][29:32],
            "PN-")
        outcomes_pn_id_timestamp_2 = fnmatch.fnmatch(create_pn_response[1]["data"]["outcomes"]["pn"][0]["id"][32:47],
                                                     "*")
        assert outcomes_pn_id_test == True
        assert outcomes_pn_id_prefix == True
        assert outcomes_pn_id_iso == True
        assert outcomes_pn_id_timestamp_1 == True
        assert outcomes_pn_id_timestamp_stage == True
        assert outcomes_pn_id_timestamp_2 == True

    @pytestrail.case("27092")
    def test_27092_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27092")
    def test_27092_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27092")
    def test_27092_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["designContest"]["serviceContractAward"] == False

    @pytestrail.case("27093")
    def test_27093_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27093")
    def test_27093_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27093")
    def test_27093_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["electronicWorkflows"]["useOrdering"] == False

    @pytestrail.case("27094")
    def test_27094_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27094")
    def test_27094_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27094")
    def test_27094_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["electronicWorkflows"]["usePayment"] == False

    @pytestrail.case("27095")
    def test_27095_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27095")
    def test_27095_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27095")
    def test_27095_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["electronicWorkflows"]["acceptInvoicing"] == False

    @pytestrail.case("27096")
    def test_27096_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27096")
    def test_27096_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27096")
    def test_27096_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["jointProcurement"]["isJointProcurement"] == False

    @pytestrail.case("27097")
    def test_27097_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27097")
    def test_27097_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27097")
    def test_27097_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["procedureOutsourcing"]["procedureOutsourced"] == False

    @pytestrail.case("27098")
    def test_27098_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27098")
    def test_27098_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27098")
    def test_27098_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["framework"]["isAFramework"] == False

    @pytestrail.case("27099")
    def test_27099_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27099")
    def test_27099_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27099")
    def test_27099_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["dynamicPurchasingSystem"]["hasDynamicPurchasingSystem"] == False

    @pytestrail.case("27100")
    def test_27100_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27100")
    def test_27100_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27100")
    def test_27100_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        assert planning_notice["releases"][0]["tender"]["lotGroups"][0]["optionToCombine"] == False

    @pytestrail.case("27101")
    def test_27101_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27101")
    def test_27101_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27101")
    def test_27101_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        assert multistage["releases"][0]["tender"]["acceleratedProcedure"]["isAcceleratedProcedure"] == False

    @pytestrail.case("27102")
    def test_27102_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27102")
    def test_27102_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27102")
    def test_27102_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        assert planning_notice["releases"][0]["tender"]["submissionMethod"][0] == "electronicSubmission"

    @pytestrail.case("27103")
    def test_27103_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27103")
    def test_27103_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27103")
    def test_27103_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        current_list = list()
        for l in planning_notice["releases"][0]["tender"]["lots"]:
            current_list.append(l["options"][0])
        print(current_list)
        assert current_list[0]["hasOptions"] == False
        assert current_list[1]["hasOptions"] == False

    @pytestrail.case("27104")
    def test_27104_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27104")
    def test_27104_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27104")
    def test_27104_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        current_list = list()
        for l in planning_notice["releases"][0]["tender"]["lots"]:
            current_list.append(l["variants"][0])
        assert current_list[0]["hasVariants"] == False
        assert current_list[1]["hasVariants"] == False

    @pytestrail.case("27105")
    def test_27105_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27105")
    def test_27105_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27105")
    def test_27105_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        current_list = list()
        for l in planning_notice["releases"][0]["tender"]["lots"]:
            current_list.append(l["renewals"][0])
        print(current_list)
        assert current_list[0]["hasRenewals"] == False
        assert current_list[1]["hasRenewals"] == False

    @pytestrail.case("27106")
    def test_27106_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27106")
    def test_27106_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27106")
    def test_27106_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    record_list.append(d_1)
        planning_notice = requests.get(url=record_list[0]["uri"]).json()
        current_list = list()
        for l in planning_notice["releases"][0]["tender"]["lots"]:
            current_list.append(l["recurrentProcurement"][0])
        print(current_list)
        assert current_list[0]["isRecurrent"] == False
        assert current_list[1]["isRecurrent"] == False

    @pytestrail.case("27107")
    def test_27107_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202

    @pytestrail.case("27107")
    def test_27107_2(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
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

    @pytestrail.case("27107")
    def test_27107_3(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, pn_create_payload=payload, pmd=additional_value)
        get_url = requests.get(url=create_pn_response[1]["data"]["url"]).json()["records"]
        record_list = list()
        for d in get_url:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    record_list.append(d_1)
        multistage = requests.get(url=record_list[0]["uri"]).json()
        print(procurement_method[additional_value])
        assert multistage["releases"][0]["tender"]["procurementMethod"] == procurement_method[
            additional_value]