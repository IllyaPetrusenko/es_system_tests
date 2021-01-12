import random
import datetime
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
    cp_id = "ocds-t1s2t3-MD-" + str(int(time.time()) * 1000 + random.randint(1,100))
    return cp_id


def prepared_fs_ocid(prepared_cpid):
    oc_id = f"{prepared_cpid}-FS-" + str(int(time.time()) * 1000 + random.randint(1, 100))
    return oc_id

def time_at_now():
    date = datetime.datetime.now()
    time_at_now_ = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    return f"{time_at_now_}"


def timestamp():
    date = datetime.datetime.now()
    time_at_now_miliseconds = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp_ = int(
        time.mktime(datetime.datetime.strptime(time_at_now_miliseconds, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000
    return timestamp_


def get_period():
    date = datetime.datetime.now()
    start_date = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    duration_date = date + datetime.timedelta(days=90)
    end_date = duration_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    return start_date, end_date
