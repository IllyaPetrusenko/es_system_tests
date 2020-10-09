import copy
import fnmatch
import requests
from pytest_testrail.plugin import pytestrail
from tests.bpe_update_ei.update_ei import bpe_update_ei
from tests.bpe_update_ei.payloads import ei_full



class TestBpeCreateEI(object):

    @pytestrail.case('22182')
    def test_22182_1(self):
        ei = copy.deepcopy(ei_full)
        ei['tender']['title'] = 'This is some text for field'
        ei['tender']['description'] = 'This is some text for field 22 orange'
        ei['tender']['classification']['id'] = ei['planning']['budget']['id']
        create_ei_response = bpe_update_ei(ei)

        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]

    @pytestrail.case('22182')
    def test_22182_2(self):
        ei = copy.deepcopy(ei_full)
        ei['tender']['title'] = 'This is some text for field'
        ei['tender']['description'] = 'This is some text for field 22 orange'
        ei['tender']['classification']['id'] = ei['planning']['budget']['id']
        create_ei_response = bpe_update_ei(ei)

        cpid = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['id'], '*')
        token = fnmatch.fnmatch(create_ei_response[1]['data']['outcomes']['ei'][0]['X-TOKEN'], '*')

        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert cpid == True
        assert token == True

    @pytestrail.case('22182')
    def test_22182_3(self):
        ei = copy.deepcopy(ei_full)
        ei['tender']['title'] = 'This is some text for field'
        ei['tender']['description'] = 'This is some text for field 22 orange'
        ei['tender']['classification']['id'] = ei['planning']['budget']['id']
        create_ei_response = bpe_update_ei(ei)
        url = create_ei_response[1]['data']['url'] + '/' + str(create_ei_response[1]['data']['outcomes']['ei'][0]['id'])
        publicPoint = requests.get(url=url).json()

        print(url)
        assert publicPoint['releases'][0]['tender']['title'] == ei['tender']['title']
        assert publicPoint['releases'][0]['tender']['classification']['id'] == ei['tender']['classification']['id']