from tests.bpe_create_ei.create_ei import bpe_create_ei
from tests.bpe_create_ei.payloads import ei_full


class TestBpeCreateEI(object):

    def test_22132_1(self):
        ei = ei_full.copy()
        del ei['tender']
        create_ei_response = bpe_create_ei(ei)
        assert create_ei_response[0].text == 'ok'
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]['X-OPERATION-ID'] == create_ei_response[2]
        assert create_ei_response[1]['errors'][0]['code'] == '400.00.00.00'
        assert create_ei_response[1]['errors'][0]['description'] == 'Data processing exception.'

