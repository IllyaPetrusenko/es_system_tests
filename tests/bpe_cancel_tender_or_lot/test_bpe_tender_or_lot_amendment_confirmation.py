from uuid import uuid4
import requests
from deepdiff import DeepDiff
from pytest_testrail.plugin import pytestrail
from tests.conftest import ConfirmTenderAmendment, ConfirmLotAmendment
from tests.essences.cancel_tender import CancelTender
from useful_functions import compare_actual_result_and_expected_result


class TestCheckOnThePossibilityOfTenderAmendmentConfirmationForTenderInActiveClarificationTenderStatus1(object):
    # Check on the possibility of tender amendment confirmation  for tender in active clarification tender state,
    # based on CnOnPn and Amendment Full Data Model
    @pytestrail.case("27602")
    def test_test_send_the_request_27602_1(self, country, language, instance, cassandra_username, cassandra_password,
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

        ConfirmTenderAmendment.ms_release_before_tender_amendment_confirmation = requests.get(
            url=cancel_tender_response[5]).json()
        ConfirmTenderAmendment.pn_release_before_tender_amendment_confirmation = requests.get(
            url=cancel_tender_response[6]).json()
        ConfirmTenderAmendment.ev_release_before_tender_amendment_confirmation = requests.get(
            url=cancel_tender_response[7]).json()
        tender_amendment_confirmation_response = cancel_tender.confirm_tender_cancellation(
            cp_id=cancel_tender_response[0],
            ev_id=cancel_tender_response[3]
        )
        ConfirmTenderAmendment.message_from_kafka = cancel_tender.get_message_from_kafka()
        ConfirmTenderAmendment.successfully_tender_amendment_confirmation = cancel_tender.\
            check_on_that_message_is_successfully_tender_amendment_confirmation(
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
        ConfirmTenderAmendment.instance_tender_url = instance_tender_url
        ConfirmTenderAmendment.instance_budget_url = instance_budget_url
        ConfirmTenderAmendment.instance_storage_url = instance_storage_url
        ConfirmTenderAmendment.cp_id = cancel_tender_response[0]
        ConfirmTenderAmendment.ev_id = cancel_tender_response[3]
        ConfirmTenderAmendment.pn_id = cancel_tender_response[1]
        ConfirmTenderAmendment.amendment_id = cancel_tender_response[8]
        ConfirmTenderAmendment.amendment_token = cancel_tender_response[9]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(tender_amendment_confirmation_response.status_code)
        )

    @pytestrail.case('27602')
    def test_see_result_from_feed_point_27602_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(ConfirmTenderAmendment.successfully_tender_amendment_confirmation)
        )

    @pytestrail.case('27602')
    def test_compare_ev_release_before_updating_and_after_updating_27602_3(self):
        ev_release_after_tender_amendment_confirmation = requests.get(
            url=f"{ConfirmTenderAmendment.message_from_kafka['data']['url']}").json()
        before_amendment_confirmation = ConfirmTenderAmendment.ev_release_before_tender_amendment_confirmation
        expected_result = {
            'dictionary_item_added': "['releases'][0]['awards']",
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_tender_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{ev_release_after_tender_amendment_confirmation['releases'][0]['id'][46:59]}",
                    'old_value': f"{before_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{before_amendment_confirmation['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_tender_amendment_confirmation['releases'][0]['date'],
                    'old_value': before_amendment_confirmation['releases'][0]['date']
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'active'
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': 'empty',
                    'old_value': 'clarification'
                },
                "root['releases'][0]['tender']['lots'][0]['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'active'
                },
                "root['releases'][0]['tender']['lots'][1]['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'active'
                },
                "root['releases'][0]['tender']['amendments'][0]['status']": {
                    'new_value': 'active',
                    'old_value': 'pending'
                }
            }
        }
        actual_result = DeepDiff(ConfirmTenderAmendment.ev_release_before_tender_amendment_confirmation,
                                 ev_release_after_tender_amendment_confirmation)
        dictionary_item_added_was_cleaned = str(actual_result['dictionary_item_added']).replace('root', '')[1:-1]
        actual_result['dictionary_item_added'] = dictionary_item_added_was_cleaned
        actual_awards = ev_release_after_tender_amendment_confirmation['releases'][0]['awards']
        expected_awards = [{
            "id": actual_awards[0]['id'],
            "title": "Lot is not awarded",
            "description": "Other reasons (discontinuation of procedure)",
            "status": "unsuccessful",
            "statusDetails": "lotCancelled",
            "date": ConfirmTenderAmendment.message_from_kafka['data']['operationDate'],
            "relatedLots": [before_amendment_confirmation['releases'][0]['tender']['lots'][0]['id']]
        }, {
            "id": actual_awards[1]['id'],
            "title": "Lot is not awarded",
            "description": "Other reasons (discontinuation of procedure)",
            "status": "unsuccessful",
            "statusDetails": "lotCancelled",
            "date": ConfirmTenderAmendment.message_from_kafka['data']['operationDate'],
            "relatedLots": [before_amendment_confirmation['releases'][0]['tender']['lots'][1]['id']]
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_awards),
            actual_result=str(actual_awards)
        )

    @pytestrail.case('27602')
    def test_compare_ev_release_before_updating_and_after_updating_27602_4(self):
        before_amendment_confirmation = ConfirmTenderAmendment.ms_release_before_tender_amendment_confirmation
        ms_release_after_tender_amendment_confirmation = requests.get(
            url=f"{ConfirmTenderAmendment.instance_tender_url}{ConfirmTenderAmendment.cp_id}/"
                f"{ConfirmTenderAmendment.cp_id}").json()

        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ms_release_after_tender_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{ms_release_after_tender_amendment_confirmation['releases'][0]['id'][29:42]}",
                    'old_value': f"{before_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{before_amendment_confirmation['releases'][0]['id'][29:42]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_tender_amendment_confirmation['releases'][0]['date'],
                    'old_value': before_amendment_confirmation['releases'][0]['date']
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'active'
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': 'empty',
                    'old_value': 'evaluation'
                }
            }
        }
        actual_result = DeepDiff(ConfirmTenderAmendment.ms_release_before_tender_amendment_confirmation,
                                 ms_release_after_tender_amendment_confirmation)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckOnThePossibilityOfTenderAmendmentConfirmationForTenderInActiveClarificationTenderStatus2(object):
    # Check on the possibility of tender amendment confirmation  for tender in active clarification tender state,
    # based on CnOnPn and Amendment Obligatory Data Model
    @pytestrail.case("27603")
    def test_test_send_the_request_27603_1(self, country, language, instance, cassandra_username, cassandra_password,
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

        ConfirmTenderAmendment.ms_release_before_tender_amendment_confirmation = requests.get(
            url=cancel_tender_response[5]).json()
        ConfirmTenderAmendment.pn_release_before_tender_amendment_confirmation = requests.get(
            url=cancel_tender_response[6]).json()
        ConfirmTenderAmendment.ev_release_before_tender_amendment_confirmation = requests.get(
            url=cancel_tender_response[7]).json()
        tender_amendment_confirmation_response = cancel_tender.confirm_tender_cancellation(
            cp_id=cancel_tender_response[0],
            ev_id=cancel_tender_response[3]
        )
        ConfirmTenderAmendment.message_from_kafka = cancel_tender.get_message_from_kafka()
        ConfirmTenderAmendment.successfully_tender_amendment_confirmation = cancel_tender. \
            check_on_that_message_is_successfully_tender_amendment_confirmation(
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
        ConfirmTenderAmendment.instance_tender_url = instance_tender_url
        ConfirmTenderAmendment.instance_budget_url = instance_budget_url
        ConfirmTenderAmendment.instance_storage_url = instance_storage_url
        ConfirmTenderAmendment.cp_id = cancel_tender_response[0]
        ConfirmTenderAmendment.ev_id = cancel_tender_response[3]
        ConfirmTenderAmendment.pn_id = cancel_tender_response[1]
        ConfirmTenderAmendment.amendment_id = cancel_tender_response[8]
        ConfirmTenderAmendment.amendment_token = cancel_tender_response[9]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(tender_amendment_confirmation_response.status_code)
        )

    @pytestrail.case('27603')
    def test_see_result_from_feed_point_27603_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(ConfirmTenderAmendment.successfully_tender_amendment_confirmation)
        )

    @pytestrail.case('27603')
    def test_compare_ev_release_before_updating_and_after_updating_27603_3(self):
        ev_release_after_tender_amendment_confirmation = requests.get(
            url=f"{ConfirmTenderAmendment.message_from_kafka['data']['url']}").json()
        before_amendment_confirmation = ConfirmTenderAmendment.ev_release_before_tender_amendment_confirmation
        expected_result = {
            'dictionary_item_added': "['releases'][0]['awards']",
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_tender_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{ev_release_after_tender_amendment_confirmation['releases'][0]['id'][46:59]}",
                    'old_value': f"{before_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{before_amendment_confirmation['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_tender_amendment_confirmation['releases'][0]['date'],
                    'old_value': before_amendment_confirmation['releases'][0]['date']
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'active'
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': 'empty',
                    'old_value': 'clarification'
                },
                "root['releases'][0]['tender']['lots'][0]['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'active'
                },
                "root['releases'][0]['tender']['lots'][1]['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'active'
                },
                "root['releases'][0]['tender']['amendments'][0]['status']": {
                    'new_value': 'active',
                    'old_value': 'pending'
                }
            }
        }
        actual_result = DeepDiff(ConfirmTenderAmendment.ev_release_before_tender_amendment_confirmation,
                                 ev_release_after_tender_amendment_confirmation)
        dictionary_item_added_was_cleaned = str(actual_result['dictionary_item_added']).replace('root', '')[1:-1]
        actual_result['dictionary_item_added'] = dictionary_item_added_was_cleaned
        actual_awards = ev_release_after_tender_amendment_confirmation['releases'][0]['awards']
        expected_awards = [{
            "id": actual_awards[0]['id'],
            "title": "Lot is not awarded",
            "description": "Other reasons (discontinuation of procedure)",
            "status": "unsuccessful",
            "statusDetails": "lotCancelled",
            "date": ConfirmTenderAmendment.message_from_kafka['data']['operationDate'],
            "relatedLots": [before_amendment_confirmation['releases'][0]['tender']['lots'][0]['id']]
        }, {
            "id": actual_awards[1]['id'],
            "title": "Lot is not awarded",
            "description": "Other reasons (discontinuation of procedure)",
            "status": "unsuccessful",
            "statusDetails": "lotCancelled",
            "date": ConfirmTenderAmendment.message_from_kafka['data']['operationDate'],
            "relatedLots": [before_amendment_confirmation['releases'][0]['tender']['lots'][1]['id']]
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_awards),
            actual_result=str(actual_awards)
        )

    @pytestrail.case('27603')
    def test_compare_ev_release_before_updating_and_after_updating_27603_4(self):
        before_amendment_confirmation = ConfirmTenderAmendment.ms_release_before_tender_amendment_confirmation
        ms_release_after_tender_amendment_confirmation = requests.get(
            url=f"{ConfirmTenderAmendment.instance_tender_url}{ConfirmTenderAmendment.cp_id}/"
                f"{ConfirmTenderAmendment.cp_id}").json()

        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ms_release_after_tender_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{ms_release_after_tender_amendment_confirmation['releases'][0]['id'][29:42]}",
                    'old_value': f"{before_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{before_amendment_confirmation['releases'][0]['id'][29:42]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_tender_amendment_confirmation['releases'][0]['date'],
                    'old_value': before_amendment_confirmation['releases'][0]['date']
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'active'
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': 'empty',
                    'old_value': 'evaluation'
                }
            }
        }
        actual_result = DeepDiff(ConfirmTenderAmendment.ms_release_before_tender_amendment_confirmation,
                                 ms_release_after_tender_amendment_confirmation)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckOnThePossibilityOfLotAmendmentConfirmationForTenderInActiveClarificationTenderStatus1(object):
    # Check on the possibility of lot amendment confirmation  for tender in active clarification tender state,
    # based on CnOnPn and Amendment Full Data Model
    @pytestrail.case("27611")
    def test_test_send_the_request_27611_1(self, country, language, instance, cassandra_username, cassandra_password,
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

        ConfirmLotAmendment.ms_release_before_lot_amendment_confirmation = requests.get(
            url=cancel_lot_response[5]).json()
        ConfirmLotAmendment.pn_release_before_lot_amendment_confirmation = requests.get(
            url=cancel_lot_response[6]).json()
        ConfirmLotAmendment.ev_release_before_lot_amendment_confirmation = requests.get(
            url=cancel_lot_response[7]).json()
        lot_amendment_confirmation_response = cancel_tender.confirm_tender_cancellation(
            cp_id=cancel_lot_response[0],
            ev_id=cancel_lot_response[3]
        )
        ConfirmLotAmendment.message_from_kafka = cancel_tender.get_message_from_kafka()
        ConfirmLotAmendment.successfully_lot_amendment_confirmation = cancel_tender. \
            check_on_that_message_is_successfully_tender_amendment_confirmation(
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
        ConfirmLotAmendment.instance_tender_url = instance_tender_url
        ConfirmLotAmendment.instance_budget_url = instance_budget_url
        ConfirmLotAmendment.instance_storage_url = instance_storage_url
        ConfirmLotAmendment.cp_id = cancel_lot_response[0]
        ConfirmLotAmendment.ev_id = cancel_lot_response[3]
        ConfirmLotAmendment.pn_id = cancel_lot_response[1]
        ConfirmLotAmendment.amendment_id = cancel_lot_response[8]
        ConfirmLotAmendment.amendment_token = cancel_lot_response[9]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(lot_amendment_confirmation_response.status_code)
        )

    @pytestrail.case('27611')
    def test_see_result_from_feed_point_27611_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(ConfirmLotAmendment.successfully_lot_amendment_confirmation)
        )

    @pytestrail.case('27611')
    def test_compare_ev_release_before_updating_and_after_updating_27611_3(self):
        ev_release_after_lot_amendment_confirmation = requests.get(
            url=f"{ConfirmLotAmendment.message_from_kafka['data']['url']}").json()
        before_amendment_confirmation = ConfirmLotAmendment.ev_release_before_lot_amendment_confirmation
        expected_result = {
            'dictionary_item_added': "['releases'][0]['awards']",
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_lot_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{ev_release_after_lot_amendment_confirmation['releases'][0]['id'][46:59]}",
                    'old_value': f"{before_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{before_amendment_confirmation['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_lot_amendment_confirmation['releases'][0]['date'],
                    'old_value': before_amendment_confirmation['releases'][0]['date']
                },
                "root['releases'][0]['tender']['lots'][0]['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'active'
                },
                "root['releases'][0]['tender']['amendments'][0]['status']": {
                    'new_value': 'active',
                    'old_value': 'pending'
                }
            }
        }
        actual_result = DeepDiff(ConfirmLotAmendment.ev_release_before_lot_amendment_confirmation,
                                 ev_release_after_lot_amendment_confirmation)
        dictionary_item_added_was_cleaned = str(actual_result['dictionary_item_added']).replace('root', '')[1:-1]
        actual_result['dictionary_item_added'] = dictionary_item_added_was_cleaned
        actual_awards = ev_release_after_lot_amendment_confirmation['releases'][0]['awards']
        expected_awards = [{
            "id": actual_awards[0]['id'],
            "title": "Lot is not awarded",
            "description": "Other reasons (discontinuation of procedure)",
            "status": "unsuccessful",
            "statusDetails": "lotCancelled",
            "date": ConfirmLotAmendment.message_from_kafka['data']['operationDate'],
            "relatedLots": [before_amendment_confirmation['releases'][0]['tender']['lots'][0]['id']]
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_awards),
            actual_result=str(actual_awards)
        )

    @pytestrail.case('27611')
    def test_compare_ev_release_before_updating_and_after_updating_27611_4(self):
        ms_release_after_lot_amendment_confirmation = requests.get(
            url=f"{ConfirmLotAmendment.instance_tender_url}{ConfirmLotAmendment.cp_id}/"
                f"{ConfirmLotAmendment.cp_id}").json()

        expected_result = {}
        actual_result = DeepDiff(ConfirmLotAmendment.ms_release_before_lot_amendment_confirmation,
                                 ms_release_after_lot_amendment_confirmation)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckOnThePossibilityOfLotAmendmentConfirmationForTenderInActiveClarificationTenderStatus2(object):
    # Check on the possibility of lot amendment confirmation  for tender in active clarification tender state,
    # based on CnOnPn and Amendment Obligatory Data Model
    @pytestrail.case("27612")
    def test_test_send_the_request_27612_1(self, country, language, instance, cassandra_username, cassandra_password,
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

        ConfirmLotAmendment.ms_release_before_lot_amendment_confirmation = requests.get(
            url=cancel_lot_response[5]).json()
        ConfirmLotAmendment.pn_release_before_lot_amendment_confirmation = requests.get(
            url=cancel_lot_response[6]).json()
        ConfirmLotAmendment.ev_release_before_lot_amendment_confirmation = requests.get(
            url=cancel_lot_response[7]).json()
        lot_amendment_confirmation_response = cancel_tender.confirm_tender_cancellation(
            cp_id=cancel_lot_response[0],
            ev_id=cancel_lot_response[3]
        )
        ConfirmLotAmendment.message_from_kafka = cancel_tender.get_message_from_kafka()
        ConfirmLotAmendment.successfully_lot_amendment_confirmation = cancel_tender. \
            check_on_that_message_is_successfully_tender_amendment_confirmation(
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
        ConfirmLotAmendment.instance_tender_url = instance_tender_url
        ConfirmLotAmendment.instance_budget_url = instance_budget_url
        ConfirmLotAmendment.instance_storage_url = instance_storage_url
        ConfirmLotAmendment.cp_id = cancel_lot_response[0]
        ConfirmLotAmendment.ev_id = cancel_lot_response[3]
        ConfirmLotAmendment.pn_id = cancel_lot_response[1]
        ConfirmLotAmendment.amendment_id = cancel_lot_response[8]
        ConfirmLotAmendment.amendment_token = cancel_lot_response[9]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(lot_amendment_confirmation_response.status_code)
        )

    @pytestrail.case('27611')
    def test_see_result_from_feed_point_27612_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(ConfirmLotAmendment.successfully_lot_amendment_confirmation)
        )

    @pytestrail.case('27611')
    def test_compare_ev_release_before_updating_and_after_updating_27612_3(self):
        ev_release_after_lot_amendment_confirmation = requests.get(
            url=f"{ConfirmLotAmendment.message_from_kafka['data']['url']}").json()
        before_amendment_confirmation = ConfirmLotAmendment.ev_release_before_lot_amendment_confirmation
        expected_result = {
            'dictionary_item_added': "['releases'][0]['awards']",
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_lot_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{ev_release_after_lot_amendment_confirmation['releases'][0]['id'][46:59]}",
                    'old_value': f"{before_amendment_confirmation['releases'][0]['ocid']}-"
                                 f"{before_amendment_confirmation['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_lot_amendment_confirmation['releases'][0]['date'],
                    'old_value': before_amendment_confirmation['releases'][0]['date']
                },
                "root['releases'][0]['tender']['lots'][0]['status']": {
                    'new_value': 'cancelled',
                    'old_value': 'active'
                },
                "root['releases'][0]['tender']['amendments'][0]['status']": {
                    'new_value': 'active',
                    'old_value': 'pending'
                }
            }
        }
        actual_result = DeepDiff(ConfirmLotAmendment.ev_release_before_lot_amendment_confirmation,
                                 ev_release_after_lot_amendment_confirmation)
        dictionary_item_added_was_cleaned = str(actual_result['dictionary_item_added']).replace('root', '')[1:-1]
        actual_result['dictionary_item_added'] = dictionary_item_added_was_cleaned
        actual_awards = ev_release_after_lot_amendment_confirmation['releases'][0]['awards']
        expected_awards = [{
            "id": actual_awards[0]['id'],
            "title": "Lot is not awarded",
            "description": "Other reasons (discontinuation of procedure)",
            "status": "unsuccessful",
            "statusDetails": "lotCancelled",
            "date": ConfirmLotAmendment.message_from_kafka['data']['operationDate'],
            "relatedLots": [before_amendment_confirmation['releases'][0]['tender']['lots'][0]['id']]
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_awards),
            actual_result=str(actual_awards)
        )

    @pytestrail.case('27611')
    def test_compare_ev_release_before_updating_and_after_updating_27612_4(self):
        ms_release_after_lot_amendment_confirmation = requests.get(
            url=f"{ConfirmLotAmendment.instance_tender_url}{ConfirmLotAmendment.cp_id}/"
                f"{ConfirmLotAmendment.cp_id}").json()

        expected_result = {}
        actual_result = DeepDiff(ConfirmLotAmendment.ms_release_before_lot_amendment_confirmation,
                                 ms_release_after_lot_amendment_confirmation)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
