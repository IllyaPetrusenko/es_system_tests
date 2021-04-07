import fnmatch
import random
import datetime
import time
from uuid import UUID

import allure
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


def prepared_pn_ocid(prepared_cpid):
    oc_id = f"{prepared_cpid}-PN-" + str(int(time.time()) * 1000 + random.randint(1, 100))
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
    tender_period = duration_date_start.strftime('%Y-%m-01T%H:%M:%SZ')
    duration_fake_tender_period = (date + datetime.timedelta(days=30)).strftime('%Y-%m-01T%H:%M:%SZ')
    duration_date_end = date + datetime.timedelta(days=90)
    end_date = duration_date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    time_at_now_miliseconds = date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp_now = int(
        time.mktime(datetime.datetime.strptime(time_at_now_miliseconds, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000
    return start_date, end_date, timestamp_now, tender_period, duration_fake_tender_period


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
    today = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return start_date, end_date, yesterday, tomorrow, today


def get_contract_period():
    date = datetime.datetime.now()
    duration_tender_start_date = date + datetime.timedelta(days=30)
    duration_start_date = date + datetime.timedelta(days=60)
    duration_end_date = date + datetime.timedelta(days=90)
    duration_last_date = date - datetime.timedelta(days=30)
    start_date = duration_start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = duration_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    tender_period_start_date = duration_tender_start_date.strftime("%Y-%m-01T%H:%M:%SZ")
    last_date = duration_last_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return start_date, end_date, tender_period_start_date, last_date


def get_human_date_in_utc_format(timestamp):
    date = datetime.datetime.utcfromtimestamp(timestamp // 1000)
    yesterday = (date - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    tomorrow = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    human_date = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return human_date, yesterday, tomorrow


def get_timestamp_from_human_date(human_date):
    timestamp = int(time.mktime(datetime.datetime.strptime(human_date, "%Y-%m-%dT%H:%M:%SZ").timetuple())) * 1000

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


def get_new_classification_id(classification_1, classification_2):
    s_1 = fnmatch.fnmatch(classification_1[0], classification_2[0])
    s_2 = fnmatch.fnmatch(classification_1[1], classification_2[1])
    s_3 = fnmatch.fnmatch(classification_1[2], classification_2[2])
    s_4 = fnmatch.fnmatch(classification_1[3], classification_2[3])
    s_5 = fnmatch.fnmatch(classification_1[4], classification_2[4])
    s_6 = fnmatch.fnmatch(classification_1[5], classification_2[5])
    s_7 = fnmatch.fnmatch(classification_1[6], classification_2[6])
    s_8 = fnmatch.fnmatch(classification_1[7], classification_2[7])
    s_9 = fnmatch.fnmatch(classification_1[8], classification_2[8])
    s_10 = fnmatch.fnmatch(classification_1[9], classification_2[9])
    new = list()
    if s_1 == True:
        new.append(classification_1[0])
    else:
        new.append("0")
    if s_2 == True:
        new.append(classification_1[1])
    else:
        new.append("0")
    if s_3 == True:
        new.append(classification_1[2])
    else:
        new.append("0")
    if s_4 == True:
        new.append(classification_1[3])
    else:
        new.append("0")
    if s_5 == True:
        new.append(classification_1[4])
    else:
        new.append("0")
    if s_6 == True:
        new.append(classification_1[5])
    else:
        new.append("0")
    if s_7 == True:
        new.append(classification_1[6])
    else:
        new.append("0")
    if s_8 == True:
        new.append(classification_1[7])
    else:
        new.append("0")
    if s_9 == True:
        new.append(classification_1[8])
    else:
        new.append("0")
    if s_10 == True:
        new.append(classification_1[9])
    else:
        new.append("0")

    return str(new[0] + new[1] + new[2] + new[3] + new[4] + new[5] + new[6] + new[7] + new[8] + new[9])


def create_enquiry_and_tender_period():
    date = datetime.datetime.now()
    duration_enquiry_end_date = date + datetime.timedelta(seconds=121)
    enquiry_start_date = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    enquiry_end_date = duration_enquiry_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    duration_tender_end_date = date + datetime.timedelta(seconds=300)
    tender_start_date = duration_enquiry_end_date
    tender_end_date = duration_tender_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    return enquiry_start_date, enquiry_end_date, tender_start_date, tender_end_date


def compare_actual_result_and_expected_result(expected_result, actual_result):
    allure.attach(expected_result, "Expected result")
    allure.attach(actual_result, "Actual result")
    if expected_result == actual_result:
        return True
    else:
        return False
