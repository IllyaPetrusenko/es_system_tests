import copy
import json
from uuid import uuid4
import requests
from deepdiff import DeepDiff
from pytest_testrail.plugin import pytestrail

from tests.conftest import UpdateCn
from tests.essences.cn import CN
from tests.iStorage import Document
from tests.payloads.cnonpn_payload import update_cn_on_pn_payload_full_data_model_with_auction, \
    update_cn_on_pn_payload_obligatory_data_model
from useful_functions import create_enquiry_and_tender_period, compare_actual_result_and_expected_result


class TestCheckOnThePossibilityOfCnOnPnUpdatingWithFullDataModel(object):
    @pytestrail.case("27598")
    def test_test_send_the_request_27598_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        enquiry_and_tender_period = create_enquiry_and_tender_period(second_enquiry=600, second_tender=900)
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
        payload = copy.deepcopy(update_cn_on_pn_payload_full_data_model_with_auction)
        payload['tender']['tenderPeriod']['endDate'] = enquiry_and_tender_period[3]
        payload['tender']['enquiryPeriod']['endDate'] = enquiry_and_tender_period[1]
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
        cn = CN(
            payload=payload,
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
        create_ev_response = cn.insert_cnonpn_full(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=121,
            second_tender=300
        )
        UpdateCn.ms_release_before_cn_updating = requests.get(url=create_ev_response[5]).json()
        UpdateCn.pn_release_before_cn_updating = requests.get(url=create_ev_response[6]).json()
        UpdateCn.ev_release_before_cn_updating = requests.get(url=create_ev_response[7]).json()
        update_cn_response = cn.update_cn(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3],
            pn_token=create_ev_response[2]
        )
        UpdateCn.message_from_kafka = cn.get_message_from_kafka()
        UpdateCn.successfully_update_cn = cn.check_on_that_message_is_successfully_update_cn(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3]
        )
        UpdateCn.payload = payload
        UpdateCn.cp_id = create_ev_response[0]
        UpdateCn.ev_id = create_ev_response[3]
        UpdateCn.pn_id = create_ev_response[1]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(update_cn_response.status_code)
        )

    @pytestrail.case('27598')
    def test_see_result_from_feed_point_27598_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(UpdateCn.successfully_update_cn)
        )

    @pytestrail.case('27598')
    def test_compare_ev_release_before_updating_and_after_updating_27598_3(self):
        ev_release_after_updating = requests.get(
            url=f"{UpdateCn.message_from_kafka['data']['url']}").json()

        expected_result = {
            'dictionary_item_added': "['releases'][0]['tender']['amendments']",
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_updating['releases'][0]['ocid']}-"
                                 f"{ev_release_after_updating['releases'][0]['id'][46:59]}",
                    'old_value': f"{UpdateCn.ev_release_before_cn_updating['releases'][0]['ocid']}-"
                                 f"{UpdateCn.ev_release_before_cn_updating['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_updating['releases'][0]['date'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': ev_release_after_updating['releases'][0]['tag'][0],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['items'][0]['internalId']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['internalId'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0][
                        'internalId']
                },
                "root['releases'][0]['tender']['items'][0]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0][
                        'description']
                },
                "root['releases'][0]['tender']['items'][0]['quantity']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['quantity'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0]['quantity']
                },
                "root['releases'][0]['tender']['items'][0]['unit']['name']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['unit']['name'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0]['unit'][
                        'name']
                },
                "root['releases'][0]['tender']['items'][0]['unit']['id']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['unit']['id'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0]['unit'][
                        'id']
                },
                "root['releases'][0]['tender']['items'][1]['internalId']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][1]['internalId'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][1][
                        'internalId']
                },
                "root['releases'][0]['tender']['items'][1]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][1]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][1][
                        'description']
                },
                "root['releases'][0]['tender']['items'][1]['quantity']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][1]['quantity'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][1]['quantity']
                },
                "root['releases'][0]['tender']['items'][1]['unit']['name']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['unit']['name'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0]['unit'][
                        'name']
                },
                "root['releases'][0]['tender']['items'][1]['unit']['id']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][1]['unit']['id'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][1]['unit'][
                        'id']
                },
                "root['releases'][0]['tender']['lots'][0]['internalId']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][0]['internalId'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                        'internalId']
                },
                "root['releases'][0]['tender']['lots'][0]['title']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][0]['title'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0]['title']
                },
                "root['releases'][0]['tender']['lots'][0]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][0]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                        'description']
                },
                "root['releases'][0]['tender']['lots'][0]['contractPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                        'startDate'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                            'startDate']
                },
                "root['releases'][0]['tender']['lots'][0]['contractPeriod']['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                        'endDate'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                            'endDate']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['streetAddress']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'streetAddress'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address']['streetAddress']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['postalCode']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'postalCode'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address']['postalCode']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']"
                "['region']['id']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'addressDetails']['region']['id'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address']['addressDetails']['region']['id']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']"
                "['region']['description']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'addressDetails']['region']['description'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address']['addressDetails']['region']['description']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']"
                "['locality']['id']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'addressDetails']['locality']['id'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address']['addressDetails']['locality']['id']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']"
                "['locality']['description']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'addressDetails']['locality']['description'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address']['addressDetails']['locality']['description']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance'][
                        'description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                        'placeOfPerformance']['description']
                },
                "root['releases'][0]['tender']['lots'][1]['internalId']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][1]['internalId'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                        'internalId']
                },
                "root['releases'][0]['tender']['lots'][1]['title']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][1]['title'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1]['title']
                },
                "root['releases'][0]['tender']['lots'][1]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][1]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                        'description']
                },
                "root['releases'][0]['tender']['lots'][1]['contractPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                        'startDate'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                            'startDate']
                },
                "root['releases'][0]['tender']['lots'][1]['contractPeriod']['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                        'endDate'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                            'endDate']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['streetAddress']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'streetAddress'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address']['streetAddress']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['postalCode']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'postalCode'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address']['postalCode']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']"
                "['region']['id']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'addressDetails']['region']['id'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address']['addressDetails']['region']['id']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']"
                "['region']['description']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'addressDetails']['region']['description'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address']['addressDetails']['region']['description']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']"
                "['locality']['id']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'addressDetails']['locality']['id'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address']['addressDetails']['locality']['id']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']"
                "['locality']['description']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'addressDetails']['locality']['description'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address']['addressDetails']['locality']['description']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance'][
                        'description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                        'placeOfPerformance']['description']
                },
                "root['releases'][0]['tender']['tenderPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['tenderPeriod']['startDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'][
                        'startDate']
                },
                "root['releases'][0]['tender']['tenderPeriod']['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['tenderPeriod']['endDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'][
                        'endDate']
                },
                "root['releases'][0]['tender']['enquiryPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']['startDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'][
                        'startDate']
                },
                "root['releases'][0]['tender']['enquiryPeriod']['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']['endDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'][
                        'endDate']
                },
                "root['releases'][0]['tender']['auctionPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['auctionPeriod']['startDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['auctionPeriod'][
                        'startDate']
                },
                "root['releases'][0]['tender']['documents'][0]['documentType']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][0]['documentType'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][0][
                        'documentType']
                },
                "root['releases'][0]['tender']['documents'][0]['title']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][0]['title'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][0][
                        'title']
                },
                "root['releases'][0]['tender']['documents'][0]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][0]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][0][
                        'description']
                },
                "root['releases'][0]['tender']['documents'][0]['datePublished']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][0]['datePublished'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][0][
                        'datePublished']
                },
                "root['releases'][0]['tender']['documents'][1]['documentType']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][1]['documentType'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][1][
                        'documentType']
                },
                "root['releases'][0]['tender']['documents'][1]['title']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][1]['title'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][1][
                        'title']
                },
                "root['releases'][0]['tender']['documents'][1]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][1]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][1][
                        'description']
                },
                "root['releases'][0]['tender']['documents'][1]['datePublished']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][1]['datePublished'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][1][
                        'datePublished']
                },
                "root['releases'][0]['tender']['documents'][2]['documentType']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][2]['documentType'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][2][
                        'documentType']
                },
                "root['releases'][0]['tender']['documents'][2]['title']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][2]['title'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][2][
                        'title']
                },
                "root['releases'][0]['tender']['documents'][2]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][2]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][2][
                        'description']
                },
                "root['releases'][0]['tender']['documents'][2]['datePublished']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][2]['datePublished'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][2][
                        'datePublished']
                },
                "root['releases'][0]['tender']['electronicAuctions']['details'][0]['auctionPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['electronicAuctions']['details'][0][
                        'auctionPeriod']['startDate'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['electronicAuctions'][
                            'details'][0][
                            'auctionPeriod']['startDate']
                },
                "root['releases'][0]['tender']['electronicAuctions']['details'][0]['electronicAuctionModalities'][0]"
                "['eligibleMinimumDifference']['amount']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['electronicAuctions']['details'][0][
                        'electronicAuctionModalities'][0]['eligibleMinimumDifference']['amount'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['electronicAuctions'][
                            'details'][0]['electronicAuctionModalities'][0]['eligibleMinimumDifference']['amount']
                },
                "root['releases'][0]['tender']['electronicAuctions']['details'][1]['auctionPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['electronicAuctions']['details'][1][
                        'auctionPeriod']['startDate'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['electronicAuctions'][
                            'details'][1]['auctionPeriod']['startDate']
                },
                "root['releases'][0]['tender']['electronicAuctions']['details'][1]['electronicAuctionModalities']"
                "[0]['eligibleMinimumDifference']['amount']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['electronicAuctions']['details'][1][
                        'electronicAuctionModalities'][0]['eligibleMinimumDifference']['amount'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['electronicAuctions'][
                            'details'][1]['electronicAuctionModalities'][0]['eligibleMinimumDifference']['amount']
                },
                "root['releases'][0]['tender']['procurementMethodRationale']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['procurementMethodRationale'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender'][
                        'procurementMethodRationale']
                }
            },
            'iterable_item_added': {
                "root['releases'][0]['tender']['items'][0]['additionalClassifications'][1]": {
                    'scheme':
                        ev_release_after_updating['releases'][0]['tender']['items'][0]['additionalClassifications'][1][
                            'scheme'],
                    'id':
                        ev_release_after_updating['releases'][0]['tender']['items'][0]['additionalClassifications'][1][
                            'id'],
                    'description':
                        ev_release_after_updating['releases'][0]['tender']['items'][0]['additionalClassifications'][1][
                            'description']
                },
                "root['releases'][0]['tender']['items'][1]['additionalClassifications'][1]": {
                    'scheme':
                        ev_release_after_updating['releases'][0]['tender']['items'][1]['additionalClassifications'][1][
                            'scheme'],
                    'id':
                        ev_release_after_updating['releases'][0]['tender']['items'][1]['additionalClassifications'][1][
                            'id'],
                    'description':
                        ev_release_after_updating['releases'][0]['tender']['items'][1]['additionalClassifications'][1][
                            'description']
                },
                "root['releases'][0]['tender']['documents'][3]": {
                    'id': ev_release_after_updating['releases'][0]['tender']['documents'][3]['id'],
                    'documentType': ev_release_after_updating['releases'][0]['tender']['documents'][3]['documentType'],
                    'title': ev_release_after_updating['releases'][0]['tender']['documents'][3]['title'],
                    'description': ev_release_after_updating['releases'][0]['tender']['documents'][3]['description'],
                    'url': ev_release_after_updating['releases'][0]['tender']['documents'][3]['url'],
                    'datePublished': ev_release_after_updating['releases'][0]['tender']['documents'][3][
                        'datePublished'],
                    'relatedLots': ev_release_after_updating['releases'][0]['tender']['documents'][3]['relatedLots']
                }
            }
        }
        actual_result = DeepDiff(UpdateCn.ev_release_before_cn_updating, ev_release_after_updating)
        dictionary_item_added_was_cleaned = str(actual_result['dictionary_item_added']).replace('root', '')[1:-1]
        actual_result['dictionary_item_added'] = dictionary_item_added_was_cleaned
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        actual_amendments = ev_release_after_updating['releases'][0]['tender']['amendments']
        expected_amendments = [{
            "id": actual_amendments[0]['id'],
            "date": UpdateCn.message_from_kafka['data']['operationDate'],
            "releaseID": ev_release_after_updating['releases'][0]['id'],
            "amendsReleaseID": f"{ev_release_after_updating['releases'][0]['ocid']}-"
                               f"{UpdateCn.message_from_kafka['data']['ocid'][32:45]}",
            "rationale": "General change of Contract Notice"
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_amendments),
            actual_result=str(actual_amendments)
        )

    @pytestrail.case('27598')
    def test_compare_ms_release_before_updating_and_after_updating_27598_4(self):
        ms_release_after_updating = requests.get(
            url=f"http://dev.public.eprocurement.systems/tenders/{UpdateCn.cp_id}/{UpdateCn.cp_id}").json()

        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': ms_release_after_updating['releases'][0]['id'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['id']
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_updating['releases'][0]['date'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['date']
                },
                "root['releases'][0]['planning']['budget']['description']": {
                    'new_value': ms_release_after_updating['releases'][0]['planning']['budget']['description'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['planning']['budget'][
                        'description']
                },
                "root['releases'][0]['planning']['rationale']": {
                    'new_value': ms_release_after_updating['releases'][0]['planning']['rationale'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['planning']['rationale']
                },
                "root['releases'][0]['tender']['title']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['title'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['tender']['title']
                },
                "root['releases'][0]['tender']['description']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['description'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['tender']['description']
                },
                "root['releases'][0]['tender']['procurementMethodRationale']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['procurementMethodRationale'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['tender'][
                        'procurementMethodRationale']
                },
                "root['releases'][0]['tender']['contractPeriod']['startDate']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['contractPeriod']['startDate'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['tender']['contractPeriod'][
                        'startDate']
                },
                "root['releases'][0]['tender']['contractPeriod']['endDate']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['contractPeriod']['endDate'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['tender']['contractPeriod'][
                        'endDate']
                },
                "root['releases'][0]['tender']['procurementMethodAdditionalInfo']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['procurementMethodAdditionalInfo'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['tender'][
                        'procurementMethodAdditionalInfo']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['id']": {
                    'new_value': ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['id'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'id']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['title']": {
                    'new_value': ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['title'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'title']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['name']": {
                    'new_value': ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['name'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'name']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['identifier']['id']": {
                    'new_value': ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['identifier'][
                        'id'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'identifier']['id']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['identifier']['uri']": {
                    'new_value': ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['identifier'][
                        'uri'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'identifier']['uri']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0]['id']": {
                    'new_value':
                        ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0][
                            'id'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'businessFunctions'][0]['id']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0]['type']": {
                    'new_value':
                        ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0][
                            'type'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'businessFunctions'][0]['type']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0]['jobTitle']": {
                    'new_value':
                        ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0][
                            'jobTitle'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'businessFunctions'][0]['jobTitle']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0]['period']['startDate']": {
                    'new_value':
                        ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0][
                            'period']['startDate'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'businessFunctions'][0]['period']['startDate']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0]['documents'][0]['id']": {
                    'new_value':
                        ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0][
                            'documents'][0]['id'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'businessFunctions'][0]['documents'][0]['id']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0]['documents'][0]['title']": {
                    'new_value':
                        ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0][
                            'documents'][0]['title'],
                    'old_value':
                        UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                            'businessFunctions'][0]['documents'][0]['title']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0]['documents'][0]"
                "['description']": {
                    'new_value':
                        ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0][
                            'documents'][0]['description'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'businessFunctions'][0]['documents'][0]['description']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0]['documents'][0]['url']": {
                    'new_value':
                        ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0][
                            'documents'][0]['url'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'businessFunctions'][0]['documents'][0]['url']
                },
                "root['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0]['documents'][0]"
                "['datePublished']": {
                    'new_value':
                        ms_release_after_updating['releases'][0]['parties'][3]['persones'][0]['businessFunctions'][0][
                            'documents'][0]['datePublished'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['parties'][3]['persones'][0][
                        'businessFunctions'][0]['documents'][0]['datePublished']
                }
            },
            'iterable_item_added': {
                "root['releases'][0]['parties'][3]['persones'][1]": {
                    'id': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1]['id'],
                    'title': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                        'title'],
                    'name': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1]['name'],
                    'identifier': {
                        'scheme': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                            'identifier']['scheme'],
                        'id': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                            'identifier']['id'],
                        'uri': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                            'identifier']['uri']
                    },
                    'businessFunctions': [{
                        'id': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                            'businessFunctions'][0]['id'],
                        'type': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                            'businessFunctions'][0]['type'],
                        'jobTitle': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                            'businessFunctions'][0]['jobTitle'],
                        'period': {
                            'startDate':
                                ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                                    'businessFunctions'][0]['period']['startDate']
                        },
                        'documents': [{
                            'id': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                                'businessFunctions'][0]['documents'][0]['id'],
                            'documentType':
                                ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                                    'businessFunctions'][0]['documents'][0]['documentType'],
                            'title': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                                'businessFunctions'][0]['documents'][0]['title'],
                            'description':
                                ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                                    'businessFunctions'][0]['documents'][0]['description'],
                            'url': ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                                'businessFunctions'][0]['documents'][0]['url'],
                            'datePublished':
                                ms_release_after_updating['releases'][0]['parties'][3]['persones'][1][
                                    'businessFunctions'][0]['documents'][0]['datePublished']
                        }]
                    }]
                },
                "root['releases'][0]['parties'][3]['persones'][2]": {
                    'id': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2]['id'],
                    'title': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                        'title'],
                    'name': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2]['name'],
                    'identifier': {
                        'scheme': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                            'identifier']['scheme'],
                        'id': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                            'identifier']['id'],
                        'uri': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                            'identifier']['uri']
                    },
                    'businessFunctions': [{
                        'id': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                            'businessFunctions'][0]['id'],
                        'type': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                            'businessFunctions'][0]['type'],
                        'jobTitle': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                            'businessFunctions'][0]['jobTitle'],
                        'period': {
                            'startDate':
                                ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                                    'businessFunctions'][0]['period']['startDate']
                        },
                        'documents': [{
                            'id': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                                'businessFunctions'][0]['documents'][0]['id'],
                            'documentType':
                                ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                                    'businessFunctions'][0]['documents'][0]['documentType'],
                            'title': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                                'businessFunctions'][0]['documents'][0]['title'],
                            'description':
                                ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                                    'businessFunctions'][0]['documents'][0]['description'],
                            'url': ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                                'businessFunctions'][0]['documents'][0]['url'],
                            'datePublished':
                                ms_release_after_updating['releases'][0]['parties'][3]['persones'][2][
                                    'businessFunctions'][0]['documents'][0]['datePublished']
                        }]
                    }]
                }
            }
        }
        actual_result = DeepDiff(UpdateCn.ms_release_before_cn_updating, ms_release_after_updating)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )

    @pytestrail.case('27598')
    def test_compare_ms_release_before_updating_and_after_updating_27598_5(self):
        pn_release_after_updating = requests.get(
            url=f"http://dev.public.eprocurement.systems/tenders/{UpdateCn.cp_id}/{UpdateCn.pn_id}").json()

        expected_result = {}
        actual_result = DeepDiff(UpdateCn.pn_release_before_cn_updating, pn_release_after_updating)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckOnThePossibilityOfCnOnPnUpdatingWithObligatoryDataModel(object):
    @pytestrail.case("27599")
    def test_test_send_the_request_27599_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        enquiry_and_tender_period = create_enquiry_and_tender_period(second_enquiry=600, second_tender=900)
        instance = instance
        first_lot_id = f"{uuid4()}"
        second_lot_id = f"{uuid4()}"
        first_item_id = f"{uuid4()}"
        second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        payload = copy.deepcopy(update_cn_on_pn_payload_obligatory_data_model)
        payload['tender']['tenderPeriod']['endDate'] = enquiry_and_tender_period[3]
        payload['tender']['enquiryPeriod']['endDate'] = enquiry_and_tender_period[1]
        payload['tender']['lots'][0]['id'] = first_lot_id
        payload['tender']['lots'][1]['id'] = second_lot_id
        payload['tender']['items'][0]['id'] = first_item_id
        payload['tender']['items'][1]['id'] = second_item_id
        payload['tender']['items'][0]['relatedLot'] = first_lot_id
        payload['tender']['items'][1]['relatedLot'] = second_lot_id
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded

        cn = CN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_three_id=document_one_was_uploaded
        )
        create_ev_response = cn.insert_cnonpn_obligatory(
            first_lot_id=first_lot_id,
            second_lot_id=second_lot_id,
            first_item_id=first_item_id,
            second_item_id=second_item_id,
            second_enquiry=121,
            second_tender=300
        )
        UpdateCn.ms_release_before_cn_updating = requests.get(url=create_ev_response[5]).json()
        UpdateCn.pn_release_before_cn_updating = requests.get(url=create_ev_response[6]).json()
        UpdateCn.ev_release_before_cn_updating = requests.get(url=create_ev_response[7]).json()
        update_cn_response = cn.update_cn(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3],
            pn_token=create_ev_response[2]
        )
        UpdateCn.message_from_kafka = cn.get_message_from_kafka()
        UpdateCn.successfully_update_cn = cn.check_on_that_message_is_successfully_update_cn(
            cp_id=create_ev_response[0],
            ev_id=create_ev_response[3]
        )
        UpdateCn.payload = payload
        UpdateCn.cp_id = create_ev_response[0]
        UpdateCn.ev_id = create_ev_response[3]
        UpdateCn.pn_id = create_ev_response[1]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(update_cn_response.status_code)
        )

    @pytestrail.case('27599')
    def test_see_result_from_feed_point_27599_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(UpdateCn.successfully_update_cn)
        )

    @pytestrail.case('27599')
    def test_compare_ev_release_before_updating_and_after_updating_27599_3(self):
        ev_release_after_updating = requests.get(
            url=f"{UpdateCn.message_from_kafka['data']['url']}").json()

        expected_result = {
            'dictionary_item_added': "['releases'][0]['tender']['amendments']",
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{ev_release_after_updating['releases'][0]['ocid']}-"
                                 f"{ev_release_after_updating['releases'][0]['id'][46:59]}",
                    'old_value': f"{UpdateCn.ev_release_before_cn_updating['releases'][0]['ocid']}-"
                                 f"{UpdateCn.ev_release_before_cn_updating['releases'][0]['id'][46:59]}"
                },
                "root['releases'][0]['date']": {
                    'new_value': ev_release_after_updating['releases'][0]['date'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': ev_release_after_updating['releases'][0]['tag'][0],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tag'][0]
                },

                "root['releases'][0]['tender']['items'][0]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0][
                        'description']
                },
                "root['releases'][0]['tender']['items'][0]['quantity']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['quantity'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0]['quantity']
                },
                "root['releases'][0]['tender']['items'][0]['unit']['name']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['unit']['name'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0]['unit'][
                        'name']
                },
                "root['releases'][0]['tender']['items'][0]['unit']['id']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['unit']['id'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0]['unit'][
                        'id']
                },
                "root['releases'][0]['tender']['items'][1]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][1]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][1][
                        'description']
                },

                "root['releases'][0]['tender']['items'][1]['quantity']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][1]['quantity'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][1]['quantity']
                },
                "root['releases'][0]['tender']['items'][1]['unit']['name']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['unit']['name'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0]['unit'][
                        'name']
                },
                "root['releases'][0]['tender']['items'][1]['unit']['id']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['items'][0]['unit']['id'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['items'][0]['unit'][
                        'id']
                },
                "root['releases'][0]['tender']['lots'][0]['title']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][0]['title'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0]['title']
                },
                "root['releases'][0]['tender']['lots'][0]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][0]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                        'description']
                },
                "root['releases'][0]['tender']['lots'][0]['contractPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                        'startDate'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                            'startDate']
                },
                "root['releases'][0]['tender']['lots'][0]['contractPeriod']['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                        'endDate'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0]['contractPeriod'][
                            'endDate']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['streetAddress']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'streetAddress'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address'][
                            'streetAddress']
                },

                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']"
                "['region']['id']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'addressDetails']['region']['id'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address'][
                            'addressDetails']['region']['id']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']"
                "['region']['description']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'addressDetails']['region']['description'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address'][
                            'addressDetails']['region']['description']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']"
                "['locality']['id']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'addressDetails']['locality']['id'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address'][
                            'addressDetails']['locality']['id']
                },
                "root['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address']['addressDetails']"
                "['locality']['description']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][0]['placeOfPerformance']['address'][
                            'addressDetails']['locality']['description'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][0][
                            'placeOfPerformance']['address'][
                            'addressDetails']['locality']['description']
                },

                "root['releases'][0]['tender']['lots'][1]['title']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][1]['title'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1]['title']
                },
                "root['releases'][0]['tender']['lots'][1]['description']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][1]['description'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1]
                    ['description']
                },
                "root['releases'][0]['tender']['lots'][1]['contractPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                        'startDate'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                            'startDate']
                },
                "root['releases'][0]['tender']['lots'][1]['contractPeriod']['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                        'endDate'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1]['contractPeriod'][
                            'endDate']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['streetAddress']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'streetAddress'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address'][
                            'streetAddress']
                },

                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']"
                "['region']['id']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'addressDetails']['region']['id'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address'][
                            'addressDetails']['region']['id']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']"
                "['region']['description']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'addressDetails']['region']['description'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address'][
                            'addressDetails']['region']['description']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']"
                "['locality']['id']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'addressDetails']['locality']['id'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address'][
                            'addressDetails']['locality']['id']
                },
                "root['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address']['addressDetails']"
                "['locality']['description']": {
                    'new_value':
                        ev_release_after_updating['releases'][0]['tender']['lots'][1]['placeOfPerformance']['address'][
                            'addressDetails']['locality']['description'],
                    'old_value':
                        UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['lots'][1][
                            'placeOfPerformance']['address'][
                            'addressDetails']['locality']['description']
                },

                "root['releases'][0]['tender']['tenderPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['tenderPeriod']['startDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'][
                        'startDate']
                },
                "root['releases'][0]['tender']['tenderPeriod']['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['tenderPeriod']['endDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['tenderPeriod'][
                        'endDate']
                },
                "root['releases'][0]['tender']['enquiryPeriod']['startDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']['startDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'][
                        'startDate']
                },
                "root['releases'][0]['tender']['enquiryPeriod']['endDate']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['enquiryPeriod']['endDate'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['enquiryPeriod'][
                        'endDate']
                },

                "root['releases'][0]['tender']['documents'][0]['documentType']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][0]['documentType'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][0][
                        'documentType']
                },
                "root['releases'][0]['tender']['documents'][0]['title']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][0]['title'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][0][
                        'title']
                },

                "root['releases'][0]['tender']['documents'][0]['datePublished']": {
                    'new_value': ev_release_after_updating['releases'][0]['tender']['documents'][0]['datePublished'],
                    'old_value': UpdateCn.ev_release_before_cn_updating['releases'][0]['tender']['documents'][0][
                        'datePublished']
                }
            }
        }
        actual_result = DeepDiff(UpdateCn.ev_release_before_cn_updating, ev_release_after_updating)
        dictionary_item_added_was_cleaned = str(actual_result['dictionary_item_added']).replace('root', '')[1:-1]
        actual_result['dictionary_item_added'] = dictionary_item_added_was_cleaned
        print(json.dumps(expected_result))
        print("///////////////////////////")
        print(json.dumps(actual_result))
        print("++++++++++++++++++++++++")
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
        actual_amendments = ev_release_after_updating['releases'][0]['tender']['amendments']
        expected_amendments = [{
            "id": actual_amendments[0]['id'],
            "date": UpdateCn.message_from_kafka['data']['operationDate'],
            "releaseID": ev_release_after_updating['releases'][0]['id'],
            "amendsReleaseID": f"{ev_release_after_updating['releases'][0]['ocid']}-"
                               f"{UpdateCn.message_from_kafka['data']['ocid'][32:45]}",
            "rationale": "General change of Contract Notice"
        }]
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_amendments),
            actual_result=str(actual_amendments)
        )

    @pytestrail.case('27599')
    def test_compare_ms_release_before_updating_and_after_updating_27599_4(self):
        ms_release_after_updating = requests.get(
            url=f"http://dev.public.eprocurement.systems/tenders/{UpdateCn.cp_id}/{UpdateCn.cp_id}").json()

        expected_result = {
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': ms_release_after_updating['releases'][0]['id'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['id']
                },
                "root['releases'][0]['date']": {
                    'new_value': ms_release_after_updating['releases'][0]['date'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['date']
                },

                "root['releases'][0]['tender']['title']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['title'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['tender']['title']
                },
                "root['releases'][0]['tender']['description']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['description'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['tender']['description']
                },

                "root['releases'][0]['tender']['contractPeriod']['startDate']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['contractPeriod']['startDate'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['tender']['contractPeriod'][
                        'startDate']
                },
                "root['releases'][0]['tender']['contractPeriod']['endDate']": {
                    'new_value': ms_release_after_updating['releases'][0]['tender']['contractPeriod']['endDate'],
                    'old_value': UpdateCn.ms_release_before_cn_updating['releases'][0]['tender']['contractPeriod'][
                        'endDate']
                }
            }
        }
        actual_result = DeepDiff(UpdateCn.ms_release_before_cn_updating, ms_release_after_updating)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )

    @pytestrail.case('27599')
    def test_compare_ms_release_before_updating_and_after_updating_27599_5(self):
        pn_release_after_updating = requests.get(
            url=f"http://dev.public.eprocurement.systems/tenders/{UpdateCn.cp_id}/{UpdateCn.pn_id}").json()

        expected_result = {}
        actual_result = DeepDiff(UpdateCn.pn_release_before_cn_updating, pn_release_after_updating)
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
