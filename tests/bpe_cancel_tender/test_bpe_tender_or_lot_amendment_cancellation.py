from uuid import uuid4
import requests
from deepdiff import DeepDiff
from pytest_testrail.plugin import pytestrail
from tests.conftest import CancelTenderAmendment
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
        tender_amendment_confirmation_response = cancel_tender.tender_amendment_cancellation(
            cp_id=cancel_tender_response[0],
            ev_id=cancel_tender_response[3]
        )
        CancelTenderAmendment.message_from_kafka = cancel_tender.get_message_from_kafka()
        CancelTenderAmendment.successfully_tender_amendment_cancellation = cancel_tender. \
            check_on_that_message_is_successfully_tender_amendment_confirmation(
                cp_id=cancel_tender_response[0],
                ev_id=cancel_tender_response[3]
            )
        CancelTenderAmendment.cp_id = cancel_tender_response[0]
        CancelTenderAmendment.ev_id = cancel_tender_response[3]
        CancelTenderAmendment.pn_id = cancel_tender_response[1]
        CancelTenderAmendment.amendment_id = cancel_tender_response[8]
        CancelTenderAmendment.amendment_token = cancel_tender_response[9]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(tender_amendment_confirmation_response.status_code)
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
            url=f"http://dev.public.eprocurement.systems/tenders/{CancelTenderAmendment.cp_id}/"
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
        tender_amendment_confirmation_response = cancel_tender.tender_amendment_cancellation(
            cp_id=cancel_tender_response[0],
            ev_id=cancel_tender_response[3]
        )
        CancelTenderAmendment.message_from_kafka = cancel_tender.get_message_from_kafka()
        CancelTenderAmendment.successfully_tender_amendment_cancellation = cancel_tender. \
            check_on_that_message_is_successfully_tender_amendment_confirmation(
                cp_id=cancel_tender_response[0],
                ev_id=cancel_tender_response[3]
            )
        CancelTenderAmendment.cp_id = cancel_tender_response[0]
        CancelTenderAmendment.ev_id = cancel_tender_response[3]
        CancelTenderAmendment.pn_id = cancel_tender_response[1]
        CancelTenderAmendment.amendment_id = cancel_tender_response[8]
        CancelTenderAmendment.amendment_token = cancel_tender_response[9]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(tender_amendment_confirmation_response.status_code)
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
            url=f"http://dev.public.eprocurement.systems/tenders/{CancelTenderAmendment.cp_id}/"
                f"{CancelTenderAmendment.cp_id}").json()

        expected_result = {}
        actual_result = DeepDiff(CancelTenderAmendment.ms_release_before_tender_amendment_cancellation,
                                 ms_release_after_tender_amendment_cancellation)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
