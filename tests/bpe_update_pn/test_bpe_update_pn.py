import copy
from uuid import uuid4
import requests
from deepdiff import DeepDiff
from pytest_testrail.plugin import pytestrail
from tests.essences.pn import PN
from tests.iStorage import Document
from tests.payloads.pn_payload import update_pn_payload_full_data_model_with_documents, \
    update_pn_payload_obligatory_data_model_without_documents
from useful_functions import compare_actual_result_and_expected_result


class TestCheckThePossibilityOfPlanningNoticeUpdatingWithFullDataModel(object):
    @pytestrail.case("27589")
    def test_send_request_see_result_in_feed_point_27589_1(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        payload = copy.deepcopy(update_pn_payload_full_data_model_with_documents)
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['documents'][0]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = second_lot_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        pn = PN(
            payload=payload,
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
        update_pn_response = pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(update_pn_response.status_code)
        )

    @pytestrail.case("27589")
    def test_send_request_see_result_in_feed_point_27589_2(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        payload = copy.deepcopy(update_pn_payload_full_data_model_with_documents)
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['documents'][0]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = second_lot_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        pn = PN(
            payload=payload,
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
        pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        pn.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(
                pn.check_on_that_message_is_successfully_update_pn(
                    cp_id=create_pn_response[4],
                    pn_id=create_pn_response[5]
                )
            )
        )

    @pytestrail.case("27589")
    def test_compare_pn_release_before_updating_and_after_updating_27589_3(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        payload = copy.deepcopy(update_pn_payload_full_data_model_with_documents)
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['documents'][0]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = second_lot_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        pn = PN(
            payload=payload,
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
        pn_release_before_updating = requests.get(url=create_pn_response[9]).json()
        pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        update_pn_response = pn.get_message_from_kafka()
        pn_release_after_updating = requests.get(url=update_pn_response['data']['url']).json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{pn_release_after_updating['releases'][0]['ocid']}-"
                                 f"{pn_release_after_updating['releases'][0]['id'][46:59]}",
                    'old_value': f"{pn_release_before_updating['releases'][0]['ocid']}-"
                                 f"{pn_release_before_updating['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': pn_release_after_updating['releases'][0]['date'],
                    'old_value': pn_release_before_updating['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': pn_release_after_updating['releases'][0]['tag'][0],
                    'old_value': pn_release_before_updating['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['items'][0]['internalId']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['items'][0]['internalId'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['items'][0]['internalId']
                },
                "root['releases'][0]['tender']['items'][0]['description']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['items'][0]['description'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['items'][0]['description']
                },
                "root['releases'][0]['tender']['items'][1]['internalId']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['items'][1]['internalId'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['items'][1]['internalId']
                },
                "root['releases'][0]['tender']['items'][1]['description']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['items'][1]['description'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['items'][1]['description']
                },
                "root['releases'][0]['tender']['lots'][0]['internalId']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['lots'][0]['internalId'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['lots'][0]['internalId']
                },
                "root['releases'][0]['tender']['lots'][0]['title']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['lots'][0]['title'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['lots'][0]['title']
                },
                "root['releases'][0]['tender']['lots'][0]['description']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['lots'][0]['description'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['lots'][0]['description']
                },
                "root['releases'][0]['tender']['lots'][0]['contractPeriod']['startDate']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                        'startDate'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                        'startDate']
                },
                "root['releases'][0]['tender']['lots'][0]['contractPeriod']['endDate']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                        'endDate'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                        'endDate']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['streetAddress']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address']['streetAddress'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address']['streetAddress']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['postalCode']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address']['postalCode'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address'][
                            'postalCode']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']["
                "'region']['id']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['region']['id'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['region']['id']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']["
                "'region']['description']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address']['addressDetails']['region']['description'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address']['addressDetails']['region']['description']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']["
                "'locality']['id']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['locality']['id'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['locality']['id']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']["
                "'locality']['description']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['locality']['description'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['locality']['description']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['description']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'description'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                            'description']
                },
                "root['releases'][0]['tender']['lots'][1]['internalId']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['lots'][1]['internalId'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['lots'][1]['internalId']
                },
                "root['releases'][0]['tender']['lots'][1]['title']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['lots'][1]['title'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['lots'][1]['title']
                },
                "root['releases'][0]['tender']['lots'][1]['description']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['lots'][1]['description'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['lots'][1]['description']
                },
                "root['releases'][0]['tender']['lots'][1]['contractPeriod']['startDate']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                        'startDate'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                        'startDate']
                },
                "root['releases'][0]['tender']['lots'][1]['contractPeriod']['endDate']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                        'endDate'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                        'endDate']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['streetAddress']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'address'][
                            'streetAddress'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'address'][
                            'streetAddress']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']["
                "'region']['id']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['region']['id'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['region']['id']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']["
                "'region']['description']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['region']['description'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['region']['description']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']["
                "'locality']['id']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['locality']['id'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['locality']['id']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']["
                "'locality']['description']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['locality']['description'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'address'][
                            'addressDetails']['locality']['description']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['description']": {
                    'new_value':
                        pn_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'description'],
                    'old_value':
                        pn_release_before_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                            'description']
                },
                "root['releases'][0]['tender']['tenderPeriod']['startDate']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['tenderPeriod']['startDate'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['tenderPeriod']['startDate']
                },
                "root['releases'][0]['tender']['documents'][0]['title']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['documents'][0]['title'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['documents'][0]['title']
                },
                "root['releases'][0]['tender']['documents'][0]['description']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['documents'][0]['description'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['documents'][0]['description']
                },
                "root['releases'][0]['tender']['documents'][0]['datePublished']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['documents'][0][
                        'datePublished'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['documents'][0][
                        'datePublished']
                },
                "root['releases'][0]['tender']['documents'][1]['title']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['documents'][1]['title'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['documents'][1]['title']
                },
                "root['releases'][0]['tender']['documents'][1]['description']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['documents'][1]['description'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['documents'][1]['description']
                },
                "root['releases'][0]['tender']['documents'][1]['datePublished']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['documents'][1][
                        'datePublished'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['documents'][1][
                        'datePublished']
                },
                "root['releases'][0]['tender']['procurementMethodRationale']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['procurementMethodRationale'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['procurementMethodRationale']
                }
            }
        }
        actual_result = DeepDiff(pn_release_before_updating, pn_release_after_updating)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )

    @pytestrail.case("27589")
    def test_compare_ms_release_before_updating_and_after_updating_27589_4(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        payload = copy.deepcopy(update_pn_payload_full_data_model_with_documents)
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['documents'][0]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = second_lot_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        pn = PN(
            payload=payload,
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
        ms_release_before_updating = requests.get(url=create_pn_response[8]).json()
        pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        update_pn_response = pn.get_message_from_kafka()
        pn_release_after_updating = requests.get(url=update_pn_response['data']['url']).json()
        related_processes_list = list()
        for d in pn_release_after_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        ms_release_after_updating = requests.get(url=related_processes_list[0]['uri']).json()

        actual_result = DeepDiff(ms_release_before_updating, ms_release_after_updating)

        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ms_release_after_updating['releases'][0]['ocid']}-"
                                 f"{ms_release_after_updating['releases'][0]['id'][29:42]}",
                    'old_value': f"{ms_release_before_updating['releases'][0]['ocid']}-"
                                 f"{ms_release_before_updating['releases'][0]['id'][29:42]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_updating['releases'][0]['date'],
                    'old_value': ms_release_before_updating['releases'][0]['date']
                },
                "root['releases'][0]['planning']['budget']['description']": {
                    'new_value': ms_release_after_updating['releases'][0]['planning']['budget']['description'],
                    'old_value': ms_release_before_updating['releases'][0]['planning']['budget']['description']
                },
                "root['releases'][0]['planning']['rationale']": {
                    'new_value': ms_release_after_updating['releases'][0]['planning']['rationale'],
                    'old_value': ms_release_before_updating['releases'][0]['planning']['rationale']
                },
                "root['releases'][0]['tender']['title']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['title'],
                    'old_value': ms_release_before_updating['releases'][0]['tender']['title']
                },
                "root['releases'][0]['tender']['description']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['description'],
                    'old_value': ms_release_before_updating['releases'][0]['tender']['description']
                },
                "root['releases'][0]['tender']['procurementMethodRationale']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['procurementMethodRationale'],
                    'old_value': ms_release_before_updating['releases'][0]['tender']['procurementMethodRationale']
                },
                "root['releases'][0]['tender']['contractPeriod']['startDate']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['contractPeriod']['startDate'],
                    'old_value': ms_release_before_updating['releases'][0]['tender']['contractPeriod']['startDate']
                },
                "root['releases'][0]['tender']['contractPeriod']['endDate']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['contractPeriod']['endDate'],
                    'old_value': ms_release_before_updating['releases'][0]['tender']['contractPeriod']['endDate']
                },
                "root['releases'][0]['tender']['procurementMethodAdditionalInfo']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['procurementMethodAdditionalInfo'],
                    'old_value': ms_release_before_updating['releases'][0]['tender']['procurementMethodAdditionalInfo']
                }
            }
        }
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )

    @pytestrail.case("27589")
    def test_compare_fs_releases_before_updating_and_after_updating_27589_5(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        payload = copy.deepcopy(update_pn_payload_full_data_model_with_documents)
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['documents'][0]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = second_lot_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        pn = PN(
            payload=payload,
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
        ms_release_before_updating = requests.get(url=create_pn_response[8]).json()
        related_fs_before_updating = list()
        for d in ms_release_before_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_fs_before_updating.append(d_1)
        fs_release_before_updating = requests.get(url=related_fs_before_updating[0]["uri"]).json()
        pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        update_pn_response = pn.get_message_from_kafka()
        pn_release_after_updating = requests.get(url=update_pn_response['data']['url']).json()
        related_ms = list()
        for d in pn_release_after_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_ms.append(d_1)
        ms_release_after_updating = requests.get(url=related_ms[0]['uri']).json()
        related_fs_after_updating = list()
        for d in ms_release_after_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_fs_after_updating.append(d_1)
        fs_release_after_updating = requests.get(url=related_fs_after_updating[0]["uri"]).json()
        actual_result = DeepDiff(fs_release_before_updating, fs_release_after_updating)
        expected_result = {}
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )

    @pytestrail.case("27589")
    def test_compare_ei_releases_before_updating_and_after_updating_27589_6(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        payload = copy.deepcopy(update_pn_payload_full_data_model_with_documents)
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['documents'][0]['relatedLots'][0] = first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = second_lot_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        pn = PN(
            payload=payload,
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
        ms_release_before_updating = requests.get(url=create_pn_response[8]).json()
        related_ei_before_updating = list()
        for d in ms_release_before_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_ei_before_updating.append(d_1)
        ei_release_before_updating = requests.get(url=related_ei_before_updating[0]["uri"]).json()
        pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        update_pn_response = pn.get_message_from_kafka()
        pn_release_after_updating = requests.get(url=update_pn_response['data']['url']).json()
        related_ms = list()
        for d in pn_release_after_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_ms.append(d_1)
        ms_release_after_updating = requests.get(url=related_ms[0]['uri']).json()
        related_ei_after_updating = list()
        for d in ms_release_after_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_ei_after_updating.append(d_1)
        ei_release_after_updating = requests.get(url=related_ei_after_updating[0]["uri"]).json()
        actual_result = DeepDiff(ei_release_before_updating, ei_release_after_updating)
        expected_result = {}
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckThePossibilityOfPlanningNoticeUpdatingWithObligatoryDataModel(object):
    @pytestrail.case("27590")
    def test_send_request_see_result_in_feed_point_27590_1(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        payload = copy.deepcopy(update_pn_payload_obligatory_data_model_without_documents)

        pn = PN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = pn.insert_pn_obligatory_()
        update_pn_response = pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(update_pn_response.status_code)
        )

    @pytestrail.case("27590")
    def test_send_request_see_result_in_feed_point_27590_2(self, country, language, instance, cassandra_username,
                                                           cassandra_password, pmd):
        payload = copy.deepcopy(update_pn_payload_obligatory_data_model_without_documents)

        pn = PN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = pn.insert_pn_obligatory_()
        pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        pn.get_message_from_kafka()
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(
                pn.check_on_that_message_is_successfully_update_pn(
                    cp_id=create_pn_response[4],
                    pn_id=create_pn_response[5]
                )
            )
        )

    @pytestrail.case("27590")
    def test_compare_pn_release_before_updating_and_after_updating_27590_3(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        payload = copy.deepcopy(update_pn_payload_obligatory_data_model_without_documents)
        pn = PN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            tender_classification_id="45100000-8"
        )
        create_pn_response = pn.insert_pn_obligatory_()
        pn_release_before_updating = requests.get(url=create_pn_response[9]).json()
        pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        update_pn_response = pn.get_message_from_kafka()
        pn_release_after_updating = requests.get(url=update_pn_response['data']['url']).json()
        pn.get_message_from_kafka()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{pn_release_after_updating['releases'][0]['ocid']}-"
                                 f"{pn_release_after_updating['releases'][0]['id'][46:59]}",
                    'old_value': f"{pn_release_before_updating['releases'][0]['ocid']}-"
                                 f"{pn_release_before_updating['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': pn_release_after_updating['releases'][0]['date'],
                    'old_value': pn_release_before_updating['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': pn_release_after_updating['releases'][0]['tag'][0],
                    'old_value': pn_release_before_updating['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['tenderPeriod']['startDate']": {
                    'new_value': pn_release_after_updating['releases'][0]['tender']['tenderPeriod']['startDate'],
                    'old_value': pn_release_before_updating['releases'][0]['tender']['tenderPeriod']['startDate']
                }
            }
        }
        actual_result = DeepDiff(pn_release_before_updating, pn_release_after_updating)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )

    @pytestrail.case("27590")
    def test_compare_ms_release_before_updating_and_after_updating_27590_4(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        payload = copy.deepcopy(update_pn_payload_obligatory_data_model_without_documents)
        pn = PN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            tender_classification_id="45100000-8"
        )
        create_pn_response = pn.insert_pn_obligatory_()
        ms_release_before_updating = requests.get(url=create_pn_response[8]).json()
        pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        update_pn_response = pn.get_message_from_kafka()
        pn_release_after_updating = requests.get(url=update_pn_response['data']['url']).json()
        related_processes_list = list()
        for d in pn_release_after_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_processes_list.append(d_1)
        ms_release_after_updating = requests.get(url=related_processes_list[0]['uri']).json()
        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ms_release_after_updating['releases'][0]['ocid']}-"
                                 f"{ms_release_after_updating['releases'][0]['id'][29:42]}",
                    'old_value': f"{ms_release_before_updating['releases'][0]['ocid']}-"
                                 f"{ms_release_before_updating['releases'][0]['id'][29:42]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_updating['releases'][0]['date'],
                    'old_value': ms_release_before_updating['releases'][0]['date']
                },
                "root['releases'][0]['tender']['title']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['title'],
                    'old_value': ms_release_before_updating['releases'][0]['tender']['title']
                },
                "root['releases'][0]['tender']['description']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['description'],
                    'old_value': ms_release_before_updating['releases'][0]['tender']['description']
                }
            }
        }
        actual_result = DeepDiff(ms_release_before_updating, ms_release_after_updating)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )

    @pytestrail.case("27590")
    def test_compare_fs_releases_before_updating_and_after_updating_27590_5(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        payload = copy.deepcopy(update_pn_payload_obligatory_data_model_without_documents)
        pn = PN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            tender_classification_id="45100000-8"
        )
        create_pn_response = pn.insert_pn_obligatory_()
        ms_release_before_updating = requests.get(url=create_pn_response[8]).json()
        related_fs_before_updating = list()
        for d in ms_release_before_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_fs_before_updating.append(d_1)
        fs_release_before_updating = requests.get(url=related_fs_before_updating[0]["uri"]).json()
        pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        update_pn_response = pn.get_message_from_kafka()
        pn_release_after_updating = requests.get(url=update_pn_response['data']['url']).json()
        related_ms = list()
        for d in pn_release_after_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_ms.append(d_1)
        ms_release_after_updating = requests.get(url=related_ms[0]['uri']).json()
        related_fs_after_updating = list()
        for d in ms_release_after_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_fundingSource"]:
                    related_fs_after_updating.append(d_1)
        fs_release_after_updating = requests.get(url=related_fs_after_updating[0]["uri"]).json()
        expected_result = {}
        actual_result = DeepDiff(fs_release_before_updating, fs_release_after_updating)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )

    @pytestrail.case("27590")
    def test_compare_ei_releases_before_updating_and_after_updating_27590_6(
            self, country, language, instance, cassandra_username, cassandra_password, pmd):
        payload = copy.deepcopy(update_pn_payload_obligatory_data_model_without_documents)
        pn = PN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            tender_classification_id="45100000-8"
        )
        create_pn_response = pn.insert_pn_obligatory_()
        ms_release_before_updating = requests.get(url=create_pn_response[8]).json()
        related_ei_before_updating = list()
        for d in ms_release_before_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_ei_before_updating.append(d_1)
        ei_release_before_updating = requests.get(url=related_ei_before_updating[0]["uri"]).json()
        pn.update_pn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        update_pn_response = pn.get_message_from_kafka()
        pn_release_after_updating = requests.get(url=update_pn_response['data']['url']).json()
        related_ms = list()
        for d in pn_release_after_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["parent"]:
                    related_ms.append(d_1)
        ms_release_after_updating = requests.get(url=related_ms[0]['uri']).json()
        related_ei_after_updating = list()
        for d in ms_release_after_updating["releases"]:
            for d_1 in d["relatedProcesses"]:
                if d_1["relationship"] == ["x_expenditureItem"]:
                    related_ei_after_updating.append(d_1)
        ei_release_after_updating = requests.get(url=related_ei_after_updating[0]["uri"]).json()
        expected_result = {}
        actual_result = DeepDiff(ei_release_before_updating, ei_release_after_updating)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
