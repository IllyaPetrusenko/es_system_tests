import copy
from uuid import uuid4
import requests
from deepdiff import DeepDiff
from pytest_testrail.plugin import pytestrail
from tests.conftest import CreateCn
from tests.essences.cn import CN
from tests.iMDM_service.get_information import MdmService
from tests.iStorage import Document
from tests.payloads.cnonpn_payload import create_cn_on_pn_payload_full_data_model_with_auction, \
    create_cn_on_pn_payload_obligatory_data_model
from useful_functions import compare_actual_result_and_expected_result, \
    get_value_from_classification_unit_dictionary_csv, get_value_from_cpvs_dictionary_csv, \
    get_value_from_classification_cpv_dictionary_xls, get_new_classification_id


class TestCheckOnCorrectnessOfPublishingEvMsPnReleasesBasedOnPnFullDataModelAndCnOnPnFullDataModel(object):
    @pytestrail.case("27595")
    def test_test_send_the_request_27595_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        CreateCn.first_lot_id = f"{uuid4()}"
        CreateCn.second_lot_id = f"{uuid4()}"
        CreateCn.first_item_id = f"{uuid4()}"
        CreateCn.second_item_id = f"{uuid4()}"
        document = Document(instance=instance)
        CreateCn.document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        CreateCn.document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        CreateCn.document_three_was_uploaded = document.uploading_document()[0]["data"]["id"]
        payload = copy.deepcopy(create_cn_on_pn_payload_full_data_model_with_auction)
        payload['tender']['electronicAuctions']['details'][0]['relatedLot'] = CreateCn.first_lot_id
        payload['tender']['electronicAuctions']['details'][1]['relatedLot'] = CreateCn.second_lot_id
        payload['tender']['lots'][0]['id'] = CreateCn.first_lot_id
        payload['tender']['lots'][1]['id'] = CreateCn.second_lot_id
        payload['tender']['items'][0]['id'] = CreateCn.first_item_id
        payload['tender']['items'][1]['id'] = CreateCn.second_item_id
        payload['tender']['items'][0]['relatedLot'] = CreateCn.first_lot_id
        payload['tender']['items'][1]['relatedLot'] = CreateCn.second_lot_id
        payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0][
            'id'] = CreateCn.document_one_was_uploaded
        payload['tender']['criteria'][1]['requirementGroups'][0]['requirements'][1]['eligibleEvidences'][0][
            'relatedDocument']['id'] = CreateCn.document_three_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][0][
            'relatedDocument']['id'] = CreateCn.document_three_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][1][
            'relatedDocument']['id'] = CreateCn.document_three_was_uploaded
        payload['tender']['criteria'][1]['relatedItem'] = CreateCn.first_lot_id
        payload['tender']['criteria'][3]['relatedItem'] = CreateCn.first_item_id
        payload['tender']['documents'][0]['id'] = CreateCn.document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = CreateCn.document_two_was_uploaded
        payload['tender']['documents'][2]['id'] = CreateCn.document_three_was_uploaded
        payload['tender']['documents'][0]['relatedLots'][0] = CreateCn.first_lot_id
        payload['tender']['documents'][1]['relatedLots'][0] = CreateCn.second_lot_id
        payload['tender']['documents'][2]['relatedLots'][0] = CreateCn.first_lot_id

        cn = CN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd,
            document_one_id=CreateCn.document_one_was_uploaded,
            document_two_id=CreateCn.document_two_was_uploaded
        )
        create_pn_response = cn.insert_pn_full_(
            first_lot_id=CreateCn.first_lot_id,
            second_lot_id=CreateCn.second_lot_id,
            first_item_id=CreateCn.first_item_id,
            second_item_id=CreateCn.second_item_id
        )
        CreateCn.ms_release_before_cn_creation = requests.get(url=create_pn_response[8]).json()
        CreateCn.pn_release_before_cn_creation = requests.get(url=create_pn_response[9]).json()
        create_cn_response = cn.create_cn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cn.get_message_from_kafka()

        CreateCn.message_from_kafka = cn.get_message_from_kafka()
        CreateCn.successfully_create_cn = cn.check_on_that_message_is_successfully_create_cn()
        CreateCn.payload = payload
        CreateCn.cp_id = create_pn_response[4]
        CreateCn.pn_id = create_pn_response[5]

        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_cn_response.status_code)
        )

    @pytestrail.case('27595')
    def test_see_result_from_feed_point_27595_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(CreateCn.successfully_create_cn)
        )

    @pytestrail.case('27595')
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_ev_release_27595_3(
            self, language):
        ev_release = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}").json()
        actual_result = ev_release
        expected_result = {
            "uri": f"http://dev.public.eprocurement.systems/tenders/{CreateCn.message_from_kafka['data']['ocid']}/"
                   f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}",
            "version": "1.1",
            "extensions": [
                "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"],
            "publisher": {
                "name": "M-Tender",
                "uri": "https://www.mtender.gov.md"
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": CreateCn.message_from_kafka['data']['operationDate'],
            "releases": [{
                "ocid": CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id'],
                "id": f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}-"
                      f"{actual_result['releases'][0]['id'][46:59]}",
                "date": CreateCn.message_from_kafka['data']['operationDate'],
                "tag": ["tender"],
                "language": language,
                "initiationType": "tender",
                "tender": {
                    "id": actual_result['releases'][0]['tender']['id'],
                    "title": "Evaluation",
                    "description": "Evaluation stage of contracting process",
                    "status": "active",
                    "statusDetails": "clarification",
                    "criteria": [{
                        "id": actual_result['releases'][0]['tender']['criteria'][0]['id'],
                        "title": CreateCn.payload['tender']['criteria'][0]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][0]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][0]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][0]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "description": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                    'requirements'][0]['description'],
                                "eligibleEvidences": [{
                                    "id": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][0]['id'],
                                    "title": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][0]['title'],
                                    "type": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][0]['type'],
                                    "description": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][0]['description'],
                                    "relatedDocument": {
                                        "id": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                            'requirements'][0]['eligibleEvidences'][0]['relatedDocument']['id']
                                    }
                                }, {
                                    "id": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][1]['id'],
                                    "title": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][1]['title'],
                                    "type": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][1]['type'],
                                    "description": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][1]['description'],
                                    "relatedDocument": {
                                        "id": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                            'requirements'][0]['eligibleEvidences'][1]['relatedDocument']['id']
                                    }
                                }],
                                "expectedValue": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                    'requirements'][0]['expectedValue']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][0]['relatesTo'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][0]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][0]['classification']['id']
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['criteria'][1]['id'],
                        "title": CreateCn.payload['tender']['criteria'][1]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][1]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][1]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "description": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][0]['description'],
                                "expectedValue": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][0]['expectedValue']
                            }, {
                                "id": actual_result['releases'][0]['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['id'],
                                "title": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "description": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['description'],
                                "period": {
                                    "startDate": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['period']['startDate'],
                                    "endDate": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['period']['endDate']
                                },
                                "eligibleEvidences": [{
                                    "id": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['eligibleEvidences'][0]['id'],
                                    "title": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['eligibleEvidences'][0]['title'],
                                    "type": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['eligibleEvidences'][0]['type'],
                                    "description": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['eligibleEvidences'][0]['description'],
                                    "relatedDocument": {
                                        "id": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                            'requirements'][1]['eligibleEvidences'][0]['relatedDocument']['id']
                                    }
                                }],
                                "minValue": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['minValue'],
                                "maxValue": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['maxValue']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][1]['relatesTo'],
                        "relatedItem": CreateCn.payload['tender']['criteria'][1]['relatedItem'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][1]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][1]['classification']['id']
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['criteria'][2]['id'],
                        "title": CreateCn.payload['tender']['criteria'][2]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][2]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "expectedValue": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][0]['expectedValue']
                            }, {
                                "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][1]['id'],
                                "title": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][1]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][1]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                            }]
                        }, {
                            "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][1]['id'],
                            "description": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "expectedValue": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][0]['expectedValue']
                            }, {
                                "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][1]['id'],
                                "title": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][1]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][1]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][2]['relatesTo'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][2]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][2]['classification']['id']
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['criteria'][3]['id'],
                        "title": CreateCn.payload['tender']['criteria'][3]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][3]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][3]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][3]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "period": {
                                    "startDate": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                        'requirements'][0]['period']['startDate'],
                                    "endDate": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                        'requirements'][0]['period']['endDate']
                                },
                                "minValue": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                    'requirements'][0]['minValue'],
                                "maxValue": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                    'requirements'][0]['maxValue']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][3]['relatesTo'],
                        "relatedItem": CreateCn.payload['tender']['criteria'][3]['relatedItem'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][3]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][3]['classification']['id']
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['criteria'][4]['id'],
                        "title": CreateCn.payload['tender']['criteria'][4]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][4]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][4]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][4]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][4]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][4]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][4]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][4]['relatesTo'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][4]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][4]['classification']['id']
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['criteria'][5]['id'],
                        "title": CreateCn.payload['tender']['criteria'][5]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][5]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][5]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][5]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][5]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][5]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][5]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][5]['relatesTo'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][5]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][5]['classification']['id']
                        }
                    }],
                    "conversions": [{
                        "id": actual_result['releases'][0]['tender']['conversions'][0]['id'],
                        "relatesTo": "requirement",
                        "relatedItem": actual_result['releases'][0]['tender']['conversions'][0]['relatedItem'],
                        "rationale": CreateCn.payload['tender']['conversions'][0]['rationale'],
                        "description": CreateCn.payload['tender']['conversions'][0]['description'],
                        "coefficients": [{
                            "id": actual_result['releases'][0]['tender']['conversions'][0]['coefficients'][0]['id'],
                            "value": CreateCn.payload['tender']['conversions'][0]['coefficients'][0]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][0]['coefficients'][0][
                                'coefficient']
                        }]
                    }, {
                        "id": actual_result['releases'][0]['tender']['conversions'][1]['id'],
                        "relatesTo": "requirement",
                        "relatedItem": actual_result['releases'][0]['tender']['conversions'][1]['relatedItem'],
                        "rationale": CreateCn.payload['tender']['conversions'][1]['rationale'],
                        "description": CreateCn.payload['tender']['conversions'][1]['description'],
                        "coefficients": [{
                            "id": actual_result['releases'][0]['tender']['conversions'][1]['coefficients'][0]['id'],
                            "value": CreateCn.payload['tender']['conversions'][1]['coefficients'][0]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][1]['coefficients'][0][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][1]['coefficients'][1]['id'],
                            "value": CreateCn.payload['tender']['conversions'][1]['coefficients'][1]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][1]['coefficients'][1][
                                'coefficient']
                        }, {
                            "id": ev_release['releases'][0]['tender']['conversions'][1]['coefficients'][2]['id'],
                            "value": CreateCn.payload['tender']['conversions'][1]['coefficients'][2]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][1]['coefficients'][2][
                                'coefficient']
                        }]
                    }, {
                        "id": actual_result['releases'][0]['tender']['conversions'][2]['id'],
                        "relatesTo": "requirement",
                        "relatedItem": actual_result['releases'][0]['tender']['conversions'][2]['relatedItem'],
                        "rationale": CreateCn.payload['tender']['conversions'][2]['rationale'],
                        "description": CreateCn.payload['tender']['conversions'][2]['description'],
                        "coefficients": [{
                            "id": actual_result['releases'][0]['tender']['conversions'][2]['coefficients'][0]['id'],
                            "value": CreateCn.payload['tender']['conversions'][2]['coefficients'][0]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][2]['coefficients'][0][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][2]['coefficients'][1]['id'],
                            "value": CreateCn.payload['tender']['conversions'][2]['coefficients'][1]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][2]['coefficients'][1][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][2]['coefficients'][2]['id'],
                            "value": CreateCn.payload['tender']['conversions'][2]['coefficients'][2]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][2]['coefficients'][2][
                                'coefficient']
                        }]
                    }, {
                        "id": actual_result['releases'][0]['tender']['conversions'][3]['id'],
                        "relatesTo": "requirement",
                        "relatedItem": actual_result['releases'][0]['tender']['conversions'][3]['relatedItem'],
                        "rationale": CreateCn.payload['tender']['conversions'][3]['rationale'],
                        "description": CreateCn.payload['tender']['conversions'][3]['description'],
                        "coefficients": [{
                            "id": actual_result['releases'][0]['tender']['conversions'][3]['coefficients'][0]['id'],
                            "value": CreateCn.payload['tender']['conversions'][3]['coefficients'][0]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][3]['coefficients'][0][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][3]['coefficients'][1]['id'],
                            "value": CreateCn.payload['tender']['conversions'][3]['coefficients'][1]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][3]['coefficients'][1][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][3]['coefficients'][2]['id'],
                            "value": CreateCn.payload['tender']['conversions'][3]['coefficients'][2]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][3]['coefficients'][2][
                                'coefficient']
                        }]
                    }],
                    "items": [{
                        "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0]['id'],
                        "internalId": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0][
                            'internalId'],
                        "description": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0][
                            'description'],
                        "classification": {
                            "scheme": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0][
                                'classification'][
                                'scheme'],
                            "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0][
                                'classification']['id'],
                            "description": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0][
                                'classification'][
                                'description']
                        },
                        "additionalClassifications": [{
                            "scheme":
                                CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0][
                                    'additionalClassifications'][
                                    0]['scheme'],
                            "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0][
                                'additionalClassifications'][
                                0]['id'],
                            "description":
                                CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0][
                                    'additionalClassifications'][
                                    0]['description']
                        }],
                        "quantity": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0][
                            'quantity'],
                        "unit": {
                            "name": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0]['unit'][
                                'name'],
                            "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0]['unit'][
                                'id']
                        },
                        "relatedLot": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][0][
                            'relatedLot']
                    }, {
                        "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1]['id'],
                        "internalId": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1][
                            'internalId'],
                        "description": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1][
                            'description'],
                        "classification": {
                            "scheme": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1][
                                'classification'][
                                'scheme'],
                            "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1][
                                'classification']['id'],
                            "description": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1][
                                'classification'][
                                'description']
                        },
                        "additionalClassifications": [{
                            "scheme":
                                CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1][
                                    'additionalClassifications'][
                                    0]['scheme'],
                            "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1][
                                'additionalClassifications'][
                                0]['id'],
                            "description":
                                CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1][
                                    'additionalClassifications'][
                                    0]['description']
                        }],
                        "quantity": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1][
                            'quantity'],
                        "unit": {
                            "name": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1]['unit'][
                                'name'],
                            "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1]['unit'][
                                'id']
                        },
                        "relatedLot": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['items'][1][
                            'relatedLot']
                    }],
                    "lots": [{
                        "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0]['id'],
                        "internalId": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                            'internalId'],
                        "title": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0]['title'],
                        "description": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                            'description'],
                        "status": "active",
                        "statusDetails": "empty",
                        "value": {
                            "amount":
                                CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0]['value'][
                                    'amount'],
                            "currency":
                                CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0]['value'][
                                    'currency']
                        },
                        "contractPeriod": {
                            "startDate": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                'contractPeriod'][
                                'startDate'],
                            "endDate": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                'contractPeriod'][
                                'endDate']
                        },
                        "placeOfPerformance": {
                            "address": {
                                "streetAddress":
                                    CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                        'placeOfPerformance'][
                                        'address']['streetAddress'],
                                "postalCode":
                                    CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                        'placeOfPerformance'][
                                        'address']['postalCode'],
                                "addressDetails": {
                                    "country": {
                                        "scheme":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['country']['scheme'],
                                        "id":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['country']['id'],
                                        "description":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['country'][
                                                'description'],
                                        "uri":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['country']['uri']
                                    },
                                    "region": {
                                        "scheme":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['region']['scheme'],
                                        "id":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['region']['id'],
                                        "description":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['region'][
                                                'description'],
                                        "uri":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['region']['uri']
                                    },
                                    "locality": {
                                        "scheme":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['locality'][
                                                'scheme'],
                                        "id":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['locality']['id'],
                                        "description":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['locality'][
                                                'description'],
                                        "uri":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                                'placeOfPerformance']['address']['addressDetails']['locality']['uri']
                                    }
                                    }
                            },
                            "description": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                'placeOfPerformance']['description']
                        },
                        "hasOptions":
                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0]['options'][0][
                                'hasOptions'],
                        "hasRecurrence":
                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                'recurrentProcurement'][0][
                                'isRecurrent'],
                        "hasRenewal":
                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0]['renewals'][0][
                                'hasRenewals']
                    }, {
                        "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1]['id'],
                        "internalId": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                            'internalId'],
                        "title": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1]['title'],
                        "description": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                            'description'],
                        "status": "active",
                        "statusDetails": "empty",
                        "value": {
                            "amount":
                                CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1]['value'][
                                    'amount'],
                            "currency":
                                CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1]['value'][
                                    'currency']
                        },
                        "contractPeriod": {
                            "startDate": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                'contractPeriod'][
                                'startDate'],
                            "endDate": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                'contractPeriod'][
                                'endDate']
                        },
                        "placeOfPerformance": {
                            "address": {
                                "streetAddress":
                                    CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                        'placeOfPerformance'][
                                        'address']['streetAddress'],
                                "postalCode":
                                    CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                        'placeOfPerformance'][
                                        'address']['postalCode'],
                                "addressDetails": {
                                    "country": {
                                        "scheme":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['country']['scheme'],
                                        "id":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['country']['id'],
                                        "description":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['country'][
                                                'description'],
                                        "uri":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['country']['uri']
                                    },
                                    "region": {
                                        "scheme":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['region']['scheme'],
                                        "id":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['region']['id'],
                                        "description":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['region'][
                                                'description'],
                                        "uri":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['region']['uri']
                                    },
                                    "locality": {
                                        "scheme":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['locality'][
                                                'scheme'],
                                        "id":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['locality']['id'],
                                        "description":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['locality'][
                                                'description'],
                                        "uri":
                                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                                'placeOfPerformance']['address']['addressDetails']['locality']['uri']
                                    }
                                    }
                            },
                            "description": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                'placeOfPerformance']['description']
                        },
                        "hasOptions":
                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1]['options'][0][
                                'hasOptions'],
                        "hasRecurrence":
                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                'recurrentProcurement'][0][
                                'isRecurrent'],
                        "hasRenewal":
                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1]['renewals'][0][
                                'hasRenewals']
                    }],
                    "lotGroups": [{
                        "optionToCombine":
                            CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lotGroups'][0][
                                'optionToCombine']
                    }],
                    "tenderPeriod": {
                        "startDate": CreateCn.payload['tender']['enquiryPeriod']['endDate'],
                        "endDate": CreateCn.payload['tender']['tenderPeriod']['endDate']
                    },
                    "enquiryPeriod": {
                        "startDate": CreateCn.message_from_kafka['data']['operationDate'],
                        "endDate": CreateCn.payload['tender']['enquiryPeriod']['endDate']
                    },
                    "auctionPeriod": {
                        "startDate": actual_result['releases'][0]['tender']['auctionPeriod']['startDate']
                    },
                    "hasEnquiries": False,
                    "documents": [{
                        "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['documents'][0]['id'],
                        "documentType": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['documents'][0][
                            'documentType'],
                        "title": CreateCn.payload['tender']['documents'][0]['title'],
                        "description": CreateCn.payload['tender']['documents'][0]['description'],
                        "url": f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                               f"{CreateCn.document_one_was_uploaded}",
                        "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                        "relatedLots": actual_result['releases'][0]['tender']['documents'][0]['relatedLots']
                    }, {
                        "id": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['documents'][1]['id'],
                        "documentType": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['documents'][0][
                            'documentType'],
                        "title": CreateCn.payload['tender']['documents'][1]['title'],
                        "description": CreateCn.payload['tender']['documents'][1]['description'],
                        "url": f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                               f"{CreateCn.document_one_was_uploaded}",
                        "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                        "relatedLots": actual_result['releases'][0]['tender']['documents'][1]['relatedLots']
                    }, {
                        "id": CreateCn.payload['tender']['documents'][2]['id'],
                        "documentType": CreateCn.payload['tender']['documents'][2]['documentType'],
                        "title": CreateCn.payload['tender']['documents'][2]['title'],
                        "description": CreateCn.payload['tender']['documents'][2]['description'],
                        "url": f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                               f"{CreateCn.payload['tender']['documents'][2]['id']}",
                        "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                        "relatedLots": actual_result['releases'][0]['tender']['documents'][2]['relatedLots']
                    }],
                    "awardCriteria": CreateCn.payload['tender']['awardCriteria'],
                    "awardCriteriaDetails": CreateCn.payload['tender']['awardCriteriaDetails'],
                    "submissionMethod": CreateCn.pn_release_before_cn_creation['releases'][0]['tender'][
                        'submissionMethod'],
                    "submissionMethodDetails": CreateCn.pn_release_before_cn_creation['releases'][0]['tender'][
                        'submissionMethodDetails'],
                    "submissionMethodRationale": CreateCn.pn_release_before_cn_creation['releases'][0]['tender'][
                        'submissionMethodRationale'],
                    "requiresElectronicCatalogue": CreateCn.pn_release_before_cn_creation['releases'][0]['tender'][
                        'requiresElectronicCatalogue'],
                    "procurementMethodModalities": CreateCn.payload['tender']['procurementMethodModalities'],
                    "electronicAuctions": {
                        "details": [{
                            "id": actual_result['releases'][0]['tender']['electronicAuctions']['details'][0]['id'],
                            "relatedLot": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][0][
                                'id'],
                            "auctionPeriod": {
                                "startDate": actual_result['releases'][0]['tender']['electronicAuctions']['details'][0][
                                    'auctionPeriod']['startDate']
                            },
                            "electronicAuctionModalities": [{
                                "url": f"http://auction.eprocurement.systems/auctions/"
                                       f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}/"
                                       f"{CreateCn.first_lot_id}",
                                "eligibleMinimumDifference": {
                                    "amount": CreateCn.payload['tender']['electronicAuctions']['details'][0][
                                        'electronicAuctionModalities'][0]['eligibleMinimumDifference']['amount'],
                                    "currency": CreateCn.payload['tender']['electronicAuctions']['details'][0][
                                        'electronicAuctionModalities'][0]['eligibleMinimumDifference']['currency']
                                }
                            }]
                        }, {
                            "id": actual_result['releases'][0]['tender']['electronicAuctions']['details'][1]['id'],
                            "relatedLot": CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['lots'][1][
                                'id'],
                            "auctionPeriod": {
                                "startDate": actual_result['releases'][0]['tender']['electronicAuctions']['details'][1][
                                    'auctionPeriod']['startDate']
                            },
                            "electronicAuctionModalities": [{
                                "url": f"http://auction.eprocurement.systems/auctions/"
                                       f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}/"
                                       f"{CreateCn.second_lot_id}",
                                "eligibleMinimumDifference": {
                                    "amount": CreateCn.payload['tender']['electronicAuctions']['details'][1][
                                        'electronicAuctionModalities'][0]['eligibleMinimumDifference']['amount'],
                                    "currency": CreateCn.payload['tender']['electronicAuctions']['details'][1][
                                        'electronicAuctionModalities'][0]['eligibleMinimumDifference']['currency']
                                }
                            }]
                        }]
                    },
                    "procurementMethodRationale": CreateCn.payload['tender']['procurementMethodRationale']
                },
                "hasPreviousNotice": True,
                "purposeOfNotice": {
                    "isACallForCompetition": True
                },
                "relatedProcesses": [{
                    "id": actual_result['releases'][0]['relatedProcesses'][0]['id'],
                    "relationship": ["parent"],
                    "scheme": "ocid",
                    "identifier": CreateCn.message_from_kafka['data']['ocid'],
                    "uri": f"http://dev.public.eprocurement.systems/tenders/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}"
                }, {
                    "id": actual_result['releases'][0]['relatedProcesses'][1]['id'],
                    "relationship": ["planning"],
                    "scheme": "ocid",
                    "identifier": CreateCn.pn_id,
                    "uri": f"http://dev.public.eprocurement.systems/tenders/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}/"
                           f"{CreateCn.pn_id}"
                }]
            }]
        }
        compare_releases = DeepDiff(expected_result, actual_result)
        assert compare_actual_result_and_expected_result(
            expected_result=str({}),
            actual_result=str(compare_releases)
        )

    @pytestrail.case('27595')
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_ms_release_27595_4(
            self, language):
        ev_release = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}").json()
        ms_release_after_cn_creation = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.message_from_kafka['data']['ocid']}").json()

        persone_document = \
            CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0]['id']
        actual_result = ms_release_after_cn_creation

        expected_result = {
            "uri": CreateCn.ms_release_before_cn_creation['uri'],
            "version": CreateCn.ms_release_before_cn_creation['version'],
            "extensions": [
                CreateCn.ms_release_before_cn_creation['extensions'][0],
                CreateCn.ms_release_before_cn_creation['extensions'][1]],
            "publisher": {
                "name": CreateCn.ms_release_before_cn_creation['publisher']['name'],
                "uri": CreateCn.ms_release_before_cn_creation['publisher']['uri']
            },
            "license": CreateCn.ms_release_before_cn_creation['license'],
            "publicationPolicy": CreateCn.ms_release_before_cn_creation['publicationPolicy'],
            "publishedDate": CreateCn.ms_release_before_cn_creation['releases'][0]['date'],
            "releases": [{
                "ocid": CreateCn.ms_release_before_cn_creation['releases'][0]['ocid'],
                "id": f"{CreateCn.ms_release_before_cn_creation['releases'][0]['ocid']}-"
                      f"{ms_release_after_cn_creation['releases'][0]['id'][29:42]}",
                "date": CreateCn.message_from_kafka['data']['operationDate'],
                "tag": ["compiled"],
                "language": language,
                "initiationType": "tender",
                "planning": {
                    "budget": {
                        "description": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                            'description'],
                        "amount": {
                            "amount":
                                CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget']['amount'][
                                    'amount'],
                            "currency":
                                CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget']['amount'][
                                    'currency']
                        },
                        "isEuropeanUnionFunded":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                'isEuropeanUnionFunded'],
                        "budgetBreakdown": [{
                            "id": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                'budgetBreakdown'][0]['id'],
                            "description": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                'budgetBreakdown'][0]['description'],
                            "amount": {
                                "amount": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['amount']['amount'],
                                "currency": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['amount']['currency']
                            },
                            "period": {
                                "startDate":
                                    CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                        'budgetBreakdown'][0]['period']['startDate'],
                                "endDate": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['period']['endDate']
                            },
                            "sourceParty": {
                                "id": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['sourceParty']['id'],
                                "name": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['sourceParty']['name']
                            },
                            "europeanUnionFunding": {
                                "projectIdentifier":
                                    CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                        'budgetBreakdown'][0]['europeanUnionFunding']['projectIdentifier'],
                                "projectName":
                                    CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                        'budgetBreakdown'][0]['europeanUnionFunding']['projectName'],
                                "uri": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['europeanUnionFunding']['uri']
                            }
                        }]
                    },
                    "rationale": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['rationale']
                },
                "tender": {
                    "id": ev_release['releases'][0]['tender']['id'],
                    "title": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['title'],
                    "description": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['description'],
                    "status": ev_release['releases'][0]['tender']['status'],
                    "statusDetails": "evaluation",
                    "value": {
                        "amount": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['value']['amount'],
                        "currency": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['value']['currency']
                    },
                    "procurementMethod": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'procurementMethod'],
                    "procurementMethodDetails": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'procurementMethodDetails'],
                    "procurementMethodRationale": CreateCn.payload['tender']['procurementMethodRationale'],
                    "mainProcurementCategory": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'mainProcurementCategory'],
                    "hasEnquiries": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['hasEnquiries'],
                    "eligibilityCriteria": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'eligibilityCriteria'],
                    "contractPeriod": {
                        "startDate": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                            'contractPeriod']['startDate'],
                        "endDate": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                            'contractPeriod']['endDate']
                    },
                    "procuringEntity": {
                        "id": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['procuringEntity']['id'],
                        "name": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['procuringEntity'][
                            'name']
                    },
                    "acceleratedProcedure": {
                        "isAcceleratedProcedure":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['acceleratedProcedure'][
                                'isAcceleratedProcedure']
                    },
                    "classification": {
                        "scheme": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['classification'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['classification']['id'],
                        "description":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['classification'][
                                'description']
                    },
                    "designContest": {
                        "serviceContractAward":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['designContest'][
                                'serviceContractAward']
                    },
                    "electronicWorkflows": {
                        "useOrdering":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['electronicWorkflows'][
                                'useOrdering'],
                        "usePayment":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['electronicWorkflows'][
                                'usePayment'],
                        "acceptInvoicing":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['electronicWorkflows'][
                                'acceptInvoicing']
                    },
                    "jointProcurement": {
                        "isJointProcurement":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['jointProcurement'][
                                'isJointProcurement']
                    },
                    "legalBasis": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['legalBasis'],
                    "procedureOutsourcing": {
                        "procedureOutsourced":
                            CreateCn.ms_release_before_cn_creation["releases"][0]["tender"]["procedureOutsourcing"][
                                "procedureOutsourced"]
                    },
                    "procurementMethodAdditionalInfo": CreateCn.payload['tender']['procurementMethodAdditionalInfo'],
                    "dynamicPurchasingSystem": {
                        "hasDynamicPurchasingSystem":
                            CreateCn.ms_release_before_cn_creation["releases"][0]["tender"]["dynamicPurchasingSystem"][
                                "hasDynamicPurchasingSystem"]
                    },
                    "framework": {
                        "isAFramework": CreateCn.ms_release_before_cn_creation["releases"][0]["tender"]["framework"][
                            "isAFramework"]
                    }
                },
                "parties": [{
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['id'],
                    "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['name'],
                    "identifier": {
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['identifier'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['identifier']['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['identifier'][
                            'legalName'],
                        "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['identifier']['uri']
                    },
                    "address": {
                        "streetAddress": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                            'streetAddress'],
                        "postalCode": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                            'postalCode'],
                        "addressDetails": {
                            "country": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['country']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['country']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['country']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['region']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['region']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['region']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['locality']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['locality']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['locality']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "additionalIdentifiers": [{
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0][
                            'additionalIdentifiers'][0]['scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0][
                            'additionalIdentifiers'][0]['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0][
                            'additionalIdentifiers'][0]['legalName'],
                        "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0][
                            'additionalIdentifiers'][0]['uri']
                    }],
                    "contactPoint": {
                        "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                            'name'],
                        "email": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                            'email'],
                        "telephone":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                                'telephone'],
                        "faxNumber":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                                'faxNumber'],
                        "url": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                            'url']
                    },
                    "details": {
                        "typeOfBuyer": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['details'][
                            'typeOfBuyer'],
                        "mainGeneralActivity":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['details'][
                                'mainGeneralActivity'],
                        "mainSectoralActivity":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['details'][
                                'mainSectoralActivity']
                    },
                    "roles": ["buyer"]
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['id'],
                    "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['name'],
                    "identifier": {
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['identifier'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['identifier']['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['identifier'][
                            'legalName'],
                        "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['identifier']['uri']
                    },
                    "address": {
                        "streetAddress": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                            'streetAddress'],
                        "postalCode": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                            'postalCode'],
                        "addressDetails": {
                            "country": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['country']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['country']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['country']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['region']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['region']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['region']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['locality']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['locality']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['locality']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "additionalIdentifiers": [{
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1][
                            'additionalIdentifiers'][0]['scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1][
                            'additionalIdentifiers'][0]['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1][
                            'additionalIdentifiers'][0]['legalName'],
                        "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1][
                            'additionalIdentifiers'][0]['uri']
                    }],
                    "contactPoint": {
                        "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                            'name'],
                        "email": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                            'email'],
                        "telephone":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                                'telephone'],
                        "faxNumber":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                                'faxNumber'],
                        "url": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                            'url']
                    },
                    "roles": ["payer"]
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['id'],
                    "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['name'],
                    "identifier": {
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['identifier'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['identifier']['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['identifier'][
                            'legalName'],
                        "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['identifier']['uri']
                    },
                    "address": {
                        "streetAddress": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                            'streetAddress'],
                        "postalCode": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                            'postalCode'],
                        "addressDetails": {
                            "country": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['country']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['country']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['country']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['region']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['region']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['region']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['locality']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['locality']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['locality']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "additionalIdentifiers": [{
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2][
                            'additionalIdentifiers'][0]['scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2][
                            'additionalIdentifiers'][0]['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2][
                            'additionalIdentifiers'][0]['legalName'],
                        "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2][
                            'additionalIdentifiers'][0]['uri']
                    }],
                    "contactPoint": {
                        "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                            'name'],
                        "email": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                            'email'],
                        "telephone":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                                'telephone'],
                        "faxNumber":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                                'faxNumber'],
                        "url": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                            'url']
                    },
                    "roles": ["funder"]
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['id'],
                    "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['name'],
                    "identifier": {
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['identifier'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['identifier']['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['identifier'][
                            'legalName'],
                        "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['identifier']['uri']
                    },
                    "address": {
                        "streetAddress": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                            'streetAddress'],
                        "postalCode": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                            'postalCode'],
                        "addressDetails": {
                            "country": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                        'addressDetails']['country']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                    'addressDetails']['country']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                        'addressDetails']['country']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                    'addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                        'addressDetails']['region']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                    'addressDetails']['region']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                        'addressDetails']['region']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                    'addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                        'addressDetails']['locality']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                    'addressDetails']['locality']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                        'addressDetails']['locality']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['address'][
                                    'addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "additionalIdentifiers": [{
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3][
                            'additionalIdentifiers'][0]['scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3][
                            'additionalIdentifiers'][0]['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3][
                            'additionalIdentifiers'][0]['legalName'],
                        "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3][
                            'additionalIdentifiers'][0]['uri']
                    }],
                    "contactPoint": {
                        "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['contactPoint'][
                            'name'],
                        "email": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['contactPoint'][
                            'email'],
                        "telephone":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['contactPoint'][
                                'telephone'],
                        "faxNumber":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['contactPoint'][
                                'faxNumber'],
                        "url": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][3]['contactPoint'][
                            'url']
                    },
                    "persones": [{
                        "id": f"{CreateCn.payload['tender']['procuringEntity']['persones'][0]['identifier']['scheme']}"
                              f"-{CreateCn.payload['tender']['procuringEntity']['persones'][0]['identifier']['id']}",
                        "title": CreateCn.payload['tender']['procuringEntity']['persones'][0]['title'],
                        "name": CreateCn.payload['tender']['procuringEntity']['persones'][0]['name'],
                        "identifier": {
                            "scheme": CreateCn.payload['tender']['procuringEntity']['persones'][0]['identifier'][
                                'scheme'],
                            "id": CreateCn.payload['tender']['procuringEntity']['persones'][0]['identifier']['id'],
                            "uri": CreateCn.payload['tender']['procuringEntity']['persones'][0]['identifier']['uri']
                        },
                        "businessFunctions": [{
                            "id": CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0][
                                'id'],
                            "type":
                                CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0][
                                    'type'],
                            "jobTitle":
                                CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0][
                                    'jobTitle'],
                            "period": {
                                "startDate":
                                    CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][
                                        0]['period']['startDate']
                            },
                            "documents": [{
                                "id": CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][
                                    0]['documents'][0]['id'],
                                "documentType":
                                    CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][
                                        0]['documents'][0]['documentType'],
                                "title":
                                    CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][
                                        0]['documents'][0]['title'],
                                "description":
                                    CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][
                                        0]['documents'][0]['description'],
                                "url":
                                    f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                                    f"{persone_document}",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                            }]
                        }]
                    }],
                    "roles": ["procuringEntity"]
                }],
                "relatedProcesses": [{
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][0]['id'],
                    "relationship": ["planning"],
                    "scheme": "ocid",
                    "identifier": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][0][
                        'identifier'],
                    "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][0]['uri']
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][1]['id'],
                    "relationship": ["x_expenditureItem"],
                    "scheme": "ocid",
                    "identifier": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][1][
                        'identifier'],
                    "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][1]['uri']
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][2]['id'],
                    "relationship": ["x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][2][
                        'identifier'],
                    "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][2]['uri']
                }, {
                    "id": ms_release_after_cn_creation["releases"][0]['relatedProcesses'][3]['id'],
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id'],
                    "uri": f"http://dev.public.eprocurement.systems/tenders/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}/"
                           f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}"
                }]
            }]
        }
        compare_releases = DeepDiff(expected_result, actual_result)
        assert compare_actual_result_and_expected_result(
            expected_result=str({}),
            actual_result=str(compare_releases)
        )

    @pytestrail.case('27595')
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_pn_release_27595_5(
            self):
        pn_release_after_cn_creation = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.pn_id}").json()
        actual_result = DeepDiff(CreateCn.pn_release_before_cn_creation, pn_release_after_cn_creation)
        expected_result = str({
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{CreateCn.pn_id}-{pn_release_after_cn_creation['releases'][0]['id'][46:59]}",
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['id']
                },
                "root['releases'][0]['date']": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['date'],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['tag'][0],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['tender']['status'],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['tender']['statusDetails'],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['statusDetails']
                }
            }
        })
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckOnCorrectnessOfPublishingEvMsPnReleasesBasedOnPnObligatoryDataModelAndCnOnPnFullDataModel(object):
    @pytestrail.case("27596")
    def test_test_send_the_request_27596_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):

        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_two_was_uploaded = document.uploading_document()[0]["data"]["id"]
        document_three_was_uploaded = document.uploading_document()[0]["data"]["id"]
        payload = copy.deepcopy(create_cn_on_pn_payload_full_data_model_with_auction)
        payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0][
            'id'] = document_one_was_uploaded
        payload['tender']['criteria'][1]['requirementGroups'][0]['requirements'][1]['eligibleEvidences'][0][
            'relatedDocument']['id'] = document_three_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][0][
            'relatedDocument']['id'] = document_three_was_uploaded
        payload['tender']['criteria'][0]['requirementGroups'][0]['requirements'][0]['eligibleEvidences'][1][
            'relatedDocument']['id'] = document_three_was_uploaded
        payload['tender']['documents'][0]['id'] = document_one_was_uploaded
        payload['tender']['documents'][1]['id'] = document_two_was_uploaded
        payload['tender']['documents'][2]['id'] = document_three_was_uploaded

        cn = CN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = cn.insert_pn_obligatory_()
        CreateCn.ms_release_before_cn_creation = requests.get(url=create_pn_response[8]).json()
        CreateCn.pn_release_before_cn_creation = requests.get(url=create_pn_response[9]).json()
        create_cn_response = cn.create_cn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cn.get_message_from_kafka()

        CreateCn.message_from_kafka = cn.get_message_from_kafka()
        CreateCn.successfully_create_cn = cn.check_on_that_message_is_successfully_create_cn()
        CreateCn.payload = payload
        CreateCn.cp_id = create_pn_response[4]
        CreateCn.pn_id = create_pn_response[5]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_cn_response.status_code)
        )

    @pytestrail.case('27596')
    def test_see_result_from_feed_point_27596_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(CreateCn.successfully_create_cn)
        )

    @pytestrail.case('27596')
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_ev_release_27596_3(
            self, language, instance, pmd):
        ev_release = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}").json()
        get_value_by_first_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            CreateCn.payload['tender']['items'][0]['classification']['id'],
            language
        )
        get_value_by_second_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            CreateCn.payload['tender']['items'][1]['classification']['id'],
            language
        )
        get_value_by_first_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            CreateCn.payload['tender']['items'][0]['additionalClassifications'][0]['id'],
            language
        )
        get_value_by_second_item_cpvs_code = get_value_from_cpvs_dictionary_csv(
            CreateCn.payload['tender']['items'][1]['additionalClassifications'][0]['id'],
            language
        )
        get_value_by_first_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            CreateCn.payload['tender']['items'][0]['unit']['id'],
            language
        )
        get_value_by_second_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            CreateCn.payload['tender']['items'][1]['unit']['id'],
            language
        )
        mdm = MdmService(
            instance=instance,
            lang=language,
            pn_lot_address_details_country_id=CreateCn.payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['country']['id'],
            pn_lot_address_details_region_id=CreateCn.payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['region']['id'],
            pn_lot_address_details_locality_id=CreateCn.payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['id'],
            pn_lot_address_details_locality_scheme=CreateCn.payload["tender"]["lots"][0]['placeOfPerformance'][
                'address']['addressDetails']['locality']['scheme']
        )
        data = mdm.process_tender_data(pmd).json()
        first_lot_country_from_mdm = \
            data["data"]["tender"]["lots"][0]['placeOfPerformance']['address']['addressDetails']['country']
        first_lot_region_from_mdm = \
            data["data"]["tender"]["lots"][0]['placeOfPerformance']['address']['addressDetails']['region']
        first_lot_locality_from_mdm = \
            data["data"]["tender"]["lots"][0]['placeOfPerformance']['address']['addressDetails']['locality']
        second_lot_country_from_mdm = \
            data["data"]["tender"]["lots"][1]['placeOfPerformance']['address']['addressDetails']['country']
        second_lot_region_from_mdm = \
            data["data"]["tender"]["lots"][1]['placeOfPerformance']['address']['addressDetails']['region']
        second_lot_locality_from_mdm = \
            data["data"]["tender"]["lots"][1]['placeOfPerformance']['address']['addressDetails']['locality']
        actual_result = ev_release
        expected_result = {
            "uri": f"http://dev.public.eprocurement.systems/tenders/{CreateCn.message_from_kafka['data']['ocid']}/"
                   f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}",
            "version": "1.1",
            "extensions": [
                "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"],
            "publisher": {
                "name": "M-Tender",
                "uri": "https://www.mtender.gov.md"
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": CreateCn.message_from_kafka['data']['operationDate'],
            "releases": [{
                "ocid": CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id'],
                "id": f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}-"
                      f"{actual_result['releases'][0]['id'][46:59]}",
                "date": CreateCn.message_from_kafka['data']['operationDate'],
                "tag": ["tender"],
                "language": language,
                "initiationType": "tender",
                "tender": {
                    "id": actual_result['releases'][0]['tender']['id'],
                    "title": "Evaluation",
                    "description": "Evaluation stage of contracting process",
                    "status": "active",
                    "statusDetails": "clarification",
                    "criteria": [{
                        "id": actual_result['releases'][0]['tender']['criteria'][0]['id'],
                        "title": CreateCn.payload['tender']['criteria'][0]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][0]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][0]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][0]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "description": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                    'requirements'][0]['description'],
                                "eligibleEvidences": [{
                                    "id": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][0]['id'],
                                    "title": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][0]['title'],
                                    "type": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][0]['type'],
                                    "description": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][0]['description'],
                                    "relatedDocument": {
                                        "id": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                            'requirements'][0]['eligibleEvidences'][0]['relatedDocument']['id']
                                    }
                                }, {
                                    "id": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][1]['id'],
                                    "title": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][1]['title'],
                                    "type": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][1]['type'],
                                    "description": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                        'requirements'][0]['eligibleEvidences'][1]['description'],
                                    "relatedDocument": {
                                        "id": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                            'requirements'][0]['eligibleEvidences'][1]['relatedDocument']['id']
                                    }
                                }],
                                "expectedValue": CreateCn.payload['tender']['criteria'][0]['requirementGroups'][0][
                                    'requirements'][0]['expectedValue']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][0]['relatesTo'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][0]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][0]['classification']['id']
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['criteria'][1]['id'],
                        "title": CreateCn.payload['tender']['criteria'][1]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][1]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][1]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "description": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][0]['description'],
                                "expectedValue": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][0]['expectedValue']
                            }, {
                                "id": actual_result['releases'][0]['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['id'],
                                "title": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "description": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['description'],
                                "period": {
                                    "startDate": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['period']['startDate'],
                                    "endDate": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['period']['endDate']
                                },
                                "eligibleEvidences": [{
                                    "id": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['eligibleEvidences'][0]['id'],
                                    "title": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['eligibleEvidences'][0]['title'],
                                    "type": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['eligibleEvidences'][0]['type'],
                                    "description": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                        'requirements'][1]['eligibleEvidences'][0]['description'],
                                    "relatedDocument": {
                                        "id": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                            'requirements'][1]['eligibleEvidences'][0]['relatedDocument']['id']
                                    }
                                }],
                                "minValue": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['minValue'],
                                "maxValue": CreateCn.payload['tender']['criteria'][1]['requirementGroups'][0][
                                    'requirements'][1]['maxValue']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][1]['relatesTo'],
                        "relatedItem": actual_result['releases'][0]['tender']['criteria'][1]['relatedItem'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][1]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][1]['classification']['id']
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['criteria'][2]['id'],
                        "title": CreateCn.payload['tender']['criteria'][2]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][2]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "expectedValue": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][0]['expectedValue']
                            }, {
                                "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][1]['id'],
                                "title": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][1]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][0][
                                    'requirements'][1]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                            }]
                        }, {
                            "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][1]['id'],
                            "description": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "expectedValue": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][0]['expectedValue']
                            }, {
                                "id": actual_result['releases'][0]['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][1]['id'],
                                "title": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][1]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][2]['requirementGroups'][1][
                                    'requirements'][1]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][2]['relatesTo'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][2]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][2]['classification']['id']
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['criteria'][3]['id'],
                        "title": CreateCn.payload['tender']['criteria'][3]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][3]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][3]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][3]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                                "period": {
                                    "startDate": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                        'requirements'][0]['period']['startDate'],
                                    "endDate": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                        'requirements'][0]['period']['endDate']
                                },
                                "minValue": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                    'requirements'][0]['minValue'],
                                "maxValue": CreateCn.payload['tender']['criteria'][3]['requirementGroups'][0][
                                    'requirements'][0]['maxValue']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][3]['relatesTo'],
                        "relatedItem": actual_result['releases'][0]['tender']['criteria'][3]['relatedItem'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][3]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][3]['classification']['id']
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['criteria'][4]['id'],
                        "title": CreateCn.payload['tender']['criteria'][4]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][4]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][4]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][4]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][4]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][4]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][4]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][4]['relatesTo'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][4]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][4]['classification']['id']
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['criteria'][5]['id'],
                        "title": CreateCn.payload['tender']['criteria'][5]['title'],
                        "source": "tenderer",
                        "description": CreateCn.payload['tender']['criteria'][5]['description'],
                        "requirementGroups": [{
                            "id": actual_result['releases'][0]['tender']['criteria'][5]['requirementGroups'][0]['id'],
                            "description": CreateCn.payload['tender']['criteria'][5]['requirementGroups'][0][
                                'description'],
                            "requirements": [{
                                "id": actual_result['releases'][0]['tender']['criteria'][5]['requirementGroups'][0][
                                    'requirements'][0]['id'],
                                "title": CreateCn.payload['tender']['criteria'][5]['requirementGroups'][0][
                                    'requirements'][0]['title'],
                                "dataType": CreateCn.payload['tender']['criteria'][5]['requirementGroups'][0][
                                    'requirements'][0]['dataType'],
                                "status": "active",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                            }]
                        }],
                        "relatesTo": CreateCn.payload['tender']['criteria'][5]['relatesTo'],
                        "classification": {
                            "scheme": CreateCn.payload['tender']['criteria'][5]['classification']['scheme'],
                            "id": CreateCn.payload['tender']['criteria'][5]['classification']['id']
                        }
                    }],
                    "conversions": [{
                        "id": actual_result['releases'][0]['tender']['conversions'][0]['id'],
                        "relatesTo": "requirement",
                        "relatedItem": actual_result['releases'][0]['tender']['conversions'][0]['relatedItem'],
                        "rationale": CreateCn.payload['tender']['conversions'][0]['rationale'],
                        "description": CreateCn.payload['tender']['conversions'][0]['description'],
                        "coefficients": [{
                            "id": actual_result['releases'][0]['tender']['conversions'][0]['coefficients'][0]['id'],
                            "value": CreateCn.payload['tender']['conversions'][0]['coefficients'][0]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][0]['coefficients'][0][
                                'coefficient']
                        }]
                    }, {
                        "id": actual_result['releases'][0]['tender']['conversions'][1]['id'],
                        "relatesTo": "requirement",
                        "relatedItem": actual_result['releases'][0]['tender']['conversions'][1]['relatedItem'],
                        "rationale": CreateCn.payload['tender']['conversions'][1]['rationale'],
                        "description": CreateCn.payload['tender']['conversions'][1]['description'],
                        "coefficients": [{
                            "id": actual_result['releases'][0]['tender']['conversions'][1]['coefficients'][0]['id'],
                            "value": CreateCn.payload['tender']['conversions'][1]['coefficients'][0]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][1]['coefficients'][0][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][1]['coefficients'][1]['id'],
                            "value": CreateCn.payload['tender']['conversions'][1]['coefficients'][1]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][1]['coefficients'][1][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][1]['coefficients'][2]['id'],
                            "value": CreateCn.payload['tender']['conversions'][1]['coefficients'][2]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][1]['coefficients'][2][
                                'coefficient']
                        }]
                    }, {
                        "id": actual_result['releases'][0]['tender']['conversions'][2]['id'],
                        "relatesTo": "requirement",
                        "relatedItem": actual_result['releases'][0]['tender']['conversions'][2]['relatedItem'],
                        "rationale": CreateCn.payload['tender']['conversions'][2]['rationale'],
                        "description": CreateCn.payload['tender']['conversions'][2]['description'],
                        "coefficients": [{
                            "id": actual_result['releases'][0]['tender']['conversions'][2]['coefficients'][0]['id'],
                            "value": CreateCn.payload['tender']['conversions'][2]['coefficients'][0]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][2]['coefficients'][0][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][2]['coefficients'][1]['id'],
                            "value": CreateCn.payload['tender']['conversions'][2]['coefficients'][1]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][2]['coefficients'][1][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][2]['coefficients'][2]['id'],
                            "value": CreateCn.payload['tender']['conversions'][2]['coefficients'][2]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][2]['coefficients'][2][
                                'coefficient']
                        }]
                    }, {
                        "id": actual_result['releases'][0]['tender']['conversions'][3]['id'],
                        "relatesTo": "requirement",
                        "relatedItem": actual_result['releases'][0]['tender']['conversions'][3]['relatedItem'],
                        "rationale": CreateCn.payload['tender']['conversions'][3]['rationale'],
                        "description": CreateCn.payload['tender']['conversions'][3]['description'],
                        "coefficients": [{
                            "id": actual_result['releases'][0]['tender']['conversions'][3]['coefficients'][0]['id'],
                            "value": CreateCn.payload['tender']['conversions'][3]['coefficients'][0]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][3]['coefficients'][0][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][3]['coefficients'][1]['id'],
                            "value": CreateCn.payload['tender']['conversions'][3]['coefficients'][1]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][3]['coefficients'][1][
                                'coefficient']
                        }, {
                            "id": actual_result['releases'][0]['tender']['conversions'][3]['coefficients'][2]['id'],
                            "value": CreateCn.payload['tender']['conversions'][3]['coefficients'][2]['value'],
                            "coefficient": CreateCn.payload['tender']['conversions'][3]['coefficients'][2][
                                'coefficient']
                        }]
                    }],
                    "items": [{
                        "id": actual_result['releases'][0]['tender']['items'][0]['id'],
                        "internalId": CreateCn.payload['tender']['items'][0]['internalId'],
                        "description": CreateCn.payload['tender']['items'][0]['description'],
                        "classification": {
                            "scheme": "CPV",
                            "id": get_value_by_first_item_cpv_code[0],
                            "description": get_value_by_first_item_cpv_code[1]
                        },
                        "additionalClassifications": [{
                            "scheme": "CPVS",
                            "id": get_value_by_first_item_cpvs_code[0],
                            "description": get_value_by_first_item_cpvs_code[2]
                        }],
                        "quantity": CreateCn.payload['tender']['items'][0]['quantity'],
                        "unit": {
                            "name": get_value_by_first_item_unit_id[1],
                            "id": get_value_by_first_item_unit_id[0]
                        },
                        "relatedLot": actual_result['releases'][0]['tender']['lots'][0]['id']
                    }, {
                        "id": actual_result['releases'][0]['tender']['items'][1]['id'],
                        "internalId": CreateCn.payload['tender']['items'][1]['internalId'],
                        "description": CreateCn.payload['tender']['items'][1]['description'],
                        "classification": {
                            "scheme": "CPV",
                            "id": get_value_by_second_item_cpv_code[0],
                            "description": get_value_by_second_item_cpv_code[1]
                        },
                        "additionalClassifications": [{
                            "scheme": "CPVS",
                            "id": get_value_by_second_item_cpvs_code[0],
                            "description": get_value_by_second_item_cpvs_code[2]
                        }],
                        "quantity": CreateCn.payload['tender']['items'][1]['quantity'],
                        "unit": {
                            "name": get_value_by_second_item_unit_id[1],
                            "id": get_value_by_second_item_unit_id[0]
                        },
                        "relatedLot": actual_result['releases'][0]['tender']['lots'][1]['id']
                    }],
                    "lots": [{
                        "id": actual_result['releases'][0]['tender']['lots'][0]['id'],
                        "internalId": CreateCn.payload['tender']['lots'][0]['internalId'],
                        "title": CreateCn.payload['tender']['lots'][0]['title'],
                        "description": CreateCn.payload['tender']['lots'][0]['description'],
                        "status": "active",
                        "statusDetails": "empty",
                        "value": {
                            "amount": CreateCn.payload['tender']['lots'][0]['value']['amount'],
                            "currency": CreateCn.payload['tender']['lots'][0]['value']['currency']
                        },
                        "contractPeriod": {
                            "startDate": CreateCn.payload['tender']['lots'][0]['contractPeriod'][
                                'startDate'],
                            "endDate": CreateCn.payload['tender']['lots'][0]['contractPeriod'][
                                'endDate']
                        },
                        "placeOfPerformance": {
                            "address": {
                                "streetAddress":
                                    CreateCn.payload['tender']['lots'][0]['placeOfPerformance'][
                                        'address']['streetAddress'],
                                "postalCode":
                                    CreateCn.payload['tender']['lots'][0]['placeOfPerformance'][
                                        'address']['postalCode'],
                                "addressDetails": {
                                    "country": {
                                        "scheme": first_lot_country_from_mdm['scheme'],
                                        "id": CreateCn.payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                            'addressDetails']['country']['id'],
                                        "description": first_lot_country_from_mdm['description'],
                                        "uri": first_lot_country_from_mdm['uri']
                                    },
                                    "region": {
                                        "scheme": first_lot_region_from_mdm['scheme'],
                                        "id": CreateCn.payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                            'addressDetails']['region']['id'],
                                        "description": first_lot_region_from_mdm['description'],
                                        "uri": first_lot_region_from_mdm['uri']
                                    },
                                    "locality": {
                                        "scheme":
                                            CreateCn.payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                                'addressDetails']['locality']['scheme'],
                                        "id": CreateCn.payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                            'addressDetails']['locality']['id'],
                                        "description": first_lot_locality_from_mdm['description'],
                                        "uri": first_lot_locality_from_mdm['uri']
                                    }
                                    }
                            },
                            "description": CreateCn.payload['tender']['lots'][0]['placeOfPerformance']['description']
                        },
                        "hasOptions": CreateCn.payload['tender']['lots'][0]['hasOptions'],
                        "options": [{
                            "description": CreateCn.payload['tender']['lots'][0]['options'][0]['description'],
                            "period": {
                                "startDate": CreateCn.payload['tender']['lots'][0]['options'][0]['period']['startDate'],
                                "endDate": CreateCn.payload['tender']['lots'][0]['options'][0]['period']['endDate'],
                                "maxExtentDate": CreateCn.payload['tender']['lots'][0]['options'][0]['period'][
                                    'maxExtentDate'],
                                "durationInDays": CreateCn.payload['tender']['lots'][0]['options'][0]['period'][
                                    'durationInDays']
                            }
                        }],
                        "hasRecurrence": CreateCn.payload['tender']['lots'][0]['hasRecurrence'],
                        "recurrence": {
                            "description": CreateCn.payload['tender']['lots'][0]['recurrence']['description'],
                            "dates": [{
                                "startDate": CreateCn.payload['tender']['lots'][0]['recurrence']['dates'][0][
                                    'startDate']
                            }, {
                                "startDate": CreateCn.payload['tender']['lots'][0]['recurrence']['dates'][0][
                                    'startDate']
                            }]
                        },
                        "hasRenewal": CreateCn.payload['tender']['lots'][0]['hasRenewal'],
                        "renewal": {
                            "description": CreateCn.payload['tender']['lots'][0]['renewal']['description'],
                            "minimumRenewals": CreateCn.payload['tender']['lots'][0]['renewal']['minimumRenewals'],
                            "maximumRenewals": CreateCn.payload['tender']['lots'][0]['renewal']['maximumRenewals'],
                            "period": {
                                "startDate": CreateCn.payload['tender']['lots'][0]['renewal']['period']['startDate'],
                                "endDate": CreateCn.payload['tender']['lots'][0]['renewal']['period']['endDate'],
                                "maxExtentDate": CreateCn.payload['tender']['lots'][0]['renewal']['period'][
                                    'maxExtentDate'],
                                "durationInDays": CreateCn.payload['tender']['lots'][0]['renewal']['period'][
                                    'durationInDays']
                            }
                        }
                    }, {
                        "id": actual_result['releases'][0]['tender']['lots'][1]['id'],
                        "internalId": CreateCn.payload['tender']['lots'][1]['internalId'],
                        "title": CreateCn.payload['tender']['lots'][1]['title'],
                        "description": CreateCn.payload['tender']['lots'][1]['description'],
                        "status": "active",
                        "statusDetails": "empty",
                        "value": {
                            "amount": CreateCn.payload['tender']['lots'][1]['value']['amount'],
                            "currency": CreateCn.payload['tender']['lots'][1]['value']['currency']
                        },
                        "contractPeriod": {
                            "startDate": CreateCn.payload['tender']['lots'][1]['contractPeriod'][
                                'startDate'],
                            "endDate": CreateCn.payload['tender']['lots'][1]['contractPeriod'][
                                'endDate']
                        },
                        "placeOfPerformance": {
                            "address": {
                                "streetAddress":
                                    CreateCn.payload['tender']['lots'][1]['placeOfPerformance'][
                                        'address']['streetAddress'],
                                "postalCode":
                                    CreateCn.payload['tender']['lots'][1]['placeOfPerformance'][
                                        'address']['postalCode'],
                                "addressDetails": {
                                    "country": {
                                        "scheme": second_lot_country_from_mdm['scheme'],
                                        "id": CreateCn.payload['tender']['lots'][1]['placeOfPerformance']['address'][
                                            'addressDetails']['country']['id'],
                                        "description": second_lot_country_from_mdm['description'],
                                        "uri": second_lot_country_from_mdm['uri']
                                    },
                                    "region": {
                                        "scheme": second_lot_region_from_mdm['scheme'],
                                        "id": CreateCn.payload['tender']['lots'][1]['placeOfPerformance']['address'][
                                            'addressDetails']['region']['id'],
                                        "description": second_lot_region_from_mdm['description'],
                                        "uri": second_lot_region_from_mdm['uri']
                                    },
                                    "locality": {
                                        "scheme":
                                            CreateCn.payload['tender']['lots'][1]['placeOfPerformance']['address'][
                                                'addressDetails']['locality']['scheme'],
                                        "id": CreateCn.payload['tender']['lots'][1]['placeOfPerformance']['address'][
                                            'addressDetails']['locality']['id'],
                                        "description": second_lot_locality_from_mdm['description'],
                                        "uri": second_lot_locality_from_mdm['uri']
                                    }
                                    }
                            },
                            "description": CreateCn.payload['tender']['lots'][1]['placeOfPerformance']['description']
                        },
                        "hasOptions": CreateCn.payload['tender']['lots'][1]['hasOptions'],
                        "options": [{
                            "description": CreateCn.payload['tender']['lots'][1]['options'][0]['description'],
                            "period": {
                                "startDate": CreateCn.payload['tender']['lots'][1]['options'][0]['period']['startDate'],
                                "endDate": CreateCn.payload['tender']['lots'][1]['options'][0]['period']['endDate'],
                                "maxExtentDate": CreateCn.payload['tender']['lots'][1]['options'][0]['period'][
                                    'maxExtentDate'],
                                "durationInDays": CreateCn.payload['tender']['lots'][1]['options'][0]['period'][
                                    'durationInDays']
                            }
                        }],
                        "hasRecurrence": CreateCn.payload['tender']['lots'][1]['hasRecurrence'],
                        "recurrence": {
                            "description": CreateCn.payload['tender']['lots'][1]['recurrence']['description'],
                            "dates": [{
                                "startDate": CreateCn.payload['tender']['lots'][1]['recurrence']['dates'][0][
                                    'startDate']
                            }, {
                                "startDate": CreateCn.payload['tender']['lots'][1]['recurrence']['dates'][0][
                                    'startDate']
                            }]
                        },
                        "hasRenewal": CreateCn.payload['tender']['lots'][1]['hasRenewal'],
                        "renewal": {
                            "description": CreateCn.payload['tender']['lots'][1]['renewal']['description'],
                            "minimumRenewals": CreateCn.payload['tender']['lots'][1]['renewal']['minimumRenewals'],
                            "maximumRenewals": CreateCn.payload['tender']['lots'][1]['renewal']['maximumRenewals'],
                            "period": {
                                "startDate": CreateCn.payload['tender']['lots'][1]['renewal']['period']['startDate'],
                                "endDate": CreateCn.payload['tender']['lots'][1]['renewal']['period']['endDate'],
                                "maxExtentDate": CreateCn.payload['tender']['lots'][1]['renewal']['period'][
                                    'maxExtentDate'],
                                "durationInDays": CreateCn.payload['tender']['lots'][1]['renewal']['period'][
                                    'durationInDays']
                            }
                        }
                    }],
                    "lotGroups": [{
                        "optionToCombine": False
                    }],
                    "tenderPeriod": {
                        "startDate": CreateCn.payload['tender']['enquiryPeriod']['endDate'],
                        "endDate": CreateCn.payload['tender']['tenderPeriod']['endDate']
                    },
                    "enquiryPeriod": {
                        "startDate": CreateCn.message_from_kafka['data']['operationDate'],
                        "endDate": CreateCn.payload['tender']['enquiryPeriod']['endDate']
                    },
                    "auctionPeriod": {
                        "startDate": actual_result['releases'][0]['tender']['auctionPeriod']['startDate']
                    },
                    "hasEnquiries": False,
                    "documents": [{
                        "id": CreateCn.payload['tender']['documents'][0]['id'],
                        "documentType": CreateCn.payload['tender']['documents'][0]['documentType'],
                        "title": CreateCn.payload['tender']['documents'][0]['title'],
                        "description": CreateCn.payload['tender']['documents'][0]['description'],
                        "url": f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                               f"{CreateCn.payload['tender']['documents'][0]['id']}",
                        "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                        "relatedLots": actual_result['releases'][0]['tender']['documents'][0]['relatedLots']
                    }, {
                        "id": CreateCn.payload['tender']['documents'][1]['id'],
                        "documentType": CreateCn.payload['tender']['documents'][1]['documentType'],
                        "title": CreateCn.payload['tender']['documents'][1]['title'],
                        "description": CreateCn.payload['tender']['documents'][1]['description'],
                        "url": f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                               f"{CreateCn.payload['tender']['documents'][1]['id']}",
                        "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                        "relatedLots": actual_result['releases'][0]['tender']['documents'][1]['relatedLots']
                    }, {
                        "id": CreateCn.payload['tender']['documents'][2]['id'],
                        "documentType": CreateCn.payload['tender']['documents'][2]['documentType'],
                        "title": CreateCn.payload['tender']['documents'][2]['title'],
                        "description": CreateCn.payload['tender']['documents'][2]['description'],
                        "url": f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                               f"{CreateCn.payload['tender']['documents'][2]['id']}",
                        "datePublished": CreateCn.message_from_kafka['data']['operationDate'],
                        "relatedLots": actual_result['releases'][0]['tender']['documents'][2]['relatedLots']
                    }],
                    "awardCriteria": CreateCn.payload['tender']['awardCriteria'],
                    "awardCriteriaDetails": CreateCn.payload['tender']['awardCriteriaDetails'],
                    "submissionMethod": ["electronicSubmission"],
                    "submissionMethodDetails": CreateCn.pn_release_before_cn_creation['releases'][0]['tender'][
                        'submissionMethodDetails'],
                    "submissionMethodRationale": CreateCn.pn_release_before_cn_creation['releases'][0]['tender'][
                        'submissionMethodRationale'],
                    "requiresElectronicCatalogue": CreateCn.pn_release_before_cn_creation['releases'][0]['tender'][
                        'requiresElectronicCatalogue'],
                    "procurementMethodModalities": CreateCn.payload['tender']['procurementMethodModalities'],
                    "electronicAuctions": {
                        "details": [{
                            "id": actual_result['releases'][0]['tender']['electronicAuctions']['details'][0]['id'],
                            "relatedLot": actual_result['releases'][0]['tender']['lots'][0]['id'],
                            "auctionPeriod": {
                                "startDate": actual_result['releases'][0]['tender']['electronicAuctions']['details'][0][
                                    'auctionPeriod']['startDate']
                            },
                            "electronicAuctionModalities": [{
                                "url": f"http://auction.eprocurement.systems/auctions/"
                                       f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}/"
                                       f"{actual_result['releases'][0]['tender']['lots'][0]['id']}",
                                "eligibleMinimumDifference": {
                                    "amount": CreateCn.payload['tender']['electronicAuctions']['details'][0][
                                        'electronicAuctionModalities'][0]['eligibleMinimumDifference']['amount'],
                                    "currency": CreateCn.payload['tender']['electronicAuctions']['details'][0][
                                        'electronicAuctionModalities'][0]['eligibleMinimumDifference']['currency']
                                }
                            }]
                        }, {
                            "id": actual_result['releases'][0]['tender']['electronicAuctions']['details'][1]['id'],
                            "relatedLot": actual_result['releases'][0]['tender']['lots'][1]['id'],
                            "auctionPeriod": {
                                "startDate": actual_result['releases'][0]['tender']['electronicAuctions']['details'][1][
                                    'auctionPeriod']['startDate']
                            },
                            "electronicAuctionModalities": [{
                                "url": f"http://auction.eprocurement.systems/auctions/"
                                       f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}/"
                                       f"{actual_result['releases'][0]['tender']['lots'][1]['id']}",
                                "eligibleMinimumDifference": {
                                    "amount": CreateCn.payload['tender']['electronicAuctions']['details'][1][
                                        'electronicAuctionModalities'][0]['eligibleMinimumDifference']['amount'],
                                    "currency": CreateCn.payload['tender']['electronicAuctions']['details'][1][
                                        'electronicAuctionModalities'][0]['eligibleMinimumDifference']['currency']
                                }
                            }]
                        }]
                    },
                    "procurementMethodRationale": CreateCn.payload['tender']['procurementMethodRationale']
                },
                "hasPreviousNotice": True,
                "purposeOfNotice": {
                    "isACallForCompetition": True
                },
                "relatedProcesses": [{
                    "id": actual_result['releases'][0]['relatedProcesses'][0]['id'],
                    "relationship": ["parent"],
                    "scheme": "ocid",
                    "identifier": CreateCn.message_from_kafka['data']['ocid'],
                    "uri": f"http://dev.public.eprocurement.systems/tenders/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}"
                }, {
                    "id": actual_result['releases'][0]['relatedProcesses'][1]['id'],
                    "relationship": ["planning"],
                    "scheme": "ocid",
                    "identifier": CreateCn.pn_id,
                    "uri": f"http://dev.public.eprocurement.systems/tenders/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}/"
                           f"{CreateCn.pn_id}"
                }]
            }]
        }
        compare_releases = DeepDiff(expected_result, actual_result)
        assert compare_actual_result_and_expected_result(
            expected_result=str({}),
            actual_result=str(compare_releases)
        )

    @pytestrail.case('27596')
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_ms_release_27596_4(
            self, language):
        ev_release = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}").json()
        ms_release_after_cn_creation = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.message_from_kafka['data']['ocid']}").json()
        if CreateCn.payload['tender']['lots'][0]['contractPeriod']['startDate'] <= \
                CreateCn.payload['tender']['lots'][1]['contractPeriod']['startDate']:
            start_date = CreateCn.payload['tender']['lots'][0]['contractPeriod']['startDate']
        elif CreateCn.payload['tender']['lots'][0]['contractPeriod']['startDate'] >= \
                CreateCn.payload['tender']['lots'][1]['contractPeriod']['startDate']:
            start_date = CreateCn.payload['tender']['lots'][1]['contractPeriod']['startDate']
        else:
            raise Exception("Can not get startDate for tender.contractPeriod")

        if CreateCn.payload['tender']['lots'][0]['contractPeriod']['endDate'] <= \
                CreateCn.payload['tender']['lots'][1]['contractPeriod']['endDate']:
            end_date = CreateCn.payload['tender']['lots'][1]['contractPeriod']['endDate']
        elif CreateCn.payload['tender']['lots'][0]['contractPeriod']['endDate'] >= \
                CreateCn.payload['tender']['lots'][1]['contractPeriod']['endDate']:
            end_date = CreateCn.payload['tender']['lots'][0]['contractPeriod']['endDate']
        else:
            raise Exception("Can not get endDate for tender.contractPeriod")

        classification_first_item = CreateCn.payload['tender']['items'][0]['classification']['id']
        classification_second_item = CreateCn.payload['tender']['items'][1]['classification']['id']
        make_tender_classification_id = get_new_classification_id(classification_first_item, classification_second_item)
        get_value_by_classification_id = get_value_from_classification_cpv_dictionary_xls(
            cpv=make_tender_classification_id,
            language=language.upper()
        )
        tender_value_amount = CreateCn.payload['tender']['lots'][0]['value']['amount'] + CreateCn.payload[
            'tender']['lots'][1]['value']['amount']
        persone_document = \
            CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]['documents'][0]['id']
        actual_result = ms_release_after_cn_creation

        expected_result = {
            "uri": CreateCn.ms_release_before_cn_creation['uri'],
            "version": CreateCn.ms_release_before_cn_creation['version'],
            "extensions": [
                CreateCn.ms_release_before_cn_creation['extensions'][0],
                CreateCn.ms_release_before_cn_creation['extensions'][1]],
            "publisher": {
                "name": CreateCn.ms_release_before_cn_creation['publisher']['name'],
                "uri": CreateCn.ms_release_before_cn_creation['publisher']['uri']
            },
            "license": CreateCn.ms_release_before_cn_creation['license'],
            "publicationPolicy": CreateCn.ms_release_before_cn_creation['publicationPolicy'],
            "publishedDate": CreateCn.ms_release_before_cn_creation['releases'][0]['date'],
            "releases": [{
                "ocid": CreateCn.ms_release_before_cn_creation['releases'][0]['ocid'],
                "id": f"{CreateCn.ms_release_before_cn_creation['releases'][0]['ocid']}-"
                      f"{ms_release_after_cn_creation['releases'][0]['id'][29:42]}",
                "date": CreateCn.message_from_kafka['data']['operationDate'],
                "tag": ["compiled"],
                "language": language,
                "initiationType": "tender",
                "planning": {
                    "budget": {
                        "amount": {
                            "amount":
                                CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget']['amount'][
                                    'amount'],
                            "currency":
                                CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget']['amount'][
                                    'currency']
                        },
                        "isEuropeanUnionFunded":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                'isEuropeanUnionFunded'],
                        "budgetBreakdown": [{
                            "id": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                'budgetBreakdown'][0]['id'],
                            "amount": {
                                "amount": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['amount']['amount'],
                                "currency": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['amount']['currency']
                            },
                            "period": {
                                "startDate":
                                    CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                        'budgetBreakdown'][0]['period']['startDate'],
                                "endDate": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['period']['endDate']
                            },
                            "sourceParty": {
                                "id": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['sourceParty']['id'],
                                "name": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['sourceParty']['name']
                            }
                        }]
                    }
                },
                "tender": {
                    "id": ev_release['releases'][0]['tender']['id'],
                    "title": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['title'],
                    "description": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['description'],
                    "status": ev_release['releases'][0]['tender']['status'],
                    "statusDetails": "evaluation",
                    "value": {
                        "amount": tender_value_amount,
                        "currency": CreateCn.payload['tender']['lots'][0]['value']['currency']
                    },
                    "procurementMethod": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'procurementMethod'],
                    "procurementMethodDetails": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'procurementMethodDetails'],
                    "procurementMethodRationale": CreateCn.payload['tender']['procurementMethodRationale'],
                    "mainProcurementCategory": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'mainProcurementCategory'],
                    "hasEnquiries": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['hasEnquiries'],
                    "eligibilityCriteria": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'eligibilityCriteria'],
                    "contractPeriod": {
                        "startDate": start_date,
                        "endDate": end_date
                    },
                    "procuringEntity": {
                        "id": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['procuringEntity']['id'],
                        "name": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['procuringEntity'][
                            'name']
                    },
                    "acceleratedProcedure": {
                        "isAcceleratedProcedure":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['acceleratedProcedure'][
                                'isAcceleratedProcedure']
                    },
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_classification_id[0],
                        "description":
                            get_value_by_classification_id[1]
                    },
                    "designContest": {
                        "serviceContractAward":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['designContest'][
                                'serviceContractAward']
                    },
                    "electronicWorkflows": {
                        "useOrdering":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['electronicWorkflows'][
                                'useOrdering'],
                        "usePayment":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['electronicWorkflows'][
                                'usePayment'],
                        "acceptInvoicing":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['electronicWorkflows'][
                                'acceptInvoicing']
                    },
                    "jointProcurement": {
                        "isJointProcurement":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['jointProcurement'][
                                'isJointProcurement']
                    },
                    "legalBasis": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['legalBasis'],
                    "procedureOutsourcing": {
                        "procedureOutsourced":
                            CreateCn.ms_release_before_cn_creation["releases"][0]["tender"]["procedureOutsourcing"][
                                "procedureOutsourced"]
                    },
                    "procurementMethodAdditionalInfo": CreateCn.payload['tender']['procurementMethodAdditionalInfo'],
                    "dynamicPurchasingSystem": {
                        "hasDynamicPurchasingSystem":
                            CreateCn.ms_release_before_cn_creation["releases"][0]["tender"]["dynamicPurchasingSystem"][
                                "hasDynamicPurchasingSystem"]
                    },
                    "framework": {
                        "isAFramework": CreateCn.ms_release_before_cn_creation["releases"][0]["tender"]["framework"][
                            "isAFramework"]
                    }
                },
                "parties": [{
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['id'],
                    "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['name'],
                    "identifier": {
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['identifier'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['identifier']['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['identifier'][
                            'legalName']
                    },
                    "address": {
                        "streetAddress": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                            'streetAddress'],
                        "addressDetails": {
                            "country": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['country']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['country']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['country']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['region']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['region']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['region']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['locality']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['locality']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['locality']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "contactPoint": {
                        "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                            'name'],
                        "email": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                            'email'],
                        "telephone":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                                'telephone']
                    },
                    "roles": ["buyer"]
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['id'],
                    "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['name'],
                    "identifier": {
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['identifier'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['identifier']['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['identifier'][
                            'legalName']
                    },
                    "address": {
                        "streetAddress": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                            'streetAddress'],
                        "addressDetails": {
                            "country": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['country']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['country']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['country']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['region']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['region']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['region']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['locality']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['locality']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['locality']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "contactPoint": {
                        "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                            'name'],
                        "email": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                            'email'],
                        "telephone":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                                'telephone']
                    },
                    "roles": ["payer"]
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['id'],
                    "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['name'],
                    "identifier": {
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['identifier'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['identifier']['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['identifier'][
                            'legalName']
                    },
                    "address": {
                        "streetAddress": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                            'streetAddress'],
                        "addressDetails": {
                            "country": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['country']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['country']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['country']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['region']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['region']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['region']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['locality']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['locality']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['locality']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "contactPoint": {
                        "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                            'name'],
                        "email": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                            'email'],
                        "telephone":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                                'telephone']
                    },
                    "persones": [{
                        "id": f"{CreateCn.payload['tender']['procuringEntity']['persones'][0]['identifier']['scheme']}"
                              f"-{CreateCn.payload['tender']['procuringEntity']['persones'][0]['identifier']['id']}",
                        "title": CreateCn.payload['tender']['procuringEntity']['persones'][0]['title'],
                        "name": CreateCn.payload['tender']['procuringEntity']['persones'][0]['name'],
                        "identifier": {
                            "scheme": CreateCn.payload['tender']['procuringEntity']['persones'][0]['identifier'][
                                'scheme'],
                            "id": CreateCn.payload['tender']['procuringEntity']['persones'][0]['identifier']['id'],
                            "uri": CreateCn.payload['tender']['procuringEntity']['persones'][0]['identifier']['uri']
                        },
                        "businessFunctions": [{
                            "id": CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0][
                                'id'],
                            "type":
                                CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0][
                                    'type'],
                            "jobTitle":
                                CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0][
                                    'jobTitle'],
                            "period": {
                                "startDate":
                                    CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][
                                        0]['period']['startDate']
                            },
                            "documents": [{
                                "id": CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][
                                    0]['documents'][0]['id'],
                                "documentType":
                                    CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][
                                        0]['documents'][0]['documentType'],
                                "title":
                                    CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][
                                        0]['documents'][0]['title'],
                                "description":
                                    CreateCn.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][
                                        0]['documents'][0]['description'],
                                "url":
                                    f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                                    f"{persone_document}",
                                "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                            }]
                        }]
                    }],
                    "roles": ["procuringEntity"]
                }],
                "relatedProcesses": [{
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][0]['id'],
                    "relationship": ["planning"],
                    "scheme": "ocid",
                    "identifier": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][0][
                        'identifier'],
                    "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][0]['uri']
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][1]['id'],
                    "relationship": ["x_expenditureItem"],
                    "scheme": "ocid",
                    "identifier": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][1][
                        'identifier'],
                    "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][1]['uri']
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][2]['id'],
                    "relationship": ["x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][2][
                        'identifier'],
                    "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][2]['uri']
                }, {
                    "id": ms_release_after_cn_creation["releases"][0]['relatedProcesses'][3]['id'],
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id'],
                    "uri": f"http://dev.public.eprocurement.systems/tenders/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}/"
                           f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}"
                }]
            }]
        }
        compare_releases = DeepDiff(expected_result, actual_result)
        assert compare_actual_result_and_expected_result(
            expected_result=str({}),
            actual_result=str(compare_releases)
        )

    @pytestrail.case('27596')
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_pn_release_27596_5(
            self):
        pn_release_after_cn_creation = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.pn_id}").json()
        actual_result = DeepDiff(CreateCn.pn_release_before_cn_creation, pn_release_after_cn_creation)
        expected_result = str({
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{CreateCn.pn_id}-{pn_release_after_cn_creation['releases'][0]['id'][46:59]}",
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['id']
                },
                "root['releases'][0]['date']": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['date'],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['tag'][0],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['tender']['status'],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['tender']['statusDetails'],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['statusDetails']
                }
            }
        })
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )


class TestCheckOnCorrectnessOfPublishingEvMsPnReleasesBasedOnPnObligatoryDataModelAndCnOnPnObligatoryDataModel(object):
    @pytestrail.case("27597")
    def test_test_send_the_request_27597_1(self, country, language, instance, cassandra_username, cassandra_password,
                                           pmd):
        document = Document(instance=instance)
        document_one_was_uploaded = document.uploading_document()[0]["data"]["id"]

        payload = copy.deepcopy(create_cn_on_pn_payload_obligatory_data_model)

        payload['tender']['documents'][0]['id'] = document_one_was_uploaded

        cn = CN(
            payload=payload,
            lang=language,
            country=country,
            instance=instance,
            cassandra_username=cassandra_username,
            cassandra_password=cassandra_password,
            pmd=pmd
        )
        create_pn_response = cn.insert_pn_obligatory_()
        CreateCn.ms_release_before_cn_creation = requests.get(url=create_pn_response[8]).json()
        CreateCn.pn_release_before_cn_creation = requests.get(url=create_pn_response[9]).json()
        create_cn_response = cn.create_cn(
            cp_id=create_pn_response[4],
            pn_id=create_pn_response[5],
            pn_token=create_pn_response[6]
        )
        cn.get_message_from_kafka()

        CreateCn.message_from_kafka = cn.get_message_from_kafka()
        CreateCn.successfully_create_cn = cn.check_on_that_message_is_successfully_create_cn()
        CreateCn.payload = payload
        CreateCn.cp_id = create_pn_response[4]
        CreateCn.pn_id = create_pn_response[5]
        assert compare_actual_result_and_expected_result(
            expected_result=str(202),
            actual_result=str(create_cn_response.status_code)
        )

    @pytestrail.case('27597')
    def test_see_result_from_feed_point_27597_2(self):
        assert compare_actual_result_and_expected_result(
            expected_result=str(True),
            actual_result=str(CreateCn.successfully_create_cn)
        )

    @pytestrail.case('27597')
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_ev_release_27597_3(
            self, language, instance, pmd):
        ev_release = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}").json()
        get_value_by_first_item_cpv_code = get_value_from_classification_cpv_dictionary_xls(
            CreateCn.payload['tender']['items'][0]['classification']['id'],
            language
        )
        get_value_by_first_item_unit_id = get_value_from_classification_unit_dictionary_csv(
            CreateCn.payload['tender']['items'][0]['unit']['id'],
            language
        )
        mdm = MdmService(
            instance=instance,
            lang=language,
            pn_lot_address_details_country_id=CreateCn.payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['country']['id'],
            pn_lot_address_details_region_id=CreateCn.payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['region']['id'],
            pn_lot_address_details_locality_id=CreateCn.payload["tender"]["lots"][0]['placeOfPerformance']['address'][
                'addressDetails']['locality']['id'],
            pn_lot_address_details_locality_scheme=CreateCn.payload["tender"]["lots"][0]['placeOfPerformance'][
                'address']['addressDetails']['locality']['scheme']
        )
        data = mdm.process_tender_data(pmd).json()
        first_lot_country_from_mdm = \
            data["data"]["tender"]["lots"][0]['placeOfPerformance']['address']['addressDetails']['country']
        first_lot_region_from_mdm = \
            data["data"]["tender"]["lots"][0]['placeOfPerformance']['address']['addressDetails']['region']
        first_lot_locality_from_mdm = \
            data["data"]["tender"]["lots"][0]['placeOfPerformance']['address']['addressDetails']['locality']

        actual_result = ev_release
        expected_result = {
            "uri": f"http://dev.public.eprocurement.systems/tenders/{CreateCn.message_from_kafka['data']['ocid']}/"
                   f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}",
            "version": "1.1",
            "extensions": [
                "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"],
            "publisher": {
                "name": "M-Tender",
                "uri": "https://www.mtender.gov.md"
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": CreateCn.message_from_kafka['data']['operationDate'],
            "releases": [{
                "ocid": CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id'],
                "id": f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}-"
                      f"{actual_result['releases'][0]['id'][46:59]}",
                "date": CreateCn.message_from_kafka['data']['operationDate'],
                "tag": ["tender"],
                "language": language,
                "initiationType": "tender",
                "tender": {
                    "id": actual_result['releases'][0]['tender']['id'],
                    "title": "Evaluation",
                    "description": "Evaluation stage of contracting process",
                    "status": "active",
                    "statusDetails": "clarification",
                    "items": [{
                        "id": actual_result['releases'][0]['tender']['items'][0]['id'],
                        "description": CreateCn.payload['tender']['items'][0]['description'],
                        "classification": {
                            "scheme": "CPV",
                            "id": get_value_by_first_item_cpv_code[0],
                            "description": get_value_by_first_item_cpv_code[1]
                        },
                        "quantity": CreateCn.payload['tender']['items'][0]['quantity'],
                        "unit": {
                            "name": get_value_by_first_item_unit_id[1],
                            "id": get_value_by_first_item_unit_id[0]
                        },
                        "relatedLot": actual_result['releases'][0]['tender']['lots'][0]['id']
                    }],
                    "lots": [{
                        "id": actual_result['releases'][0]['tender']['lots'][0]['id'],
                        "title": CreateCn.payload['tender']['lots'][0]['title'],
                        "description": CreateCn.payload['tender']['lots'][0]['description'],
                        "status": "active",
                        "statusDetails": "empty",
                        "value": {
                            "amount": CreateCn.payload['tender']['lots'][0]['value']['amount'],
                            "currency": CreateCn.payload['tender']['lots'][0]['value']['currency']
                        },
                        "contractPeriod": {
                            "startDate": CreateCn.payload['tender']['lots'][0]['contractPeriod'][
                                'startDate'],
                            "endDate": CreateCn.payload['tender']['lots'][0]['contractPeriod'][
                                'endDate']
                        },
                        "placeOfPerformance": {
                            "address": {
                                "streetAddress":
                                    CreateCn.payload['tender']['lots'][0]['placeOfPerformance'][
                                        'address']['streetAddress'],
                                "addressDetails": {
                                    "country": {
                                        "scheme": first_lot_country_from_mdm['scheme'],
                                        "id": CreateCn.payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                            'addressDetails']['country']['id'],
                                        "description": first_lot_country_from_mdm['description'],
                                        "uri": first_lot_country_from_mdm['uri']
                                    },
                                    "region": {
                                        "scheme": first_lot_region_from_mdm['scheme'],
                                        "id": CreateCn.payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                            'addressDetails']['region']['id'],
                                        "description": first_lot_region_from_mdm['description'],
                                        "uri": first_lot_region_from_mdm['uri']
                                    },
                                    "locality": {
                                        "scheme":
                                            CreateCn.payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                                'addressDetails']['locality']['scheme'],
                                        "id": CreateCn.payload['tender']['lots'][0]['placeOfPerformance']['address'][
                                            'addressDetails']['locality']['id'],
                                        "description": first_lot_locality_from_mdm['description'],
                                        "uri": first_lot_locality_from_mdm['uri']
                                    }
                                    }
                            }
                        },
                        "hasOptions": False,
                        "hasRecurrence": False,
                        "hasRenewal": False,

                    }],
                    "lotGroups": [{
                        "optionToCombine": False
                    }],
                    "tenderPeriod": {
                        "startDate": CreateCn.payload['tender']['enquiryPeriod']['endDate'],
                        "endDate": CreateCn.payload['tender']['tenderPeriod']['endDate']
                    },
                    "enquiryPeriod": {
                        "startDate": CreateCn.message_from_kafka['data']['operationDate'],
                        "endDate": CreateCn.payload['tender']['enquiryPeriod']['endDate']
                    },
                    "hasEnquiries": False,
                    "documents": [{
                        "id": CreateCn.payload['tender']['documents'][0]['id'],
                        "documentType": CreateCn.payload['tender']['documents'][0]['documentType'],
                        "title": CreateCn.payload['tender']['documents'][0]['title'],
                        "url": f"https://dev.bpe.eprocurement.systems/api/v1/storage/get/"
                               f"{CreateCn.payload['tender']['documents'][0]['id']}",
                        "datePublished": CreateCn.message_from_kafka['data']['operationDate']
                    }],
                    "awardCriteria": CreateCn.payload['tender']['awardCriteria'],
                    "awardCriteriaDetails": CreateCn.payload['tender']['awardCriteriaDetails'],
                    "submissionMethod": ["electronicSubmission"],
                    "submissionMethodDetails": CreateCn.pn_release_before_cn_creation['releases'][0]['tender'][
                        'submissionMethodDetails'],
                    "submissionMethodRationale": CreateCn.pn_release_before_cn_creation['releases'][0]['tender'][
                        'submissionMethodRationale'],
                    "requiresElectronicCatalogue": CreateCn.pn_release_before_cn_creation['releases'][0]['tender'][
                        'requiresElectronicCatalogue'],
                },
                "hasPreviousNotice": True,
                "purposeOfNotice": {
                    "isACallForCompetition": True
                },
                "relatedProcesses": [{
                    "id": actual_result['releases'][0]['relatedProcesses'][0]['id'],
                    "relationship": ["parent"],
                    "scheme": "ocid",
                    "identifier": CreateCn.message_from_kafka['data']['ocid'],
                    "uri": f"http://dev.public.eprocurement.systems/tenders/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}"
                }, {
                    "id": actual_result['releases'][0]['relatedProcesses'][1]['id'],
                    "relationship": ["planning"],
                    "scheme": "ocid",
                    "identifier": CreateCn.pn_id,
                    "uri": f"http://dev.public.eprocurement.systems/tenders/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}/"
                           f"{CreateCn.pn_id}"
                }]
            }]
        }
        compare_releases = DeepDiff(expected_result, actual_result)
        assert compare_actual_result_and_expected_result(
            expected_result=str({}),
            actual_result=str(compare_releases)
        )

    @pytestrail.case('27597')
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_ms_release_27597_4(
            self, language):
        ev_release = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}").json()
        ms_release_after_cn_creation = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.message_from_kafka['data']['ocid']}").json()
        get_value_by_classification_id = get_value_from_classification_cpv_dictionary_xls(
            cpv=CreateCn.payload['tender']['items'][0]['classification']['id'],
            language=language.upper()
        )

        actual_result = ms_release_after_cn_creation
        expected_result = {
            "uri": CreateCn.ms_release_before_cn_creation['uri'],
            "version": CreateCn.ms_release_before_cn_creation['version'],
            "extensions": [
                CreateCn.ms_release_before_cn_creation['extensions'][0],
                CreateCn.ms_release_before_cn_creation['extensions'][1]],
            "publisher": {
                "name": CreateCn.ms_release_before_cn_creation['publisher']['name'],
                "uri": CreateCn.ms_release_before_cn_creation['publisher']['uri']
            },
            "license": CreateCn.ms_release_before_cn_creation['license'],
            "publicationPolicy": CreateCn.ms_release_before_cn_creation['publicationPolicy'],
            "publishedDate": CreateCn.ms_release_before_cn_creation['releases'][0]['date'],
            "releases": [{
                "ocid": CreateCn.ms_release_before_cn_creation['releases'][0]['ocid'],
                "id": f"{CreateCn.ms_release_before_cn_creation['releases'][0]['ocid']}-"
                      f"{ms_release_after_cn_creation['releases'][0]['id'][29:42]}",
                "date": CreateCn.message_from_kafka['data']['operationDate'],
                "tag": ["compiled"],
                "language": language,
                "initiationType": "tender",
                "planning": {
                    "budget": {
                        "amount": {
                            "amount":
                                CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget']['amount'][
                                    'amount'],
                            "currency":
                                CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget']['amount'][
                                    'currency']
                        },
                        "isEuropeanUnionFunded":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                'isEuropeanUnionFunded'],
                        "budgetBreakdown": [{
                            "id": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                'budgetBreakdown'][0]['id'],
                            "amount": {
                                "amount": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['amount']['amount'],
                                "currency": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['amount']['currency']
                            },
                            "period": {
                                "startDate":
                                    CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                        'budgetBreakdown'][0]['period']['startDate'],
                                "endDate": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['period']['endDate']
                            },
                            "sourceParty": {
                                "id": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['sourceParty']['id'],
                                "name": CreateCn.ms_release_before_cn_creation['releases'][0]['planning']['budget'][
                                    'budgetBreakdown'][0]['sourceParty']['name']
                            }
                        }]
                    }
                },
                "tender": {
                    "id": ev_release['releases'][0]['tender']['id'],
                    "title": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['title'],
                    "description": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['description'],
                    "status": ev_release['releases'][0]['tender']['status'],
                    "statusDetails": "evaluation",
                    "value": {
                        "amount": CreateCn.payload['tender']['lots'][0]['value']['amount'],
                        "currency": CreateCn.payload['tender']['lots'][0]['value']['currency']
                    },
                    "procurementMethod": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'procurementMethod'],
                    "procurementMethodDetails": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'procurementMethodDetails'],
                    "mainProcurementCategory": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'mainProcurementCategory'],
                    "hasEnquiries": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['hasEnquiries'],
                    "eligibilityCriteria": CreateCn.ms_release_before_cn_creation['releases'][0]['tender'][
                        'eligibilityCriteria'],
                    "contractPeriod": {
                        "startDate": CreateCn.payload['tender']['lots'][0]['contractPeriod']['startDate'],
                        "endDate": CreateCn.payload['tender']['lots'][0]['contractPeriod']['endDate']
                    },
                    "procuringEntity": {
                        "id": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['procuringEntity']['id'],
                        "name": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['procuringEntity'][
                            'name']
                    },
                    "acceleratedProcedure": {
                        "isAcceleratedProcedure":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['acceleratedProcedure'][
                                'isAcceleratedProcedure']
                    },
                    "classification": {
                        "scheme": "CPV",
                        "id": get_value_by_classification_id[0],
                        "description":
                            get_value_by_classification_id[1]
                    },
                    "designContest": {
                        "serviceContractAward":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['designContest'][
                                'serviceContractAward']
                    },
                    "electronicWorkflows": {
                        "useOrdering":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['electronicWorkflows'][
                                'useOrdering'],
                        "usePayment":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['electronicWorkflows'][
                                'usePayment'],
                        "acceptInvoicing":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['electronicWorkflows'][
                                'acceptInvoicing']
                    },
                    "jointProcurement": {
                        "isJointProcurement":
                            CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['jointProcurement'][
                                'isJointProcurement']
                    },
                    "legalBasis": CreateCn.ms_release_before_cn_creation['releases'][0]['tender']['legalBasis'],
                    "procedureOutsourcing": {
                        "procedureOutsourced":
                            CreateCn.ms_release_before_cn_creation["releases"][0]["tender"]["procedureOutsourcing"][
                                "procedureOutsourced"]
                    },
                    "dynamicPurchasingSystem": {
                        "hasDynamicPurchasingSystem":
                            CreateCn.ms_release_before_cn_creation["releases"][0]["tender"]["dynamicPurchasingSystem"][
                                "hasDynamicPurchasingSystem"]
                    },
                    "framework": {
                        "isAFramework": CreateCn.ms_release_before_cn_creation["releases"][0]["tender"]["framework"][
                            "isAFramework"]
                    }
                },
                "parties": [{
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['id'],
                    "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['name'],
                    "identifier": {
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['identifier'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['identifier']['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['identifier'][
                            'legalName']
                    },
                    "address": {
                        "streetAddress": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                            'streetAddress'],
                        "addressDetails": {
                            "country": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['country']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['country']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['country']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['region']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['region']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['region']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['locality']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['locality']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                        'addressDetails']['locality']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['address'][
                                    'addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "contactPoint": {
                        "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                            'name'],
                        "email": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                            'email'],
                        "telephone":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][0]['contactPoint'][
                                'telephone']
                    },
                    "roles": ["buyer"]
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['id'],
                    "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['name'],
                    "identifier": {
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['identifier'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['identifier']['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['identifier'][
                            'legalName']
                    },
                    "address": {
                        "streetAddress": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                            'streetAddress'],
                        "addressDetails": {
                            "country": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['country']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['country']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['country']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['region']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['region']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['region']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['locality']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['locality']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                        'addressDetails']['locality']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['address'][
                                    'addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "contactPoint": {
                        "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                            'name'],
                        "email": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                            'email'],
                        "telephone":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][1]['contactPoint'][
                                'telephone']
                    },
                    "roles": ["payer"]
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['id'],
                    "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['name'],
                    "identifier": {
                        "scheme": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['identifier'][
                            'scheme'],
                        "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['identifier']['id'],
                        "legalName": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['identifier'][
                            'legalName']
                    },
                    "address": {
                        "streetAddress": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                            'streetAddress'],
                        "addressDetails": {
                            "country": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['country']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['country']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['country']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['country']['uri']
                            },
                            "region": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['region']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['region']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['region']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['region']['uri']
                            },
                            "locality": {
                                "scheme":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['locality']['scheme'],
                                "id": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['locality']['id'],
                                "description":
                                    CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                        'addressDetails']['locality']['description'],
                                "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['address'][
                                    'addressDetails']['locality']['uri']
                            }
                        }
                    },
                    "contactPoint": {
                        "name": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                            'name'],
                        "email": CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                            'email'],
                        "telephone":
                            CreateCn.ms_release_before_cn_creation["releases"][0]['parties'][2]['contactPoint'][
                                'telephone']
                    },
                    "roles": ["procuringEntity"]
                }],
                "relatedProcesses": [{
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][0]['id'],
                    "relationship": ["planning"],
                    "scheme": "ocid",
                    "identifier": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][0][
                        'identifier'],
                    "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][0]['uri']
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][1]['id'],
                    "relationship": ["x_expenditureItem"],
                    "scheme": "ocid",
                    "identifier": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][1][
                        'identifier'],
                    "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][1]['uri']
                }, {
                    "id": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][2]['id'],
                    "relationship": ["x_fundingSource"],
                    "scheme": "ocid",
                    "identifier": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][2][
                        'identifier'],
                    "uri": CreateCn.ms_release_before_cn_creation["releases"][0]['relatedProcesses'][2]['uri']
                }, {
                    "id": ms_release_after_cn_creation["releases"][0]['relatedProcesses'][3]['id'],
                    "relationship": ["x_evaluation"],
                    "scheme": "ocid",
                    "identifier": CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id'],
                    "uri": f"http://dev.public.eprocurement.systems/tenders/"
                           f"{CreateCn.message_from_kafka['data']['ocid']}/"
                           f"{CreateCn.message_from_kafka['data']['outcomes']['ev'][0]['id']}"
                }]
            }]
        }
        compare_releases = DeepDiff(expected_result, actual_result)
        assert compare_actual_result_and_expected_result(
            expected_result=str({}),
            actual_result=str(compare_releases)
        )

    @pytestrail.case('27597')
    def test_check_on_the_platform_data_has_been_transferred_and_displayed_correctly_in_the_pn_release_27597_5(
            self):
        pn_release_after_cn_creation = requests.get(
            url=f"{CreateCn.message_from_kafka['data']['url']}/"
                f"{CreateCn.pn_id}").json()
        actual_result = DeepDiff(CreateCn.pn_release_before_cn_creation, pn_release_after_cn_creation)
        expected_result = str({
            'values_changed': {
                "root['releases'][0]['id']": {
                    'new_value': f"{CreateCn.pn_id}-{pn_release_after_cn_creation['releases'][0]['id'][46:59]}",
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['id']
                },
                "root['releases'][0]['date']": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['date'],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['date']
                },
                "root['releases'][0]['tag'][0]": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['tag'][0],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['tag'][0]
                },
                "root['releases'][0]['tender']['status']": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['tender']['status'],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['status']
                },
                "root['releases'][0]['tender']['statusDetails']": {
                    'new_value': pn_release_after_cn_creation['releases'][0]['tender']['statusDetails'],
                    'old_value': CreateCn.pn_release_before_cn_creation['releases'][0]['tender']['statusDetails']
                }
            }
        })
        assert compare_actual_result_and_expected_result(
            expected_result=str(expected_result),
            actual_result=str(actual_result)
        )
