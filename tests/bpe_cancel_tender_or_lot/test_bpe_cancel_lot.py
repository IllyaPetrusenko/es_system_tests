import copy
from uuid import uuid4
import requests
from deepdiff import DeepDiff
from pytest_testrail.plugin import pytestrail
from tests.conftest import CancelLot
from tests.essences.cancel_tender import CancelTender

from tests.iStorage import Document
from tests.payloads.cancel_tender import cancel_tender_or_lot_payload_full_data_model, \
    cancel_tender_or_lot_payload_obligatory_data_model
from useful_functions import compare_actual_result_and_expected_result


class TestCheckOnThePossibilityOfLotCancellationForTenderInActiveClarificationTenderStateWithFullDataModel1(object):
    # Check on the possibility of lot cancellation for tender in active clarification tender state
    # with full data model in request, based on CnOnPn full data model.
    @pytestrail.case("27607")
    def test_test_send_the_request_27607_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        payload = copy.deepcopy(cancel_tender_or_lot_payload_full_data_model)
        payload['amendments'][0]['documents'][0]['id'] = document_one_was_uploaded
        cancel_tender = CancelTender(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_ev_response = cancel_tender.insert_cnonpn_full(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=121,
            second_tender=300
        )
        CancelLot.ms_release_before_lot_cancelling = requests.get(url=create_ev_response[5]).json()
        CancelLot.pn_release_before_lot_cancelling = requests.get(url=create_ev_response[6]).json()
        CancelLot.ev_release_before_lot_cancelling = requests.get(url=create_ev_response[7]).json()
        cancel_lot_response = cancel_tender.cancel_lot(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3],
            pn_token=create_ev_response[2],
            lot_id=first_lot_id
        )
        CancelLot.message_from_kafka = cancel_tender.get_message_from_kafka()
        CancelLot.successfully_cancel_lot = cancel_tender.check_on_that_message_is_successfully_cancel_tender(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3]
        )
        CancelLot.payload = payload
        CancelLot.cp_id = create_ev_response[0]
        CancelLot.ev_id = create_ev_response[3]
        CancelLot.pn_id = create_ev_response[1]
        CancelLot.lot_id = first_lot_id
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(cancel_lot_response.status_code)
        )

    @pytestrail.case('27607')
    def test_see_result_from_feed_point_27607_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(CancelLot.successfully_cancel_lot)
        )

    @pytestrail.case('27607')
    def test_compare_ev_release_before_updating_and_after_updating_27607_3(self):
        ev_release_after_cancelling = requests.get(
            url=f"{CancelLot.message_from_kafka['data']['url']}").json()


        expected_result = {
            'dictionary_item_added': "['releases'][0]['tender']['amendments']",
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_cancelling['releases'][0]['ocid']}-"
                                 f"{ev_release_after_cancelling['releases'][0]['id'][46:59]}",
                    'old_value': f"{CancelLot.ev_release_before_lot_cancelling['releases'][0]['ocid']}-"
                                 f"{CancelLot.ev_release_before_lot_cancelling['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_cancelling['releases'][0]['date'],
                    'old_value': CancelLot.ev_release_before_lot_cancelling['releases'][0]['date']
                }
            }
        }
        actual_result = DeepDiff(CancelLot.ev_release_before_lot_cancelling, ev_release_after_cancelling)
        dictionary_item_added_was_cleaned = str(actual_result['dictionary_item_added']).replace('root', '')[1:-1]
        actual_result['dictionary_item_added'] = dictionary_item_added_was_cleaned
        actual_amendments = ev_release_after_cancelling['releases'][0]['tender']['amendments']
        expected_amendments = [{
            "id": actual_amendments[0]['id'],
            "type": "cancellation",
            "status": "pending",
            "relatesTo": "lot",
            "relatedItem": CancelLot.lot_id,
            "date": CancelLot.message_from_kafka['data']['operationDate'],
            "description": CancelLot.payload['amendments'][0]['description'],
            "rationale": CancelLot.payload['amendments'][0]['rationale'],
            "documents": [{
                "id": CancelLot.payload['amendments'][0]['documents'][0]['id'],
                "documentType": CancelLot.payload['amendments'][0]['documents'][0]['documentType'],
                "title": CancelLot.payload['amendments'][0]['documents'][0]['title'],
                "description": CancelLot.payload['amendments'][0]['documents'][0]['description'],
                "url": f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                       f"{CancelLot.payload['amendments'][0]['documents'][0]['id']}",
                "datePublished": CancelLot.message_from_kafka['data']['operationDate']
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

    @pytestrail.case('27607')
    def test_compare_ev_release_before_updating_and_after_updating_27607_4(self):
        ms_release_after_cancelling = requests.get(
            url=f"http://dev.public.eprocurement.systems/tenders/{CancelLot.cp_id}/{CancelLot.cp_id}").json()

        expected_result = {}
        actual_result = DeepDiff(CancelLot.ms_release_before_lot_cancelling, ms_release_after_cancelling)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckOnThePossibilityOfLotCancellationForTenderInActiveClarificationTenderStateWithFullDataModel2(object):
    # Check on the possibility of lot cancellation for tender in active clarification tender state
    # with full data model in request, based on CnOnPn obligatory data model.
    @pytestrail.case("27608")
    def test_test_send_the_request_27608_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        payload = copy.deepcopy(cancel_tender_or_lot_payload_obligatory_data_model)
        cancel_tender = CancelTender(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_ev_response = cancel_tender.insert_cnonpn_obligatory(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=121,
            second_tender=300
        )
        CancelLot.ms_release_before_lot_cancelling = requests.get(url=create_ev_response[5]).json()
        CancelLot.pn_release_before_lot_cancelling = requests.get(url=create_ev_response[6]).json()
        CancelLot.ev_release_before_lot_cancelling = requests.get(url=create_ev_response[7]).json()
        cancel_lot_response = cancel_tender.cancel_lot(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3],
            pn_token=create_ev_response[2],
            lot_id=first_lot_id
        )
        CancelLot.message_from_kafka = cancel_tender.get_message_from_kafka()
        CancelLot.successfully_cancel_lot = cancel_tender.check_on_that_message_is_successfully_cancel_tender(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3]
        )
        CancelLot.payload = payload
        CancelLot.cp_id = create_ev_response[0]
        CancelLot.ev_id = create_ev_response[3]
        CancelLot.pn_id = create_ev_response[1]
        CancelLot.lot_id = first_lot_id
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(cancel_lot_response.status_code)
        )

    @pytestrail.case('27608')
    def test_see_result_from_feed_point_27608_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(CancelLot.successfully_cancel_lot)
        )

    @pytestrail.case('27608')
    def test_compare_ev_release_before_updating_and_after_updating_27608_3(self):
        ev_release_after_cancelling = requests.get(
            url=f"{CancelLot.message_from_kafka['data']['url']}").json()

        expected_result = {
            'dictionary_item_added': "['releases'][0]['tender']['amendments']",
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_cancelling['releases'][0]['ocid']}-"
                                 f"{ev_release_after_cancelling['releases'][0]['id'][46:59]}",
                    'old_value': f"{CancelLot.ev_release_before_lot_cancelling['releases'][0]['ocid']}-"
                                 f"{CancelLot.ev_release_before_lot_cancelling['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_cancelling['releases'][0]['date'],
                    'old_value': CancelLot.ev_release_before_lot_cancelling['releases'][0]['date']
                }
            }
        }
        actual_result = DeepDiff(CancelLot.ev_release_before_lot_cancelling, ev_release_after_cancelling)
        dictionary_item_added_was_cleaned = str(actual_result['dictionary_item_added']).replace('root', '')[1:-1]
        actual_result['dictionary_item_added'] = dictionary_item_added_was_cleaned
        actual_amendments = ev_release_after_cancelling['releases'][0]['tender']['amendments']
        expected_amendments = [{
            "id": actual_amendments[0]['id'],
            "type": "cancellation",
            "status": "pending",
            "relatesTo": "lot",
            "relatedItem": CancelLot.lot_id,
            "date": CancelLot.message_from_kafka['data']['operationDate'],
            "rationale": CancelLot.payload['amendments'][0]['rationale'],
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_amendments),
            actual_result=str(actual_amendments)
        )

    @pytestrail.case('27608')
    def test_compare_ev_release_before_updating_and_after_updating_27608_4(self):
        ms_release_after_cancelling = requests.get(
            url=f"http://dev.public.eprocurement.systems/tenders/{CancelLot.cp_id}/{CancelLot.cp_id}").json()
        expected_result = {}
        actual_result = DeepDiff(CancelLot.ms_release_before_lot_cancelling, ms_release_after_cancelling)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
