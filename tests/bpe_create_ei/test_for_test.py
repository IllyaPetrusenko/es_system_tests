import copy, datetime, fnmatch, time, requests, pytest, allure

from pytest_testrail.plugin import pytestrail
from useful_functions import is_valid_uuid, is_it_uuid, get_human_date_in_utc_format, get_period
from tests.bpe_create_ei.create_ei import EI
from tests.bpe_create_ei.payloads import payload_ei_full_data_model


@allure.title("Check the impossibility to create EI without obligatory data")
def test_22132():

    @allure.title("Delete tender object from the payload.")
    @pytest.mark.smoke
    @pytestrail.case("22132")
    def test_22132_1(self, country, language):
        ei = EI()
        payload = copy.deepcopy(payload_ei_full_data_model)
        del payload["tender"]
        create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)
        message_from_kafka = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.00.00.00"
        assert message_from_kafka["errors"][0]["description"] == "Data processing exception."
