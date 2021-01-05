import random
import time
from uuid import UUID

import requests

from config import host


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except:
        return False
    return str(uuid_obj) == uuid_to_test


def get_access_token_for_platform_two():
    access_token = requests.get(
        url=host + '/auth/signin',
        headers={
            'Authorization': 'Basic YXV0b21hdGlvbl91c2VyOnBhc3N3b3Jk'
        }).json()['data']['tokens']['access']
    return access_token

def prepared_cpid():
    cp_id = "ocds-t1s2t3-MD-" + str(int(time.time()) * 1000 + random.randint(1, 100))
    return cp_id