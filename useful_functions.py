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


def is_it_uuid(uuid_to_test, version):
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

def prepared_test_cpid():
    cp_id = "test-t1s2t3-MD-" + str(int(time.time()) * 1000 + random.randint(1, 100))
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
    duration_date_start = date + datetime.timedelta(days=0)
    start_date = duration_date_start.strftime('%Y-%m-%dT%H:%M:%SZ')
    duration_date_end = date + datetime.timedelta(days=90)
    end_date = duration_date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_at_now_miliseconds = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp_now = int(
        time.mktime(datetime.datetime.strptime(time_at_now_miliseconds, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000
    return start_date, end_date, timestamp_now


def get_new_period():
    date = datetime.datetime.now()
    duration_start_date = date + datetime.timedelta(days=5)
    yesterday_start_date = date - datetime.timedelta(days=1)
    duration_end_date = date + datetime.timedelta(days=10)
    tomorrow_end_date = date + datetime.timedelta(days=91)
    start_date = duration_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = duration_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    yesterday = yesterday_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    tomorrow = tomorrow_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return start_date, end_date, yesterday, tomorrow


def get_contract_period():
    date = datetime.datetime.now()
    duration_tender_start_date = date + datetime.timedelta(days=30)
    duration_start_date = date + datetime.timedelta(days=60)
    duration_end_date = date + datetime.timedelta(days=90)
    start_date = duration_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = duration_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    tender_period_start_date = duration_tender_start_date.strftime("%Y-%m-01T%H:%M:%SZ")
    return start_date, end_date, tender_period_start_date


def get_human_date_in_utc_format(timestamp):
    date = datetime.datetime.utcfromtimestamp(timestamp // 1000)
    human_date = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return human_date


def get_timestamp_from_human_date(human_date):
    timestamp = int(time.mktime(datetime.datetime.strptime(human_date, "%Y-%m-%dT%H:%M:%SZ").timetuple()))

    return timestamp


# This function removes attributes with the * value from a dictionary:
def get_clear_dict(d, v):
    li = list()
    for key, value in d.items():
        a = (key, value == v)
        if a[1] == True:
            li.append(a[0])
            continue
    for l in li:
        if l in d:
            del d[l]
    return d
