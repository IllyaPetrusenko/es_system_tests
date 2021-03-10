import copy
import fnmatch

import requests
from pytest_testrail.plugin import pytestrail

from config import host
from tests.authorization import get_access_token_for_platform_one, get_x_operation_id
from tests.bpe_create_ei.create_ei import bpe_create_ei
from tests.bpe_create_ei.payloads import ei_full

@pytestrail.case('22134')
def test_22134():
        ei = copy.deepcopy(ei_full)
        access_token = get_access_token_for_platform_one()
        x_operation_id = get_x_operation_id(access_token)
        request_to_create_ei = requests.post(
            url=host + '/do/ei?country=MD&lang=ru',
            headers={
                'Authorization': 'Bearer ' + access_token,
                'X-OPERATION-ID': x_operation_id,
                'Content-Type': 'application/json'},
            json=ei)
        print(request_to_create_ei)