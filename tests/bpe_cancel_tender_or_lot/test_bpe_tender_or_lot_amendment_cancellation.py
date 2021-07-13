from uuid import uuid4
import requests
from deepdiff import DeepDiff
from pytest_testrail.plugin import pytestrail
from tests.conftest import CancelTenderAmendment, CancelLotAmendment
from tests.essences.cancel_tender import CancelTender
from useful_functions import compare_actual_result_and_expected_result


class TestCheckOnThePossibilityOfTenderAmendmentCancellationForTenderInActiveClarificationTenderStatus1(object):
    # Check on the possibility of tender amendment cancellation  for tender in active clarification tender state,
    # based on CnOnPn and Amendment Full Data Model
    @pytestrail.case("27605")
    def test_test_send_the_request_27605_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        cancel_tender = CancelTender(
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        cancel_tender_response = cancel_tender.insert_cancel_tender_full(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=121,
            second_tender=300

        )

        CancelTenderAmendment.ms_release_before_tender_amendment_cancellation = requests.get(
            url=cancel_tender_response[5]).json()
        CancelTenderAmendment.pn_release_before_tender_amendment_cancellation = requests.get(
            url=cancel_tender_response[6]).json()
        CancelTenderAmendment.ev_release_before_tender_amendment_cancellation = requests.get(
            url=cancel_tender_response[7]).json()
        tender_amendment_cancellation_response = cancel_tender.tender_amendment_cancellation(
            cp_id=cancel_tender_response[0],
            ev_id=cancel_tender_response[3]
        )
        CancelTenderAmendment.message_from_kafka = cancel_tender.get_message_from_kafka()
        CancelTenderAmendment.successfully_tender_amendment_cancellation = cancel_tender. \
            check_on_that_message_is_successfully_tender_amendment_cancellation(
                cp_id=cancel_tender_response[0],
                ev_id=cancel_tender_response[3]
            )
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
        CancelTenderAmendment.instance_tender_url = instance_tender_url
        CancelTenderAmendment.instance_budget_url = instance_budget_url
        CancelTenderAmendment.instance_storage_url = instance_storage_url
        CancelTenderAmendment.cp_id = cancel_tender_response[0]
        CancelTenderAmendment.ev_id = cancel_tender_response[3]
        CancelTenderAmendment.pn_id = cancel_tender_response[1]
        CancelTenderAmendment.amendment_id = cancel_tender_response[8]
        CancelTenderAmendment.amendment_token = cancel_tender_response[9]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(tender_amendment_cancellation_response.status_code)
        )

    @pytestrail.case('27605')
    def test_see_result_from_feed_point_27605_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(CancelTenderAmendment.successfully_tender_amendment_cancellation
                              )
        )

    @pytestrail.case('27605')
    def test_compare_ev_release_before_updating_and_after_updating_27605_3(self):
        ev_release_after_tender_amendment_cancellation = requests.get(
            url=f"{CancelTenderAmendment.message_from_kafka['data']['url']}").json()
        before_tender_amendment_cancellation = CancelTenderAmendment.ev_release_before_tender_amendment_cancellation
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_tender_amendment_cancellation['releases'][0]['ocid']}-"
                                 f"{ev_release_after_tender_amendment_cancellation['releases'][0]['id'][46:59]}",
                    'old_value': f"{before_tender_amendment_cancellation['releases'][0]['ocid']}-"
                                 f"{before_tender_amendment_cancellation['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_tender_amendment_cancellation['releases'][0]['date'],
                    'old_value': before_tender_amendment_cancellation['releases'][0]['date']
                },
                "root['releases'][0]['tender']['amendments'][0]['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'pending'
                }
            }
        }
        actual_result = DeepDiff(CancelTenderAmendment.ev_release_before_tender_amendment_cancellation,
                                 ev_release_after_tender_amendment_cancellation)
        previous_amendments = before_tender_amendment_cancellation['releases'][0]['tender']['amendments']
        actual_amendments = ev_release_after_tender_amendment_cancellation['releases'][0]['tender']['amendments']
        expected_amendments = [{
            "id": previous_amendments[0]['id'],
            "type": "cancellation",
            "status": "cancelled",
            "relatesTo": "tender",
            "relatedItem": CancelTenderAmendment.message_from_kafka['data']['ocid'],
            "date": previous_amendments[0]['date'],
            "description": previous_amendments[0]['description'],
            "rationale": previous_amendments[0]['rationale'],
            "documents": [{
                "id": previous_amendments[0]['documents'][0]['id'],
                "documentType": previous_amendments[0]['documents'][0]['documentType'],
                "title": previous_amendments[0]['documents'][0]['title'],
                "description": previous_amendments[0]['documents'][0]['description'],
                "url": previous_amendments[0]['documents'][0]['url'],
                "datePublished": previous_amendments[0]['documents'][0]['datePublished']
            }]
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_amendments),
            actual_result=str(actual_amendments)
        )

    @pytestrail.case('27605')
    def test_compare_ev_release_before_updating_and_after_updating_27605_4(self):
        ms_release_after_tender_amendment_cancellation = requests.get(
            url=f"{CancelTenderAmendment.instance_tender_url}{CancelTenderAmendment.cp_id}/"
                f"{CancelTenderAmendment.cp_id}").json()

        expected_result = {}
        actual_result = DeepDiff(CancelTenderAmendment.ms_release_before_tender_amendment_cancellation,
                                 ms_release_after_tender_amendment_cancellation)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckOnThePossibilityOfTenderAmendmentCancellationForTenderInActiveClarificationTenderStatus2(object):
    # Check on the possibility of tender amendment cancellation  for tender in active clarification tender state,
    # based on CnOnPn and Amendment Obligatory Data Model
    @pytestrail.case("27606")
    def test_test_send_the_request_27606_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        cancel_tender = CancelTender(
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        cancel_tender_response = cancel_tender.insert_cancel_tender_obligatory(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=121,
            second_tender=300

        )

        CancelTenderAmendment.ms_release_before_tender_amendment_cancellation = requests.get(
            url=cancel_tender_response[5]).json()
        CancelTenderAmendment.pn_release_before_tender_amendment_cancellation = requests.get(
            url=cancel_tender_response[6]).json()
        CancelTenderAmendment.ev_release_before_tender_amendment_cancellation = requests.get(
            url=cancel_tender_response[7]).json()
        tender_amendment_cancellation_response = cancel_tender.tender_amendment_cancellation(
            cp_id=cancel_tender_response[0],
            ev_id=cancel_tender_response[3]
        )
        CancelTenderAmendment.message_from_kafka = cancel_tender.get_message_from_kafka()
        CancelTenderAmendment.successfully_tender_amendment_cancellation = cancel_tender. \
            check_on_that_message_is_successfully_tender_amendment_cancellation(
                cp_id=cancel_tender_response[0],
                ev_id=cancel_tender_response[3]
            )
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
        CancelTenderAmendment.instance_tender_url = instance_tender_url
        CancelTenderAmendment.instance_budget_url = instance_budget_url
        CancelTenderAmendment.instance_storage_url = instance_storage_url
        CancelTenderAmendment.cp_id = cancel_tender_response[0]
        CancelTenderAmendment.ev_id = cancel_tender_response[3]
        CancelTenderAmendment.pn_id = cancel_tender_response[1]
        CancelTenderAmendment.amendment_id = cancel_tender_response[8]
        CancelTenderAmendment.amendment_token = cancel_tender_response[9]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(tender_amendment_cancellation_response.status_code)
        )

    @pytestrail.case('27606')
    def test_see_result_from_feed_point_27606_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(CancelTenderAmendment.successfully_tender_amendment_cancellation)
        )

    @pytestrail.case('27606')
    def test_compare_ev_release_before_updating_and_after_updating_27606_3(self):
        ev_release_after_tender_amendment_cancellation = requests.get(
            url=f"{CancelTenderAmendment.message_from_kafka['data']['url']}").json()
        before_tender_amendment_cancellation = CancelTenderAmendment.ev_release_before_tender_amendment_cancellation
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_tender_amendment_cancellation['releases'][0]['ocid']}-"
                                 f"{ev_release_after_tender_amendment_cancellation['releases'][0]['id'][46:59]}",
                    'old_value': f"{before_tender_amendment_cancellation['releases'][0]['ocid']}-"
                                 f"{before_tender_amendment_cancellation['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_tender_amendment_cancellation['releases'][0]['date'],
                    'old_value': before_tender_amendment_cancellation['releases'][0]['date']
                },
                "root['releases'][0]['tender']['amendments'][0]['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'pending'
                }
            }
        }
        actual_result = DeepDiff(CancelTenderAmendment.ev_release_before_tender_amendment_cancellation,
                                 ev_release_after_tender_amendment_cancellation)
        previous_amendments = before_tender_amendment_cancellation['releases'][0]['tender']['amendments']
        actual_amendments = ev_release_after_tender_amendment_cancellation['releases'][0]['tender']['amendments']
        expected_amendments = [{
            "id": previous_amendments[0]['id'],
            "type": "cancellation",
            "status": "cancelled",
            "relatesTo": "tender",
            "relatedItem": CancelTenderAmendment.message_from_kafka['data']['ocid'],
            "date": previous_amendments[0]['date'],
            "rationale": previous_amendments[0]['rationale']
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_amendments),
            actual_result=str(actual_amendments)
        )

    @pytestrail.case('27606')
    def test_compare_ev_release_before_updating_and_after_updating_27606_4(self):
        ms_release_after_tender_amendment_cancellation = requests.get(
            url=f"{CancelTenderAmendment.instance_tender_url}{CancelTenderAmendment.cp_id}/"
                f"{CancelTenderAmendment.cp_id}").json()

        expected_result = {}
        actual_result = DeepDiff(CancelTenderAmendment.ms_release_before_tender_amendment_cancellation,
                                 ms_release_after_tender_amendment_cancellation)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckOnThePossibilityOfLotAmendmentCancellationForTenderInActiveClarificationTenderStatus1(object):
    # Check on the possibility of lot amendment cancellation  for tender in active clarification tender state,
    # based on CnOnPn and Amendment Full Data Model
    @pytestrail.case("27609")
    def test_test_send_the_request_27609_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        cancel_tender = CancelTender(
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        cancel_lot_response = cancel_tender.insert_cancel_lot_full(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=121,
            second_tender=300,
            lot_id=first_lot_id
        )

        CancelLotAmendment.ms_release_before_lot_amendment_cancellation = requests.get(
            url=cancel_lot_response[5]).json()
        CancelLotAmendment.pn_release_before_lot_amendment_cancellation = requests.get(
            url=cancel_lot_response[6]).json()
        CancelLotAmendment.ev_release_before_lot_amendment_cancellation = requests.get(
            url=cancel_lot_response[7]).json()
        lot_amendment_cancellation_response = cancel_tender.tender_amendment_cancellation(
                cp_id=cancel_lot_response[0],
                ev_id=cancel_lot_response[3]
            )
        CancelLotAmendment.message_from_kafka = cancel_tender.get_message_from_kafka()
        CancelLotAmendment.successfully_lot_amendment_cancellation = cancel_tender. \
            check_on_that_message_is_successfully_tender_amendment_cancellation(
                cp_id=cancel_lot_response[0],
                ev_id=cancel_lot_response[3]
            )
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
        CancelLotAmendment.instance_tender_url = instance_tender_url
        CancelLotAmendment.instance_budget_url = instance_budget_url
        CancelLotAmendment.instance_storage_url = instance_storage_url
        CancelLotAmendment.cp_id = cancel_lot_response[0]
        CancelLotAmendment.ev_id = cancel_lot_response[3]
        CancelLotAmendment.pn_id = cancel_lot_response[1]
        CancelLotAmendment.lot_id = first_lot_id
        CancelLotAmendment.amendment_id = cancel_lot_response[8]
        CancelLotAmendment.amendment_token = cancel_lot_response[9]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(lot_amendment_cancellation_response.status_code)
        )

    @pytestrail.case('27609')
    def test_see_result_from_feed_point_27609_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(CancelLotAmendment.successfully_lot_amendment_cancellation)
        )

    @pytestrail.case('27609')
    def test_compare_ev_release_before_updating_and_after_updating_27609_3(self):
        ev_release_after_lot_amendment_cancellation = requests.get(
            url=f"{CancelLotAmendment.message_from_kafka['data']['url']}").json()
        before_lot_amendment_cancellation = CancelLotAmendment.ev_release_before_lot_amendment_cancellation
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_lot_amendment_cancellation['releases'][0]['ocid']}-"
                                 f"{ev_release_after_lot_amendment_cancellation['releases'][0]['id'][46:59]}",
                    'old_value': f"{before_lot_amendment_cancellation['releases'][0]['ocid']}-"
                                 f"{before_lot_amendment_cancellation['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_lot_amendment_cancellation['releases'][0]['date'],
                    'old_value': before_lot_amendment_cancellation['releases'][0]['date']
                },
                "root['releases'][0]['tender']['amendments'][0]['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'pending'
                }
            }
        }
        actual_result = DeepDiff(CancelLotAmendment.ev_release_before_lot_amendment_cancellation,
                                 ev_release_after_lot_amendment_cancellation)
        previous_amendments = before_lot_amendment_cancellation['releases'][0]['tender']['amendments']
        actual_amendments = ev_release_after_lot_amendment_cancellation['releases'][0]['tender']['amendments']
        expected_amendments = [{
            "id": previous_amendments[0]['id'],
            "type": "cancellation",
            "status": "cancelled",
            "relatesTo": "lot",
            "relatedItem": CancelLotAmendment.lot_id,
            "date": previous_amendments[0]['date'],
            "description": previous_amendments[0]['description'],
            "rationale": previous_amendments[0]['rationale'],
            "documents": [{
                "id": previous_amendments[0]['documents'][0]['id'],
                "documentType": previous_amendments[0]['documents'][0]['documentType'],
                "title": previous_amendments[0]['documents'][0]['title'],
                "description": previous_amendments[0]['documents'][0]['description'],
                "url": previous_amendments[0]['documents'][0]['url'],
                "datePublished": previous_amendments[0]['documents'][0]['datePublished']
            }]
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_amendments),
            actual_result=str(actual_amendments)
        )

    @pytestrail.case('27609')
    def test_compare_ev_release_before_updating_and_after_updating_27609_4(self):
        ms_release_after_lot_amendment_cancellation = requests.get(
            url=f"{CancelLotAmendment.instance_tender_url}{CancelLotAmendment.cp_id}/"
                f"{CancelLotAmendment.cp_id}").json()

        expected_result = {}
        actual_result = DeepDiff(CancelLotAmendment.ms_release_before_lot_amendment_cancellation,
                                 ms_release_after_lot_amendment_cancellation)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckOnThePossibilityOfLotAmendmentCancellationForTenderInActiveClarificationTenderStatus2(object):
    # Check on the possibility of lot amendment cancellation  for tender in active clarification tender state,
    # based on CnOnPn and Amendment Obligatory Data Model
    @pytestrail.case("27610")
    def test_test_send_the_request_27610_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        cancel_tender = CancelTender(
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        cancel_lot_response = cancel_tender.insert_cancel_lot_obligatory(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=121,
            second_tender=300,
            lot_id=first_lot_id
        )

        CancelLotAmendment.ms_release_before_lot_amendment_cancellation = requests.get(
            url=cancel_lot_response[5]).json()
        CancelLotAmendment.pn_release_before_lot_amendment_cancellation = requests.get(
            url=cancel_lot_response[6]).json()
        CancelLotAmendment.ev_release_before_lot_amendment_cancellation = requests.get(
            url=cancel_lot_response[7]).json()
        lot_amendment_cancellation_response = cancel_tender.tender_amendment_cancellation(
                cp_id=cancel_lot_response[0],
                ev_id=cancel_lot_response[3]
            )
        CancelLotAmendment.message_from_kafka = cancel_tender.get_message_from_kafka()
        CancelLotAmendment.successfully_lot_amendment_cancellation = cancel_tender. \
            check_on_that_message_is_successfully_tender_amendment_cancellation(
                cp_id=cancel_lot_response[0],
                ev_id=cancel_lot_response[3]
            )
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
        CancelLotAmendment.instance_tender_url = instance_tender_url
        CancelLotAmendment.instance_budget_url = instance_budget_url
        CancelLotAmendment.instance_storage_url = instance_storage_url
        CancelLotAmendment.cp_id = cancel_lot_response[0]
        CancelLotAmendment.ev_id = cancel_lot_response[3]
        CancelLotAmendment.pn_id = cancel_lot_response[1]
        CancelLotAmendment.lot_id = first_lot_id
        CancelLotAmendment.amendment_id = cancel_lot_response[8]
        CancelLotAmendment.amendment_token = cancel_lot_response[9]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(lot_amendment_cancellation_response.status_code)
        )

    @pytestrail.case('27610')
    def test_see_result_from_feed_point_27610_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(CancelLotAmendment.successfully_lot_amendment_cancellation)
        )

    @pytestrail.case('27610')
    def test_compare_ev_release_before_updating_and_after_updating_27610_3(self):
        ev_release_after_lot_amendment_cancellation = requests.get(
            url=f"{CancelLotAmendment.message_from_kafka['data']['url']}").json()
        before_lot_amendment_cancellation = CancelLotAmendment.ev_release_before_lot_amendment_cancellation
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_lot_amendment_cancellation['releases'][0]['ocid']}-"
                                 f"{ev_release_after_lot_amendment_cancellation['releases'][0]['id'][46:59]}",
                    'old_value': f"{before_lot_amendment_cancellation['releases'][0]['ocid']}-"
                                 f"{before_lot_amendment_cancellation['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_lot_amendment_cancellation['releases'][0]['date'],
                    'old_value': before_lot_amendment_cancellation['releases'][0]['date']
                },
                "root['releases'][0]['tender']['amendments'][0]['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'pending'
                }
            }
        }
        actual_result = DeepDiff(CancelLotAmendment.ev_release_before_lot_amendment_cancellation,
                                 ev_release_after_lot_amendment_cancellation)
        previous_amendments = before_lot_amendment_cancellation['releases'][0]['tender']['amendments']
        actual_amendments = ev_release_after_lot_amendment_cancellation['releases'][0]['tender']['amendments']
        expected_amendments = [{
            "id": previous_amendments[0]['id'],
            "type": "cancellation",
            "status": "cancelled",
            "relatesTo": "lot",
            "relatedItem": CancelLotAmendment.lot_id,
            "date": previous_amendments[0]['date'],
            "rationale": previous_amendments[0]['rationale']
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_amendments),
            actual_result=str(actual_amendments)
        )

    @pytestrail.case('27610')
    def test_compare_ev_release_before_updating_and_after_updating_27610_4(self):
        ms_release_after_lot_amendment_cancellation = requests.get(
            url=f"{CancelLotAmendment.instance_tender_url}{CancelLotAmendment.cp_id}/"
                f"{CancelLotAmendment.cp_id}").json()

        expected_result = {}
        actual_result = DeepDiff(CancelLotAmendment.ms_release_before_lot_amendment_cancellation,
                                 ms_release_after_lot_amendment_cancellation)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
