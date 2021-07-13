import copy
import datetime
import json
from uuid import uuid4
import requests
from deepdiff import DeepDiff
from pytest_testrail.plugin import pytestrail
from tests.Cassandra_session import Cassandra
from tests.conftest import UpdateCn, EnquiryGlobal
from tests.essences.cn import CN
from tests.essences.enquiry import Enquiry
from tests.iStorage import Document
from tests.payloads.cnonpn_payload import update_cn_on_pn_payload_full_data_model_with_auction
from tests.payloads.enquiry_period import create_enquiry_full_data_model
from useful_functions import calculated_new_date_for_request_sending, time_bot, \
    compare_actual_result_and_expected_result, create_enquiry_and_tender_period


class TestCheckOnThePossibilityOfEnquiryPeriodReschedulingForTenderInActiveClarificationTenderState1(object):
    # Check on the possibility of inquiry period rescheduling for tender in active clarification tender state,
    # after "checkpoint" time if enquiry Period in request is equal than enquiry Period in DB
    @pytestrail.case("27613")
    def test_test_send_the_request_27613_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_three_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_four_was_uploaded = document.uploading_document()[0]["data"]["id"]

        UpdateCn.cn_class = CN(
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded,
            document_three_id=document_three_was_uploaded
        )
        create_ev_response = UpdateCn.cn_class.insert_cnonpn_full(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=200,
            second_tender=400
        )
        UpdateCn.ms_release_before_cn_updating = requests.get(url=create_ev_response[5]).json()
        UpdateCn.pn_release_before_cn_updating = requests.get(url=create_ev_response[6]).json()
        UpdateCn.ev_release_before_cn_updating = requests.get(url=create_ev_response[7]).json()
        UpdateCn.enquiry_period_start_date = create_ev_response[8]
        UpdateCn.enquiry_period_end_date = create_ev_response[9]
        database = Cassandra(
            cp_id=create_ev_response[0],
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        offset_extended = database.execute_cql_from_clarification_rules_by_country_pmd_parameter(
            country=country,
            pmd=pmd,
            parameter='offsetExtended'
        )
        calculate_date_for_request_sending = calculated_new_date_for_request_sending(
            human_date=create_ev_response[9],
            value=offset_extended
        )
        time_bot(calculate_date_for_request_sending[0])
        payload = copy.deepcopy(update_cn_on_pn_payload_full_data_model_with_auction)
        payload['tender']['tenderPeriod']['endDate'] = create_ev_response[11]
        payload['tender']['enquiryPeriod']['endDate'] = create_ev_response[9]
        payload['tender']['electronicAuctions']['details'][0]['relatedLot'] = first_lot_id
        payload['tender']['electronicAuctions']['details'][1]['relatedLot'] = second_lot_id
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0][
            'id'] = document_one_was_uploaded
        payload['tender']['procuringEntity']['persones'][1]['businessFunctions'][0]['documents'][0][
            'id'] = document_two_was_uploaded
        payload['tender']['criteria'][1]['requirementGroups'][0]['requirements'][1]['eligibleEvidences'][0][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][0][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][1][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][1]['relatedItem'] = first_lot_id
        payload['tender']['criteria'][3]['relatedItem'] = first_item_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        payload['tender']['documents'][2]['id'] = document_three_was_uploaded
        payload['tender']['documents'][3]['id'] = document_four_was_uploaded
        payload['tender']['documents'][0]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = second_lot_id
        payload['tender']['documents'][2]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][3]['relatedLots'][0] = first_lot_id
        update_cn_response = UpdateCn.cn_class.update_cn(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3],
            pn_token=create_ev_response[2],
            payload=payload
        )
        UpdateCn.message_from_kafka = UpdateCn.cn_class.get_message_from_kafka()
        instance_tender_url = None
        instance_budget_url = None
        instance_storage_url = None
        if instance == "dev":
            instance_tender_url = "http://dev.public.eprocurement.systems/tenders/"
            instance_budget_url = "http://dev.public.eprocurement.systems/budgets/"
            instance_storage_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
        if instance == "sandbox":
            instance_tender_url = "http://public.eprocurement.systems/tenders/"
            instance_budget_url = "http://public.eprocurement.systems/budgets/"
            instance_storage_url = "http://storage.eprocurement.systems/get/"
        UpdateCn.instance_tender_url = instance_tender_url
        UpdateCn.instance_budget_url = instance_budget_url
        UpdateCn.instance_storage_url = instance_storage_url
        UpdateCn.payload = payload
        UpdateCn.cp_id = create_ev_response[0]
        UpdateCn.ev_id = create_ev_response[3]
        UpdateCn.pn_id = create_ev_response[1]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(update_cn_response.status_code)
        )

    @pytestrail.case('27613')
    def test_see_result_from_feed_point_27613_2(self):
        UpdateCn.successfully_update_cn = UpdateCn.cn_class.check_on_that_message_is_successfully_update_cn(
            cp_id=UpdateCn.cp_id,
            ev_id=UpdateCn.ev_id
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(UpdateCn.successfully_update_cn)
        )

    @pytestrail.case('27613')
    def test_compare_ev_release_before_updating_and_after_updating_27613_3(self):
        ev_release_after_updating = requests.get(
            url=f"{UpdateCn.message_from_kafka['data']['url']}").json()
        expected_result_tender_period = {
            'values_changed': {
                "root['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['tenderPeriod']['startDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'][
                        'startDate']
                },
                "root['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['tenderPeriod']['endDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'][
                        'endDate']
                }
            }
        }
        expected_result_enquiry_period = {
            'values_changed': {
                "root['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']['endDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'][
                        'endDate']
                }
            }
        }
        actual_result_tender_period = DeepDiff(
            UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'],
            ev_release_after_updating['releases'][0]['tender']['tenderPeriod']
        )
        actual_result_enquiry_period = DeepDiff(
            UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'],
            ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result_tender_period),
            actual_result=str(actual_result_tender_period)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result_enquiry_period),
            actual_result=str(actual_result_enquiry_period)
        )


class TestCheckOnThePossibilityOfEnquiryPeriodReschedulingForTenderInActiveClarificationTenderState2(object):
    # Check on the possibility of enquiry period rescheduling for tender in active clarification tender state,
    # after "checkpoint" time if enquiryPeriod in request is bigger than enquiry Period in DB
    @pytestrail.case("27614")
    def test_test_send_the_request_27614_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_three_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_four_was_uploaded = document.uploading_document()[0]["data"]["id"]

        UpdateCn.cn_class = CN(
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded,
            document_three_id=document_three_was_uploaded
        )
        create_ev_response = UpdateCn.cn_class.insert_cnonpn_full(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=200,
            second_tender=400
        )
        UpdateCn.ms_release_before_cn_updating = requests.get(url=create_ev_response[5]).json()
        UpdateCn.pn_release_before_cn_updating = requests.get(url=create_ev_response[6]).json()
        UpdateCn.ev_release_before_cn_updating = requests.get(url=create_ev_response[7]).json()
        UpdateCn.enquiry_period_start_date = create_ev_response[8]
        UpdateCn.enquiry_period_end_date = create_ev_response[9]
        database = Cassandra(
            cp_id=create_ev_response[0],
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password
        )
        offset_extended = database.execute_cql_from_clarification_rules_by_country_pmd_parameter(
            country=country,
            pmd=pmd,
            parameter='offsetExtended'
        )
        calculate_date_for_request_sending = calculated_new_date_for_request_sending(
            human_date=create_ev_response[9],
            value=offset_extended
        )
        time_bot(calculate_date_for_request_sending[0])
        new_enquiry_and_tender_period = create_enquiry_and_tender_period(
            second_enquiry=300,
            second_tender=600
        )
        payload = copy.deepcopy(update_cn_on_pn_payload_full_data_model_with_auction)
        payload['tender']['tenderPeriod']['endDate'] = new_enquiry_and_tender_period[3]
        payload['tender']['enquiryPeriod']['endDate'] = new_enquiry_and_tender_period[1]
        payload['tender']['electronicAuctions']['details'][0]['relatedLot'] = first_lot_id
        payload['tender']['electronicAuctions']['details'][1]['relatedLot'] = second_lot_id
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0][
            'id'] = document_one_was_uploaded
        payload['tender']['procuringEntity']['persones'][1]['businessFunctions'][0]['documents'][0][
            'id'] = document_two_was_uploaded
        payload['tender']['criteria'][1]['requirementGroups'][0]['requirements'][1]['eligibleEvidences'][0][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][0][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][1][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][1]['relatedItem'] = first_lot_id
        payload['tender']['criteria'][3]['relatedItem'] = first_item_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        payload['tender']['documents'][2]['id'] = document_three_was_uploaded
        payload['tender']['documents'][3]['id'] = document_four_was_uploaded
        payload['tender']['documents'][0]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = second_lot_id
        payload['tender']['documents'][2]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][3]['relatedLots'][0] = first_lot_id
        update_cn_response = UpdateCn.cn_class.update_cn(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3],
            pn_token=create_ev_response[2],
            payload=payload
        )
        UpdateCn.message_from_kafka = UpdateCn.cn_class.get_message_from_kafka()

        UpdateCn.payload = payload
        UpdateCn.cp_id = create_ev_response[0]
        UpdateCn.ev_id = create_ev_response[3]
        UpdateCn.pn_id = create_ev_response[1]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(update_cn_response.status_code)
        )

    @pytestrail.case('27614')
    def test_see_result_from_feed_point_27614_2(self):
        UpdateCn.successfully_update_cn = UpdateCn.cn_class.check_on_that_message_is_successfully_update_cn(
            cp_id=UpdateCn.cp_id,
            ev_id=UpdateCn.ev_id
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(UpdateCn.successfully_update_cn)
        )

    @pytestrail.case('27614')
    def test_compare_ev_release_before_updating_and_after_updating_27614_3(self):
        ev_release_after_updating = requests.get(
            url=f"{UpdateCn.message_from_kafka['data']['url']}").json()
        expected_result_tender_period = {
            'values_changed': {
                "root['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['tenderPeriod']['startDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'][
                        'startDate']
                },
                "root['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['tenderPeriod']['endDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'][
                        'endDate']
                }
            }
        }
        expected_result_enquiry_period = {
            'values_changed': {
                "root['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']['endDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'][
                        'endDate']
                }
            }
        }
        actual_result_tender_period = DeepDiff(
            UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'],
            ev_release_after_updating['releases'][0]['tender']['tenderPeriod']
        )
        actual_result_enquiry_period = DeepDiff(
            UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'],
            ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result_tender_period),
            actual_result=str(actual_result_tender_period)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result_enquiry_period),
            actual_result=str(actual_result_enquiry_period)
        )


class TestCheckOnTheImpossibilityOfEnquiryPeriodReschedulingForTenderInActiveClarificationTenderState1(object):
    # Check on the impossibility of enquiry period reschedule for tender in active clarification tender state,
    # before "checkpoint" time if enquiry Period in request is equal than enquiry Period in DB
    @pytestrail.case("27615")
    def test_test_send_the_request_27615_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_three_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_four_was_uploaded = document.uploading_document()[0]["data"]["id"]

        UpdateCn.cn_class = CN(
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded,
            document_three_id=document_three_was_uploaded
        )
        create_ev_response = UpdateCn.cn_class.insert_cnonpn_full(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=200,
            second_tender=400
        )
        UpdateCn.ms_release_before_cn_updating = requests.get(url=create_ev_response[5]).json()
        UpdateCn.pn_release_before_cn_updating = requests.get(url=create_ev_response[6]).json()
        UpdateCn.ev_release_before_cn_updating = requests.get(url=create_ev_response[7]).json()
        UpdateCn.enquiry_period_start_date = create_ev_response[8]
        UpdateCn.enquiry_period_end_date = create_ev_response[9]
        payload = copy.deepcopy(update_cn_on_pn_payload_full_data_model_with_auction)
        payload['tender']['tenderPeriod']['endDate'] = create_ev_response[11]
        payload['tender']['enquiryPeriod']['endDate'] = create_ev_response[9]
        payload['tender']['electronicAuctions']['details'][0]['relatedLot'] = first_lot_id
        payload['tender']['electronicAuctions']['details'][1]['relatedLot'] = second_lot_id
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0][
            'id'] = document_one_was_uploaded
        payload['tender']['procuringEntity']['persones'][1]['businessFunctions'][0]['documents'][0][
            'id'] = document_two_was_uploaded
        payload['tender']['criteria'][1]['requirementGroups'][0]['requirements'][1]['eligibleEvidences'][0][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][0][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][1][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][1]['relatedItem'] = first_lot_id
        payload['tender']['criteria'][3]['relatedItem'] = first_item_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        payload['tender']['documents'][2]['id'] = document_three_was_uploaded
        payload['tender']['documents'][3]['id'] = document_four_was_uploaded
        payload['tender']['documents'][0]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = second_lot_id
        payload['tender']['documents'][2]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][3]['relatedLots'][0] = first_lot_id
        update_cn_response = UpdateCn.cn_class.update_cn(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3],
            pn_token=create_ev_response[2],
            payload=payload
        )
        UpdateCn.message_from_kafka = UpdateCn.cn_class.get_message_from_kafka()
        instance_tender_url = None
        instance_budget_url = None
        instance_storage_url = None
        if instance == "dev":
            instance_tender_url = "http://dev.public.eprocurement.systems/tenders/"
            instance_budget_url = "http://dev.public.eprocurement.systems/budgets/"
            instance_storage_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
        if instance == "sandbox":
            instance_tender_url = "http://public.eprocurement.systems/tenders/"
            instance_budget_url = "http://public.eprocurement.systems/budgets/"
            instance_storage_url = "http://storage.eprocurement.systems/get/"
        UpdateCn.instance_tender_url = instance_tender_url
        UpdateCn.instance_budget_url = instance_budget_url
        UpdateCn.instance_storage_url = instance_storage_url
        UpdateCn.payload = payload
        UpdateCn.cp_id = create_ev_response[0]
        UpdateCn.ev_id = create_ev_response[3]
        UpdateCn.pn_id = create_ev_response[1]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(update_cn_response.status_code)
        )

    @pytestrail.case('27615')
    def test_see_result_from_feed_point_27615_2(self):
        UpdateCn.successfully_update_cn = UpdateCn.cn_class.check_on_that_message_is_successfully_update_cn(
            cp_id=UpdateCn.cp_id,
            ev_id=UpdateCn.ev_id
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(UpdateCn.successfully_update_cn)
        )

    @pytestrail.case('27615')
    def test_compare_ev_release_before_updating_and_after_updating_27615_3(self):
        ev_release_after_updating = requests.get(
            url=f"{UpdateCn.message_from_kafka['data']['url']}").json()
        expected_result_tender_period = {}
        expected_result_enquiry_period = {}
        actual_result_tender_period = DeepDiff(
            UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'],
            ev_release_after_updating['releases'][0]['tender']['tenderPeriod']
        )
        actual_result_enquiry_period = DeepDiff(
            UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'],
            ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result_tender_period),
            actual_result=str(actual_result_tender_period)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result_enquiry_period),
            actual_result=str(actual_result_enquiry_period)
        )


class TestCheckOnThePossibilityOfEnquiryPeriodReschedulingForTenderInActiveClarificationTenderState3(object):
    # Check on the possibility of enquiry period resheduling for tender in active clarification tender state,
    # before "checkpoint" time if enquiryPeriod in request is bigger enquiryPeriod  in DB
    @pytestrail.case("27616")
    def test_test_send_the_request_27616_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_three_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_four_was_uploaded = document.uploading_document()[0]["data"]["id"]

        UpdateCn.cn_class = CN(
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded,
            document_three_id=document_three_was_uploaded
        )
        create_ev_response = UpdateCn.cn_class.insert_cnonpn_full(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=200,
            second_tender=400
        )
        UpdateCn.ms_release_before_cn_updating = requests.get(url=create_ev_response[5]).json()
        UpdateCn.pn_release_before_cn_updating = requests.get(url=create_ev_response[6]).json()
        UpdateCn.ev_release_before_cn_updating = requests.get(url=create_ev_response[7]).json()
        UpdateCn.enquiry_period_start_date = create_ev_response[8]
        UpdateCn.enquiry_period_end_date = create_ev_response[9]
        new_enquiry_and_tender_period = create_enquiry_and_tender_period(
            second_enquiry=300,
            second_tender=600
        )
        payload = copy.deepcopy(update_cn_on_pn_payload_full_data_model_with_auction)
        payload['tender']['tenderPeriod']['endDate'] = new_enquiry_and_tender_period[3]
        payload['tender']['enquiryPeriod']['endDate'] = new_enquiry_and_tender_period[1]
        payload['tender']['electronicAuctions']['details'][0]['relatedLot'] = first_lot_id
        payload['tender']['electronicAuctions']['details'][1]['relatedLot'] = second_lot_id
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0][
            'id'] = document_one_was_uploaded
        payload['tender']['procuringEntity']['persones'][1]['businessFunctions'][0]['documents'][0][
            'id'] = document_two_was_uploaded
        payload['tender']['criteria'][1]['requirementGroups'][0]['requirements'][1]['eligibleEvidences'][0][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][0][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][1][
            'relatedDocument']['id'] = document_four_was_uploaded
        payload['tender']['criteria'][1]['relatedItem'] = first_lot_id
        payload['tender']['criteria'][3]['relatedItem'] = first_item_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        payload['tender']['documents'][2]['id'] = document_three_was_uploaded
        payload['tender']['documents'][3]['id'] = document_four_was_uploaded
        payload['tender']['documents'][0]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = second_lot_id
        payload['tender']['documents'][2]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][3]['relatedLots'][0] = first_lot_id
        update_cn_response = UpdateCn.cn_class.update_cn(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3],
            pn_token=create_ev_response[2],
            payload=payload
        )
        UpdateCn.message_from_kafka = UpdateCn.cn_class.get_message_from_kafka()
        instance_tender_url = None
        instance_budget_url = None
        instance_storage_url = None
        if instance == "dev":
            instance_tender_url = "http://dev.public.eprocurement.systems/tenders/"
            instance_budget_url = "http://dev.public.eprocurement.systems/budgets/"
            instance_storage_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
        if instance == "sandbox":
            instance_tender_url = "http://public.eprocurement.systems/tenders/"
            instance_budget_url = "http://public.eprocurement.systems/budgets/"
            instance_storage_url = "http://storage.eprocurement.systems/get/"
        UpdateCn.instance_tender_url = instance_tender_url
        UpdateCn.instance_budget_url = instance_budget_url
        UpdateCn.instance_storage_url = instance_storage_url
        UpdateCn.payload = payload
        UpdateCn.cp_id = create_ev_response[0]
        UpdateCn.ev_id = create_ev_response[3]
        UpdateCn.pn_id = create_ev_response[1]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(update_cn_response.status_code)
        )

    @pytestrail.case('27616')
    def test_see_result_from_feed_point_27616_2(self):
        UpdateCn.successfully_update_cn = UpdateCn.cn_class.check_on_that_message_is_successfully_update_cn(
            cp_id=UpdateCn.cp_id,
            ev_id=UpdateCn.ev_id
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(UpdateCn.successfully_update_cn)
        )

    @pytestrail.case('27616')
    def test_compare_ev_release_before_updating_and_after_updating_27616_3(self):
        ev_release_after_updating = requests.get(
            url=f"{UpdateCn.message_from_kafka['data']['url']}").json()
        expected_result_tender_period = {
            'values_changed': {
                "root['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['tenderPeriod']['startDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'][
                        'startDate']
                },
                "root['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['tenderPeriod']['endDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'][
                        'endDate']
                }
            }
        }
        expected_result_enquiry_period = {
            'values_changed': {
                "root['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']['endDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'][
                        'endDate']
                }
            }
        }
        actual_result_tender_period = DeepDiff(
            UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'],
            ev_release_after_updating['releases'][0]['tender']['tenderPeriod']
        )
        actual_result_enquiry_period = DeepDiff(
            UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'],
            ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result_tender_period),
            actual_result=str(actual_result_tender_period)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result_enquiry_period),
            actual_result=str(actual_result_enquiry_period)
        )


class TestCheckOnThePossibilityOfSuspendingTender(object):
    # Tatarenko Roman  30/06/2021 4:05 PM
    # Привет! Подскажи, пожалуйста: при заморозке тендера что должно публиковаться в ev релизе и что в ms релизе.
    # А именно, в ev релизе нет атрибута аuthor.id.
    # Должен ли быть в  ms релизе объект  с ролью enquiries?
    # http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1625056672060/
    # ocds-t1s2t3-MD-1625056672060-EV-1625056672097
    # к примеру "eClarification при сохранении вопроса формирует "ID" (enquiry/author/id) автора
    # (организации, задавшей вопрос) в формате {identifier.scheme}-{identifier.id},
    # полученные из секции enquiry.author."

    # Eduard Makhankov
    # 4: 11 PM
    # при заморозке устанавливается только новое состояние, автор вопроса сейчас не должен публиковаться, по
    # требованию Молдован
    @pytestrail.case("27617")
    def test_test_send_the_request_27617_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        EnquiryGlobal.enquiry_class = Enquiry(
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_ev_response = EnquiryGlobal.enquiry_class.insert_cnonpn_obligatory(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=300,
            second_tender=602
        )
        EnquiryGlobal.ms_release_before_enquiry_creating = requests.get(url=create_ev_response[5]).json()
        EnquiryGlobal.pn_release_before_enquiry_creating = requests.get(url=create_ev_response[6]).json()
        EnquiryGlobal.ev_release_before_enquiry_creating = requests.get(url=create_ev_response[7]).json()
        EnquiryGlobal.enquiry_period_start_date = create_ev_response[8]
        EnquiryGlobal.enquiry_period_end_date = create_ev_response[9]
        EnquiryGlobal.tender_period_start_date = create_ev_response[10]
        EnquiryGlobal.tender_period_end_date = create_ev_response[11]
        payload = copy.deepcopy(create_enquiry_full_data_model)
        payload['enquiry']['relatedLot'] = first_lot_id
        create_enquiry_response = EnquiryGlobal.enquiry_class.create_enquiry(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3],
            payload=payload
        )
        EnquiryGlobal.message_from_kafka = EnquiryGlobal.enquiry_class.get_message_from_kafka()
        instance_tender_url = None
        instance_budget_url = None
        instance_storage_url = None
        if instance == "dev":
            instance_tender_url = "http://dev.public.eprocurement.systems/tenders/"
            instance_budget_url = "http://dev.public.eprocurement.systems/budgets/"
            instance_storage_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
        if instance == "sandbox":
            instance_tender_url = "http://public.eprocurement.systems/tenders/"
            instance_budget_url = "http://public.eprocurement.systems/budgets/"
            instance_storage_url = "http://storage.eprocurement.systems/get/"
        EnquiryGlobal.instance_tender_url = instance_tender_url
        EnquiryGlobal.instance_budget_url = instance_budget_url
        EnquiryGlobal.instance_storage_url = instance_storage_url
        EnquiryGlobal.payload = payload
        EnquiryGlobal.cp_id = create_ev_response[0]
        EnquiryGlobal.ev_id = create_ev_response[3]
        EnquiryGlobal.pn_id = create_ev_response[1]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_enquiry_response.status_code)
        )

    @pytestrail.case('27617')
    def test_see_result_from_feed_point_27617_2(self):
        # Can not to take second message ( public, without token) from kafka.
        privat = EnquiryGlobal.enquiry_class.check_on_that_message_is_successfully_create_enquiry_with_token(
            cp_id=EnquiryGlobal.cp_id,
            ev_id=EnquiryGlobal.ev_id
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(privat)
        )

    @pytestrail.case('27617')
    def test_compare_ev_release_before_updating_and_after_updating_27617_3(self):
        date_transformation = datetime.datetime.strptime(EnquiryGlobal.enquiry_period_end_date, "%Y-%m-%dT%H:%M:%SZ")
        time_bot(expected_time=date_transformation)
        ev_release_after_enquiry = requests.get(
            url=f"{EnquiryGlobal.message_from_kafka['data']['url']}").json()
        expected_result = {
            'dictionary_item_added': "['releases'][0]['tender']['enquiries']",
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_enquiry['releases'][0]['ocid']}-"
                                 f"{ev_release_after_enquiry['releases'][0]['id'][46:59]}",
                    'old_value': f"{EnquiryGlobal.ev_release_before_enquiry_creating['releases'][0]['ocid']}-"
                                 f"{EnquiryGlobal.ev_release_before_enquiry_creating['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_enquiry['releases'][0]['date'],
                    'old_value': EnquiryGlobal.ev_release_before_enquiry_creating['releases'][0]['date']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': 'suspended',
                    'old_value': 'clarification'
                },
                "root['releases'][0]['tender']['hasEnquiries']": {
                    'new_value': True,
                    'old_value': False
                }
            }
        }
        actual_result = DeepDiff(
            EnquiryGlobal.ev_release_before_enquiry_creating,
            ev_release_after_enquiry
        )
        dictionary_item_added_was_cleaned = str(actual_result['dictionary_item_added']).replace('root', '')[1:-1]
        actual_result['dictionary_item_added'] = dictionary_item_added_was_cleaned
        actual_enquiries = ev_release_after_enquiry['releases'][0]['tender']['enquiries']
        expected_enquiries = [{
            "id": actual_enquiries[0]['id'],
            "date": EnquiryGlobal.message_from_kafka['data']['operationDate'],
            "title": EnquiryGlobal.payload['enquiry']['title'],
            "description": EnquiryGlobal.payload['enquiry']['description'],
            "relatedLot": ev_release_after_enquiry['releases'][0]['tender']['lots'][0]['id'],
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_enquiries),
            actual_result=str(actual_enquiries)
        )

    @pytestrail.case('27617')
    def test_compare_ms_release_before_updating_and_after_updating_27617_4(self):
        date_transformation = datetime.datetime.strptime(EnquiryGlobal.enquiry_period_end_date, "%Y-%m-%dT%H:%M:%SZ")
        time_bot(expected_time=date_transformation)
        ms_release_after_enquiry = requests.get(
            url=f"{EnquiryGlobal.instance_tender_url}"
                f"/{EnquiryGlobal.cp_id}/{EnquiryGlobal.cp_id}").json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ms_release_after_enquiry['releases'][0]['ocid']}-"
                                 f"{ms_release_after_enquiry['releases'][0]['id'][29:42]}",
                    'old_value': f"{EnquiryGlobal.ms_release_before_enquiry_creating['releases'][0]['ocid']}-"
                                 f"{EnquiryGlobal.ms_release_before_enquiry_creating['releases'][0]['id'][29:42]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_enquiry['releases'][0]['date'],
                    'old_value': EnquiryGlobal.ms_release_before_enquiry_creating['releases'][0]['date']
                },
                "root['releases'][0]['tender']['hasEnquiries']": {
                    'new_value': True,
                    'old_value': False
                }
            }
        }
        actual_result = DeepDiff(
            EnquiryGlobal.ms_release_before_enquiry_creating,
            ms_release_after_enquiry
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )

# Трошки не дороблено.
# class TestCheckOnThePossibilityOfSuspendingTender(object):
#     # Tatarenko Roman  30/06/2021 4:05 PM
#     # Привет! Подскажи, пожалуйста: при заморозке тендера что должно публиковаться в ev релизе и что в ms релизе.
#     # А именно, в ev релизе нет атрибута аuthor.id.
#     # Должен ли быть в  ms релизе объект  с ролью enquiries?
#     # http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1625056672060/
#     # ocds-t1s2t3-MD-1625056672060-EV-1625056672097
#     # к примеру "eClarification при сохранении вопроса формирует "ID" (enquiry/author/id) автора
#     # (организации, задавшей вопрос) в формате {identifier.scheme}-{identifier.id},
#     # полученные из секции enquiry.author."
#
#     # Eduard Makhankov
#     # 4: 11 PM
#     # при заморозке устанавливается только новое состояние, автор вопроса сейчас не должен публиковаться, по
#     # требованию Молдован
#     @pytestrail.case("27618")
#     def test_test_send_the_request_27618_1(self, country, language, instance, cassandra_username, cassandra_password,
#                                            pmd):
#         instance = instance
#         first_lot_id = f"{uuid4()}"
#         second_lot_id = f"{uuid4()}"
#         first_item_id = f"{uuid4()}"
#         second_item_id = f"{uuid4()}"
#         EnquiryGlobal.enquiry_class = Enquiry(
#             lang=language,
#             country=country,
#             instance=instance,
#             cassandra_username=cassandra_username,
#             cassandra_password=cassandra_password,
#             pmd=pmd
#         )
#         create_ev_response = EnquiryGlobal.enquiry_class.insert_cnonpn_full(
#             first_lot_id=first_lot_id,
#             second_lot_id=second_lot_id,
#             first_item_id=first_item_id,
#             second_item_id=second_item_id,
#             second_enquiry=121,
#             second_tender=302
#         )
#         EnquiryGlobal.ms_release_before_enquiry_creating = requests.get(url=create_ev_response[5]).json()
#         EnquiryGlobal.pn_release_before_enquiry_creating = requests.get(url=create_ev_response[6]).json()
#         EnquiryGlobal.ev_release_before_enquiry_creating = requests.get(url=create_ev_response[7]).json()
#         EnquiryGlobal.enquiry_period_start_date = create_ev_response[8]
#         EnquiryGlobal.enquiry_period_end_date = create_ev_response[9]
#         EnquiryGlobal.tender_period_start_date = create_ev_response[10]
#         EnquiryGlobal.tender_period_end_date = create_ev_response[11]
#         payload = copy.deepcopy(create_enquiry_full_data_model)
#         payload['enquiry']['relatedLot'] = first_lot_id
#         create_enquiry_response = EnquiryGlobal.enquiry_class.create_enquiry(
#             cp_id=create_ev_response[0],
#             ev_id=create_ev_response[3],
#             payload=payload
#         )
#         EnquiryGlobal.message_from_kafka = EnquiryGlobal.enquiry_class.get_message_from_kafka()
#         EnquiryGlobal.payload = payload
#         EnquiryGlobal.cp_id = create_ev_response[0]
#         EnquiryGlobal.ev_id = create_ev_response[3]
#         EnquiryGlobal.pn_id = create_ev_response[1]
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(202),
#             actual_result=str(create_enquiry_response.status_code)
#         )
#
#     @pytestrail.case('27618')
#     def test_see_result_from_feed_point_27618_2(self):
#         # Can not to take second message ( public, without token) from kafka.
#         privat = EnquiryGlobal.enquiry_class.check_on_that_message_is_successfully_create_enquiry_with_token(
#             cp_id=EnquiryGlobal.cp_id,
#             ev_id=EnquiryGlobal.ev_id
#         )
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(True),
#             actual_result=str(privat)
#         )
#
#     @pytestrail.case('27618')
#     def test_compare_ev_release_before_updating_and_after_updating_27618_3(self):
#         date_transformation = datetime.datetime.strptime(EnquiryGlobal.enquiry_period_end_date, "%Y-%m-%dT%H:%M:%SZ")
#         time_bot(expected_time=date_transformation)
#         ev_release_after_enquiry = requests.get(
#             url=f"{EnquiryGlobal.message_from_kafka['data']['url']}").json()
#         expected_result = {
#             'dictionary_item_added': "['releases'][0]['tender']['enquiries']",
#             'values_changed': {
#                 "root['releases'][0]['id']": {
#                     'new_value': f"{ev_release_after_enquiry['releases'][0]['ocid']}-"
#                                  f"{ev_release_after_enquiry['releases'][0]['id'][46:59]}",
#                     'old_value': f"{EnquiryGlobal.ev_release_before_enquiry_creating['releases'][0]['ocid']}-"
#                                  f"{EnquiryGlobal.ev_release_before_enquiry_creating['releases'][0]['id'][46:59]}"
#                 },
#                 "root['releases'][0]['date']": {
#                     'new_value': ev_release_after_enquiry['releases'][0]['date'],
#                     'old_value': EnquiryGlobal.ev_release_before_enquiry_creating['releases'][0]['date']
#                 },
#                 "root['releases'][0]['tender']['statusDetails']": {
#                     'new_value': 'suspended',
#                     'old_value': 'clarification'
#                 },
#                 "root['releases'][0]['tender']['hasEnquiries']": {
#                     'new_value': True,
#                     'old_value': False
#                 }
#             }
#         }
#         actual_result = DeepDiff(
#             EnquiryGlobal.ev_release_before_enquiry_creating,
#             ev_release_after_enquiry
#         )
#         dictionary_item_added_was_cleaned = str(actual_result['dictionary_item_added']).replace('root', '')[1:-1]
#         actual_result['dictionary_item_added'] = dictionary_item_added_was_cleaned
#         actual_enquiries = ev_release_after_enquiry['releases'][0]['tender']['enquiries']
#         expected_enquiries = [{
#             "id": actual_enquiries[0]['id'],
#             "date": EnquiryGlobal.message_from_kafka['data']['operationDate'],
#             "title": EnquiryGlobal.payload['enquiry']['title'],
#             "description": EnquiryGlobal.payload['enquiry']['description'],
#             "relatedLot": ev_release_after_enquiry['releases'][0]['tender']['lots'][0]['id'],
#         }]
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(expected_result),
#             actual_result=str(actual_result)
#         )
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(expected_enquiries),
#             actual_result=str(actual_enquiries)
#         )
#
#     @pytestrail.case('27618')
#     def test_compare_ms_release_before_updating_and_after_updating_27618_4(self):
#         date_transformation = datetime.datetime.strptime(EnquiryGlobal.enquiry_period_end_date, "%Y-%m-%dT%H:%M:%SZ")
#         time_bot(expected_time=date_transformation)
#         ms_release_after_enquiry = requests.get(
#             url=f"http://dev.public.eprocurement.systems/tenders"
#                 f"/{EnquiryGlobal.cp_id}/{EnquiryGlobal.cp_id}").json()
#         expected_result = {
#             'values_changed': {
#                 "root['releases'][0]['id']": {
#                     'new_value': f"{ms_release_after_enquiry['releases'][0]['ocid']}-"
#                                  f"{ms_release_after_enquiry['releases'][0]['id'][29:42]}",
#                     'old_value': f"{EnquiryGlobal.ms_release_before_enquiry_creating['releases'][0]['ocid']}-"
#                                  f"{EnquiryGlobal.ms_release_before_enquiry_creating['releases'][0]['id'][29:42]}"
#                 },
#                 "root['releases'][0]['date']": {
#                     'new_value': ms_release_after_enquiry['releases'][0]['date'],
#                     'old_value': EnquiryGlobal.ms_release_before_enquiry_creating['releases'][0]['date']
#                 },
#                 "root['releases'][0]['tender']['hasEnquiries']": {
#                     'new_value': True,
#                     'old_value': False
#                 }
#             }
#         }
#         actual_result = DeepDiff(
#             EnquiryGlobal.ms_release_before_enquiry_creating,
#             ms_release_after_enquiry
#         )
#         assert compare_actual_result_and_expected_result(
#             expected_result=str(expected_result),
#             actual_result=str(actual_result)
#         )
