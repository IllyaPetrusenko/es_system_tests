import csv
import fnmatch
import json
import random
import datetime
import time
from uuid import UUID
import allure
import requests
import xlrd


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def is_it_uuid(uuid_to_test, version):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


@allure.step('Get access token')
def get_access_token_for_platform_two(host):
    platform_two = 'Basic YXV0b21hdGlvbl91c2VyOnBhc3N3b3Jk'
    access_token = requests.get(
        url=host + '/auth/signin',
        headers={
            'Authorization': platform_two
        }).json()
    allure.attach(host + '/auth/signin', 'HOST')
    allure.attach(platform_two, 'Platform credentials for authorization')
    allure.attach(json.dumps(access_token), 'Response from auth service')
    access_token = access_token['data']['tokens']['access']
    allure.attach(str(access_token), 'Access token')
    return access_token


def prepared_cp_id():
    cp_id = "ocds-t1s2t3-MD-" + str(int(time.time()) * 1000 + random.randint(1, 100))
    return cp_id


def prepared_test_cp_id():
    cp_id = "test-t1s2t3-MD-" + str(int(time.time()) * 1000 + random.randint(1, 100))
    return cp_id


def prepared_fs_oc_id(cp_id):
    fs_id = f"{cp_id}-FS-" + str(int(time.time()) * 1000 + random.randint(1, 100))
    return fs_id


def prepared_pn_oc_id(prepared_cp_id):
    oc_id = f"{prepared_cp_id}-PN-" + str(int(time.time()) * 1000 + random.randint(1, 100))
    return oc_id


def time_at_now():
    date = datetime.datetime.now()
    time_at_now_ = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    return f"{time_at_now_}"


def time_at_now_as_utc(gep_hour=3):
    date = datetime.datetime.now()
    set_date = date - datetime.timedelta(hours=gep_hour, seconds=1)
    time_at_now_ = set_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    make_timestamp = int(
        time.mktime(datetime.datetime.strptime(time_at_now_, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())) * 1000
    return f"{time_at_now_}", make_timestamp


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
    start_date_plus_one_year = (duration_start_date + datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date_plus_one_year = (duration_end_date + datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return start_date, end_date, yesterday, tomorrow, today, start_date_plus_one_year, end_date_plus_one_year


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


def get_human_date_in_utc_format(time_stamp):
    date = datetime.datetime.utcfromtimestamp(time_stamp // 1000)
    yesterday = (date - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    tomorrow = (date + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    human_date = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return human_date, yesterday, tomorrow


def get_timestamp_from_human_date(human_date):
    time_stamp = int(time.mktime(datetime.datetime.strptime(human_date, "%Y-%m-%dT%H:%M:%SZ").timetuple())) * 1000

    return time_stamp


# This function removes attributes with the * value from a dictionary:
# ====================================================================
def get_clear_dict(d, v):
    li = list()
    for key, value in d.items():
        a = (key, value == v)
        if a[1] is True:
            li.append(a[0])
            continue
    for i in li:
        if i in d:
            del d[i]
    return d


# ====================================================================


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
    if s_1 is True:
        new.append(classification_1[0])
    else:
        new.append("0")
    if s_2 is True:
        new.append(classification_1[1])
    else:
        new.append("0")
    if s_3 is True:
        new.append(classification_1[2])
    else:
        new.append("0")
    if s_4 is True:
        new.append(classification_1[3])
    else:
        new.append("0")
    if s_5 is True:
        new.append(classification_1[4])
    else:
        new.append("0")
    if s_6 is True:
        new.append(classification_1[5])
    else:
        new.append("0")
    if s_7 is True:
        new.append(classification_1[6])
    else:
        new.append("0")
    if s_8 is True:
        new.append(classification_1[7])
    else:
        new.append("0")
    if s_9 is True:
        new.append(classification_1[8])
    else:
        new.append("0")
    if s_10 is True:
        new.append(classification_1[9])
    else:
        new.append("0")

    return str(new[0] + new[1] + new[2] + new[3] + new[4] + new[5] + new[6] + new[7])


def create_enquiry_and_tender_period():
    date = datetime.datetime.now()
    duration_enquiry_end_date = date + datetime.timedelta(seconds=121)
    enquiry_start_date = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    enquiry_end_date = duration_enquiry_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    duration_tender_end_date = date + datetime.timedelta(seconds=300)
    tender_start_date = duration_enquiry_end_date
    tender_end_date = duration_tender_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    return enquiry_start_date, enquiry_end_date, tender_start_date, tender_end_date


@allure.step('Compare actual and expected results')
def compare_actual_result_and_expected_result(expected_result, actual_result):
    allure.attach(expected_result, "Expected result")
    allure.attach(actual_result, "Actual result")
    if expected_result == actual_result:
        return True
    else:
        return False


# @allure.step('REQUEST_OF_UPDATE_EI')
# def request_update_ei(access_token, x_operation_id, cpid, ei_token, payload):
#     environment_host = set_instance_for_request()
#     update_ei_response = requests.post(
#         url=environment_host + update_ei + cpid,
#         headers={
#             'Authorization': 'Bearer ' + access_token,
#             'X-OPERATION-ID': x_operation_id,
#             'X-TOKEN': ei_token,
#             'Content-Type': 'application/json'},
#         json=payload)
#     allure.attach(environment_host + update_ei + cpid, 'URL')
#     allure.attach(access_token, 'ACCESS_TOKEN')
#     allure.attach(x_operation_id, 'X-OPERATION-ID')
#     allure.attach(cpid, 'CPID')
#     allure.attach(ei_token, 'X-TOKEN')
#     allure.attach(str(payload), 'PAYLOAD')
#     return update_ei_response

def get_value_from_classification_cpv_dictionary_xls(cpv, language):
    # Open current xlsx file.
    excel_data_file = xlrd.open_workbook('CPV_dictionary.xls')
    # Take current page of the file.
    sheet = excel_data_file.sheet_by_index(0)

    classification_description = []
    # How mach rows contains into file?
    rows_number = sheet.nrows
    column_number = sheet.ncols
    requested_row = list()
    requested_column = list()
    if rows_number > 0:
        for row in range(0, rows_number):
            if cpv in sheet.row(row)[0].value:
                requested_row.append(row)

    if column_number > 0:
        for column in range(0, column_number):
            if language.upper() in sheet.col(column)[0].value:
                requested_column.append(column)
    new_cpv = sheet.cell_value(rowx=int(requested_row[0]), colx=0)
    description = sheet.cell_value(rowx=int(requested_row[0]), colx=int(requested_column[0]))
    return new_cpv, description


def get_value_from_cpvs_dictionary_csv(cpvs, language):
    with open('CPVS_dictionary.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            cur_arr = row[0].split(';')
            if cur_arr[0] == cpvs and cur_arr[3] == f'"{language}"':
                return cur_arr[0].replace('"', ''), cur_arr[1].replace('"', ''), cur_arr[2].replace('"', ''), cur_arr[
                    3].replace('"', '')


def get_value_from_classification_unit_dictionary_csv(unit_id, language):
    with open('Units_dictionary.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            cur_arr = row[0].split(',')
            if cur_arr[0] == f'{unit_id}' and cur_arr[4].replace(';', '') == f'"{language}"':
                return cur_arr[0].replace("'", ""), cur_arr[2].replace('"', ''),
