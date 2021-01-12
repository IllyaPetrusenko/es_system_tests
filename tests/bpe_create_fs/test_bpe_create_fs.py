import copy
import datetime
import fnmatch
import json
import time
import requests
from pytest_testrail.plugin import pytestrail

from tests.presets import set_instance_for_request
from useful_functions import prepared_cpid, is_valid_uuid
from config import create_fs, host
from tests.Cassandra_session import get_date_execute_cql_from_orchestrator_operation_step_by_oper_id
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.bpe_create_ei.payloads import ei_full, ei_obligatory
from tests.bpe_create_fs.create_fs import bpe_create_fs
from tests.bpe_create_fs.payloads import fs_create_full_treasury_money, fs_create_obligatory_treasury_money, \
    fs_create_full_own_money, fs_create_obligatory_own_money
from tests.kafka_messages import get_message_from_kafka


class TestBpeCreateEI(object):
    @pytestrail.case('24601')
    def test_24601_1(self):
        ei_create = copy.deepcopy(ei_obligatory)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24601')
    def test_24601_2(self):
        ei_create = copy.deepcopy(ei_obligatory)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True

    @pytestrail.case('24601')
    def test_24601_3(self):
        ei_create = copy.deepcopy(ei_obligatory)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['id'] == fs_create['planning']['budget']['id']
        assert publicPoint_create['releases'][0]['planning']['budget']['description'] == \
               fs_create['planning']['budget']['description']
        assert publicPoint_create['releases'][0]['planning']['budget']['period']['startDate'] == \
               fs_create['planning']['budget']['period']['startDate']
        assert publicPoint_create['releases'][0]['planning']['budget']['period']['endDate'] == \
               fs_create['planning']['budget']['period']['endDate']
        assert publicPoint_create['releases'][0]['planning']['budget']['amount']['amount'] == \
               fs_create['planning']['budget']['amount']['amount']
        assert publicPoint_create['releases'][0]['planning']['budget']['amount']['currency'] == \
               fs_create['planning']['budget']['amount']['currency']
        assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['projectIdentifier'] == \
               fs_create['planning']['budget']['europeanUnionFunding']['projectIdentifier']
        assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['projectName'] == \
               fs_create['planning']['budget']['europeanUnionFunding']['projectName']
        assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['uri'] == \
               fs_create['planning']['budget']['europeanUnionFunding']['uri']
        assert publicPoint_create['releases'][0]['planning']['budget']['isEuropeanUnionFunded'] == \
               fs_create['planning']['budget']['isEuropeanUnionFunded']
        assert publicPoint_create['releases'][0]['planning']['budget']['project'] == fs_create['planning']['budget'][
            'project']
        assert publicPoint_create['releases'][0]['planning']['budget']['projectID'] == fs_create['planning']['budget'][
            'projectID']
        assert publicPoint_create['releases'][0]['planning']['budget']['uri'] == fs_create['planning']['budget']['uri']
        assert publicPoint_create['releases'][0]['planning']['rationale'] == fs_create['planning']['rationale']
        assert publicPoint_create['releases'][0]['parties'][0]['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
               fs_create['tender']['procuringEntity']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['name'] == fs_create['tender']['procuringEntity']['name']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['scheme'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['legalName'] == \
               fs_create['tender']['procuringEntity']['identifier']['legalName']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['uri'] == \
               fs_create['tender']['procuringEntity']['identifier']['uri']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['streetAddress'] == \
               fs_create['tender']['procuringEntity']['address']['streetAddress']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['postalCode'] == \
               fs_create['tender']['procuringEntity']['address']['postalCode']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['scheme'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['id'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id']
        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['legalName'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName']
        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['uri'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['name'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['name']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['email'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['email']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['telephone'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['telephone']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['faxNumber'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['faxNumber']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['url'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['url']

    @pytestrail.case('24602')
    def test_24602_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24602')
    def test_24602_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True

    @pytestrail.case('24602')
    def test_24602_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['period']['startDate'] == \
               fs_create['planning']['budget']['period']['startDate']
        assert publicPoint_create['releases'][0]['planning']['budget']['period']['endDate'] == \
               fs_create['planning']['budget']['period']['endDate']
        assert publicPoint_create['releases'][0]['planning']['budget']['amount']['amount'] == \
               fs_create['planning']['budget']['amount']['amount']
        assert publicPoint_create['releases'][0]['planning']['budget']['amount']['currency'] == \
               fs_create['planning']['budget']['amount']['currency']
        assert publicPoint_create['releases'][0]['planning']['budget']['isEuropeanUnionFunded'] == \
               fs_create['planning']['budget']['isEuropeanUnionFunded']
        assert publicPoint_create['releases'][0]['parties'][0]['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
               fs_create['tender']['procuringEntity']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['name'] == fs_create['tender']['procuringEntity']['name']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['scheme'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['legalName'] == \
               fs_create['tender']['procuringEntity']['identifier']['legalName']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['name'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['name']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['email'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['email']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['telephone'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['telephone']

    @pytestrail.case('24603')
    def test_24603_1(self):
        ei_create = copy.deepcopy(ei_obligatory)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        print(json.dumps(fs_create))
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24603')
    def test_24603_2(self):
        ei_create = copy.deepcopy(ei_obligatory)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True

    @pytestrail.case('24603')
    def test_24603_3(self):
        ei_create = copy.deepcopy(ei_obligatory)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['id'] == fs_create['planning']['budget']['id']
        assert publicPoint_create['releases'][0]['planning']['budget']['description'] == \
               fs_create['planning']['budget']['description']
        assert publicPoint_create['releases'][0]['planning']['budget']['period']['startDate'] == \
               fs_create['planning']['budget']['period']['startDate']
        assert publicPoint_create['releases'][0]['planning']['budget']['period']['endDate'] == \
               fs_create['planning']['budget']['period']['endDate']
        assert publicPoint_create['releases'][0]['planning']['budget']['amount']['amount'] == \
               fs_create['planning']['budget']['amount']['amount']
        assert publicPoint_create['releases'][0]['planning']['budget']['amount']['currency'] == \
               fs_create['planning']['budget']['amount']['currency']
        assert publicPoint_create['releases'][0]['planning']['budget']['isEuropeanUnionFunded'] == \
               fs_create['planning']['budget']['isEuropeanUnionFunded']
        assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['id'] == \
               fs_create['buyer']['identifier']['scheme'] + '-' + fs_create['buyer']['identifier']['id']
        assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['name'] == fs_create['buyer'][
            'name']
        assert publicPoint_create['releases'][0]['planning']['budget']['project'] == fs_create['planning']['budget'][
            'project']
        assert publicPoint_create['releases'][0]['planning']['budget']['projectID'] == fs_create['planning']['budget'][
            'projectID']
        assert publicPoint_create['releases'][0]['planning']['budget']['uri'] == fs_create['planning']['budget']['uri']
        assert publicPoint_create['releases'][0]['planning']['rationale'] == fs_create['planning']['rationale']
        assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['projectIdentifier'] == \
               fs_create['planning']['budget']['europeanUnionFunding']['projectIdentifier']
        assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['projectName'] == \
               fs_create['planning']['budget']['europeanUnionFunding']['projectName']
        assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['uri'] == \
               fs_create['planning']['budget']['europeanUnionFunding']['uri']
        assert publicPoint_create['releases'][0]['parties'][1]['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
               fs_create['tender']['procuringEntity']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['name'] == fs_create['tender']['procuringEntity']['name']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['scheme'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['legalName'] == \
               fs_create['tender']['procuringEntity']['identifier']['legalName']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['uri'] == \
               fs_create['tender']['procuringEntity']['identifier']['uri']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['streetAddress'] == \
               fs_create['tender']['procuringEntity']['address']['streetAddress']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['postalCode'] == \
               fs_create['tender']['procuringEntity']['address']['postalCode']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['country']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['region']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['scheme'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['scheme'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme']
        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['id'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id']
        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['legalName'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName']
        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['uri'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['name'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['name']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['email'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['email']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['telephone'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['telephone']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['faxNumber'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['faxNumber']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['url'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['url']
        assert publicPoint_create['releases'][0]['parties'][0]['id'] == \
               fs_create['buyer']['identifier']['scheme'] + '-' + \
               fs_create['buyer']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['name'] == fs_create['buyer']['name']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['scheme'] == \
               fs_create['buyer']['identifier']['scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['id'] == \
               fs_create['buyer']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['legalName'] == \
               fs_create['buyer']['identifier']['legalName']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['uri'] == \
               fs_create['buyer']['identifier']['uri']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['streetAddress'] == \
               fs_create['buyer']['address']['streetAddress']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['postalCode'] == \
               fs_create['buyer']['address']['postalCode']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
               fs_create['buyer']['address']['addressDetails']['country']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
               fs_create['buyer']['address']['addressDetails']['region']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == \
               fs_create['buyer']['address']['addressDetails']['locality']['scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
               fs_create['buyer']['address']['addressDetails']['locality']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['scheme'] == \
               fs_create['buyer']['additionalIdentifiers'][0]['scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['id'] == \
               fs_create['buyer']['additionalIdentifiers'][0]['id']
        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['legalName'] == \
               fs_create['buyer']['additionalIdentifiers'][0]['legalName']
        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['uri'] == \
               fs_create['buyer']['additionalIdentifiers'][0]['uri']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['name'] == \
               fs_create['buyer']['contactPoint']['name']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['email'] == \
               fs_create['buyer']['contactPoint']['email']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['telephone'] == \
               fs_create['buyer']['contactPoint']['telephone']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['faxNumber'] == \
               fs_create['buyer']['contactPoint']['faxNumber']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['url'] == \
               fs_create['buyer']['contactPoint']['url']

    @pytestrail.case('24604')
    def test_24604_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24604')
    def test_24604_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True

    @pytestrail.case('24604')
    def test_24604_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['period']['startDate'] == \
               fs_create['planning']['budget']['period']['startDate']
        assert publicPoint_create['releases'][0]['planning']['budget']['period']['endDate'] == \
               fs_create['planning']['budget']['period']['endDate']
        assert publicPoint_create['releases'][0]['planning']['budget']['amount']['amount'] == \
               fs_create['planning']['budget']['amount']['amount']
        assert publicPoint_create['releases'][0]['planning']['budget']['amount']['currency'] == \
               fs_create['planning']['budget']['amount']['currency']
        assert publicPoint_create['releases'][0]['planning']['budget']['isEuropeanUnionFunded'] == \
               fs_create['planning']['budget']['isEuropeanUnionFunded']
        assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['id'] == \
               fs_create['buyer']['identifier']['scheme'] + '-' + fs_create['buyer']['identifier']['id']
        assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['name'] == fs_create['buyer'][
            'name']
        assert publicPoint_create['releases'][0]['parties'][1]['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
               fs_create['tender']['procuringEntity']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['name'] == fs_create['tender']['procuringEntity']['name']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['scheme'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['legalName'] == \
               fs_create['tender']['procuringEntity']['identifier']['legalName']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['streetAddress'] == \
               fs_create['tender']['procuringEntity']['address']['streetAddress']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['country']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['region']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['scheme'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['name'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['name']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['email'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['email']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['telephone'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['telephone']
        assert publicPoint_create['releases'][0]['parties'][0]['id'] == \
               fs_create['buyer']['identifier']['scheme'] + '-' + \
               fs_create['buyer']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['name'] == fs_create['buyer']['name']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['scheme'] == \
               fs_create['buyer']['identifier']['scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['id'] == \
               fs_create['buyer']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['legalName'] == \
               fs_create['buyer']['identifier']['legalName']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['streetAddress'] == \
               fs_create['buyer']['address']['streetAddress']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
               fs_create['buyer']['address']['addressDetails']['country']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
               fs_create['buyer']['address']['addressDetails']['region']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == \
               fs_create['buyer']['address']['addressDetails']['locality']['scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
               fs_create['buyer']['address']['addressDetails']['locality']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['name'] == \
               fs_create['buyer']['contactPoint']['name']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['email'] == \
               fs_create['buyer']['contactPoint']['email']
        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['telephone'] == \
               fs_create['buyer']['contactPoint']['telephone']

    @pytestrail.case('24605')
    def test_24605_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.00.00.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'Data processing exception.'

    @pytestrail.case('24605')
    def test_24605_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.request.TenderFsCreate] value ' \
                                                                    'failed for JSON property procuringEntity due ' \
                                                                    'to missing (therefore NULL) value for creator ' \
                                                                    'parameter procuringEntity which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.budget.model.dto.fs.request.Fs' \
                                                                    'Create[\"tender\"]->com.procurement.budget.' \
                                                                    'model.dto.fs.request.TenderFsCreate' \
                                                                    '[\"procuringEntity\"])'

    @pytestrail.case('24605')
    def test_24605_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['name']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs] value ' \
                                                                    'failed for JSON property name due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'name which is a non-nullable type\n at [Source:' \
                                                                    ' UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.budget.' \
                                                                    'model.dto.fs.request.FsCreate[\"tender\"]->' \
                                                                    'com.procurement.budget.model.dto.fs.request.' \
                                                                    'TenderFsCreate[\"procuringEntity\"]->com.' \
                                                                    'procurement.budget.model.dto.fs.Organization' \
                                                                    'ReferenceFs[\"name\"])'

    @pytestrail.case('24605')
    def test_24605_4(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['identifier']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs] value ' \
                                                                    'failed for JSON property identifier due to ' \
                                                                    'missing (therefore NULL) value for creator ' \
                                                                    'parameter identifier which is a non-nullable ' \
                                                                    'type\n at [Source: UNKNOWN; line: -1, column:' \
                                                                    ' -1] (through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"tender\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.request.TenderFsCreate[\"procuring' \
                                                                    'Entity\"]->com.procurement.budget.model.dto.fs.' \
                                                                    'OrganizationReferenceFs[\"identifier\"])'

    @pytestrail.case('24605')
    def test_24605_5(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['identifier']['id']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of [' \
                                                                    'simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Identifier] value failed for JSON ' \
                                                                    'property id due to missing (therefore NULL) ' \
                                                                    'value for creator parameter id which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: -1, ' \
                                                                    'column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"tender\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.TenderFS' \
                                                                    '[\"procuringEntity\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.OrganizationReference' \
                                                                    '[\"identifier\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.Identifier[\"id\"])'

    @pytestrail.case('24605')
    def test_24605_6(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['identifier']['scheme']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Identifier] value failed for JSON ' \
                                                                    'property scheme due to missing (therefore NULL) ' \
                                                                    'value for creator parameter scheme which is a ' \
                                                                    'non-nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"tender\"]' \
                                                                    '->com.procurement.mdm.model.dto.data.TenderFS' \
                                                                    '[\"procuringEntity\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.OrganizationReference' \
                                                                    '[\"identifier\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.Identifier[\"scheme\"])'

    @pytestrail.case('24605')
    def test_24605_7(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['identifier']['legalName']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.ocds.Identifier] value failed for ' \
                                                                    'JSON property legalName due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'legalName which is a non-nullable type\n at ' \
                                                                    '[Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"tender\"]->com.procurement.budget.model.dto.' \
                                                                    'fs.request.TenderFsCreate[\"procuring' \
                                                                    'Entity\"]->com.procurement.budget.model.dto.' \
                                                                    'fs.OrganizationReferenceFs[\"identifier\"]->' \
                                                                    'com.procurement.budget.model.dto.ocds.' \
                                                                    'Identifier[\"legalName\"])'

    @pytestrail.case('24605')
    def test_24605_8(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs] value ' \
                                                                    'failed for JSON property address due to missing' \
                                                                    ' (therefore NULL) value for creator parameter ' \
                                                                    'address which is a non-nullable type\n at ' \
                                                                    '[Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"tender\"]->com.procurement.budget.model.dto.' \
                                                                    'fs.request.TenderFsCreate[\"procuring' \
                                                                    'Entity\"]->com.procurement.budget.model.dto.' \
                                                                    'fs.OrganizationReferenceFs[\"address\"])'

    @pytestrail.case('24605')
    def test_24605_9(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']['streetAddress']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Address] value failed for JSON ' \
                                                                    'property streetAddress due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'streetAddress which is a non-nullable type\n ' \
                                                                    'at [Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.mdm.' \
                                                                    'model.dto.data.FS[\"tender\"]->com.procurement.' \
                                                                    'mdm.model.dto.data.TenderFS[\"procuring' \
                                                                    'Entity\"]->com.procurement.mdm.model.dto.data.' \
                                                                    'OrganizationReference[\"address\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Address' \
                                                                    '[\"streetAddress\"])'

    @pytestrail.case('24605')
    def test_24605_10(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']['addressDetails']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Address] value failed for JSON ' \
                                                                    'property addressDetails due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'addressDetails which is a non-nullable type\n ' \
                                                                    'at [Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.mdm.' \
                                                                    'model.dto.data.FS[\"tender\"]->com.procurement.' \
                                                                    'mdm.model.dto.data.TenderFS[\"procuring' \
                                                                    'Entity\"]->com.procurement.mdm.model.dto.data.' \
                                                                    'OrganizationReference[\"address\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Address' \
                                                                    '[\"addressDetails\"])'

    @pytestrail.case('24605')
    def test_24605_11(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']['addressDetails']['country']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.AddressDetails] value failed for JSON ' \
                                                                    'property country due to missing (therefore ' \
                                                                    'NULL) value for creator parameter country which ' \
                                                                    'is a non-nullable type\n at [Source: UNKNOWN; ' \
                                                                    'line: -1, column: -1] (through reference chain: ' \
                                                                    'com.procurement.mdm.model.dto.data.FS' \
                                                                    '[\"tender\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.TenderFS[\"procuringEntity\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"address\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Address[\"addressDetails\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"country\"])'

    @pytestrail.case('24605')
    def test_24605_12(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.CountryDetails] value failed for ' \
                                                                    'JSON property id due to missing (therefore ' \
                                                                    'NULL) value for creator parameter id which is ' \
                                                                    'a non-nullable type\n at [Source: UNKNOWN; ' \
                                                                    'line: -1, column: -1] (through reference chain: ' \
                                                                    'com.procurement.mdm.model.dto.data.FS' \
                                                                    '[\"tender\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.TenderFS[\"procuringEntity\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"address\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Address[\"addressDetails\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"country\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.CountryDetails[\"id\"])'

    @pytestrail.case('24605')
    def test_24605_13(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']['addressDetails']['region']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.AddressDetails] value failed for JSON ' \
                                                                    'property region due to missing (therefore NULL) ' \
                                                                    'value for creator parameter region which is a non' \
                                                                    '-nullable type\n at [Source: UNKNOWN; line: -1, ' \
                                                                    'column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"tender\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.TenderFS' \
                                                                    '[\"procuringEntity\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.OrganizationReference' \
                                                                    '[\"address\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.Address[\"addressDetails\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"region\"])'

    @pytestrail.case('24605')
    def test_24605_14(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.RegionDetails] value failed for JSON ' \
                                                                    'property id due to missing (therefore NULL) ' \
                                                                    'value for creator parameter id which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: -1, ' \
                                                                    'column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"tender\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.TenderFS' \
                                                                    '[\"procuringEntity\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.OrganizationReference' \
                                                                    '[\"address\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.Address[\"addressDetails\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.AddressDetails' \
                                                                    '[\"region\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.RegionDetails[\"id\"])'

    @pytestrail.case('24605')
    def test_24605_15(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.AddressDetails] value failed for JSON ' \
                                                                    'property locality due to missing (therefore ' \
                                                                    'NULL) value for creator parameter locality ' \
                                                                    'which is a non-nullable type\n at [Source: ' \
                                                                    'UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.mdm.model.dto.' \
                                                                    'data.FS[\"tender\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.TenderFS[\"procuringEntity\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"address\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Address[\"addressDetails\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"locality\"])'

    @pytestrail.case('24605')
    def test_24605_16(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.LocalityDetails] value failed for JSON ' \
                                                                    'property id due to missing (therefore NULL) ' \
                                                                    'value for creator parameter id which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: -1, ' \
                                                                    'column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"tender\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.TenderFS' \
                                                                    '[\"procuringEntity\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.OrganizationReference' \
                                                                    '[\"address\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.Address[\"addressDetails\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.AddressDetails' \
                                                                    '[\"locality\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.LocalityDetails[\"id\"])'

    @pytestrail.case('24605')
    def test_24605_17(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.LocalityDetails] value failed for ' \
                                                                    'JSON property scheme due to missing (therefore ' \
                                                                    'NULL) value for creator parameter scheme which ' \
                                                                    'is a non-nullable type\n at [Source: UNKNOWN; ' \
                                                                    'line: -1, column: -1] (through reference chain: ' \
                                                                    'com.procurement.mdm.model.dto.data.FS' \
                                                                    '[\"tender\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.TenderFS[\"procuringEntity\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"address\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Address[\"addressDetails\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"locality\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.LocalityDetails[\"scheme\"])'

    @pytestrail.case('24605')
    def test_24605_18(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.LocalityDetails] value failed for ' \
                                                                    'JSON property description due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'description which is a non-nullable type\n at ' \
                                                                    '[Source: UNKNOWN; line: -1, column: -1] (through' \
                                                                    ' reference chain: com.procurement.mdm.model.' \
                                                                    'dto.data.FS[\"tender\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.TenderFS[\"procuringEntity\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"address\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Address[\"addressDetails\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"locality\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.LocalityDetails[\"description\"])'

    @pytestrail.case('24605')
    def test_24605_19(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['contactPoint']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs] value ' \
                                                                    'failed for JSON property contactPoint due to ' \
                                                                    'missing (therefore NULL) value for creator ' \
                                                                    'parameter contactPoint which is a non-nullable ' \
                                                                    'type\n at [Source: UNKNOWN; line: -1, column: ' \
                                                                    '-1] (through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"tender\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.request.TenderFsCreate' \
                                                                    '[\"procuringEntity\"]->com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs' \
                                                                    '[\"contactPoint\"])'

    @pytestrail.case('24605')
    def test_24605_20(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['contactPoint']['name']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.ContactPoint] value failed for JSON ' \
                                                                    'property name due to missing (therefore NULL) ' \
                                                                    'value for creator parameter name which is a ' \
                                                                    'non-nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"tender\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.TenderFS' \
                                                                    '[\"procuringEntity\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.OrganizationReference' \
                                                                    '[\"contactPoint\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.ContactPoint[\"name\"])'

    @pytestrail.case('24605')
    def test_24605_21(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['contactPoint']['email']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.ContactPoint] value failed for JSON ' \
                                                                    'property email due to missing (therefore NULL) ' \
                                                                    'value for creator parameter email which is a ' \
                                                                    'non-nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"tender\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.TenderFS' \
                                                                    '[\"procuringEntity\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.OrganizationReference' \
                                                                    '[\"contactPoint\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.ContactPoint[\"email\"])'

    @pytestrail.case('24605')
    def test_24605_22(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['tender']['procuringEntity']['contactPoint']['telephone']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.ContactPoint] value failed for JSON ' \
                                                                    'property telephone due to missing (therefore ' \
                                                                    'NULL) value for creator parameter telephone ' \
                                                                    'which is a non-nullable type\n at [Source: ' \
                                                                    'UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.mdm.model.' \
                                                                    'dto.data.FS[\"tender\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.TenderFS[\"procuringEntity\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.' \
                                                                    'OrganizationReference[\"contactPoint\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.ContactPoint' \
                                                                    '[\"telephone\"])'

    @pytestrail.case('24605')
    def test_24605_23(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['name']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs] value ' \
                                                                    'failed for JSON property name due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'name which is a non-nullable type\n at [Source:' \
                                                                    ' UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.budget.model.' \
                                                                    'dto.fs.request.FsCreate[\"buyer\"]->com.' \
                                                                    'procurement.budget.model.dto.fs.Organization' \
                                                                    'ReferenceFs[\"name\"])'

    @pytestrail.case('24605')
    def test_24605_24(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['identifier']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs] value ' \
                                                                    'failed for JSON property identifier due to ' \
                                                                    'missing (therefore NULL) value for creator ' \
                                                                    'parameter identifier which is a non-nullable ' \
                                                                    'type\n at [Source: UNKNOWN; line: -1, column:' \
                                                                    ' -1] (through reference chain: com.' \
                                                                    'procurement.budget.model.dto.fs.request.' \
                                                                    'FsCreate[\"buyer\"]->com.procurement.' \
                                                                    'budget.model.dto.fs.OrganizationReference' \
                                                                    'Fs[\"identifier\"])'

    @pytestrail.case('24605')
    def test_24605_25(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['identifier']['id']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Identifier] value failed for JSON ' \
                                                                    'property id due to missing (therefore NULL) ' \
                                                                    'value for creator parameter id which is a ' \
                                                                    'non-nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: ' \
                                                                    'com.procurement.mdm.model.dto.data.FS' \
                                                                    '[\"buyer\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.OrganizationReference[\"identifier\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Identifier' \
                                                                    '[\"id\"])'

    @pytestrail.case('24605')
    def test_24605_26(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['identifier']['scheme']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Identifier] value failed for JSON ' \
                                                                    'property scheme due to missing (therefore NULL) ' \
                                                                    'value for creator parameter scheme which is a ' \
                                                                    'non-nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"buyer\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"identifier\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Identifier[\"scheme\"])'

    @pytestrail.case('24605')
    def test_24605_27(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['identifier']['legalName']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.ocds.Identifier] value failed for ' \
                                                                    'JSON property legalName due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'legalName which is a non-nullable ' \
                                                                    'type\n at [Source: UNKNOWN; line: -1, ' \
                                                                    'column: -1] (through reference chain: ' \
                                                                    'com.procurement.budget.model.dto.fs.request.' \
                                                                    'FsCreate[\"buyer\"]->com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs' \
                                                                    '[\"identifier\"]->com.procurement.budget.' \
                                                                    'model.dto.ocds.Identifier[\"legalName\"])'

    @pytestrail.case('24605')
    def test_24605_28(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs] value ' \
                                                                    'failed for JSON property address due to ' \
                                                                    'missing (therefore NULL) value for creator ' \
                                                                    'parameter address which is a non-nullable ' \
                                                                    'type\n at [Source: UNKNOWN; line: -1, column: ' \
                                                                    '-1] (through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"buyer\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.OrganizationReferenceFs[\"address\"])'

    @pytestrail.case('24605')
    def test_24605_29(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']['streetAddress']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Address] value failed for JSON ' \
                                                                    'property streetAddress due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'streetAddress which is a non-nullable type\n ' \
                                                                    'at [Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.mdm.' \
                                                                    'model.dto.data.FS[\"buyer\"]->com.procurement.' \
                                                                    'mdm.model.dto.data.OrganizationReference' \
                                                                    '[\"address\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.Address[\"streetAddress\"])'

    @pytestrail.case('24605')
    def test_24605_30(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']['streetAddress']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Address] value failed for JSON ' \
                                                                    'property streetAddress due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'streetAddress which is a non-nullable type\n ' \
                                                                    'at [Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.mdm.' \
                                                                    'model.dto.data.FS[\"buyer\"]->com.procurement.' \
                                                                    'mdm.model.dto.data.OrganizationReference' \
                                                                    '[\"address\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.Address[\"streetAddress\"])'

    @pytestrail.case('24605')
    def test_24605_31(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']['addressDetails']['country']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.' \
                                                                    'MissingKotlinParameterException: Instantiation ' \
                                                                    'of [simple type, class com.procurement.mdm.' \
                                                                    'model.dto.data.AddressDetails] value failed ' \
                                                                    'for JSON property country due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'country which is a non-nullable type\n at ' \
                                                                    '[Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.mdm.' \
                                                                    'model.dto.data.FS[\"buyer\"]->com.procurement.' \
                                                                    'mdm.model.dto.data.OrganizationReference' \
                                                                    '[\"address\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.Address[\"addressDetails\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"country\"])'

    @pytestrail.case('24605')
    def test_24605_32(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']['addressDetails']['country']['id']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.CountryDetails] value failed for JSON ' \
                                                                    'property id due to missing (therefore NULL) ' \
                                                                    'value for creator parameter id which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"buyer\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"address\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Address[\"addressDetails\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"country\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.CountryDetails[\"id\"])'

    @pytestrail.case('24605')
    def test_24605_33(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']['addressDetails']['region']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.AddressDetails] value failed for JSON ' \
                                                                    'property region due to missing (therefore ' \
                                                                    'NULL) value for creator parameter region which ' \
                                                                    'is a non-nullable type\n at [Source: UNKNOWN; ' \
                                                                    'line: -1, column: -1] (through reference chain: ' \
                                                                    'com.procurement.mdm.model.dto.data.FS[\"buyer\"]' \
                                                                    '->com.procurement.mdm.model.dto.data.' \
                                                                    'OrganizationReference[\"address\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Address' \
                                                                    '[\"addressDetails\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.AddressDetails[\"region\"])'

    @pytestrail.case('24605')
    def test_24605_34(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']['addressDetails']['region']['id']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.RegionDetails] value failed for JSON ' \
                                                                    'property id due to missing (therefore NULL) ' \
                                                                    'value for creator parameter id which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: -1, ' \
                                                                    'column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"buyer\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"address\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Address[\"addressDetails\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"region\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.RegionDetails[\"id\"])'

    @pytestrail.case('24605')
    def test_24605_35(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']['addressDetails']['locality']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlin' \
                                                                    'ParameterException: Instantiation of [simple ' \
                                                                    'type, class com.procurement.mdm.model.dto.data.' \
                                                                    'AddressDetails] value failed for JSON property ' \
                                                                    'locality due to missing (therefore NULL) value ' \
                                                                    'for creator parameter locality which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: -1, ' \
                                                                    'column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"buyer\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"address\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Address[\"addressDetails\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.AddressDetails' \
                                                                    '[\"locality\"])'

    @pytestrail.case('24605')
    def test_24605_36(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']['addressDetails']['locality']['scheme']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.LocalityDetails] value failed for JSON ' \
                                                                    'property scheme due to missing (therefore NULL) ' \
                                                                    'value for creator parameter scheme which is a ' \
                                                                    'non-nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"buyer\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"address\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Address[\"addressDetails\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"locality\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.LocalityDetails[\"scheme\"])'

    @pytestrail.case('24605')
    def test_24605_37(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']['addressDetails']['locality']['id']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.LocalityDetails] value failed for ' \
                                                                    'JSON property id due to missing (therefore ' \
                                                                    'NULL) value for creator parameter id which is ' \
                                                                    'a non-nullable type\n at [Source: UNKNOWN; ' \
                                                                    'line: -1, column: -1] (through reference chain: ' \
                                                                    'com.procurement.mdm.model.dto.data.FS' \
                                                                    '[\"buyer\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.OrganizationReference[\"address\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Address' \
                                                                    '[\"addressDetails\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.AddressDetails[\"locality\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.LocalityDetails' \
                                                                    '[\"id\"])'

    @pytestrail.case('24605')
    def test_24605_38(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['address']['addressDetails']['locality']['description']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.LocalityDetails] value failed for ' \
                                                                    'JSON property description due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'description which is a non-nullable type\n ' \
                                                                    'at [Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.mdm.' \
                                                                    'model.dto.data.FS[\"buyer\"]->com.procurement.' \
                                                                    'mdm.model.dto.data.OrganizationReference' \
                                                                    '[\"address\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.Address[\"addressDetails\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"locality\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.LocalityDetails[\"description\"])'

    @pytestrail.case('24605')
    def test_24605_39(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['contactPoint']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs] value ' \
                                                                    'failed for JSON property contactPoint due to ' \
                                                                    'missing (therefore NULL) value for creator ' \
                                                                    'parameter contactPoint which is a non-nullable ' \
                                                                    'type\n at [Source: UNKNOWN; line: -1, column: ' \
                                                                    '-1] (through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"buyer\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.OrganizationReferenceFs[\"contactPoint\"])'

    @pytestrail.case('24605')
    def test_24605_40(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['contactPoint']['name']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.ContactPoint] value failed for JSON ' \
                                                                    'property name due to missing (therefore NULL) ' \
                                                                    'value for creator parameter name which is a ' \
                                                                    'non-nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"buyer\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"contactPoint\"]->com.procurement.' \
                                                                    'mdm.model.dto.data.ContactPoint[\"name\"])'

    @pytestrail.case('24605')
    def test_24605_41(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['contactPoint']['email']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.ContactPoint] value failed for JSON ' \
                                                                    'property email due to missing (therefore NULL) ' \
                                                                    'value for creator parameter email which is a ' \
                                                                    'non-nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"buyer\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"contactPoint\"]->com.procurement.' \
                                                                    'mdm.model.dto.data.ContactPoint[\"email\"])'

    @pytestrail.case('24605')
    def test_24605_42(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['buyer']['contactPoint']['telephone']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.ContactPoint] value failed for JSON ' \
                                                                    'property telephone due to missing (therefore ' \
                                                                    'NULL) value for creator parameter telephone ' \
                                                                    'which is a non-nullable type\n at [Source: ' \
                                                                    'UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.mdm.model.dto.' \
                                                                    'data.FS[\"buyer\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.OrganizationReference' \
                                                                    '[\"contactPoint\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.ContactPoint[\"telephone\"])'

    @pytestrail.case('24605')
    def test_24605_43(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['planning']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.00.00.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'Data processing exception.'

    @pytestrail.case('24605')
    def test_24605_44(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['planning']['budget']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.00.00.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'Data processing exception.'

    @pytestrail.case('24605')
    def test_24605_45(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['planning']['budget']['period']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.request.BudgetFsCreate] value ' \
                                                                    'failed for JSON property period due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'period which is a non-nullable type\n at ' \
                                                                    '[Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"planning\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.request.PlanningFsCreate[\"budget\"]->' \
                                                                    'com.procurement.budget.model.dto.fs.request.' \
                                                                    'BudgetFsCreate[\"period\"])'

    @pytestrail.case('24605')
    def test_24605_46(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['planning']['budget']['period']['startDate']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.ocds.Period] value failed for JSON ' \
                                                                    'property startDate due to missing (therefore ' \
                                                                    'NULL) value for creator parameter startDate ' \
                                                                    'which is a non-nullable type\n at [Source: ' \
                                                                    'UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.budget.' \
                                                                    'model.dto.fs.request.FsCreate[\"planning\"]->' \
                                                                    'com.procurement.budget.model.dto.fs.request.' \
                                                                    'PlanningFsCreate[\"budget\"]->com.procurement.' \
                                                                    'budget.model.dto.fs.request.BudgetFsCreate' \
                                                                    '[\"period\"]->com.procurement.budget.model.dto.' \
                                                                    'ocds.Period[\"startDate\"])'

    @pytestrail.case('24605')
    def test_24605_47(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['planning']['budget']['period']['endDate']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.ocds.Period] value failed for ' \
                                                                    'JSON property endDate due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'endDate which is a non-nullable type\n at ' \
                                                                    '[Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"planning\"]->com.procurement.budget.' \
                                                                    'model.dto.fs.request.PlanningFsCreate' \
                                                                    '[\"budget\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.request.BudgetFsCreate[\"period\"]->' \
                                                                    'com.procurement.budget.model.dto.ocds.' \
                                                                    'Period[\"endDate\"])'

    @pytestrail.case('24605')
    def test_24605_48(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['planning']['budget']['amount']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.00.00.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'Data processing exception.'

    @pytestrail.case('24605')
    def test_24605_49(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['planning']['budget']['amount']['amount']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.ocds.Value] value failed for JSON ' \
                                                                    'property amount due to missing (therefore NULL) ' \
                                                                    'value for creator parameter amount which is a ' \
                                                                    'non-nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"planning\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.request.PlanningFsCreate[\"budget\"]->' \
                                                                    'com.procurement.budget.model.dto.fs.request.' \
                                                                    'BudgetFsCreate[\"amount\"]->com.procurement.' \
                                                                    'budget.model.dto.ocds.Value[\"amount\"])'

    @pytestrail.case('24605')
    def test_24605_50(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['planning']['budget']['amount']['currency']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.ValueFS] value failed for JSON ' \
                                                                    'property currency due to missing (therefore ' \
                                                                    'NULL) value for creator parameter currency ' \
                                                                    'which is a non-nullable type\n at [Source: ' \
                                                                    'UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.mdm.model.dto.' \
                                                                    'data.FS[\"planning\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.PlanningFS[\"budget\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.BudgetFS' \
                                                                    '[\"amount\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.ValueFS[\"currency\"])'

    @pytestrail.case('24605')
    def test_24605_51(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        del fs_create['planning']['budget']['isEuropeanUnionFunded']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.fs.request.BudgetFsCreate] value ' \
                                                                    'failed for JSON property isEuropeanUnionFunded ' \
                                                                    'due to missing (therefore NULL) value for ' \
                                                                    'creator parameter isEuropeanUnionFunded ' \
                                                                    'which is a non-nullable type\n at [Source: ' \
                                                                    'UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.budget.model.' \
                                                                    'dto.fs.request.FsCreate[\"planning\"]->com.' \
                                                                    'procurement.budget.model.dto.fs.request.' \
                                                                    'PlanningFsCreate[\"budget\"]->com.procurement.' \
                                                                    'budget.model.dto.fs.request.BudgetFsCreate' \
                                                                    '[\"isEuropeanUnionFunded\"])'

    @pytestrail.case('24605')
    def test_24605_52(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
        del fs_create['planning']['budget']['europeanUnionFunding']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.01.04'
        assert create_fs_response[1]['errors'][0]['description'] == 'EuropeanUnionFunding must not be empty.'

    @pytestrail.case('24605')
    def test_24605_53(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
        del fs_create['planning']['budget']['europeanUnionFunding']['projectName']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.ocds.EuropeanUnionFunding] value ' \
                                                                    'failed for JSON property projectName due to ' \
                                                                    'missing (therefore NULL) value for creator ' \
                                                                    'parameter projectName which is a non-nullable ' \
                                                                    'type\n at [Source: UNKNOWN; line: -1, column: ' \
                                                                    '-1] (through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"planning\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.request.PlanningFsCreate[\"budget\"]->' \
                                                                    'com.procurement.budget.model.dto.fs.request.' \
                                                                    'BudgetFsCreate[\"europeanUnionFunding\"]->com.' \
                                                                    'procurement.budget.model.dto.ocds.European' \
                                                                    'UnionFunding[\"projectName\"])'

    @pytestrail.case('24605')
    def test_24605_54(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
        del fs_create['planning']['budget']['europeanUnionFunding']['projectIdentifier']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.ocds.EuropeanUnionFunding] value ' \
                                                                    'failed for JSON property projectIdentifier due ' \
                                                                    'to missing (therefore NULL) value for creator ' \
                                                                    'parameter projectIdentifier which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.budget.model.dto.fs.request.' \
                                                                    'FsCreate[\"planning\"]->com.procurement.budget.' \
                                                                    'model.dto.fs.request.PlanningFsCreate' \
                                                                    '[\"budget\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.request.BudgetFsCreate[\"europeanUnion' \
                                                                    'Funding\"]->com.procurement.budget.model.dto.' \
                                                                    'ocds.EuropeanUnionFunding[\"projectIdentifier\"])'

    @pytestrail.case('24605')
    def test_24605_55(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        del fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Identifier] value failed for JSON ' \
                                                                    'property id due to missing (therefore NULL) ' \
                                                                    'value for creator parameter id which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: ' \
                                                                    'com.procurement.mdm.model.dto.data.' \
                                                                    'FS[\"tender\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.TenderFS[\"procuringEntity\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"additionalIdentifiers\"]->java.util.' \
                                                                    'ArrayList[0]->com.procurement.mdm.model.dto.' \
                                                                    'data.Identifier[\"id\"])'

    @pytestrail.case('24605')
    def test_24605_56(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        del fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Identifier] value failed for JSON ' \
                                                                    'property scheme due to missing (therefore NULL) ' \
                                                                    'value for creator parameter scheme which is a ' \
                                                                    'non-nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.FS[\"tender\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.TenderFS' \
                                                                    '[\"procuringEntity\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.OrganizationReference' \
                                                                    '[\"additionalIdentifiers\"]->java.util.' \
                                                                    'ArrayList[0]->com.procurement.mdm.model.' \
                                                                    'dto.data.Identifier[\"scheme\"])'

    @pytestrail.case('24605')
    def test_24605_57(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        del fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.' \
                                                                    'MissingKotlinParameterException: Instantiation ' \
                                                                    'of [simple type, class com.procurement.budget.' \
                                                                    'model.dto.ocds.Identifier] value failed for ' \
                                                                    'JSON property legalName due to missing ' \
                                                                    '(therefore NULL) value for creator parameter ' \
                                                                    'legalName which is a non-nullable type\n at ' \
                                                                    '[Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"tender\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.request.TenderFsCreate' \
                                                                    '[\"procuringEntity\"]->com.procurement.budget.' \
                                                                    'model.dto.fs.OrganizationReferenceFs' \
                                                                    '[\"additionalIdentifiers\"]->java.util.' \
                                                                    'ArrayList[0]->com.procurement.budget.model.' \
                                                                    'dto.ocds.Identifier[\"legalName\"])'

    @pytestrail.case('24605')
    def test_24605_58(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        del fs_create['buyer']['additionalIdentifiers'][0]['id']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Identifier] value failed for JSON ' \
                                                                    'property id due to missing (therefore NULL) ' \
                                                                    'value for creator parameter id which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: ' \
                                                                    'com.procurement.mdm.model.dto.data.FS' \
                                                                    '[\"buyer\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.OrganizationReference[\"additional' \
                                                                    'Identifiers\"]->java.util.ArrayList[0]->com.' \
                                                                    'procurement.mdm.model.dto.data.Identifier' \
                                                                    '[\"id\"])'

    @pytestrail.case('24605')
    def test_24605_59(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        del fs_create['buyer']['additionalIdentifiers'][0]['scheme']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.Identifier] value failed for JSON ' \
                                                                    'property scheme due to missing (therefore ' \
                                                                    'NULL) value for creator parameter scheme ' \
                                                                    'which is a non-nullable type\n at [Source: ' \
                                                                    'UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.mdm.model.' \
                                                                    'dto.data.FS[\"buyer\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.OrganizationReference' \
                                                                    '[\"additionalIdentifiers\"]->java.util.ArrayList' \
                                                                    '[0]->com.procurement.mdm.model.dto.data.' \
                                                                    'Identifier[\"scheme\"])'

    @pytestrail.case('24605')
    def test_24605_60(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        del fs_create['buyer']['additionalIdentifiers'][0]['legalName']
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.MissingKotlin' \
                                                                    'ParameterException: Instantiation of [simple ' \
                                                                    'type, class com.procurement.budget.model.dto.' \
                                                                    'ocds.Identifier] value failed for JSON property ' \
                                                                    'legalName due to missing (therefore NULL) value ' \
                                                                    'for creator parameter legalName which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: -1, ' \
                                                                    'column: -1] (through reference chain: com.' \
                                                                    'procurement.budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"buyer\"]->com.procurement.budget.model.dto.' \
                                                                    'fs.OrganizationReferenceFs[\"additional' \
                                                                    'Identifiers\"]->java.util.ArrayList[0]->com.' \
                                                                    'procurement.budget.model.dto.ocds.Identifier' \
                                                                    '[\"legalName\"])'

    @pytestrail.case('24606')
    def test_24606_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['name'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['name'] == fs_create['tender']['procuringEntity']['name']

    @pytestrail.case('24606')
    def test_24606_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['identifier']['uri'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['uri'] == \
               fs_create['tender']['procuringEntity']['identifier']['uri']

    @pytestrail.case('24606')
    def test_24606_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['identifier']['id'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['id']

    @pytestrail.case('24606')
    def test_24606_4(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['identifier']['legalName'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['legalName'] == \
               fs_create['tender']['procuringEntity']['identifier']['legalName']

    @pytestrail.case('24606')
    def test_24606_5(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['address']['streetAddress'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['address']['streetAddress'] == \
               fs_create['tender']['procuringEntity']['address']['streetAddress']

    @pytestrail.case('24606')
    def test_24606_6(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['address']['postalCode'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['address']['postalCode'] == \
               fs_create['tender']['procuringEntity']['address']['postalCode']

    @pytestrail.case('24606')
    def test_24606_7(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']

    @pytestrail.case('24606')
    def test_24606_8(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['scheme'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']

    @pytestrail.case('24606')
    def test_24606_9(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality'][
                   'description'] == fs_create['tender']['procuringEntity']['address']['addressDetails']['locality'][
                   'description']

    @pytestrail.case('24606')
    def test_24606_10(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['contactPoint']['name'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['name'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['name']

    @pytestrail.case('24606')
    def test_24606_11(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['contactPoint']['email'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['email'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['email']

    @pytestrail.case('24606')
    def test_24606_12(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['contactPoint']['telephone'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['telephone'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['telephone']

    @pytestrail.case('24606')
    def test_24606_13(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['contactPoint']['faxNumber'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['faxNumber'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['faxNumber']

    @pytestrail.case('24606')
    def test_24606_14(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['contactPoint']['url'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['url'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['url']

    @pytestrail.case('24606')
    def test_24606_15(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['id'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id']

    @pytestrail.case('24606')
    def test_24606_16(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['scheme'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme']

    @pytestrail.case('24606')
    def test_24606_17(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['legalName'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName']

    @pytestrail.case('24606')
    def test_24606_18(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)

        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['uri'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri']

    @pytestrail.case('24606')
    def test_24606_19(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['name'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['name'] == fs_create['buyer']['name']

    @pytestrail.case('24606')
    def test_24606_20(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['id'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['id'] == fs_create['buyer']['identifier'][
            'id']

    @pytestrail.case('24606')
    def test_24606_21(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['legalName'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['legalName'] == \
               fs_create['buyer']['identifier']['legalName']

    @pytestrail.case('24606')
    def test_24606_22(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['uri'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['identifier']['uri'] == \
               fs_create['buyer']['identifier']['uri']

    @pytestrail.case('24606')
    def test_24606_23(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['address']['streetAddress'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['streetAddress'] == \
               fs_create['buyer']['address']['streetAddress']

    @pytestrail.case('24606')
    def test_24606_24(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['address']['postalCode'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['postalCode'] == \
               fs_create['buyer']['address']['postalCode']

    @pytestrail.case('24606')
    def test_24606_25(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['address']['addressDetails']['locality']['scheme'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'] == \
               fs_create['buyer']['address']['addressDetails']['locality']['scheme']

    @pytestrail.case('24606')
    def test_24606_26(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
        fs_create['buyer']['address']['addressDetails']['locality']['id'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
               fs_create['buyer']['address']['addressDetails']['locality']['id']

    @pytestrail.case('24606')
    def test_24606_27(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['address']['addressDetails']['locality']['scheme'] = 'other'
        fs_create['buyer']['address']['addressDetails']['locality']['description'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
                   'description'] == \
               fs_create['buyer']['address']['addressDetails']['locality']['description']

    @pytestrail.case('24606')
    def test_24606_28(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['contactPoint']['url'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['url'] == \
               fs_create['buyer']['contactPoint']['url']

    @pytestrail.case('24606')
    def test_24606_29(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['contactPoint']['name'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['name'] == \
               fs_create['buyer']['contactPoint']['name']

    @pytestrail.case('24606')
    def test_24606_30(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['contactPoint']['email'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['email'] == \
               fs_create['buyer']['contactPoint']['email']

    @pytestrail.case('24606')
    def test_24606_31(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['contactPoint']['telephone'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['telephone'] == \
               fs_create['buyer']['contactPoint']['telephone']

    @pytestrail.case('24606')
    def test_24606_32(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['contactPoint']['faxNumber'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['contactPoint']['faxNumber'] == \
               fs_create['buyer']['contactPoint']['faxNumber']

    @pytestrail.case('24606')
    def test_24606_33(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['additionalIdentifiers'][0]['id'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['id'] == \
               fs_create['buyer']['additionalIdentifiers'][0]['id']

    @pytestrail.case('24606')
    def test_24606_34(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['additionalIdentifiers'][0]['scheme'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['scheme'] == \
               fs_create['buyer']['additionalIdentifiers'][0]['scheme']

    @pytestrail.case('24606')
    def test_24606_35(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['additionalIdentifiers'][0]['legalName'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['legalName'] == \
               fs_create['buyer']['additionalIdentifiers'][0]['legalName']

    @pytestrail.case('24606')
    def test_24606_36(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['additionalIdentifiers'][0]['uri'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['additionalIdentifiers'][0]['uri'] == \
               fs_create['buyer']['additionalIdentifiers'][0]['uri']

    @pytestrail.case('24606')
    def test_24606_37(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['rationale'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['rationale'] == \
               fs_create['planning']['rationale']

    @pytestrail.case('24606')
    def test_24606_38(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['id'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['id'] == \
               fs_create['planning']['budget']['id']

    @pytestrail.case('24606')
    def test_24606_39(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['description'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['description'] == \
               fs_create['planning']['budget']['description']

    @pytestrail.case('24606')
    def test_24606_40(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
        fs_create['planning']['budget']['europeanUnionFunding']['projectName'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['projectName'] == \
               fs_create['planning']['budget']['europeanUnionFunding']['projectName']

    @pytestrail.case('24606')
    def test_24606_41(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
        fs_create['planning']['budget']['europeanUnionFunding']['projectIdentifier'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['europeanUnionFunding']['projectIdentifier'] == \
               fs_create['planning']['budget']['europeanUnionFunding']['projectIdentifier']

    @pytestrail.case('24606')
    def test_24606_42(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['project'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['project'] == fs_create['planning']['budget'][
            'project']

    @pytestrail.case('24606')
    def test_24606_43(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['projectID'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['projectID'] == fs_create['planning']['budget'][
            'projectID']

    @pytestrail.case('24606')
    def test_24606_44(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['uri'] = ''
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')
        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['uri'] == fs_create['planning']['budget'][
            'uri']

    @pytestrail.case('24607')
    def test_24607_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)
        host = set_instance_for_request()

        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create)
        time.sleep(2)

        get_message_from_kafka(x_operation_id)

        assert create_fs_response_1[0].text == 'ok'
        assert create_fs_response_1[0].status_code == 202
        assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]

    @pytestrail.case('24607')
    def test_24607_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)
        host = set_instance_for_request()

        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create)
        time.sleep(2)

        get_message_from_kafka(x_operation_id)

        ocid = fnmatch.fnmatch(create_fs_response_1[1]['data']['ocid'], '*')
        assert ocid == True
        assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]

    @pytestrail.case('24607')
    def test_24607_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)
        host = set_instance_for_request()
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        create_fs_response_2 = requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create)
        time.sleep(2)

        message_from_kafka = get_message_from_kafka(x_operation_id)

        assert create_fs_response_2.text == 'ok'
        assert create_fs_response_2.status_code == 202
        assert message_from_kafka['X-OPERATION-ID'] == x_operation_id

    @pytestrail.case('24607')
    def test_24607_4(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)
        host = set_instance_for_request()
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)

        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create)
        time.sleep(2)

        message_from_kafka = get_message_from_kafka(x_operation_id)

        ocid = fnmatch.fnmatch(message_from_kafka['data']['ocid'], '*')
        assert ocid == True
        assert message_from_kafka['X-OPERATION-ID'] == x_operation_id

    @pytestrail.case('24608')
    def test_24608_1(self):
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)

        time.sleep(2)
        host = set_instance_for_request()
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        fake_cpid = prepared_cpid()
        create_fs_response = requests.post(
            url=host + create_fs + fake_cpid,
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create)
        time.sleep(1)

        assert create_fs_response.status_code == 400
        assert create_fs_response.json()['errors'][0]['code'] == '400.00.00.00'
        assert create_fs_response.json()['errors'][0]['description'] == 'Context not found.'

    @pytestrail.case('24609')
    def test_24609_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24609')
    def test_24609_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True

    @pytestrail.case('24610')
    def test_24610_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24610')
    def test_24610_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24610')
    def test_24610_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        timestamp = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'][32:45], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['data']['outcomes']['fs'][0]['id'][0:28] == create_fs_response[3]
        assert create_fs_response[1]['data']['outcomes']['fs'][0]['id'][28:32] == '-FS-'
        assert timestamp == True

    @pytestrail.case('24611')
    def test_24611_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24611')
    def test_24611_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24611')
    def test_24611_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        url_create_fs = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']

        publicPoint_update = requests.get(url=url_create_fs).json()

        check_tender_id = is_valid_uuid(publicPoint_update['releases'][0]['tender']['id'])
        assert check_tender_id == True

    @pytestrail.case('24612')
    def test_24612_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['amount'] = 133.26
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
        time.sleep(2)

        fs_create_2 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['amount'] = 50.34
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'

        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        host = set_instance_for_request()
        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create_2)
        time.sleep(2)

        get_message_from_kafka(x_operation_id)

        assert create_fs_response_1[0].text == 'ok'
        assert create_fs_response_1[0].status_code == 202
        assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]

    @pytestrail.case('24612')
    def test_24612_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['amount'] = 133.26
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
        time.sleep(2)

        fs_create_2 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['amount'] = 50.34
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'

        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        host = set_instance_for_request()
        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create_2)
        time.sleep(2)

        get_message_from_kafka(x_operation_id)

        ocid = fnmatch.fnmatch(create_fs_response_1[1]['data']['ocid'], '*')
        assert ocid == True
        assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]

    @pytestrail.case('24612')
    def test_24612_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['amount'] = 133.26
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
        time.sleep(2)

        fs_create_2 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_2['planning']['budget']['amount']['amount'] = 50.34
        fs_create_2['planning']['budget']['amount']['currency'] = 'EUR'

        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        host = set_instance_for_request()
        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create_2)
        time.sleep(2)

        message_from_kafka = get_message_from_kafka(x_operation_id)
        url_create_ei = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0]['id'][
                                                                  0:28]

        publicPoint_create_ei = requests.get(url=url_create_ei).json()
        sum_of_fs = fs_create_1['planning']['budget']['amount']['amount'] + fs_create_2['planning']['budget']['amount'][
            'amount']

        assert publicPoint_create_ei['releases'][0]['planning']['budget']['amount']['amount'] == sum_of_fs

    @pytestrail.case('24613')
    def test_24613_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24613')
    def test_24613_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24613')
    def test_24613_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        url_create_fs = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_update = requests.get(url=url_create_fs).json()

        assert publicPoint_update['releases'][0]['planning']['budget']['verified'] == True

    @pytestrail.case('24614')
    def test_24614_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24614')
    def test_24614_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24614')
    def test_24614_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        url_create_fs = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_update = requests.get(url=url_create_fs).json()

        assert publicPoint_update['releases'][0]['planning']['budget']['verified'] == False

    @pytestrail.case('24615')
    def test_24615_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24615')
    def test_24615_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True

    @pytestrail.case('24615')
    def test_24615_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['tender']['statusDetails'] == 'empty'

    @pytestrail.case('24616')
    def test_24616_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24616')
    def test_24616_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True

    @pytestrail.case('24616')
    def test_24616_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['tender']['status'] == 'active'

    @pytestrail.case('24617')
    def test_24617_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24617')
    def test_24617_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True

    @pytestrail.case('24617')
    def test_24617_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['tender']['status'] == 'planning'

    @pytestrail.case('24618')
    def test_24618_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24618')
    def test_24618_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True

    @pytestrail.case('24618')
    def test_24618_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()

        assert publicPoint_create['releases'][0]['parties'][0]['roles'][0] != 'funder'

    @pytestrail.case('24619')
    def test_24619_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24619')
    def test_24619_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['ocid'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True

    @pytestrail.case('24619')
    def test_24619_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_update = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_update).json()
        print(url_update)
        assert publicPoint_create['releases'][0]['parties'][0]['roles'][0] == 'funder'
        assert publicPoint_create['releases'][0]['parties'][1]['roles'][0] != 'funder'

    @pytestrail.case('24620')
    def test_24620_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['name'] = 'Znatok'
        fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
        fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
        fs_create['tender']['procuringEntity']['identifier']['legalName'] = 'Kunitskiy Peto Oleksiyovich company'
        fs_create['tender']['procuringEntity']['identifier']['url'] = 'www.dobro.ua'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id'] = 'Dodatovo id'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme'] = 'PROSTO'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName'] = 'Ne_yiridi4na_osoba'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri'] = 'www.zeebra.ua'
        fs_create['tender']['procuringEntity']['address']['streetAddress'] = 'Voloshkova'
        fs_create['tender']['procuringEntity']['address']['postalCode'] = '77777'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '1700000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '1701000'
        fs_create['tender']['procuringEntity']['contactPoint']['name'] = 'Petro Oleksiyovich'
        fs_create['tender']['procuringEntity']['contactPoint']['email'] = 'petro@sobakin.md'
        fs_create['tender']['procuringEntity']['contactPoint']['telephone'] = '044-555-88-96'
        fs_create['tender']['procuringEntity']['contactPoint']['faxNumber'] = '044-555-88-97'
        fs_create['tender']['procuringEntity']['contactPoint']['url'] = 'www.webPetrovicha'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24620')
    def test_24620_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['name'] = 'Znatok'
        fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
        fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
        fs_create['tender']['procuringEntity']['identifier']['legalName'] = 'Kunitskiy Peto Oleksiyovich company'
        fs_create['tender']['procuringEntity']['identifier']['url'] = 'www.dobro.ua'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id'] = 'Dodatovo id'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme'] = 'PROSTO'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName'] = 'Ne_yiridi4na_osoba'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri'] = 'www.zeebra.ua'
        fs_create['tender']['procuringEntity']['address']['streetAddress'] = 'Voloshkova'
        fs_create['tender']['procuringEntity']['address']['postalCode'] = '77777'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '1700000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '1701000'
        fs_create['tender']['procuringEntity']['contactPoint']['name'] = 'Petro Oleksiyovich'
        fs_create['tender']['procuringEntity']['contactPoint']['email'] = 'petro@sobakin.md'
        fs_create['tender']['procuringEntity']['contactPoint']['telephone'] = '044-555-88-96'
        fs_create['tender']['procuringEntity']['contactPoint']['faxNumber'] = '044-555-88-97'
        fs_create['tender']['procuringEntity']['contactPoint']['url'] = 'www.webPetrovicha'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24620')
    def test_24620_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['name'] = 'Znatok'
        fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
        fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'
        fs_create['tender']['procuringEntity']['identifier']['legalName'] = 'Kunitskiy Peto Oleksiyovich company'
        fs_create['tender']['procuringEntity']['identifier']['url'] = 'www.dobro.ua'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id'] = 'Dodatovo id'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme'] = 'PROSTO'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName'] = 'Ne_yiridi4na_osoba'
        fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri'] = 'www.zeebra.ua'
        fs_create['tender']['procuringEntity']['address']['streetAddress'] = 'Voloshkova'
        fs_create['tender']['procuringEntity']['address']['postalCode'] = '77777'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '1700000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '1701000'
        fs_create['tender']['procuringEntity']['contactPoint']['name'] = 'Petro Oleksiyovich'
        fs_create['tender']['procuringEntity']['contactPoint']['email'] = 'petro@sobakin.md'
        fs_create['tender']['procuringEntity']['contactPoint']['telephone'] = '044-555-88-96'
        fs_create['tender']['procuringEntity']['contactPoint']['faxNumber'] = '044-555-88-97'
        fs_create['tender']['procuringEntity']['contactPoint']['url'] = 'www.webPetrovicha'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][1]['roles'][0] == 'payer'
        assert publicPoint_create['releases'][0]['parties'][1]['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
               fs_create['tender']['procuringEntity']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['name'] == fs_create['tender']['procuringEntity']['name']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['scheme'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['legalName'] == \
               fs_create['tender']['procuringEntity']['identifier']['legalName']
        assert publicPoint_create['releases'][0]['parties'][1]['identifier']['uri'] == \
               fs_create['tender']['procuringEntity']['identifier']['uri']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['streetAddress'] == \
               fs_create['tender']['procuringEntity']['address']['streetAddress']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['postalCode'] == \
               fs_create['tender']['procuringEntity']['address']['postalCode']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['country']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['region']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['scheme'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme']
        assert publicPoint_create['releases'][0]['parties'][1]['address']['addressDetails']['locality']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['scheme'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['scheme']
        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['id'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['id']
        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['legalName'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['legalName']
        assert publicPoint_create['releases'][0]['parties'][1]['additionalIdentifiers'][0]['uri'] == \
               fs_create['tender']['procuringEntity']['additionalIdentifiers'][0]['uri']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['name'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['name']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['email'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['email']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['telephone'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['telephone']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['faxNumber'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['faxNumber']
        assert publicPoint_create['releases'][0]['parties'][1]['contactPoint']['url'] == \
               fs_create['tender']['procuringEntity']['contactPoint']['url']

    @pytestrail.case('24621')
    def test_24621_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['id'] = 'fs_01010101-test'
        fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24621')
    def test_24621_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['id'] = 'fs_01010101-test'
        fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24621')
    def test_24621_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['id'] = 'fs_01010101-test'
        fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['id'] == \
               fs_create['buyer']['identifier']['scheme'] + '-' + fs_create['buyer']['identifier']['id']

    @pytestrail.case('24622')
    def test_24622_1(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['buyer']['identifier']['id'] = 'ei_01010101-test'
        ei_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
        fs_create = copy.deepcopy(fs_create_full_treasury_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24622')
    def test_24622_2(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['buyer']['identifier']['id'] = 'ei_01010101-test'
        ei_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
        fs_create = copy.deepcopy(fs_create_full_treasury_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24622')
    def test_24622_3(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['buyer']['identifier']['id'] = 'ei_01010101-test'
        ei_create['buyer']['identifier']['scheme'] = 'MD-IDNO'
        fs_create = copy.deepcopy(fs_create_full_treasury_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['id'] == \
               ei_create['buyer']['identifier']['scheme'] + '-' + ei_create['buyer']['identifier']['id']

    @pytestrail.case('24623')
    def test_24623_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['name'] = 'name from fs buyer'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24623')
    def test_24623_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['name'] = 'name from fs buyer'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24623')
    def test_24623_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['name'] = 'name from fs buyer'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['name'] == \
               fs_create['buyer']['name']

    @pytestrail.case('24624')
    def test_24624_1(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['buyer']['name'] = 'name from ei buyer'
        fs_create = copy.deepcopy(fs_create_full_treasury_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24624')
    def test_24624_2(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['buyer']['name'] = 'name from ei buyer'
        fs_create = copy.deepcopy(fs_create_full_treasury_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24624')
    def test_24624_3(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['buyer']['name'] = 'name from ei buyer'
        fs_create = copy.deepcopy(fs_create_full_treasury_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['planning']['budget']['sourceEntity']['name'] == \
               ei_create['buyer']['name']

    @pytestrail.case('24625')
    def test_24625_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
        fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24625')
    def test_24625_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
        fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24625')
    def test_24625_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['identifier']['id'] = '777'
        fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][1]['roles'][0] == 'payer'
        assert publicPoint_create['releases'][0]['parties'][1]['id'] == \
               fs_create['tender']['procuringEntity']['identifier']['scheme'] + '-' + \
               fs_create['tender']['procuringEntity']['identifier']['id']

    @pytestrail.case('24626')
    def test_24626_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['id'] = '222'
        fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24626')
    def test_24626_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['id'] = '222'
        fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24626')
    def test_24626_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['id'] = '222'
        fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()
        print(url_create)
        assert publicPoint_create['releases'][0]['parties'][0]['roles'][0] == 'funder'
        assert publicPoint_create['releases'][0]['parties'][0]['id'] == \
               fs_create['buyer']['identifier']['scheme'] + '-' + fs_create['buyer']['identifier']['id']

    @pytestrail.case('24627')
    def test_24627_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['amount']['currency'] = 'USD'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24627')
    def test_24627_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['amount']['currency'] = 'USD'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24628')
    def test_24628(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        fs_create['planning']['budget']['amount']['currency'] = 'UAH'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00.10'
        assert create_fs_response[1]['errors'][0]['description'] == 'Currency not found. '

    @pytestrail.case('24629')
    def test_24629(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'ADCDEF'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00.12'
        assert create_fs_response[1]['errors'][0]['description'] == 'Registration scheme not found. '

    @pytestrail.case('24630')
    def test_24630(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        fs_create['buyer']['identifier']['scheme'] = 'ADCDEF'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00.12'
        assert create_fs_response[1]['errors'][0]['description'] == 'Registration scheme not found. '

    @pytestrail.case('24631')
    def test_24631_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24631')
    def test_24631_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['identifier']['scheme'] = 'MD-IDNO'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24632')
    def test_24632_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24632')
    def test_24632_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['identifier']['scheme'] = 'MD-IDNO'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24633')
    def test_24633(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        fs_create['planning']['budget']['amount']['currency'] = True
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.databind.JsonMapping' \
                                                                    'Exception: (was com.procurement.mdm.exception.' \
                                                                    'InErrorException) (through reference chain: com.' \
                                                                    'procurement.mdm.model.dto.data.' \
                                                                    'FS[\"planning\"]->com.procurement.mdm.model.' \
                                                                    'dto.data.PlanningFS[\"budget\"]->com.' \
                                                                    'procurement.mdm.model.dto.data.BudgetFS' \
                                                                    '[\"amount\"]->com.procurement.mdm.model.dto.' \
                                                                    'data.ValueFS[\"currency\"])'

    @pytestrail.case('24634')
    def test_24634_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['amount']['amount'] = 0.01

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24634')
    def test_24634_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['amount']['amount'] = 0.01

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24635')
    def test_24635(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        fs_create['planning']['budget']['amount']['amount'] = 0
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00.07'
        assert create_fs_response[1]['errors'][0]['description'] == 'Invalid amount.'

    @pytestrail.case('24636')
    def test_24636(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        fs_create['planning']['budget']['amount']['amount'] = -25.3
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00.07'
        assert create_fs_response[1]['errors'][0]['description'] == 'Invalid amount.'

    @pytestrail.case('24637')
    def test_24637(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_own_money)
        fs_create['planning']['budget']['amount']['amount'] = False
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.databind.exc.Mismatched' \
                                                                    'InputException: Cannot deserialize instance ' \
                                                                    'of `java.math.BigDecimal` out of VALUE_FALSE ' \
                                                                    'token\n at [Source: UNKNOWN; line: -1, column:' \
                                                                    ' -1] (through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"planning\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.request.PlanningFsCreate[\"budget\"]->' \
                                                                    'com.procurement.budget.model.dto.fs.request.' \
                                                                    'BudgetFsCreate[\"amount\"]->com.procurement.' \
                                                                    'budget.model.dto.ocds.Value[\"amount\"])'

    @pytestrail.case('24638')
    def test_24638_1(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24638')
    def test_24638_2(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24639')
    def test_24639_1(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24639')
    def test_24639_2(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24640')
    def test_24640(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['planning']['budget']['period']['startDate'] = '2020-01-05T00:00:00Z'
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.01.01'
        assert create_fs_response[1]['errors'][0]['description'] == 'Invalid period.'

    @pytestrail.case('24641')
    def test_24641(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['planning']['budget']['period']['endDate'] = '2020-12-31T00:00:00Z'
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['endDate'] = '2021-01-01T00:00:00Z'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.01.01'
        assert create_fs_response[1]['errors'][0]['description'] == 'Invalid period.'

    @pytestrail.case('24642')
    def test_24642(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['startDate'] = '2021-01-05T00:00:00Z'
        fs_create['planning']['budget']['period']['endDate'] = '2021-01-01T00:00:00Z'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.01.01'
        assert create_fs_response[1]['errors'][0]['description'] == 'Invalid period.'

    @pytestrail.case('24643')
    def test_24643(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
        ei_create['planning']['budget']['period']['endDate'] = '2020-12-20T00:00:00Z'
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
        fs_create['planning']['budget']['period']['endDate'] = '2020-12-20T00:00:00Z'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24644')
    def test_24644(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
        ei_create['planning']['budget']['period']['endDate'] = '2020-12-20T00:00:00Z'
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
        today = datetime.datetime.now()

        tomorrow = today.day + 1

        fs_create['planning']['budget']['period']['endDate'] = f'2020-12-{tomorrow}T16:16:29Z'

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24645')
    def test_24645(self):
        ei_create = copy.deepcopy(ei_full)
        ei_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
        ei_create['planning']['budget']['period']['endDate'] = '2020-12-09T00:00:00Z'
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['startDate'] = '2020-01-01T00:00:00Z'
        fs_create['planning']['budget']['period']['endDate'] = '2020-12-09T00:00:00Z'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.01.01'
        assert create_fs_response[1]['errors'][0]['description'] == 'Invalid period.'

    @pytestrail.case('24646')
    def test_24646(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
        del fs_create['planning']['budget']['europeanUnionFunding']['projectName']

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.ocds.EuropeanUnionFunding] value ' \
                                                                    'failed for JSON property projectName due to ' \
                                                                    'missing (therefore NULL) value for creator ' \
                                                                    'parameter projectName which is a non-nullable ' \
                                                                    'type\n at [Source: UNKNOWN; line: -1, column: ' \
                                                                    '-1] (through reference chain: com.procurement.' \
                                                                    'budget.model.dto.fs.request.FsCreate' \
                                                                    '[\"planning\"]->com.procurement.budget.model.' \
                                                                    'dto.fs.request.PlanningFsCreate[\"budget\"]' \
                                                                    '->com.procurement.budget.model.dto.fs.request.' \
                                                                    'BudgetFsCreate[\"europeanUnionFunding\"]->com.' \
                                                                    'procurement.budget.model.dto.ocds.EuropeanUnion' \
                                                                    'Funding[\"projectName\"])'

    @pytestrail.case('24647')
    def test_24647(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['isEuropeanUnionFunded'] = True
        del fs_create['planning']['budget']['europeanUnionFunding']['projectIdentifier']

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.budget.' \
                                                                    'model.dto.ocds.EuropeanUnionFunding] value ' \
                                                                    'failed for JSON property projectIdentifier due ' \
                                                                    'to missing (therefore NULL) value for creator ' \
                                                                    'parameter projectIdentifier which is a non-' \
                                                                    'nullable type\n at [Source: UNKNOWN; line: ' \
                                                                    '-1, column: -1] (through reference chain: ' \
                                                                    'com.procurement.budget.model.dto.fs.request.' \
                                                                    'FsCreate[\"planning\"]->com.procurement.budget.' \
                                                                    'model.dto.fs.request.PlanningFsCreate' \
                                                                    '[\"budget\"]->com.procurement.budget.model.dto.' \
                                                                    'fs.request.BudgetFsCreate[\"europeanUnion' \
                                                                    'Funding\"]->com.procurement.budget.model.dto.' \
                                                                    'ocds.EuropeanUnionFunding[\"projectIdentifier\"])'

    @pytestrail.case('24648')
    def test_24648_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['currency'] = 'MDL'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
        time.sleep(2)
        fs_create_2 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_2['planning']['budget']['amount']['currency'] = 'EUR'
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        host = set_instance_for_request()
        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create_2)
        time.sleep(2)

        get_message_from_kafka(x_operation_id)

        assert create_fs_response_1[0].text == 'ok'
        assert create_fs_response_1[0].status_code == 202
        assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]

    @pytestrail.case('24648')
    def test_24648_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['currency'] = 'MDL'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
        time.sleep(2)
        fs_create_2 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_2['planning']['budget']['amount']['currency'] = 'EUR'
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        host = set_instance_for_request()
        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create_2)
        time.sleep(2)

        messages = get_message_from_kafka(x_operation_id)

        assert messages['X-OPERATION-ID'] == x_operation_id
        assert messages['errors'][0]['code'] == '400.10.00.06'
        assert messages['errors'][0]['description'] == 'Invalid currency.'

    @pytestrail.case('24649')
    def test_24649(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['planning']['budget']['period']['startDate'] = '2020/08/10T11:00:00Z'
        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.10.00'
        assert create_fs_response[1]['errors'][0]['description'] == \
               f"com.fasterxml.jackson.databind.JsonMappingException: Text " \
               f"'{fs_create['planning']['budget']['period']['startDate']}' " \
               f"could not be parsed at index 4 (through reference chain: com.procurement.budget.model.dto.fs." \
               f"request.FsCreate[\"planning\"]->com.procurement.budget.model.dto.fs.request.PlanningFsCreate" \
               f"[\"budget\"]->com.procurement.budget.model.dto.fs.request.BudgetFsCreate[\"period\"]->com." \
               f"procurement.budget.model.dto.ocds.Period[\"startDate\"])"

    @pytestrail.case('24650')
    def test_24650_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24650')
    def test_24650_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24650')
    def test_24650_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['tag'][0] == 'planning'

    @pytestrail.case('24651')
    def test_24651_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24651')
    def test_24651_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24651')
    def test_24651_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        date_from_database = get_date_execute_cql_from_orchestrator_operation_step_by_oper_id(create_fs_response[2],
                                                                                              'NoticeCreateReleaseTask')
        date_in_format = date_from_database.strftime('%Y-%m-%dT%H:%M:%SZ')

        assert publicPoint_create['releases'][0]['date'] == date_in_format

    @pytestrail.case('24652')
    def test_24652_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24652')
    def test_24652_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)

        create_fs_response = bpe_create_fs(ei_create, fs_create)

        time.sleep(2)
        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        timestamp = fnmatch.fnmatch(publicPoint_create['releases'][0]['id'][46:58], '*')

        assert publicPoint_create['releases'][0]['id'][0:28] == create_fs_response[1]['data']['outcomes']['fs'][0][
                                                                    'id'][0:28]
        assert publicPoint_create['releases'][0]['id'][28:32] == create_fs_response[1]['data']['outcomes']['fs'][0][
                                                                     'id'][28:32]
        assert publicPoint_create['releases'][0]['id'][32:45] == create_fs_response[1]['data']['outcomes']['fs'][0][
                                                                     'id'][32:45]
        assert publicPoint_create['releases'][0]['id'][45:46] == '-'
        assert timestamp == True

    @pytestrail.case('24653')
    def test_24653_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['amount'] = 133.26
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
        time.sleep(2)

        fs_create_2 = copy.deepcopy(fs_create_full_own_money)
        fs_create_1['planning']['budget']['amount']['amount'] = 50.34
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'

        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        host = set_instance_for_request()
        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create_2)
        time.sleep(2)

        get_message_from_kafka(x_operation_id)

        assert create_fs_response_1[0].text == 'ok'
        assert create_fs_response_1[0].status_code == 202
        assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]

    @pytestrail.case('24653')
    def test_24653_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['amount'] = 133.26
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
        time.sleep(2)

        fs_create_2 = copy.deepcopy(fs_create_full_own_money)
        fs_create_1['planning']['budget']['amount']['amount'] = 50.34
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'

        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        host = set_instance_for_request()
        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create_2)
        time.sleep(2)

        get_message_from_kafka(x_operation_id)

        ocid = fnmatch.fnmatch(create_fs_response_1[1]['data']['ocid'], '*')
        assert ocid == True
        assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]

    @pytestrail.case('24653')
    def test_24653_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['amount'] = 133.26
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
        time.sleep(2)

        fs_create_2 = copy.deepcopy(fs_create_full_own_money)
        fs_create_2['planning']['budget']['amount']['amount'] = 50.34
        fs_create_2['planning']['budget']['amount']['currency'] = 'EUR'

        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        host = set_instance_for_request()
        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create_2)
        time.sleep(2)

        message_from_kafka = get_message_from_kafka(x_operation_id)
        url_create_ei = message_from_kafka['data']['url'] + '/' + message_from_kafka['data']['outcomes']['fs'][0]['id'][
                                                                  0:28]

        publicPoint_create_ei = requests.get(url=url_create_ei).json()
        sum_of_fs = fs_create_1['planning']['budget']['amount']['amount'] + fs_create_2['planning']['budget']['amount'][
            'amount']

        assert publicPoint_create_ei['releases'][0]['planning']['budget']['amount']['amount'] == sum_of_fs

    @pytestrail.case('24655')
    def test_24655_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['currency'] = 'MDL'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)

        assert create_fs_response_1[0].text == 'ok'
        assert create_fs_response_1[0].status_code == 202
        assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]

    @pytestrail.case('24655')
    def test_24655_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['currency'] = 'MDL'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)

        ocid = fnmatch.fnmatch(create_fs_response_1[1]['data']['ocid'], '*')
        assert ocid == True
        assert create_fs_response_1[1]['X-OPERATION-ID'] == create_fs_response_1[2]

    @pytestrail.case('24655')
    def test_24655_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['currency'] = 'MDL'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)

        url_create_ei = create_fs_response_1[1]['data']['url'] + '/' + create_fs_response_1[3]

        publicPoint_create_ei = requests.get(url=url_create_ei).json()
        print(url_create_ei)
        assert publicPoint_create_ei['releases'][0]['planning']['budget']['amount']['currency'] == \
               fs_create_1['planning']['budget']['amount']['currency']

    @pytestrail.case('24656')
    def test_24656(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create_1 = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create_1['planning']['budget']['amount']['currency'] = 'EUR'
        create_fs_response_1 = bpe_create_fs(ei_create, fs_create_1)
        time.sleep(2)

        fs_create_2 = copy.deepcopy(fs_create_full_own_money)
        fs_create_2['planning']['budget']['amount']['currency'] = 'USD'

        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        host = set_instance_for_request()
        requests.post(
            url=host + create_fs + create_fs_response_1[3],
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=fs_create_2)
        time.sleep(2)

        message_from_kafka = get_message_from_kafka(x_operation_id)

        assert message_from_kafka['errors'][0]['code'] == '400.10.00.06'
        assert message_from_kafka['errors'][0]['description'] == 'Invalid currency.'

    @pytestrail.case('24657')
    def test_24657_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24657')
    def test_24657_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24657')
    def test_24657_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()
        country_scheme = fnmatch.fnmatch(publicPoint_create['releases'][0]['parties'][0]
                                         ['address']['addressDetails']['country']['scheme'], '*')
        country_id = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'], '*')
        country_description = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['description'], '*')
        country_uri = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['uri'], '*')

        assert country_scheme == True
        assert country_id == True
        assert country_description == True
        assert country_uri == True
        assert publicPoint_create['releases'][0]['parties'][0]['roles'][0] == 'payer'

    @pytestrail.case('24657')
    def test_24657_4(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_obligatory_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'description'] == 'Moldova, Republica'
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'scheme'] == 'iso-alpha2'
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'uri'] == 'https://www.iso.org'

    @pytestrail.case('24658')
    def test_24658_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24658')
    def test_24658_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24658')
    def test_24658_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['buyer']['address']['addressDetails']['country']['id'] = 'MD'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()
        country_scheme = fnmatch.fnmatch(publicPoint_create['releases'][0]['parties'][0]
                                         ['address']['addressDetails']['country']['scheme'], '*')
        country_id = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'], '*')
        country_description = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['description'], '*')
        country_uri = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['uri'], '*')

        assert country_scheme == True
        assert country_id == True
        assert country_description == True
        assert country_uri == True
        assert publicPoint_create['releases'][0]['parties'][0]['roles'][0] == 'funder'
        assert publicPoint_create['releases'][0]['parties'][1]['roles'][0] == 'payer'

    @pytestrail.case('24658')
    def test_24658_4(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_own_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'MD'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country']['id'] == \
               fs_create['buyer']['address']['addressDetails']['country']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'description'] == 'Moldova, Republica'
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'scheme'] == 'iso-alpha2'
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'uri'] == 'https://www.iso.org'

    @pytestrail.case('24659')
    def test_24659_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
            "country": {
                "id": "MD",
                "scheme": "prosto_scheme"
            },
            "region": {
                "id": "3400000"
            },
            "locality": {
                "scheme": "CUATM",
                "id": "3401000",
                "description": ""
            }
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24659')
    def test_24659_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
            "country": {
                "id": "MD",
                "scheme": "prosto_scheme"
            },
            "region": {
                "id": "3400000"
            },
            "locality": {
                "scheme": "CUATM",
                "id": "3401000",
                "description": ""
            }
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24659')
    def test_24659_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
            "country": {
                "id": "MD",
                "scheme": "prosto_scheme"
            },
            "region": {
                "id": "3400000"
            },
            "locality": {
                "scheme": "CUATM",
                "id": "3401000",
                "description": ""
            }
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'scheme'] == 'iso-alpha2'

    @pytestrail.case('24660')
    def test_24660_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
            "country": {
                "id": "MD",
                "uri": "www.lol.md"
            },
            "region": {
                "id": "3400000"
            },
            "locality": {
                "scheme": "CUATM",
                "id": "3401000",
                "description": ""
            }
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24660')
    def test_24660_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
            "country": {
                "id": "MD",
                "uri": "www.lol.md"
            },
            "region": {
                "id": "3400000"
            },
            "locality": {
                "scheme": "CUATM",
                "id": "3401000",
                "description": ""
            }
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24660')
    def test_24660_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
            "country": {
                "id": "MD",
                "uri": "www.lol.md"
            },
            "region": {
                "id": "3400000"
            },
            "locality": {
                "scheme": "CUATM",
                "id": "3401000",
                "description": ""
            }
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'uri'] == 'https://www.iso.org'

    @pytestrail.case('24661')
    def test_24661_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
            "country": {
                "id": "MD",
                "description": " opis_polya_1"
            },
            "region": {
                "id": "3400000"
            },
            "locality": {
                "scheme": "CUATM",
                "id": "3401000",
                "description": ""
            }
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24661')
    def test_24661_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
            "country": {
                "id": "MD",
                "description": " opis_polya_1"
            },
            "region": {
                "id": "3400000"
            },
            "locality": {
                "scheme": "CUATM",
                "id": "3401000",
                "description": ""
            }
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24661')
    def test_24661_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails'] = {
            "country": {
                "id": "MD",
                "description": " opis_polya_1"
            },
            "region": {
                "id": "3400000"
            },
            "locality": {
                "scheme": "CUATM",
                "id": "3401000",
                "description": ""
            }
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['country'][
                   'description'] == 'Moldova, Republica'

    @pytestrail.case('24662')
    def test_24662_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'DE'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24662')
    def test_24662_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = 'DE'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.01.10'
        assert create_fs_response[1]['errors'][0]['description'] == 'Invalid country. '

    @pytestrail.case('24663')
    def test_24663_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24663')
    def test_24663_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24663')
    def test_24663_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        check_region_scheme = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['scheme'], '*')
        check_region_id = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'], '*')
        check_region_description = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['description'], '*')
        check_region_uri = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['uri'], '*')

        assert check_region_scheme == True
        assert check_region_id == True
        assert check_region_description == True
        assert check_region_uri == True

    @pytestrail.case('24663')
    def test_24663_4(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'scheme'] == 'CUATM'
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'description'] == 'Donduşeni'
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'uri'] == 'http://statistica.md'

    @pytestrail.case('24664')
    def test_24664_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['scheme'] = 'prosto_scheme'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24664')
    def test_24664_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['scheme'] = 'prosto_scheme'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24664')
    def test_24664_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['scheme'] = 'prosto_scheme'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'scheme'] == 'CUATM'

    @pytestrail.case('24665')
    def test_24665_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['uri'] = 'prosto_uri'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24665')
    def test_24665_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['uri'] = 'prosto_uri'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24665')
    def test_24665_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['uri'] = 'prosto_uri'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'uri'] == 'http://statistica.md'

    @pytestrail.case('24666')
    def test_24666_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['description'] = 'prosto_descri'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24666')
    def test_24666_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['description'] = 'prosto_descri'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24666')
    def test_24666_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['description'] = 'prosto_descri'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['region'][
                   'description'] == 'Donduşeni'

    @pytestrail.case('24667')
    def test_24667_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '4to_popalo'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24667')
    def test_24667_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '4to_popalo'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00.13'
        assert create_fs_response[1]['errors'][0]['description'] == 'Region not found. '

    @pytestrail.case('24668')
    def test_24668_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality'] = {
            "scheme": "CUATM",
            "id": "4to_popalo",
            "description": "google"
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24668')
    def test_24668_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality'] = {
            "scheme": "CUATM",
            "id": "4to_popalo",
            "description": "google"
        }

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00.14'
        assert create_fs_response[1]['errors'][0]['description'] == 'Locality not found. '

    @pytestrail.case('24669')
    def test_24669_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24669')
    def test_24669_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24669')
    def test_24669_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        check_locality_scheme = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['scheme'], '*')
        check_locality_id = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'], '*')
        check_locality_description = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['description'],
            '*')
        check_locality_uri = fnmatch.fnmatch(
            publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['uri'], '*')

        assert check_locality_scheme == True
        assert check_locality_id == True
        assert check_locality_description == True
        assert check_locality_uri == True

    @pytestrail.case('24669')
    def test_24669_4(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'CUATM'

        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
                   'scheme'] == 'CUATM'
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
                   'description'] == 'or.Donduşeni (r-l Donduşeni)'
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
                   'uri'] == 'http://statistica.md'

    @pytestrail.case('24670')
    def test_24670_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
        del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description']
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24670')
    def test_24670_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '3401000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
        del fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description']
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert create_fs_response[1]['errors'][0]['code'] == '400.20.00'
        assert create_fs_response[1]['errors'][0]['description'] == 'com.fasterxml.jackson.module.kotlin.Missing' \
                                                                    'KotlinParameterException: Instantiation of ' \
                                                                    '[simple type, class com.procurement.mdm.model.' \
                                                                    'dto.data.LocalityDetails] value failed for JSON ' \
                                                                    'property description due to missing (therefore ' \
                                                                    'NULL) value for creator parameter description ' \
                                                                    'which is a non-nullable type\n at [Source: ' \
                                                                    'UNKNOWN; line: -1, column: -1] (through ' \
                                                                    'reference chain: com.procurement.mdm.model.' \
                                                                    'dto.data.FS[\"tender\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.TenderFS[\"procuringEntity\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Organization' \
                                                                    'Reference[\"address\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.Address[\"addressDetails\"]->' \
                                                                    'com.procurement.mdm.model.dto.data.Address' \
                                                                    'Details[\"locality\"]->com.procurement.mdm.' \
                                                                    'model.dto.data.LocalityDetails[\"description\"])'

    @pytestrail.case('24671')
    def test_24671_1(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '777K'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description'] = 'rusanovka'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        assert create_fs_response[0].text == 'ok'
        assert create_fs_response[0].status_code == 202
        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]

    @pytestrail.case('24671')
    def test_24671_2(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '777K'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description'] = 'rusanovka'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        ocid = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['id'], '*')
        token = fnmatch.fnmatch(create_fs_response[1]['data']['outcomes']['fs'][0]['X-TOKEN'], '*')

        assert create_fs_response[1]['X-OPERATION-ID'] == create_fs_response[2]
        assert ocid == True
        assert token == True

    @pytestrail.case('24671')
    def test_24671_3(self):
        ei_create = copy.deepcopy(ei_full)
        fs_create = copy.deepcopy(fs_create_full_treasury_money)
        fs_create['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = '3400000'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = '777K'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = 'other'
        fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['description'] = 'rusanovka'
        create_fs_response = bpe_create_fs(ei_create, fs_create)
        time.sleep(2)

        url_create = create_fs_response[1]['data']['url'] + '/' + create_fs_response[1]['data']['outcomes']['fs'][0][
            'id']
        publicPoint_create = requests.get(url=url_create).json()

        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
                   'scheme'] == fs_create['tender']['procuringEntity']['address']['addressDetails']['locality'][
                   'scheme']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality']['id'] == \
               fs_create['tender']['procuringEntity']['address']['addressDetails']['locality']['id']
        assert publicPoint_create['releases'][0]['parties'][0]['address']['addressDetails']['locality'][
                   'description'] == fs_create['tender']['procuringEntity']['address']['addressDetails']['locality'][
                   'description']
