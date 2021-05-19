
# import copy
# import json
# import time
# from uuid import uuid4
#
# import requests
# from pytest_testrail.plugin import pytestrail
#
# from tests.Cassandra_session import execute_cql_from_orchestrator_operation_step, \
#     execute_cql_from_orchestrator_operation_step_by_oper_id
# from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
# from tests.bpe_update_pn.payloads import pn_update_full_data_model_with_documents, \
#     pn_update_obligatory_data_model_without_documents
# from tests.bpe_update_pn.update_pn import bpe_update_pn_one_fs_if_pn_obligatory, bpe_update_pn_one_fs_if_pn_full, \
#     get_some_id_of_pn_record
# from tests.cassandra_inserts_into_Database import insert_into_db_create_pn_full_data_model, \
#     insert_into_db_create_pn_obligatory_data_model
# from tests.iStorage import get_hash_md5, get_weught, correct_document_uploading
# from tests.kafka_messages import get_message_from_kafka
# from tests.presets import set_instance_for_request, update_pn
# from useful_functions import prepared_cpid, get_access_token_for_platform_two, get_human_date_in_utc_format
#
#
# class TestBpeCreatePN(object):
#     @pytestrail.case("27179")
#     def test_27179_1_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["planning"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.PnUpdate] value failed for JSON " \
#                                                                     "property planning due to missing (therefore " \
#                                                                     "NULL) value for creator parameter planning " \
#                                                                     "which is a non-nullable type\n at [Source: " \
#                                                                     "UNKNOWN; line: -1, column: -1] (through " \
#                                                                     "reference chain: com.procurement.access.model." \
#                                                                     "dto.pn.PnUpdate[\"planning\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_2_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["planning"]["budget"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.PlanningPnUpdate] value failed for " \
#                                                                     "JSON property budget due to missing (therefore " \
#                                                                     "NULL) value for creator parameter budget which " \
#                                                                     "is a non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference chain: " \
#                                                                     "com.procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"planning\"]->com.procurement.access.model." \
#                                                                     "dto.pn.PlanningPnUpdate[\"budget\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_3_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.00.00.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "Data processing exception."
#
#     @pytestrail.case("27179")
#     def test_27179_4_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["title"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.TenderPnUpdate] value failed for " \
#                                                                     "JSON property title due to missing (therefore " \
#                                                                     "NULL) value for creator parameter title which " \
#                                                                     "is a non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference chain: " \
#                                                                     "com.procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"tender\"]->com.procurement.access.model.dto." \
#                                                                     "pn.TenderPnUpdate[\"title\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_5_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["description"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.TenderPnUpdate] value failed for " \
#                                                                     "JSON property description due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "description which is a non-nullable " \
#                                                                     "type\n at [Source: UNKNOWN; line: -1, " \
#                                                                     "column: -1] (through reference chain: com." \
#                                                                     "procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"tender\"]->com.procurement.access.model." \
#                                                                     "dto.pn.TenderPnUpdate[\"description\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_6_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["tenderPeriod"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.TenderPnUpdate] value failed for " \
#                                                                     "JSON property tenderPeriod due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "tenderPeriod which is a non-nullable type\n " \
#                                                                     "at [Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement.a" \
#                                                                     "ccess.model.dto.pn.PnUpdate[\"tender\"]->com." \
#                                                                     "procurement.access.model.dto.pn.TenderPn" \
#                                                                     "Update[\"tenderPeriod\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_7_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["tenderPeriod"]["startDate"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.PeriodPnUpdate] value failed for " \
#                                                                     "JSON property startDate due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "startDate which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.Tender" \
#                                                                     "PnUpdate[\"tenderPeriod\"]->com.procurement." \
#                                                                     "access.model.dto.pn.PeriodPnUpdate[\"startDate\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_8_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.29"
#         assert update_pn_response[1]["errors"][0]["description"] == "Lots must not be empty."
#
#     @pytestrail.case("27179")
#     def test_27179_9_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["id"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.LotPnUpdate] value failed for JSON " \
#                                                                     "property id due to missing (therefore NULL) " \
#                                                                     "value for creator parameter id which is a non-" \
#                                                                     "nullable type\n at [Source: UNKNOWN; line: -1, " \
#                                                                     "column: -1] (through reference chain: com." \
#                                                                     "procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"tender\"]->com.procurement.access.model.dto." \
#                                                                     "pn.TenderPnUpdate[\"lots\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.access.model.d" \
#                                                                     "to.pn.LotPnUpdate[\"id\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_10_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["title"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.LotPnUpdate] value failed for " \
#                                                                     "JSON property title due to missing (therefore " \
#                                                                     "NULL) value for creator parameter title which " \
#                                                                     "is a non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference chain: " \
#                                                                     "com.procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"tender\"]->com.procurement.access.model.dto." \
#                                                                     "pn.TenderPnUpdate[\"lots\"]->java.util.Array" \
#                                                                     "List[0]->com.procurement.access.model.dto.pn." \
#                                                                     "LotPnUpdate[\"title\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_11_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["description"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.LotPnUpdate] value failed for " \
#                                                                     "JSON property description due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "description which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->com." \
#                                                                     "procurement.access.model.dto.pn.TenderPnUpdate" \
#                                                                     "[\"lots\"]->java.util.ArrayList[0]->com." \
#                                                                     "procurement.access.model.dto.pn.LotPnUpdate" \
#                                                                     "[\"description\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_12_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["value"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.LotPnUpdate] value failed for " \
#                                                                     "JSON property value due to missing (therefore " \
#                                                                     "NULL) value for creator parameter value which " \
#                                                                     "is a non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference chain: " \
#                                                                     "com.procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"tender\"]->com.procurement.access.model." \
#                                                                     "dto.pn.TenderPnUpdate[\"lots\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.access.model." \
#                                                                     "dto.pn.LotPnUpdate[\"value\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_13_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["value"]["amount"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.Value] value failed for JSON " \
#                                                                     "property amount due to missing (therefore NULL) " \
#                                                                     "value for creator parameter amount which is a " \
#                                                                     "non-nullable type\n at [Source: UNKNOWN; line: " \
#                                                                     "-1, column: -1] (through reference chain: com." \
#                                                                     "procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"tender\"]->com.procurement.access.model." \
#                                                                     "dto.pn.TenderPnUpdate[\"lots\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.access.model." \
#                                                                     "dto.pn.LotPnUpdate[\"value\"]->com.procurement." \
#                                                                     "access.model.dto.ocds.Value[\"amount\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_14_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["value"]["currency"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.Value] value failed for JSON " \
#                                                                     "property currency due to missing (therefore " \
#                                                                     "NULL) value for creator parameter currency " \
#                                                                     "which is a non-nullable type\n at [Source: " \
#                                                                     "UNKNOWN; line: -1, column: -1] (through " \
#                                                                     "reference chain: com.procurement.access." \
#                                                                     "model.dto.pn.PnUpdate[\"tender\"]->com." \
#                                                                     "procurement.access.model.dto.pn.TenderPn" \
#                                                                     "Update[\"lots\"]->java.util.ArrayList[0]->" \
#                                                                     "com.procurement.access.model.dto.pn.LotPn" \
#                                                                     "Update[\"value\"]->com.procurement.access." \
#                                                                     "model.dto.ocds.Value[\"currency\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_15_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["contractPeriod"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.LotPnUpdate] value failed for " \
#                                                                     "JSON property contractPeriod due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "contractPeriod which is a non-nullable type\n " \
#                                                                     "at [Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.TenderPn" \
#                                                                     "Update[\"lots\"]->java.util.ArrayList[0]->" \
#                                                                     "com.procurement.access.model.dto.pn.LotPn" \
#                                                                     "Update[\"contractPeriod\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_16_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["contractPeriod"]["startDate"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.ContractPeriod] value failed " \
#                                                                     "for JSON property startDate due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "startDate which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.TenderPn" \
#                                                                     "Update[\"lots\"]->java.util.ArrayList[0]->" \
#                                                                     "com.procurement.access.model.dto.pn.LotPn" \
#                                                                     "Update[\"contractPeriod\"]->com.procurement." \
#                                                                     "access.model.dto.ocds.ContractPeriod" \
#                                                                     "[\"startDate\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_17_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["contractPeriod"]["endDate"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.ContractPeriod] value failed " \
#                                                                     "for JSON property endDate due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "endDate which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.TenderPn" \
#                                                                     "Update[\"lots\"]->java.util.ArrayList[0]->" \
#                                                                     "com.procurement.access.model.dto.pn.Lot" \
#                                                                     "PnUpdate[\"contractPeriod\"]->com.procurement." \
#                                                                     "access.model.dto.ocds.ContractPeriod" \
#                                                                     "[\"endDate\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_18_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.LotPnUpdate] value failed for " \
#                                                                     "JSON property placeOfPerformance due to " \
#                                                                     "missing (therefore NULL) value for creator " \
#                                                                     "parameter placeOfPerformance which is a " \
#                                                                     "non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference " \
#                                                                     "chain: com.procurement.access.model.dto.pn." \
#                                                                     "PnUpdate[\"tender\"]->com.procurement.access." \
#                                                                     "model.dto.pn.TenderPnUpdate[\"lots\"]->java." \
#                                                                     "util.ArrayList[0]->com.procurement.access." \
#                                                                     "model.dto.pn.LotPnUpdate[\"placeOfPerformance\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_19_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm.model." \
#                                                                     "dto.data.PlaceOfPerformance] value failed for " \
#                                                                     "JSON property address due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "address which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "mdm.model.dto.data.TD[\"tender\"]->com." \
#                                                                     "procurement.mdm.model.dto.data.TenderTD" \
#                                                                     "[\"lots\"]->java.util.ArrayList[0]->com." \
#                                                                     "procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement." \
#                                                                     "mdm.model.dto.data.PlaceOfPerformance" \
#                                                                     "[\"address\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_20_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm.model." \
#                                                                     "dto.data.Address] value failed for JSON " \
#                                                                     "property streetAddress due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "streetAddress which is a non-nullable " \
#                                                                     "type\n at [Source: UNKNOWN; line: -1, " \
#                                                                     "column: -1] (through reference chain: com." \
#                                                                     "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.TenderTD" \
#                                                                     "[\"lots\"]->java.util.ArrayList[0]->com." \
#                                                                     "procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.PlaceOfPerformance[\"address\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.Address" \
#                                                                     "[\"streetAddress\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_21_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm.model." \
#                                                                     "dto.data.Address] value failed for JSON " \
#                                                                     "property addressDetails due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "addressDetails which is a non-nullable " \
#                                                                     "type\n at [Source: UNKNOWN; line: -1, " \
#                                                                     "column: -1] (through reference chain: com." \
#                                                                     "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.TenderTD" \
#                                                                     "[\"lots\"]->java.util.ArrayList[0]->com." \
#                                                                     "procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement." \
#                                                                     "mdm.model.dto.data.PlaceOfPerformance" \
#                                                                     "[\"address\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.Address[\"addressDetails\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_22_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm.model." \
#                                                                     "dto.data.AddressDetails] value failed for JSON " \
#                                                                     "property country due to missing (therefore " \
#                                                                     "NULL) value for creator parameter country which " \
#                                                                     "is a non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.PlaceOfPerformance[\"address\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Address" \
#                                                                     "[\"addressDetails\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.AddressDetails[\"country\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_23_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm.model." \
#                                                                     "dto.data.CountryDetails] value failed for " \
#                                                                     "JSON property id due to missing (therefore " \
#                                                                     "NULL) value for creator parameter id which " \
#                                                                     "is a non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference " \
#                                                                     "chain: com.procurement.mdm.model.dto.data." \
#                                                                     "TD[\"tender\"]->com.procurement.mdm.model." \
#                                                                     "dto.data.TenderTD[\"lots\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.mdm.model.dto." \
#                                                                     "data.LotTD[\"placeOfPerformance\"]->com." \
#                                                                     "procurement.mdm.model.dto.data.PlaceOf" \
#                                                                     "Performance[\"address\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.Address[\"addressDetails\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.Address" \
#                                                                     "Details[\"country\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.CountryDetails[\"id\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_24_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm." \
#                                                                     "model.dto.data.AddressDetails] value failed " \
#                                                                     "for JSON property region due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "region which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "mdm.model.dto.data.TD[\"tender\"]->com." \
#                                                                     "procurement.mdm.model.dto.data.TenderTD" \
#                                                                     "[\"lots\"]->java.util.ArrayList[0]->com." \
#                                                                     "procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement." \
#                                                                     "mdm.model.dto.data.PlaceOfPerformance" \
#                                                                     "[\"address\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.Address[\"addressDetails\"]->com." \
#                                                                     "procurement.mdm.model.dto.data.AddressDetails" \
#                                                                     "[\"region\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_25_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm.model." \
#                                                                     "dto.data.RegionDetails] value failed for JSON " \
#                                                                     "property id due to missing (therefore NULL) " \
#                                                                     "value for creator parameter id which is a non-" \
#                                                                     "nullable type\n at [Source: UNKNOWN; line: " \
#                                                                     "-1, column: -1] (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data." \
#                                                                     "TD[\"tender\"]->com.procurement.mdm.model." \
#                                                                     "dto.data.TenderTD[\"lots\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.mdm.model." \
#                                                                     "dto.data.LotTD[\"placeOfPerformance\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.Place" \
#                                                                     "OfPerformance[\"address\"]->com.procurement." \
#                                                                     "mdm.model.dto.data.Address[\"addressDetails\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Address" \
#                                                                     "Details[\"region\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.RegionDetails[\"id\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_26_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm.model." \
#                                                                     "dto.data.AddressDetails] value failed for " \
#                                                                     "JSON property locality due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "locality which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement.mdm." \
#                                                                     "model.dto.data.TD[\"tender\"]->com.procurement." \
#                                                                     "mdm.model.dto.data.TenderTD[\"lots\"]->java." \
#                                                                     "util.ArrayList[0]->com.procurement.mdm.model." \
#                                                                     "dto.data.LotTD[\"placeOfPerformance\"]->com." \
#                                                                     "procurement.mdm.model.dto.data.PlaceOf" \
#                                                                     "Performance[\"address\"]->com.procurement." \
#                                                                     "mdm.model.dto.data.Address[\"addressDetails\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Address" \
#                                                                     "Details[\"locality\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_27_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm.model." \
#                                                                     "dto.data.LocalityDetails] value failed for " \
#                                                                     "JSON property scheme due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "scheme which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement.mdm." \
#                                                                     "model.dto.data.TD[\"tender\"]->com.procurement." \
#                                                                     "mdm.model.dto.data.TenderTD[\"lots\"]->java." \
#                                                                     "util.ArrayList[0]->com.procurement.mdm.model." \
#                                                                     "dto.data.LotTD[\"placeOfPerformance\"]->com." \
#                                                                     "procurement.mdm.model.dto.data.PlaceOf" \
#                                                                     "Performance[\"address\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.Address[\"addressDetails\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.Address" \
#                                                                     "Details[\"locality\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.LocalityDetails[\"scheme\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_28_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm.model." \
#                                                                     "dto.data.LocalityDetails] value failed for JSON " \
#                                                                     "property id due to missing (therefore NULL) " \
#                                                                     "value for creator parameter id which is a non-" \
#                                                                     "nullable type\n at [Source: UNKNOWN; line: " \
#                                                                     "-1, column: -1] (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data." \
#                                                                     "TD[\"tender\"]->com.procurement.mdm.model." \
#                                                                     "dto.data.TenderTD[\"lots\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.mdm.model." \
#                                                                     "dto.data.LotTD[\"placeOfPerformance\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.PlaceOf" \
#                                                                     "Performance[\"address\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.Address[\"addressDetails\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.Address" \
#                                                                     "Details[\"locality\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.LocalityDetails[\"id\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_29_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["description"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.mdm.model." \
#                                                                     "dto.data.LocalityDetails] value failed for " \
#                                                                     "JSON property description due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "description which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement.mdm." \
#                                                                     "model.dto.data.TD[\"tender\"]->com." \
#                                                                     "procurement.mdm.model.dto.data.TenderTD" \
#                                                                     "[\"lots\"]->java.util.ArrayList[0]->com." \
#                                                                     "procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.PlaceOfPerformance[\"address\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Address" \
#                                                                     "[\"addressDetails\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.AddressDetails[\"locality\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.Locality" \
#                                                                     "Details[\"description\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_30_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.28"
#         assert update_pn_response[1]["errors"][0]["description"] == "Items must not be empty."
#
#     @pytestrail.case("27179")
#     def test_27179_31_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["id"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "infrastructure.handler.v1.model.request." \
#                                                                     "CheckItemsRequest$Item] value failed for " \
#                                                                     "JSON property id due to missing (therefore " \
#                                                                     "NULL) value for creator parameter id which " \
#                                                                     "is a non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference " \
#                                                                     "chain: com.procurement.access.infrastructure." \
#                                                                     "handler.v1.model.request.CheckItemsRequest" \
#                                                                     "[\"items\"]->java.util.ArrayList[0]->com." \
#                                                                     "procurement.access.infrastructure.handler.v1." \
#                                                                     "model.request.CheckItemsRequest$Item[\"id\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_32_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["classification"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "infrastructure.handler.v1.model.request." \
#                                                                     "CheckItemsRequest$Item] value failed for " \
#                                                                     "JSON property classification due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "classification which is a non-nullable " \
#                                                                     "type\n at [Source: UNKNOWN; line: -1, column: " \
#                                                                     "-1] (through reference chain: com.procurement." \
#                                                                     "access.infrastructure.handler.v1.model." \
#                                                                     "request.CheckItemsRequest[\"items\"]->java." \
#                                                                     "util.ArrayList[0]->com.procurement.access." \
#                                                                     "infrastructure.handler.v1.model.request." \
#                                                                     "CheckItemsRequest$Item[\"classification\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_33_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["classification"]["id"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "infrastructure.handler.v1.model.request." \
#                                                                     "CheckItemsRequest$Item$Classification] value " \
#                                                                     "failed for JSON property id due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "id which is a non-nullable type\n at [Source: " \
#                                                                     "UNKNOWN; line: -1, column: -1] (through " \
#                                                                     "reference chain: com.procurement.access." \
#                                                                     "infrastructure.handler.v1.model.request.Check" \
#                                                                     "ItemsRequest[\"items\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.access.infrastructure." \
#                                                                     "handler.v1.model.request.CheckItemsRequest$" \
#                                                                     "Item[\"classification\"]->com.procurement." \
#                                                                     "access.infrastructure.handler.v1.model." \
#                                                                     "request.CheckItemsRequest$Item$" \
#                                                                     "Classification[\"id\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_34_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["classification"]["scheme"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.Classification] value failed " \
#                                                                     "for JSON property scheme due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "scheme which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.Tender" \
#                                                                     "PnUpdate[\"items\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.access.model.dto.pn.ItemPn" \
#                                                                     "Update[\"classification\"]->com.procurement." \
#                                                                     "access.model.dto.ocds.Classification[\"scheme\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_35_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["classification"]["description"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.Classification] value failed " \
#                                                                     "for JSON property description due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "description which is a non-nullable type\n " \
#                                                                     "at [Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.TenderPn" \
#                                                                     "Update[\"items\"]->java.util.ArrayList[0]->" \
#                                                                     "com.procurement.access.model.dto.pn.ItemPn" \
#                                                                     "Update[\"classification\"]->com.procurement." \
#                                                                     "access.model.dto.ocds.Classification" \
#                                                                     "[\"description\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_36_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["additionalClassifications"][0]["id"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.Classification] value failed " \
#                                                                     "for JSON property id due to missing (therefore " \
#                                                                     "NULL) value for creator parameter id which is " \
#                                                                     "a non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference chain:" \
#                                                                     " com.procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"tender\"]->com.procurement.access.model." \
#                                                                     "dto.pn.TenderPnUpdate[\"items\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.access.model." \
#                                                                     "dto.pn.ItemPnUpdate[\"additional" \
#                                                                     "Classifications\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.access.model.dto.ocds." \
#                                                                     "Classification[\"id\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_37_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["additionalClassifications"][0]["scheme"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.Classification] value failed " \
#                                                                     "for JSON property scheme due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "scheme which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.Tender" \
#                                                                     "PnUpdate[\"items\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.access.model.dto.pn.Item" \
#                                                                     "PnUpdate[\"additionalClassifications\"]->" \
#                                                                     "java.util.ArrayList[0]->com.procurement.access." \
#                                                                     "model.dto.ocds.Classification[\"scheme\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_38_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["additionalClassifications"][0]["description"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.Classification] value failed " \
#                                                                     "for JSON property description due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "description which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.Tender" \
#                                                                     "PnUpdate[\"items\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.access.model.dto.pn.Item" \
#                                                                     "PnUpdate[\"additionalClassifications\"]->" \
#                                                                     "java.util.ArrayList[0]->com.procurement." \
#                                                                     "access.model.dto.ocds.Classification" \
#                                                                     "[\"description\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_39_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["quantity"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.ItemPnUpdate] value failed for " \
#                                                                     "JSON property quantity due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "quantity which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.Tender" \
#                                                                     "PnUpdate[\"items\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.access.model.dto.pn.Item" \
#                                                                     "PnUpdate[\"quantity\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_40_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["unit"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.ItemPnUpdate] value failed for " \
#                                                                     "JSON property unit due to missing (therefore " \
#                                                                     "NULL) value for creator parameter unit which " \
#                                                                     "is a non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference chain:" \
#                                                                     " com.procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"tender\"]->com.procurement.access.model.dto." \
#                                                                     "pn.TenderPnUpdate[\"items\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.access.model." \
#                                                                     "dto.pn.ItemPnUpdate[\"unit\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_41_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["unit"]["id"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module." \
#                                                                     "kotlin.MissingKotlinParameter" \
#                                                                     "Exception: Instantiation of " \
#                                                                     "[simple type, class com." \
#                                                                     "procurement.access.model.dto." \
#                                                                     "ocds.Unit] value failed for " \
#                                                                     "JSON property id due to missing " \
#                                                                     "(therefore NULL) value for creator" \
#                                                                     " parameter id which is a non-" \
#                                                                     "nullable type\n at [Source: " \
#                                                                     "UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com." \
#                                                                     "procurement.access.model.dto.pn." \
#                                                                     "PnUpdate[\"tender\"]->com." \
#                                                                     "procurement.access.model.dto.pn." \
#                                                                     "TenderPnUpdate[\"items\"]->java." \
#                                                                     "util.ArrayList[0]->com." \
#                                                                     "procurement.access.model.dto." \
#                                                                     "pn.ItemPnUpdate[\"unit\"]->com." \
#                                                                     "procurement.access.model.dto." \
#                                                                     "ocds.Unit[\"id\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_42_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["unit"]["name"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.Unit] value failed for JSON " \
#                                                                     "property name due to missing (therefore NULL) " \
#                                                                     "value for creator parameter name which is a " \
#                                                                     "non-nullable type\n at [Source: UNKNOWN; line:" \
#                                                                     " -1, column: -1] (through reference chain: " \
#                                                                     "com.procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"tender\"]->com.procurement.access.model." \
#                                                                     "dto.pn.TenderPnUpdate[\"items\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.access.model." \
#                                                                     "dto.pn.ItemPnUpdate[\"unit\"]->com.procurement." \
#                                                                     "access.model.dto.ocds.Unit[\"name\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_43_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["description"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.ItemPnUpdate] value failed for " \
#                                                                     "JSON property description due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "description which is a non-nullable type\n at" \
#                                                                     " [Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.Tender" \
#                                                                     "PnUpdate[\"items\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.access.model.dto.pn.ItemPn" \
#                                                                     "Update[\"description\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_44_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["items"][0]["relatedLot"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "infrastructure.handler.v1.model.request.Check" \
#                                                                     "ItemsRequest$Item] value failed for JSON " \
#                                                                     "property relatedLot due to missing (therefore " \
#                                                                     "NULL) value for creator parameter relatedLot " \
#                                                                     "which is a non-nullable type\n at [Source: " \
#                                                                     "UNKNOWN; line: -1, column: -1] (through " \
#                                                                     "reference chain: com.procurement.access." \
#                                                                     "infrastructure.handler.v1.model.request." \
#                                                                     "CheckItemsRequest[\"items\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.access." \
#                                                                     "infrastructure.handler.v1.model.request." \
#                                                                     "CheckItemsRequest$Item[\"relatedLot\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_45_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["documents"][0]["documentType"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.ocds.Document] value failed for " \
#                                                                     "JSON property documentType due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "documentType which is a non-nullable type\n " \
#                                                                     "at [Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.Tender" \
#                                                                     "PnUpdate[\"documents\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.access.model.dto.ocds." \
#                                                                     "Document[\"documentType\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_46_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["documents"][0]["id"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "500.14.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.storage." \
#                                                                     "model.dto.registration.Document] value failed " \
#                                                                     "for JSON property id due to missing (therefore " \
#                                                                     "NULL) value for creator parameter id which is a" \
#                                                                     " non-nullable type\n at [Source: UNKNOWN; line: " \
#                                                                     "-1, column: -1] (through reference chain: com." \
#                                                                     "procurement.storage.model.dto.registration." \
#                                                                     "DocumentsRq[\"documents\"]->java.util.ArrayList" \
#                                                                     "[0]->com.procurement.storage.model.dto." \
#                                                                     "registration.Document[\"id\"])"
#
#     @pytestrail.case("27179")
#     def test_27179_47_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         del payload["tender"]["documents"][0]["title"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0]["description"] == "Incorrect an attribute value. Missing attribute " \
#                                                                     "'document.title' at 'tender'."
#
#     @pytestrail.case("27180")
#     def test_27180_1_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         del payload["planning"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_obligatory(cpid=cpid, pn_update_payload=payload,
#                                                                    additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.PnUpdate] value failed for JSON " \
#                                                                     "property planning due to missing (therefore " \
#                                                                     "NULL) value for creator parameter planning " \
#                                                                     "which is a non-nullable type\n at [Source: " \
#                                                                     "UNKNOWN; line: -1, column: -1] (through " \
#                                                                     "reference chain: com.procurement.access." \
#                                                                     "model.dto.pn.PnUpdate[\"planning\"])"
#
#     @pytestrail.case("27180")
#     def test_27180_2_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         del payload["planning"]["budget"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_obligatory(cpid=cpid, pn_update_payload=payload,
#                                                                    additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.PlanningPnUpdate] value failed " \
#                                                                     "for JSON property budget due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "budget which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"planning\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.Planning" \
#                                                                     "PnUpdate[\"budget\"])"
#
#     @pytestrail.case("27180")
#     def test_27180_3_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         del payload["tender"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_obligatory(cpid=cpid, pn_update_payload=payload,
#                                                                    additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.00.00.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "Data processing exception."
#
#     @pytestrail.case("27180")
#     def test_27180_4_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         del payload["tender"]["title"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_obligatory(cpid=cpid, pn_update_payload=payload,
#                                                                    additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.TenderPnUpdate] value failed for " \
#                                                                     "JSON property title due to missing (therefore " \
#                                                                     "NULL) value for creator parameter title which " \
#                                                                     "is a non-nullable type\n at [Source: UNKNOWN; " \
#                                                                     "line: -1, column: -1] (through reference " \
#                                                                     "chain: com.procurement.access.model.dto.pn." \
#                                                                     "PnUpdate[\"tender\"]->com.procurement.access." \
#                                                                     "model.dto.pn.TenderPnUpdate[\"title\"])"
#
#     @pytestrail.case("27180")
#     def test_27180_5_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         del payload["tender"]["description"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_obligatory(cpid=cpid, pn_update_payload=payload,
#                                                                    additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.TenderPnUpdate] value failed for " \
#                                                                     "JSON property description due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "description which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.Tender" \
#                                                                     "PnUpdate[\"description\"])"
#
#     @pytestrail.case("27180")
#     def test_27180_6_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         del payload["tender"]["tenderPeriod"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_obligatory(cpid=cpid, pn_update_payload=payload,
#                                                                    additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.TenderPnUpdate] value failed for " \
#                                                                     "JSON property tenderPeriod due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "tenderPeriod which is a non-nullable type\n " \
#                                                                     "at [Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->" \
#                                                                     "com.procurement.access.model.dto.pn.TenderPn" \
#                                                                     "Update[\"tenderPeriod\"])"
#
#     @pytestrail.case("27180")
#     def test_27180_7_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         del payload["tender"]["tenderPeriod"]["startDate"]
#         update_pn_response = bpe_update_pn_one_fs_if_pn_obligatory(cpid=cpid, pn_update_payload=payload,
#                                                                    additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.module.kotlin.Missing" \
#                                                                     "KotlinParameterException: Instantiation of " \
#                                                                     "[simple type, class com.procurement.access." \
#                                                                     "model.dto.pn.PeriodPnUpdate] value failed " \
#                                                                     "for JSON property startDate due to missing " \
#                                                                     "(therefore NULL) value for creator parameter " \
#                                                                     "startDate which is a non-nullable type\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->com." \
#                                                                     "procurement.access.model.dto.pn.TenderPn" \
#                                                                     "Update[\"tenderPeriod\"]->com.procurement." \
#                                                                     "access.model.dto.pn.PeriodPnUpdate" \
#                                                                     "[\"startDate\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_1_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["planning"]["rationale"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_record = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         record_list = list()
#         for d in pn_record["releases"][0]["relatedProcesses"]:
#             if d["relationship"] == ["parent"]:
#                 record_list.append(d)
#         multistage = requests.get(url=record_list[0]["uri"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert multistage["releases"][0]["planning"]["rationale"] == str(payload["planning"]["rationale"]).lower()
#
#     @pytestrail.case("27190")
#     def test_27190_2_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["planning"]["budget"]["description"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_record = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         record_list = list()
#         for d in pn_record["releases"][0]["relatedProcesses"]:
#             if d["relationship"] == ["parent"]:
#                 record_list.append(d)
#         multistage = requests.get(url=record_list[0]["uri"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert multistage["releases"][0]["planning"]["budget"]["description"] == str(
#             payload["planning"]["budget"]["description"]).lower()
#
#     @pytestrail.case("27190")
#     def test_27190_3_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["title"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_record = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         record_list = list()
#         for d in pn_record["releases"][0]["relatedProcesses"]:
#             if d["relationship"] == ["parent"]:
#                 record_list.append(d)
#         multistage = requests.get(url=record_list[0]["uri"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert multistage["releases"][0]["tender"]["title"] == str(payload["tender"]["title"]).lower()
#
#     @pytestrail.case("27190")
#     def test_27190_4_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["description"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_record = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         record_list = list()
#         for d in pn_record["releases"][0]["relatedProcesses"]:
#             if d["relationship"] == ["parent"]:
#                 record_list.append(d)
#         multistage = requests.get(url=record_list[0]["uri"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert multistage["releases"][0]["tender"]["description"] == str(payload["tender"]["description"]).lower()
#
#     @pytestrail.case("27190")
#     def test_27190_5_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["legalBasis"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_record = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         record_list = list()
#         for d in pn_record["releases"][0]["relatedProcesses"]:
#             if d["relationship"] == ["parent"]:
#                 record_list.append(d)
#         ms_after_updating = requests.get(url=record_list[0]["uri"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[3]["releases"][0]["tender"]["legalBasis"] == \
#                ms_after_updating["releases"][0]["tender"]["legalBasis"]
#
#     @pytestrail.case("27190")
#     def test_27190_6_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["procurementMethodRationale"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_record = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         record_list = list()
#         for d in pn_record["releases"][0]["relatedProcesses"]:
#             if d["relationship"] == ["parent"]:
#                 record_list.append(d)
#         multistage = requests.get(url=record_list[0]["uri"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert multistage["releases"][0]["tender"]["procurementMethodRationale"] == str(
#             payload["tender"]["procurementMethodRationale"]).lower()
#
#     @pytestrail.case("27190")
#     def test_27190_7_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["procurementMethodAdditionalInfo"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_record = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         record_list = list()
#         for d in pn_record["releases"][0]["relatedProcesses"]:
#             if d["relationship"] == ["parent"]:
#                 record_list.append(d)
#         multistage = requests.get(url=record_list[0]["uri"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert multistage["releases"][0]["tender"]["procurementMethodAdditionalInfo"] == str(
#             payload["tender"]["procurementMethodAdditionalInfo"]).lower()
#
#     @pytestrail.case("27190")
#     def test_27190_8_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["tenderPeriod"]["startDate"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: Text 'false' could not be parsed at " \
#                                                                     "index 0 (through reference chain: com." \
#                                                                     "procurement.access.model.dto.pn.PnUpdate" \
#                                                                     "[\"tender\"]->com.procurement.access.model." \
#                                                                     "dto.pn.TenderPnUpdate[\"tenderPeriod\"]->com." \
#                                                                     "procurement.access.model.dto.pn.PeriodPnUpdate" \
#                                                                     "[\"startDate\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_9_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["id"] = False
#         host = set_instance_for_request()
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#         assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                  "Exception: (was com.procurement.mdm.exception." \
#                                                                  "InErrorException) (through reference chain: " \
#                                                                  "com.procurement.mdm.model.dto.data." \
#                                                                  "TD[\"tender\"]->com.procurement.mdm.model." \
#                                                                  "dto.data.TenderTD[\"lots\"]->java.util." \
#                                                                  "ArrayList[0]->com.procurement.mdm.model.dto." \
#                                                                  "data.LotTD[\"id\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_10_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["internalId"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"internalId\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_11_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["title"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm." \
#                                                                     "exception.InErrorException) (through " \
#                                                                     "reference chain: com.procurement.mdm.model." \
#                                                                     "dto.data.TD[\"tender\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.TenderTD[\"lots\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.mdm.model.dto." \
#                                                                     "data.LotTD[\"title\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_12_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["description"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model." \
#                                                                     "dto.data.TenderTD[\"lots\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.mdm.model.dto." \
#                                                                     "data.LotTD[\"description\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_13_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["value"]["amount"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc.Mismatched" \
#                                                                     "InputException: Cannot deserialize instance " \
#                                                                     "of `java.math.BigDecimal` out of VALUE_FALSE " \
#                                                                     "token\n at [Source: UNKNOWN; line: -1, column:" \
#                                                                     " -1] (through reference chain: com.procurement." \
#                                                                     "mdm.model.dto.data.TD[\"tender\"]->com." \
#                                                                     "procurement.mdm.model.dto.data.TenderTD" \
#                                                                     "[\"lots\"]->java.util.ArrayList[0]->com." \
#                                                                     "procurement.mdm.model.dto.data.LotTD[\"value\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Value" \
#                                                                     "[\"amount\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_14_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["value"]["currency"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"value\"]->com.procurement.mdm.model.dto.data." \
#                                                                     "Value[\"currency\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_15_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model." \
#                                                                     "dto.data.TenderTD[\"lots\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.mdm.model." \
#                                                                     "dto.data.LotTD[\"contractPeriod\"]->com." \
#                                                                     "procurement.mdm.model.dto.data.ContractPeriod" \
#                                                                     "[\"startDate\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_16_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["contractPeriod"]["endDate"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList" \
#                                                                     "[0]->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"contractPeriod\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.ContractPeriod[\"endDate\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_17_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.PlaceOfPerformance[\"address\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Address" \
#                                                                     "[\"streetAddress\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_18_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["postalCode"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.PlaceOfPerformance[\"address\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Address" \
#                                                                     "[\"postalCode\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_19_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.PlaceOfPerformance[\"address\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Address" \
#                                                                     "[\"addressDetails\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.AddressDetails[\"country\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.Country" \
#                                                                     "Details[\"id\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_20_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model." \
#                                                                     "dto.data.TenderTD[\"lots\"]->java.util.Array" \
#                                                                     "List[0]->com.procurement.mdm.model.dto.data." \
#                                                                     "LotTD[\"placeOfPerformance\"]->com.procurement." \
#                                                                     "mdm.model.dto.data.PlaceOfPerformance" \
#                                                                     "[\"address\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.Address[\"addressDetails\"]->com." \
#                                                                     "procurement.mdm.model.dto.data.AddressDetails" \
#                                                                     "[\"region\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.RegionDetails[\"id\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_21_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.PlaceOfPerformance[\"address\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Address" \
#                                                                     "[\"addressDetails\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.AddressDetails[\"locality\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.Locality" \
#                                                                     "Details[\"scheme\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_22_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.PlaceOfPerformance[\"address\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Address" \
#                                                                     "[\"addressDetails\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.AddressDetails[\"locality\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.Locality" \
#                                                                     "Details[\"id\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_23_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"][
#             "description"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.PlaceOfPerformance[\"address\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.Address" \
#                                                                     "[\"addressDetails\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.AddressDetails[\"locality\"]->" \
#                                                                     "com.procurement.mdm.model.dto.data.Locality" \
#                                                                     "Details[\"description\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_24_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["description"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList" \
#                                                                     "[0]->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"placeOfPerformance\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.PlaceOfPerformance" \
#                                                                     "[\"description\"])"
#
# # we expect to get error.code = 400.20.00 from eMDM, but system returns error.code = 400.03.10.11 from eAccess
# # QA team decided we had failed this case, but system had returned the error and it is ok on 15/03/2021
#     @pytestrail.case("27190")
#     def test_27190_25_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         if "tender" in payload.keys() and "lots" in payload["tender"].keys():
#             if "id" in payload["tender"]["lots"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][0]["id"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["lots"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][1]["id"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "items" in payload["tender"].keys():
#             if "id" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["id"] = enrich_payload[0][0]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["relatedLot"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["items"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["id"] = enrich_payload[0][1]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["relatedLot"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "documents" in payload["tender"].keys():
#             if "id" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["id"] = enrich_payload[2][0]
#             if "relatedLots" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["relatedLots"] = [enrich_payload[1][0]]
#             if "id" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["id"] = enrich_payload[2][1]
#             if "relatedLots" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["relatedLots"] = [enrich_payload[1][1]]
#         payload["tender"]["items"][0]["id"] = False
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#         assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                  "Exception: (was com.procurement.mdm.exception." \
#                                                                  "InErrorException) (through reference chain: com." \
#                                                                  "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
#                                                                  "com.procurement.mdm.model.dto.data.TenderTD" \
#                                                                  "[\"items\"]->java.util.ArrayList[0]->com." \
#                                                                  "procurement.mdm.model.dto.data.ItemTD[\"id\"])"
#
# # we have case "27190_10" like this
# # we expect to get error.code = 400.20.00 from eMDM, but system does not return error
# # QA team decided we had failed this case, but system had not returned the error and it is ok on 15/03/2021
#     @pytestrail.case("27190")
#     def test_27190_26_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["internalId"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"lots\"]->java.util.ArrayList[0]" \
#                                                                     "->com.procurement.mdm.model.dto.data.LotTD" \
#                                                                     "[\"internalId\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_27_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["classification"]["id"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_after_updating = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[4]["releases"][0]["tender"]["items"][0]["classification"]["id"] == \
#                pn_after_updating["releases"][0]["tender"]["items"][0]["classification"]["id"]
#
# # we expect to get error.code = 400.20.00 from eMDM, but system returns error.code = 400.03.00 from eAccess
# # QA team decided we had failed this case, but system had returned the error and it is ok on 15/03/2021
#     @pytestrail.case("27190")
#     def test_27190_28_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["classification"]["scheme"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model.dto." \
#                                                                     "data.TenderTD[\"items\"]->java.util.ArrayList" \
#                                                                     "[0]->com.procurement.mdm.model.dto.data.ItemTD" \
#                                                                     "[\"classification\"]->com.procurement.mdm." \
#                                                                     "model.dto.data.ClassificationTD[\"scheme\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_29_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["classification"]["description"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_after_updating = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[4]["releases"][0]["tender"]["items"][0]["classification"]["description"] == \
#                pn_after_updating["releases"][0]["tender"]["items"][0]["classification"]["description"]
#
#     @pytestrail.case("27190")
#     def test_27190_30_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["additionalClassifications"][0]["id"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_after_updating = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[4]["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"] == \
#                pn_after_updating["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["id"]
#
# # we expect to get error.code = 400.20.00 from eMDM, but system returns error.code = 400.03.00 from eAccess
# # QA team decided we had failed this case, but system had returned the error and it is ok on 15/03/2021
#     @pytestrail.case("27190")
#     def test_27190_31_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["additionalClassifications"][0]["scheme"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                     "Exception: (was com.procurement.mdm.exception." \
#                                                                     "InErrorException) (through reference chain: " \
#                                                                     "com.procurement.mdm.model.dto.data.TD" \
#                                                                     "[\"tender\"]->com.procurement.mdm.model." \
#                                                                     "dto.data.TenderTD[\"items\"]->java.util." \
#                                                                     "ArrayList[0]->com.procurement.mdm.model.dto." \
#                                                                     "data.ItemTD[\"additionalClassifications\"]" \
#                                                                     "->java.util.ArrayList[0]->com.procurement.mdm." \
#                                                                     "model.dto.data.ClassificationTD[\"scheme\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_32_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["additionalClassifications"][0]["description"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_after_updating = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[4]["releases"][0]["tender"]["items"][0]["additionalClassifications"][0][
#                    "description"] == \
#                pn_after_updating["releases"][0]["tender"]["items"][0]["additionalClassifications"][0]["description"]
#
# # we expect to get error.code = 400.20.00 from eMDM, but system returns error.code = 400.03.00 from eAccess
# # QA team decided we had failed this case, but system had returned the error and it is ok on 15/03/2021
#     @pytestrail.case("27190")
#     def test_27190_33_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["quantity"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc.Mismatched" \
#                                                                     "InputException: Cannot deserialize instance " \
#                                                                     "ofjava.math.BigDecimalout of VALUE_TRUE " \
#                                                                     "token\n at [Source: UNKNOWN; line: -1, " \
#                                                                     "column: -1] (through reference chain: com." \
#                                                                     "procurement.mdm.model.dto.data.TD[\"tender\"]" \
#                                                                     "->com.procurement.mdm.model.dto.data.TenderTD" \
#                                                                     "[\"items\"]->java.util.ArrayList[0]->com." \
#                                                                     "procurement.mdm.model.dto.data.ItemTD" \
#                                                                     "[\"quantity\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_34_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["unit"]["id"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_after_updating = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[4]["releases"][0]["tender"]["items"][0]["unit"]["id"] == \
#                pn_after_updating["releases"][0]["tender"]["items"][0]["unit"]["id"]
#
#     @pytestrail.case("27190")
#     def test_27190_35_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["unit"]["id"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_after_updating = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[4]["releases"][0]["tender"]["items"][0]["unit"]["name"] == \
#                pn_after_updating["releases"][0]["tender"]["items"][0]["unit"]["name"]
#
#     @pytestrail.case("27190")
#     def test_27190_36_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["description"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_after_updating = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert pn_after_updating["releases"][0]["tender"]["items"][0]["description"] == \
#                str(payload["tender"]["items"][0]["description"]).lower()
#
# # we expect to get error.code = 400.20.00 from eMDM, but system returns error.code = 400.03.10.17 from eAccess
# # QA team decided we had failed this case, but system had returned the error and it is ok on 15/03/2021
#     @pytestrail.case("27190")
#     def test_27190_37_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         if "tender" in payload.keys() and "lots" in payload["tender"].keys():
#             if "id" in payload["tender"]["lots"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][0]["id"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["lots"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][1]["id"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "items" in payload["tender"].keys():
#             if "id" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["id"] = enrich_payload[0][0]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["relatedLot"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["items"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["id"] = enrich_payload[0][1]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["relatedLot"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "documents" in payload["tender"].keys():
#             if "id" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["id"] = enrich_payload[2][0]
#             if "relatedLots" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["relatedLots"] = [enrich_payload[1][0]]
#             if "id" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["id"] = enrich_payload[2][1]
#             if "relatedLots" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["relatedLots"] = [enrich_payload[1][1]]
#         payload["tender"]["items"][0]["relatedLot"] = False
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.20.00"
#         assert message_from_kafka["errors"][0]["description"] == "com.fasterxml.jackson.databind.JsonMapping" \
#                                                                  "Exception: (was com.procurement.mdm.exception." \
#                                                                  "InErrorException) (through reference chain: com." \
#                                                                  "procurement.mdm.model.dto.data.TD[\"tender\"]->" \
#                                                                  "com.procurement.mdm.model.dto.data.TenderTD" \
#                                                                  "[\"items\"]->java.util.ArrayList[0]->com." \
#                                                                  "procurement.mdm.model.dto.data.ItemTD" \
#                                                                  "[\"relatedLot\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_38_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["documents"][0]["documentType"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0]["description"] == "com.fasterxml.jackson.databind.exc.Invalid" \
#                                                                     "DefinitionException: Cannot construct instance " \
#                                                                     "of `com.procurement.access.domain.model.enums." \
#                                                                     "DocumentType`, problem: Unknown value for enum" \
#                                                                     "Type com.procurement.access.domain.model.enums." \
#                                                                     "DocumentType: false, Allowed values are " \
#                                                                     "evaluationCriteria, eligibilityCriteria, bill" \
#                                                                     "OfQuantity, illustration, marketStudies, tender" \
#                                                                     "Notice, biddingDocuments, procurementPlan, " \
#                                                                     "technicalSpecifications, contractDraft, hearing" \
#                                                                     "Notice, clarifications, environmentalImpact, " \
#                                                                     "assetAndLiabilityAssessment, riskProvisions, " \
#                                                                     "complaints, needsAssessment, feasibilityStudy, " \
#                                                                     "projectPlan, conflictOfInterest, cancellation" \
#                                                                     "Details, shortlistedFirms, evaluationReports, " \
#                                                                     "contractArrangements, contractGuarantees\n at " \
#                                                                     "[Source: UNKNOWN; line: -1, column: -1] " \
#                                                                     "(through reference chain: com.procurement." \
#                                                                     "access.model.dto.pn.PnUpdate[\"tender\"]->com." \
#                                                                     "procurement.access.model.dto.pn.TenderPnUpdate" \
#                                                                     "[\"documents\"]->java.util.ArrayList[0]->com." \
#                                                                     "procurement.access.model.dto.ocds.Document" \
#                                                                     "[\"documentType\"])"
#
#     @pytestrail.case("27190")
#     def test_27190_39_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         if "tender" in payload.keys() and "lots" in payload["tender"].keys():
#             if "id" in payload["tender"]["lots"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][0]["id"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["lots"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][1]["id"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "items" in payload["tender"].keys():
#             if "id" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["id"] = enrich_payload[0][0]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["relatedLot"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["items"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["id"] = enrich_payload[0][1]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["relatedLot"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "documents" in payload["tender"].keys():
#             if "id" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["id"] = enrich_payload[2][0]
#             if "relatedLots" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["relatedLots"] = [enrich_payload[1][0]]
#             if "id" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["id"] = enrich_payload[2][1]
#             if "relatedLots" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["relatedLots"] = [enrich_payload[1][1]]
#         payload["tender"]["documents"][0]["id"] = False
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.14.00.14"
#         assert message_from_kafka["errors"][0][
#                    "description"] == f"Files not found: [{str(payload['tender']['documents'][0]['id']).lower()}]"
#
#     @pytestrail.case("27190")
#     def test_27190_40_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["documents"][0]["title"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_after_updating = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert pn_after_updating["releases"][0]["tender"]["documents"][0]["title"] == \
#                str(payload["tender"]["documents"][0]["title"]).lower()
#
#     @pytestrail.case("27190")
#     def test_27190_41_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["documents"][0]["description"] = False
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         pn_after_updating = requests.get(url=update_pn_response[1]["data"]["url"]).json()
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert pn_after_updating["releases"][0]["tender"]["documents"][0]["description"] == \
#                str(payload["tender"]["documents"][0]["description"]).lower()
#
#     @pytestrail.case("27190")
#     def test_27190_42_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         if "tender" in payload.keys() and "lots" in payload["tender"].keys():
#             if "id" in payload["tender"]["lots"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][0]["id"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["lots"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][1]["id"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "items" in payload["tender"].keys():
#             if "id" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["id"] = enrich_payload[0][0]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["relatedLot"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["items"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["id"] = enrich_payload[0][1]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["relatedLot"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "documents" in payload["tender"].keys():
#             if "id" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["id"] = enrich_payload[2][0]
#             if "relatedLots" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["relatedLots"] = [enrich_payload[1][0]]
#             if "id" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["id"] = enrich_payload[2][1]
#             if "relatedLots" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["relatedLots"] = [enrich_payload[1][1]]
#         payload["tender"]["documents"][0]["relatedLots"] = [False]
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.03.10.06"
#         assert message_from_kafka["errors"][0]["description"] == "Invalid documents related lots."
#
#     @pytestrail.case("27185")
#     def test_27185_1_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["planning"]["rationale"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'request.planning.rationale' is " \
#                                      "empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_2_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["planning"]["budget"]["description"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'planning.budget.description' is " \
#                                      "empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_3_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["title"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.title' is empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_4_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["description"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.description' is empty " \
#                                      "or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_5_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["procurementMethodRationale"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.procurementMethod" \
#                                      "Rationale' is empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_6_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["procurementMethodAdditionalInfo"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.procurementMethod" \
#                                      "AdditionalInfo' is empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_7_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["tenderPeriod"]["startDate"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "com.fasterxml.jackson.databind.JsonMappingException: Text '' could not be " \
#                                      "parsed at index 0 (through reference chain: com.procurement.access.model.dto." \
#                                      "pn.PnUpdate[\"tender\"]->com.procurement.access.model.dto.pn.TenderPnUpdate" \
#                                      "[\"tenderPeriod\"]->com.procurement.access.model.dto.pn.PeriodPnUpdate" \
#                                      "[\"startDate\"])"
#
#     @pytestrail.case("27190")
#     def test_27185_8_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         if "tender" in payload.keys() and "lots" in payload["tender"].keys():
#             if "id" in payload["tender"]["lots"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][0]["id"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["lots"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][1]["id"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "items" in payload["tender"].keys():
#             if "id" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["id"] = enrich_payload[0][0]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["relatedLot"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["items"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["id"] = enrich_payload[0][1]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["relatedLot"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "documents" in payload["tender"].keys():
#             if "id" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["id"] = enrich_payload[2][0]
#             if "relatedLots" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["relatedLots"] = [enrich_payload[1][0]]
#             if "id" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["id"] = enrich_payload[2][1]
#             if "relatedLots" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["relatedLots"] = [enrich_payload[1][1]]
#         payload["tender"]["lots"][0]["id"] = ""
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.03.10.17"
#         assert message_from_kafka["errors"][0]["description"] == "Invalid items related lots."
#
#     @pytestrail.case("27185")
#     def test_27185_9_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["internalId"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.lots.internalId' is " \
#                                      "empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_10_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["title"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.lots.title' is " \
#                                      "empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_11_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["description"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.lots.description' is " \
#                                      "empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_12_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["value"]["currency"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.15"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Invalid lot currency."
#
#     @pytestrail.case("27185")
#     def test_27185_13_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["contractPeriod"]["startDate"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "com.fasterxml.jackson.databind.JsonMappingException: Text '' could not be " \
#                                      "parsed at index 0 (through reference chain: com.procurement.access.model.dto." \
#                                      "pn.PnUpdate[\"tender\"]->com.procurement.access.model.dto.pn.TenderPnUpdate" \
#                                      "[\"lots\"]->java.util.ArrayList[0]->com.procurement.access.model.dto.pn.Lot" \
#                                      "PnUpdate[\"contractPeriod\"]->com.procurement.access.model.dto.ocds.Contract" \
#                                      "Period[\"startDate\"])"
#
#     @pytestrail.case("27185")
#     def test_27185_15_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["streetAddress"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.lots.placeOf" \
#                                      "Performance.address.streetAddress' is empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_16_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["postalCode"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.lots.placeOfPerformance." \
#                                      "address.postalCode' is empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_17_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["country"]["id"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00.11"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Country not found. "
#
#     @pytestrail.case("27185")
#     def test_27185_18_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["region"]["id"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.20.00.13"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Region not found. "
#
# # !Pay attention It is a  bag ->
# # locality.scheme was published as empty string on PublicPoint
# # https://ustudio.atlassian.net/browse/ES-5775
#     @pytestrail.case("27185")
#     def test_27185_19_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.lots.placeOfPerformance." \
#                                      "address.addressDetails.locality.scheme' is empty or blank."
#
# # !Pay attention It is a critical bag ->
# # locality.id was published as empty string on PublicPoint
# # https://ustudio.atlassian.net/browse/ES-5775
#     @pytestrail.case("27185")
#     def test_27185_20_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"] = "tEST"
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["id"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.lots.placeOf" \
#                                      "Performance.address.addressDetails.locality.id' is empty or blank."
#
# # !Pay attention It is a critical bag ->
# # locality.id was published as empty sting on PublicPoint
# # https://ustudio.atlassian.net/browse/ES-5775
#     @pytestrail.case("27185")
#     def test_27185_21_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["scheme"] = "tEST"
#         payload["tender"]["lots"][0]["placeOfPerformance"]["address"]["addressDetails"]["locality"]["description"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.lots.placeOfPerformance." \
#                                      "address.addressDetails.locality.description' is empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_22_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["lots"][0]["placeOfPerformance"]["description"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.lots.placeOfPerformance." \
#                                      "description' is empty or blank."
#
#     @pytestrail.case("27190")
#     def test_27185_23_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         if "tender" in payload.keys() and "lots" in payload["tender"].keys():
#             if "id" in payload["tender"]["lots"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][0]["id"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["lots"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][1]["id"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "items" in payload["tender"].keys():
#             if "id" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["id"] = enrich_payload[0][0]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["relatedLot"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["items"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["id"] = enrich_payload[0][1]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["relatedLot"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "documents" in payload["tender"].keys():
#             if "id" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["id"] = enrich_payload[2][0]
#             if "relatedLots" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["relatedLots"] = [enrich_payload[1][0]]
#             if "id" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["id"] = enrich_payload[2][1]
#             if "relatedLots" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["relatedLots"] = [enrich_payload[1][1]]
#         payload["tender"]["items"][0]["id"] = ""
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.03.10.67"
#         assert message_from_kafka["errors"][0]["description"] == "Incorrect an attribute value. The attribute " \
#                                                                  "'tender.items.id' is empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_24_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["internalId"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.items.internalId' is " \
#                                      "empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_25_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["classification"]["scheme"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "com.fasterxml.jackson.databind.exc.InvalidDefinitionException: Cannot " \
#                                      "construct instance of `com.procurement.access.domain.model.enums.Scheme`, " \
#                                      "problem: Unknown value for enumType com.procurement.access.domain.model." \
#                                      "enums.Scheme: , Allowed values are CPV, CPVS, GSIN, UNSPSC, CPC, OKDP, " \
#                                      "OKPD\n at [Source: UNKNOWN; line: -1, column: -1] (through reference chain: " \
#                                      "com.procurement.access.model.dto.pn.PnUpdate[\"tender\"]->com.procurement." \
#                                      "access.model.dto.pn.TenderPnUpdate[\"items\"]->java.util.ArrayList[0]->com." \
#                                      "procurement.access.model.dto.pn.ItemPnUpdate[\"classification\"]->com." \
#                                      "procurement.access.model.dto.ocds.Classification[\"scheme\"])"
#
#     @pytestrail.case("27185")
#     def test_27185_26_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["additionalClassifications"][0]["scheme"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "com.fasterxml.jackson.databind.exc.InvalidDefinitionException: Cannot " \
#                                      "construct instance of `com.procurement.access.domain.model.enums.Scheme`, " \
#                                      "problem: Unknown value for enumType com.procurement.access.domain.model." \
#                                      "enums.Scheme: , Allowed values are CPV, CPVS, GSIN, UNSPSC, CPC, OKDP, " \
#                                      "OKPD\n at [Source: UNKNOWN; line: -1, column: -1] (through reference " \
#                                      "chain: com.procurement.access.model.dto.pn.PnUpdate[\"tender\"]->com." \
#                                      "procurement.access.model.dto.pn.TenderPnUpdate[\"items\"]->java.util." \
#                                      "ArrayList[0]->com.procurement.access.model.dto.pn.ItemPnUpdate[\"additional" \
#                                      "Classifications\"]->java.util.ArrayList[0]->com.procurement.access.model.dto." \
#                                      "ocds.Classification[\"scheme\"])"
#
#
#     @pytestrail.case("27185")
#     def test_27185_27_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["items"][0]["description"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.items.description' " \
#                                      "is empty or blank."
#
#     @pytestrail.case("27190")
#     def test_27185_28_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         if "tender" in payload.keys() and "lots" in payload["tender"].keys():
#             if "id" in payload["tender"]["lots"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][0]["id"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["lots"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][1]["id"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "items" in payload["tender"].keys():
#             if "id" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["id"] = enrich_payload[0][0]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["relatedLot"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["items"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["id"] = enrich_payload[0][1]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["relatedLot"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "documents" in payload["tender"].keys():
#             if "id" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["id"] = enrich_payload[2][0]
#             if "relatedLots" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["relatedLots"] = [enrich_payload[1][0]]
#             if "id" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["id"] = enrich_payload[2][1]
#             if "relatedLots" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["relatedLots"] = [enrich_payload[1][1]]
#         payload["tender"]["items"][0]["relatedLot"] = ""
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.03.10.17"
#         assert message_from_kafka["errors"][0]["description"] == "Invalid items related lots."
#
#     @pytestrail.case("27185")
#     def test_27185_29_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["documents"][0]["documentType"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.00"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "com.fasterxml.jackson.databind.exc.InvalidDefinitionException: Cannot " \
#                                      "construct instance of `com.procurement.access.domain.model.enums." \
#                                      "DocumentType`, problem: Unknown value for enumType com.procurement." \
#                                      "access.domain.model.enums.DocumentType: , Allowed values are " \
#                                      "evaluationCriteria, eligibilityCriteria, billOfQuantity, illustration, " \
#                                      "marketStudies, tenderNotice, biddingDocuments, procurementPlan, " \
#                                      "technicalSpecifications, contractDraft, hearingNotice, clarifications, " \
#                                      "environmentalImpact, assetAndLiabilityAssessment, riskProvisions, " \
#                                      "complaints, needsAssessment, feasibilityStudy, projectPlan, " \
#                                      "conflictOfInterest, cancellationDetails, shortlistedFirms, " \
#                                      "evaluationReports, contractArrangements, contractGuarantees\n at " \
#                                      "[Source: UNKNOWN; line: -1, column: -1] (through reference chain: " \
#                                      "com.procurement.access.model.dto.pn.PnUpdate[\"tender\"]->com." \
#                                      "procurement.access.model.dto.pn.TenderPnUpdate[\"documents\"]->java." \
#                                      "util.ArrayList[0]->com.procurement.access.model.dto.ocds.Document" \
#                                      "[\"documentType\"])"
#
#     @pytestrail.case("27190")
#     def test_27185_30_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         if "tender" in payload.keys() and "lots" in payload["tender"].keys():
#             if "id" in payload["tender"]["lots"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][0]["id"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["lots"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][1]["id"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "items" in payload["tender"].keys():
#             if "id" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["id"] = enrich_payload[0][0]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["relatedLot"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["items"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["id"] = enrich_payload[0][1]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["relatedLot"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "documents" in payload["tender"].keys():
#             if "id" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["id"] = enrich_payload[2][0]
#             if "relatedLots" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["relatedLots"] = [enrich_payload[1][0]]
#             if "id" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["id"] = enrich_payload[2][1]
#             if "relatedLots" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["relatedLots"] = [enrich_payload[1][1]]
#         payload["tender"]["documents"][0]["id"] = ""
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.14.00.02"
#         assert message_from_kafka["errors"][0]["description"] == "Invalid documents ids: The id of the document " \
#                                                                  "is empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_31_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["documents"][0]["title"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.documents.title' " \
#                                      "is empty or blank."
#
#     @pytestrail.case("27185")
#     def test_27185_32_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["documents"][0]["description"] = ""
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["errors"][0]["code"] == "400.03.10.67"
#         assert update_pn_response[1]["errors"][0][
#                    "description"] == "Incorrect an attribute value. The attribute 'tender.documents.description' " \
#                                      "is empty or blank."
#
#     @pytestrail.case("27190")
#     def test_27185_30_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         if "tender" in payload.keys() and "lots" in payload["tender"].keys():
#             if "id" in payload["tender"]["lots"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][0]["id"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["lots"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["lots"][1]["id"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "items" in payload["tender"].keys():
#             if "id" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["id"] = enrich_payload[0][0]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][0]["relatedLot"] = enrich_payload[1][0]
#             if "id" in payload["tender"]["items"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["id"] = enrich_payload[0][1]
#             if "relatedLot" in payload["tender"]["items"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["items"][1]["relatedLot"] = enrich_payload[1][1]
#
#         if "tender" in payload.keys() and "documents" in payload["tender"].keys():
#             if "id" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["id"] = enrich_payload[2][0]
#             if "relatedLots" in payload["tender"]["documents"][0].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][0]["relatedLots"] = [enrich_payload[1][0]]
#             if "id" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["id"] = enrich_payload[2][1]
#             if "relatedLots" in payload["tender"]["documents"][1].keys():
#                 enrich_payload = get_some_id_of_pn_record(url=create_pn[0])
#                 payload["tender"]["documents"][1]["relatedLots"] = [enrich_payload[1][1]]
#         payload["tender"]["documents"][0]["relatedLots"] = [""]
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.03.10.06"
#         assert message_from_kafka["errors"][0]["description"] == "Invalid documents related lots."
#
#     @pytestrail.case("27181")
#     def test_27181_1_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         access_token = "zzz"
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_obligatory_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         host = set_instance_for_request()
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         dict = json.loads(request_to_update_pn.text)
#         assert request_to_update_pn.status_code == 401
#         assert dict["errors"][0]["code"] == "401.81.03.04"
#         assert dict["errors"][0]["description"] == "The error of verification of the authentication token."
#
#     @pytestrail.case("27182")
#     def test_27182_2_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         pn_token = str(uuid4())
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_obligatory_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         host = set_instance_for_request()
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': pn_token,
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["errors"][0]["code"] == "400.03.10.04"
#         assert message_from_kafka["errors"][0]["description"] == "Invalid token."
#
#     @pytestrail.case("27183")
#     def test_27183_1_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_obligatory_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         host = set_instance_for_request()
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         dict = json.loads(request_to_update_pn.text)
#         assert request_to_update_pn.status_code == 400
#         assert dict["errors"][0]["code"] == "400.00.00.00"
#         assert dict["errors"][0][
#                    "description"] == "Missing request header 'X-TOKEN' for method parameter of type String"
#
#     @pytestrail.case("27184")
#     def test_27184_1_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_two()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_obligatory_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         host = set_instance_for_request()
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         error_from_DB = execute_cql_from_orchestrator_operation_step(cpid, 'AccessUpdatePnTask')
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert error_from_DB['errors'][0]['code'] == '400.03.00.02'
#         assert error_from_DB['errors'][0]['description'] == 'Invalid owner.'
#
#     @pytestrail.case("27186")
#     def test_27186_1_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#
#     @pytestrail.case("27186")
#     def test_27186_2_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert update_pn_response[1]["data"]["ocid"] == update_pn_response[5]
#         assert update_pn_response[1]["data"][
#                    "url"] == f"http://dev.public.eprocurement.systems/tenders/{cpid}/{update_pn_response[5]}"
#
#     @pytestrail.case("27186")
#     def test_27186_3_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         get_pn_url = f"http://dev.public.eprocurement.systems/tenders/{cpid}/{update_pn_response[5]}"
#         pn_record = requests.get(url=get_pn_url).json()
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert pn_record["releases"][0]["tender"]["status"] == "planning"
#         assert pn_record["releases"][0]["tender"]["statusDetails"] == "planning"
#
#     @pytestrail.case("27186")
#     def test_27186_4_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         get_pn_url = f"http://dev.public.eprocurement.systems/tenders/{cpid}/{update_pn_response[5]}"
#         pn_record = requests.get(url=get_pn_url).json()
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert pn_record["releases"][0]["tag"] == ["planningUpdate"]
#
#     @pytestrail.case("27186")
#     def test_27186_5_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         get_pn_url = f"http://dev.public.eprocurement.systems/tenders/{cpid}/{update_pn_response[5]}"
#         pn_record = requests.get(url=get_pn_url).json()
#
#         release_id = pn_record['releases'][0]['id']
#         timestamp = int(release_id[46:59])
#
#         date = get_human_date_in_utc_format(timestamp)
#
#         assert update_pn_response[1]["X-OPERATION-ID"] == update_pn_response[2]
#         assert release_id[0:45] == update_pn_response[5]
#         assert pn_record['releases'][0]['date'] == date[0]
#         assert pn_record['releases'][0]['id'] == f"{update_pn_response[5]}" + f"-{str(timestamp)}"
#
#     @pytestrail.case("27187")
#     def test_27187_1_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         host = set_instance_for_request()
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#
#     @pytestrail.case("27187")
#     def test_27187_2_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_full_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_obligatory_data_model_without_documents)
#         host = set_instance_for_request()
#         requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["data"]["ocid"] == create_pn[3]
#         assert message_from_kafka["data"][
#                    "url"] == f"http://dev.public.eprocurement.systems/tenders/{cpid}/{create_pn[3]}"
#
#     @pytestrail.case("27188")
#     def test_27188_1_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_obligatory_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         request_to_update_pn = requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert request_to_update_pn.text == "ok"
#         assert request_to_update_pn.status_code == 202
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#
#     @pytestrail.case("27188")
#     def test_27188_2_smoke(self, additional_value):
#         access_token = get_access_token_for_platform_one()
#         x_operation_id = get_x_operation_id(access_token)
#         time.sleep(2)
#         cpid = prepared_cpid()
#         ei_id = prepared_cpid()
#         create_pn = insert_into_db_create_pn_obligatory_data_model(cpid, ei_id, additional_value)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         host = set_instance_for_request()
#         requests.post(
#             url=host + update_pn + cpid + '/' + create_pn[3],
#             headers={
#                 'Authorization': 'Bearer ' + access_token,
#                 'X-OPERATION-ID': x_operation_id,
#                 'X-TOKEN': create_pn[4],
#                 'Content-Type': 'application/json'},
#             json=payload)
#         time.sleep(2)
#         message_from_kafka = get_message_from_kafka(x_operation_id)
#         assert message_from_kafka["X-OPERATION-ID"] == x_operation_id
#         assert message_from_kafka["data"]["ocid"] == create_pn[3]
#         assert message_from_kafka["data"][
#                    "url"] == f"http://dev.public.eprocurement.systems/tenders/{cpid}/{create_pn[3]}"
#
#     @pytestrail.case("27191")
#     def test_27191_1_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#
#     @pytestrail.case("27191")
#     def test_27191_2(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         message_from_kafka = get_message_from_kafka(update_pn_response[2])
#         assert message_from_kafka["X-OPERATION-ID"] == update_pn_response[2]
#         assert message_from_kafka["data"]["ocid"] == update_pn_response[5]
#         assert message_from_kafka["data"][
#                    "url"] == f"http://dev.public.eprocurement.systems/tenders/{cpid}/{update_pn_response[5]}"
#
#     @pytestrail.case("27191")
#     def test_27191_3_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         execute_cql_from_orchestrator_operation_step_by_oper_id(update_pn_response[2], 'NoticeCreateReleaseTask')
#
#     @pytestrail.case("27191")
#     def test_27191_4_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         message_from_kafka = get_message_from_kafka(update_pn_response[2])
#         get_pn_url = message_from_kafka["data"]["url"]
#         pn_record = requests.get(url=get_pn_url).json()
#         start_date_from_database = execute_cql_from_orchestrator_operation_step_by_oper_id(update_pn_response[2],
#                                                                                            'NoticeCreateReleaseTask')
#         assert message_from_kafka["X-OPERATION-ID"] == update_pn_response[2]
#         assert pn_record['releases'][0]['date'] == start_date_from_database[3]["startDate"]
#
#     @pytestrail.case("27192")
#     def test_27192_1_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         # We have this file ->
#         path = "/home/roman/Documents/git/es_system_tests/API.pdf"
#         # File name, which we have ->
#         file_name = "API.pdf"
#         # Path of file ->
#         dir_path = "/home/roman/Documents/git/es_system_tests/"
#         # Register and download the file in iStorage service ->
#         document = correct_document_uploading(path=path, file_name=file_name, dir_path=dir_path)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["documents"][0]["id"] = document[0][0]
#
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         assert update_pn_response[0].text == "ok"
#         assert update_pn_response[0].status_code == 202
#
#     @pytestrail.case("27192")
#     def test_27192_2_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         # We have this file ->
#         path = "/home/roman/Documents/git/es_system_tests/API.pdf"
#         # File name, which we have ->
#         file_name = "API.pdf"
#         # Path of file ->
#         dir_path = "/home/roman/Documents/git/es_system_tests/"
#         # Register and download the file in iStorage service ->
#         document = correct_document_uploading(path=path, file_name=file_name, dir_path=dir_path)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["documents"][0]["id"] = document[0][0]
#
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         message_from_kafka = get_message_from_kafka(update_pn_response[2])
#         assert message_from_kafka["X-OPERATION-ID"] == update_pn_response[2]
#         assert message_from_kafka["data"]["ocid"] == update_pn_response[5]
#         assert message_from_kafka["data"][
#                    "url"] == f"http://dev.public.eprocurement.systems/tenders/{cpid}/{update_pn_response[5]}"
#
#     @pytestrail.case("27192")
#     def test_27192_3_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         # We have this file ->
#         path = "/home/roman/Documents/git/es_system_tests/API.pdf"
#         # File name, which we have ->
#         file_name = "API.pdf"
#         # Path of file ->
#         dir_path = "/home/roman/Documents/git/es_system_tests/"
#         # Register and download the file in iStorage service ->
#         document = correct_document_uploading(path=path, file_name=file_name, dir_path=dir_path)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["documents"][0]["id"] = document[0][0]
#
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         message_from_kafka = get_message_from_kafka(update_pn_response[2])
#         get_pn_url = message_from_kafka["data"]["url"]
#         pn_record = requests.get(url=get_pn_url).json()
#
#         assert message_from_kafka["X-OPERATION-ID"] == update_pn_response[2]
#         assert pn_record['releases'][0]['tender']["documents"][0]["id"] == payload["tender"]["documents"][0]["id"]
#
#     @pytestrail.case("27192")
#     def test_27192_4_smoke(self, additional_value):
#         cpid = prepared_cpid()
#         # We have this file ->
#         path = "/home/roman/Documents/git/es_system_tests/API.pdf"
#         # File name, which we have ->
#         file_name = "API.pdf"
#         # Path of file ->
#         dir_path = "/home/roman/Documents/git/es_system_tests/"
#         # Register and download the file in iStorage service ->
#         document = correct_document_uploading(path=path, file_name=file_name, dir_path=dir_path)
#         payload = copy.deepcopy(pn_update_full_data_model_with_documents)
#         payload["tender"]["documents"][0]["id"] = document[0][0]
#
#         update_pn_response = bpe_update_pn_one_fs_if_pn_full(cpid=cpid, pn_update_payload=payload,
#                                                              additional_value=additional_value)
#         message_from_kafka = get_message_from_kafka(update_pn_response[2])
#         get_pn_url = message_from_kafka["data"]["url"]
#         pn_record = requests.get(url=get_pn_url).json()
#
#         # Open the file for writing, in 'wb' mode ->
#         f = open(f"/home/roman/Documents/git/es_system_tests/download/{file_name}",
#                  "wb")
#         open_document = requests.get(
#             url=pn_record["releases"][0]["tender"]["documents"][0]["url"]).content
#         # Write the content to a file ->
#         f.write(open_document)
#         # Close the file, which was downloaded
#         f.close()
#         # Calculate the hash of file, which was downloaded ->
#         hash_of_downloaded_file = get_hash_md5(f"/home/roman/Documents/git/es_system_tests/download/{file_name}")
#         # Calculate the weight of file, which was downloaded ->
#         weight_of_downloaded_file = get_weught(f"/home/roman/Documents/git/es_system_tests/download/{file_name}")
#         assert document[1] == hash_of_downloaded_file
#         assert document[2] == weight_of_downloaded_file
#
#
#
#
#
#
#
#
