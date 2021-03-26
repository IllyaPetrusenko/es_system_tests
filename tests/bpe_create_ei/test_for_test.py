import copy, allure
import datetime
import fnmatch
from uuid import UUID
import time
import requests
from pytest_testrail.plugin import pytestrail
from useful_functions import is_valid_uuid
from tests.bpe_create_ei.create_ei import bpe_create_ei
from tests.bpe_create_ei.payloads import ei_full, ei_obligatory


class TestBpeCreateEI(object):
    @allure.feature('CreateEI')
    @pytestrail.case("22132")
    def test_22132_1(self):
        ei = copy.deepcopy(ei_full)
        del ei["tender"]
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == "ok"
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]["X-OPERATION-ID"] == create_ei_response[2]
        assert create_ei_response[1]["errors"][0]["code"] == "400.00.00.00"
        assert create_ei_response[1]["errors"][0]["description"] == "Data processing exception."

    @allure.feature('CreateEI')
    @pytestrail.case("22132")
    def test_22132_2(self):
        ei = copy.deepcopy(ei_full)
        del ei["tender"]["title"]
        create_ei_response = bpe_create_ei(ei)

        assert create_ei_response[0].text == "ok"
        assert create_ei_response[0].status_code == 202
        assert create_ei_response[1]["X-OPERATION-ID"] == create_ei_response[2]
        assert create_ei_response[1]["errors"][0]["code"] == "400.10.00"
        assert create_ei_response[1]["errors"][0]["description"] == 'com.fasterxml.jackson.module.kotlin.' \
                                                                    'MissingKotlinParameterException: Instantiation ' \
                                                                    'of [simple type, class com.procurement.budget.' \
                                                                    'model.dto.ei.request.EiCreate$TenderEiCreate] ' \
                                                                    'value failed for JSON property title due to ' \
                                                                    'missing (therefore NULL) value for creator ' \
                                                                    'parameter title which is a non-nullable type\n ' \
                                                                    'at [Source: UNKNOWN; line: -1, column: -1] ' \
                                                                    '(through reference chain: com.procurement.' \
                                                                    'budget.model.dto.ei.request.EiCreate' \
                                                                    '[\"tender\"]->com.procurement.budget.model.' \
                                                                    'dto.ei.request.EiCreate$TenderEiCreate[\"title\"])'