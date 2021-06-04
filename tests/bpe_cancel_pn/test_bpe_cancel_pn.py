from uuid import uuid4
import requests
from deepdiff import DeepDiff
from pytest_testrail.plugin import pytestrail
from tests.essences.pn import PN
from tests.iStorage import Document
from useful_functions import compare_actual_result_and_expected_result


class TestCheckOnPossibilityOfCancellingThePnAfterPlanningNoticeCreationWithFullDataModel(object):
    @pytestrail.case('27591')
    def test_send_the_request_27591_1(self, country, language, instance, cassandra_username, cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]

        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded
        )
        create_pn_response = pn.insert_pn_full_(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id
        )
        cancel_pn_response = pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(cancel_pn_response.status_code)
        )

    @pytestrail.case('27591')
    def test_send_request_see_result_in_feed_point_27591_2(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]

        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded
        )
        create_pn_response = pn.insert_pn_full_(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id
        )
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        pn.check_on_that_message_is_successfully_cancel_pn(cp_id=create_pn_response[5])
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(pn.check_on_that_message_is_successfully_cancel_pn(cp_id=create_pn_response[4]))
        )

    @pytestrail.case('27591')
    def test_compare_pn_release_before_cancelling_and_after_cancelling_27591_3(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]

        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded
        )
        create_pn_response = pn.insert_pn_full_(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id
        )
        pn_release_before_cancelling = requests.get(url=create_pn_response[9]).json()
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cancel_pn_response = pn.get_message_from_kafka()
        pn_record_after_cancelling = requests.get(url=cancel_pn_response['data']['url']).json()['records']
        actual_releases_list = list()
        for d in pn_record_after_cancelling:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    actual_releases_list.append(d_1)
        pn_release_after_cancelling = requests.get(url=actual_releases_list[0]["uri"]).json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{pn_release_after_cancelling['releases'][0]['ocid']}-"
                                 f"{pn_release_after_cancelling['releases'][0]['id'][46:59]}",
                    'old_value': f"{pn_release_before_cancelling['releases'][0]['ocid']}-"
                                 f"{pn_release_before_cancelling['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['date'],
                    'old_value': pn_release_before_cancelling['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tag'][0],
                    'old_value': pn_release_before_cancelling['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['status'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['statusDetails'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['statusDetails']
                },
                "root['releases'][0]['tender']['lots'][0]['status']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['lots'][0]['status'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['lots'][0]['status']
                },
                "root['releases'][0]['tender']['lots'][1]['status']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['lots'][1]['status'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['lots'][1]['status']
                }
            }
        }

        actual_result = DeepDiff(pn_release_before_cancelling, pn_release_after_cancelling)
        assert compare_actual_result_and_expected_result(
            expected_result=expected_result,
            actual_result=actual_result
        )

    @pytestrail.case('27591')
    def test_compare_pn_release_before_cancelling_and_after_cancelling_27591_4(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]

        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded
        )
        create_pn_response = pn.insert_pn_full_(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id
        )
        ms_release_before_cancelling = requests.get(url=create_pn_response[8]).json()
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cancel_pn_response = pn.get_message_from_kafka()
        pn_record_after_cancelling = requests.get(url=cancel_pn_response['data']['url']).json()['records']
        actual_releases_list = list()
        for d in pn_record_after_cancelling:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    actual_releases_list.append(d_1)
        ms_release_after_cancelling = requests.get(url=actual_releases_list[0]["uri"]).json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ms_release_after_cancelling['releases'][0]['ocid']}-"
                                 f"{ms_release_after_cancelling['releases'][0]['id'][29:42]}",
                    'old_value': f"{ms_release_before_cancelling['releases'][0]['ocid']}-"
                                 f"{ms_release_before_cancelling['releases'][0]['id'][29:42]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['date'],
                    'old_value': ms_release_before_cancelling['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tag'][0],
                    'old_value': ms_release_before_cancelling['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tender']['status'],
                    'old_value': ms_release_before_cancelling['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tender']['statusDetails'],
                    'old_value': ms_release_before_cancelling['releases'][0]['tender']['statusDetails']
                }
            }
        }
        actual_result = DeepDiff(ms_release_before_cancelling, ms_release_after_cancelling)
        assert compare_actual_result_and_expected_result(
            expected_result=expected_result,
            actual_result=actual_result
        )


class TestCheckOnPossibilityOfCancellingThePnAfterPlanningNoticeCreationWithObligatoryDataModel(object):
    @pytestrail.case('27592')
    def test_send_the_request_27592_1(self, country, language, instance, cassandra_username, cassandra_password, pmd):
        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = pn.insert_pn_obligatory_()
        cancel_pn_response = pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(cancel_pn_response.status_code)
        )

    @pytestrail.case('27592')
    def test_send_request_see_result_in_feed_point_27592_2(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = pn.insert_pn_obligatory_()
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        pn.check_on_that_message_is_successfully_cancel_pn(cp_id=create_pn_response[5])
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(pn.check_on_that_message_is_successfully_cancel_pn(cp_id=create_pn_response[4]))
        )

    @pytestrail.case('27592')
    def test_compare_pn_release_before_cancelling_and_after_cancelling_27592_3(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = pn.insert_pn_obligatory_()
        pn_release_before_cancelling = requests.get(url=create_pn_response[9]).json()
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cancel_pn_response = pn.get_message_from_kafka()
        pn_record_after_cancelling = requests.get(url=cancel_pn_response['data']['url']).json()['records']
        actual_releases_list = list()
        for d in pn_record_after_cancelling:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    actual_releases_list.append(d_1)
        pn_release_after_cancelling = requests.get(url=actual_releases_list[0]["uri"]).json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{pn_release_after_cancelling['releases'][0]['ocid']}-"
                                 f"{pn_release_after_cancelling['releases'][0]['id'][46:59]}",
                    'old_value': f"{pn_release_before_cancelling['releases'][0]['ocid']}-"
                                 f"{pn_release_before_cancelling['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['date'],
                    'old_value': pn_release_before_cancelling['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tag'][0],
                    'old_value': pn_release_before_cancelling['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['status'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['statusDetails'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['statusDetails']
                }
            }
        }

        actual_result = DeepDiff(pn_release_before_cancelling, pn_release_after_cancelling)
        assert compare_actual_result_and_expected_result(
            expected_result=expected_result,
            actual_result=actual_result
        )

    @pytestrail.case('27592')
    def test_compare_pn_release_before_cancelling_and_after_cancelling_27592_4(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = pn.insert_pn_obligatory_()
        ms_release_before_cancelling = requests.get(url=create_pn_response[8]).json()
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cancel_pn_response = pn.get_message_from_kafka()
        pn_record_after_cancelling = requests.get(url=cancel_pn_response['data']['url']).json()['records']
        actual_releases_list = list()
        for d in pn_record_after_cancelling:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    actual_releases_list.append(d_1)
        ms_release_after_cancelling = requests.get(url=actual_releases_list[0]["uri"]).json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ms_release_after_cancelling['releases'][0]['ocid']}-"
                                 f"{ms_release_after_cancelling['releases'][0]['id'][29:42]}",
                    'old_value': f"{ms_release_before_cancelling['releases'][0]['ocid']}-"
                                 f"{ms_release_before_cancelling['releases'][0]['id'][29:42]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['date'],
                    'old_value': ms_release_before_cancelling['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tag'][0],
                    'old_value': ms_release_before_cancelling['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tender']['status'],
                    'old_value': ms_release_before_cancelling['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tender']['statusDetails'],
                    'old_value': ms_release_before_cancelling['releases'][0]['tender']['statusDetails']
                }
            }
        }
        actual_result = DeepDiff(ms_release_before_cancelling, ms_release_after_cancelling)
        assert compare_actual_result_and_expected_result(
            expected_result=expected_result,
            actual_result=actual_result
        )


class TestCheckOnPossibilityOfCancellingThePnAfterPlanningNoticeUpdatingWithFullDataModel(object):
    @pytestrail.case('27593')
    def test_send_the_request_27593_1(self, country, language, instance, cassandra_username, cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]

        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded
        )
        create_pn_response = pn.insert_pn_full_update(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id
        )
        cancel_pn_response = pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(cancel_pn_response.status_code)
        )

    @pytestrail.case('27593')
    def test_send_request_see_result_in_feed_point_27593_2(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]

        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded
        )
        create_pn_response = pn.insert_pn_full_update(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id
        )
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        pn.check_on_that_message_is_successfully_cancel_pn(cp_id=create_pn_response[5])
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(pn.check_on_that_message_is_successfully_cancel_pn(cp_id=create_pn_response[4]))
        )

    @pytestrail.case('27593')
    def test_compare_pn_release_before_cancelling_and_after_cancelling_27593_3(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]

        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded
        )
        create_pn_response = pn.insert_pn_full_update(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id
        )
        pn_release_before_cancelling = requests.get(url=create_pn_response[9]).json()
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cancel_pn_response = pn.get_message_from_kafka()
        pn_record_after_cancelling = requests.get(url=cancel_pn_response['data']['url']).json()['records']
        actual_releases_list = list()
        for d in pn_record_after_cancelling:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    actual_releases_list.append(d_1)
        pn_release_after_cancelling = requests.get(url=actual_releases_list[0]["uri"]).json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{pn_release_after_cancelling['releases'][0]['ocid']}-"
                                 f"{pn_release_after_cancelling['releases'][0]['id'][46:59]}",
                    'old_value': f"{pn_release_before_cancelling['releases'][0]['ocid']}-"
                                 f"{pn_release_before_cancelling['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['date'],
                    'old_value': pn_release_before_cancelling['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tag'][0],
                    'old_value': pn_release_before_cancelling['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['status'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['statusDetails'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['statusDetails']
                },
                "root['releases'][0]['tender']['lots'][0]['status']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['lots'][0]['status'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['lots'][0]['status']
                },
                "root['releases'][0]['tender']['lots'][1]['status']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['lots'][1]['status'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['lots'][1]['status']
                }
            }
        }

        actual_result = DeepDiff(pn_release_before_cancelling, pn_release_after_cancelling)
        assert compare_actual_result_and_expected_result(
            expected_result=expected_result,
            actual_result=actual_result
        )

    @pytestrail.case('27593')
    def test_compare_pn_release_before_cancelling_and_after_cancelling_27593_4(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]

        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=document_one_was_uploaded,
            document_two_id=document_two_was_uploaded
        )
        create_pn_response = pn.insert_pn_full_update(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id
        )
        ms_release_before_cancelling = requests.get(url=create_pn_response[8]).json()
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cancel_pn_response = pn.get_message_from_kafka()
        pn_record_after_cancelling = requests.get(url=cancel_pn_response['data']['url']).json()['records']
        actual_releases_list = list()
        for d in pn_record_after_cancelling:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    actual_releases_list.append(d_1)
        ms_release_after_cancelling = requests.get(url=actual_releases_list[0]["uri"]).json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ms_release_after_cancelling['releases'][0]['ocid']}-"
                                 f"{ms_release_after_cancelling['releases'][0]['id'][29:42]}",
                    'old_value': f"{ms_release_before_cancelling['releases'][0]['ocid']}-"
                                 f"{ms_release_before_cancelling['releases'][0]['id'][29:42]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['date'],
                    'old_value': ms_release_before_cancelling['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tag'][0],
                    'old_value': ms_release_before_cancelling['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tender']['status'],
                    'old_value': ms_release_before_cancelling['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tender']['statusDetails'],
                    'old_value': ms_release_before_cancelling['releases'][0]['tender']['statusDetails']
                }
            }
        }
        actual_result = DeepDiff(ms_release_before_cancelling, ms_release_after_cancelling)
        assert compare_actual_result_and_expected_result(
            expected_result=expected_result,
            actual_result=actual_result
        )


class TestCheckOnPossibilityOfCancellingThePnAfterPlanningNoticeUpdatingWithObligatoryDataModel(object):
    @pytestrail.case('27594')
    def test_send_the_request_27594_1(self, country, language, instance, cassandra_username, cassandra_password, pmd):
        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = pn.insert_pn_obligatory_update()
        cancel_pn_response = pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(cancel_pn_response.status_code)
        )

    @pytestrail.case('27594')
    def test_send_request_see_result_in_feed_point_27594_2(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = pn.insert_pn_obligatory_update()
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        pn.check_on_that_message_is_successfully_cancel_pn(cp_id=create_pn_response[5])
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(pn.check_on_that_message_is_successfully_cancel_pn(cp_id=create_pn_response[4]))
        )

    @pytestrail.case('27594')
    def test_compare_pn_release_before_cancelling_and_after_cancelling_27594_3(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = pn.insert_pn_obligatory_update()
        pn_release_before_cancelling = requests.get(url=create_pn_response[9]).json()
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cancel_pn_response = pn.get_message_from_kafka()
        pn_record_after_cancelling = requests.get(url=cancel_pn_response['data']['url']).json()['records']
        actual_releases_list = list()
        for d in pn_record_after_cancelling:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["planning"]:
                    actual_releases_list.append(d_1)
        pn_release_after_cancelling = requests.get(url=actual_releases_list[0]["uri"]).json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{pn_release_after_cancelling['releases'][0]['ocid']}-"
                                 f"{pn_release_after_cancelling['releases'][0]['id'][46:59]}",
                    'old_value': f"{pn_release_before_cancelling['releases'][0]['ocid']}-"
                                 f"{pn_release_before_cancelling['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['date'],
                    'old_value': pn_release_before_cancelling['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tag'][0],
                    'old_value': pn_release_before_cancelling['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['status'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': pn_release_after_cancelling['releases'][0]['tender']['statusDetails'],
                    'old_value': pn_release_before_cancelling['releases'][0]['tender']['statusDetails']
                }
            }
        }

        actual_result = DeepDiff(pn_release_before_cancelling, pn_release_after_cancelling)
        assert compare_actual_result_and_expected_result(
            expected_result=expected_result,
            actual_result=actual_result
        )

    @pytestrail.case('27594')
    def test_compare_pn_release_before_cancelling_and_after_cancelling_27594_4(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        pn = PN(
            payload=None,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = pn.insert_pn_obligatory_update()
        ms_release_before_cancelling = requests.get(url=create_pn_response[8]).json()
        pn.cancel_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cancel_pn_response = pn.get_message_from_kafka()
        pn_record_after_cancelling = requests.get(url=cancel_pn_response['data']['url']).json()['records']
        actual_releases_list = list()
        for d in pn_record_after_cancelling:
            for d_1 in d["compiledRelease"]["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    actual_releases_list.append(d_1)
        ms_release_after_cancelling = requests.get(url=actual_releases_list[0]["uri"]).json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ms_release_after_cancelling['releases'][0]['ocid']}-"
                                 f"{ms_release_after_cancelling['releases'][0]['id'][29:42]}",
                    'old_value': f"{ms_release_before_cancelling['releases'][0]['ocid']}-"
                                 f"{ms_release_before_cancelling['releases'][0]['id'][29:42]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['date'],
                    'old_value': ms_release_before_cancelling['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tag'][0],
                    'old_value': ms_release_before_cancelling['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tender']['status'],
                    'old_value': ms_release_before_cancelling['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': ms_release_after_cancelling['releases'][0]['tender']['statusDetails'],
                    'old_value': ms_release_before_cancelling['releases'][0]['tender']['statusDetails']
                }
            }
        }
        actual_result = DeepDiff(ms_release_before_cancelling, ms_release_after_cancelling)
        assert compare_actual_result_and_expected_result(
            expected_result=expected_result,
            actual_result=actual_result
        )
