import copy

from pytest_testrail.plugin import pytestrail

from useful_functions import prepared_cpid


class TestBpeCreatePN(object):
    @pytestrail.case("27008")
    def test_27008_1(self, additional_value):
        cpid = prepared_cpid()
        payload = copy.deepcopy(pn_create_full_data_model_with_documents)
        create_pn_response = bpe_create_pn_one_fs(cpid, payload, additional_value)
        assert create_pn_response[0].text == "ok"
        assert create_pn_response[0].status_code == 202
        assert create_pn_response[1]["X-OPERATION-ID"] == create_pn_response[2]