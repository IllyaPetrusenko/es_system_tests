import copy, datetime, fnmatch, time, requests, pytest
from pytest_testrail.plugin import pytestrail
from useful_functions import is_valid_uuid, is_it_uuid, get_human_date_in_utc_format, get_period
from tests.bpe_create_ei.create_ei import EI
from tests.bpe_create_ei.payloads import payload_ei_full_data_model


class TestBpeCreateEI(object):

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytestrail.case("22132")
    def test_22132_1(self, country, language):
        ei = EI()
        with pytest.allure.step('Take payload'):
            payload = copy.deepcopy(payload_ei_full_data_model)

        with pytest.allure.step('Delete tender object from payload'):
            del payload["tender"]

        with pytest.allure.step('Create EI'):
            create_ei_response = ei.create_request_ei(payload=payload, lang=language, country=country)

        with pytest.allure.step('Take message from Kafka'):
            message_from_kafka = ei.get_message_from_kafka()
        assert create_ei_response.text == "ok"
        assert create_ei_response.status_code == 202
        assert message_from_kafka["errors"][0]["code"] == "400.00.00.00"
        assert message_from_kafka["errors"][0]["description"] == "Data processing exception."
